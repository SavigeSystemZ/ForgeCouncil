"""Shared subprocess dispatch completion: run_step, ledger, run terminal state, artifacts."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from forge_council import local_runner
from forge_council.schema_util import validate_instance_or_raise_http
from forge_council.store_protocol import RunLedgerRunStepJobStore


async def execute_subprocess_dispatch(
    store: RunLedgerRunStepJobStore,
    *,
    run_id: str,
    dispatch_id: str,
    argv: list[str],
    env_overlay: dict[str, str] | None,
    workspace_id: str,
    project_id: str,
    trace_id: str | None,
    step_id: str,
) -> dict[str, Any]:
    """Run subprocess, persist step + ledger + terminal run; return API result fields."""
    run = store.get_run(run_id)
    if not run:
        return {
            "dispatch_id": dispatch_id,
            "run_id": run_id,
            "step_id": step_id,
            "status": "failed",
            "exit_code": -1,
            "stdout_snip": "",
            "stderr_snip": "forge_council: run not found during execution",
            "stdout_artifact_relpath": None,
            "stderr_artifact_relpath": None,
        }

    now = dt.datetime.now(dt.UTC)
    now_s = now.isoformat().replace("+00:00", "Z")
    seq = len(store.list_run_steps(run_id))
    step_running: dict[str, Any] = {
        "schema_version": "1",
        "step_id": step_id,
        "run_id": run_id,
        "sequence_no": seq,
        "agent_role": "local_runner",
        "action_type": "subprocess",
        "status": "running",
        "started_at": now_s,
    }
    validate_instance_or_raise_http("run_step", step_running)
    store.put_run_step(run_id, step_running)

    merged = dict(run)
    merged["status"] = "running"
    merged["run_id"] = run_id
    merged.setdefault("schema_version", run.get("schema_version") or "1")
    validate_instance_or_raise_http("run", merged)
    store.put_run(run_id, merged)

    cwd = local_runner.resolve_workdir()
    timeout = local_runner.exec_timeout_sec()
    try:
        code, out, err = await local_runner.run_subprocess_async(
            argv,
            cwd=cwd,
            env_overlay=env_overlay,
            timeout=timeout,
        )
    except Exception as e:  # noqa: BLE001
        code = -1
        out = ""
        err = f"forge_council: subprocess error: {e}"

    end = dt.datetime.now(dt.UTC)
    end_s = end.isoformat().replace("+00:00", "Z")
    term = "succeeded" if code == 0 else "failed"
    step_final = {
        **step_running,
        "status": term,
        "finished_at": end_s,
    }
    validate_instance_or_raise_http("run_step", step_final)
    store.put_run_step(run_id, step_final)

    stdout_ref, stderr_ref = local_runner.write_dispatch_log_artifacts(
        run_id=run_id,
        step_id=step_id,
        stdout_text=out,
        stderr_text=err,
    )

    meta_payload: dict[str, Any] = {
        "dispatch_id": dispatch_id,
        "step_id": step_id,
        "argv0": argv[0],
        "exit_code": code,
        "stdout_snip": local_runner.truncate_output(out),
        "stderr_snip": local_runner.truncate_output(err),
        "stdout_bytes": len(out.encode("utf-8", errors="replace")),
        "stderr_bytes": len(err.encode("utf-8", errors="replace")),
    }
    if stdout_ref:
        meta_payload["stdout_artifact_relpath"] = stdout_ref
    if stderr_ref:
        meta_payload["stderr_artifact_relpath"] = stderr_ref

    meta = {
        "schema_version": "1",
        "event_id": str(uuid.uuid4()),
        "timestamp": end_s,
        "workspace_id": workspace_id,
        "project_id": project_id,
        "run_id": run_id,
        "event_type": "tool_invocation_meta",
        "actor": "system",
        "payload_json": meta_payload,
    }
    if trace_id:
        meta["trace_id"] = trace_id
    validate_instance_or_raise_http("ledger_event", meta)
    store.append_ledger_event(run_id, meta)

    cur = store.get_run(run_id) or merged
    final_run = dict(cur)
    final_run["status"] = "completed" if code == 0 else "failed"
    final_run["finished_at"] = end_s
    final_run["run_id"] = run_id
    validate_instance_or_raise_http("run", final_run)
    store.put_run(run_id, final_run)

    return {
        "dispatch_id": dispatch_id,
        "run_id": run_id,
        "step_id": step_id,
        "status": final_run["status"],
        "exit_code": code,
        "stdout_snip": local_runner.truncate_output(out),
        "stderr_snip": local_runner.truncate_output(err),
        "stdout_artifact_relpath": stdout_ref,
        "stderr_artifact_relpath": stderr_ref,
    }
