"""Background worker: claim queued dispatch jobs and run subprocess completion."""

from __future__ import annotations

import asyncio
import datetime as dt
import logging
from contextlib import suppress

from fastapi import FastAPI

from forge_council import local_runner
from forge_council.dispatch_execution import execute_subprocess_dispatch
from forge_council.store_protocol import RunLedgerRunStepJobStore

logger = logging.getLogger(__name__)


async def _emit_job_snapshot(app: FastAPI, store: RunLedgerRunStepJobStore, job_id: str) -> None:
    bc = getattr(app.state, "dispatch_job_broadcaster", None)
    if bc is None:
        return
    row = store.get_dispatch_job(job_id)
    if row:
        await bc.publish(job_id, dict(row))


async def run_dispatch_worker_loop(app: FastAPI, stop: asyncio.Event) -> None:
    store: RunLedgerRunStepJobStore = app.state.store
    while not stop.is_set():
        job = store.claim_next_dispatch_job()
        if job is None:
            with suppress(TimeoutError):
                await asyncio.wait_for(stop.wait(), timeout=0.2)
            continue
        job_id = str(job["job_id"])
        run_id = str(job["run_id"])
        await _emit_job_snapshot(app, store, job_id)
        if local_runner.dispatch_kill_switch_active():
            end = dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")
            store.finish_dispatch_job(
                job_id,
                status="failed",
                result={
                    "dispatch_id": job.get("dispatch_id"),
                    "run_id": run_id,
                    "step_id": job.get("step_id"),
                    "status": "failed",
                    "exit_code": -1,
                    "stderr_snip": "FC_DISPATCH_KILL_SWITCH active; job not executed",
                },
                finished_at=end,
            )
            await _emit_job_snapshot(app, store, job_id)
            continue
        try:
            env_raw = job.get("env")
            env_overlay: dict[str, str] | None = (
                dict(env_raw) if isinstance(env_raw, dict) else None
            )
            result = await execute_subprocess_dispatch(
                store,
                run_id=run_id,
                dispatch_id=str(job["dispatch_id"]),
                argv=list(job["argv"]),
                env_overlay=env_overlay,
                workspace_id=str(job["workspace_id"]),
                project_id=str(job["project_id"]),
                trace_id=job.get("trace_id") if job.get("trace_id") else None,
                step_id=str(job["step_id"]),
            )
            st = "completed" if int(result.get("exit_code", -1)) == 0 else "failed"
            end = dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")
            store.finish_dispatch_job(job_id, status=st, result=result, finished_at=end)
            await _emit_job_snapshot(app, store, job_id)
        except Exception as e:  # noqa: BLE001
            logger.exception("dispatch job %s failed", job_id)
            end = dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")
            store.finish_dispatch_job(
                job_id,
                status="failed",
                result={
                    "dispatch_id": job.get("dispatch_id"),
                    "run_id": run_id,
                    "step_id": job.get("step_id"),
                    "status": "failed",
                    "exit_code": -1,
                    "stderr_snip": str(e),
                },
                finished_at=end,
            )
            await _emit_job_snapshot(app, store, job_id)
