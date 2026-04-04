"""In-memory Run and LedgerEvent store (M5 persistence stub)."""

from __future__ import annotations

import datetime as dt
import threading
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunStoreState:
    runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    ledger_by_run: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    run_steps_by_run: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    dispatch_records: dict[str, dict[str, Any]] = field(default_factory=dict)
    dispatch_order: list[str] = field(default_factory=list)


class MemoryStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._state = RunStoreState()

    def put_run(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._state.runs[run_id] = dict(payload)
            self._state.ledger_by_run.setdefault(run_id, [])
            self._state.run_steps_by_run.setdefault(run_id, {})
            return self._state.runs[run_id]

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            r = self._state.runs.get(run_id)
            return dict(r) if r else None

    def list_runs(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(r) for r in self._state.runs.values()]

    def append_ledger_event(self, run_id: str, event: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            if run_id not in self._state.runs:
                raise KeyError(f"unknown run_id: {run_id}")
            events = self._state.ledger_by_run.setdefault(run_id, [])
            events.append(dict(event))
            return dict(event)

    def list_ledger_events(self, run_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(e) for e in self._state.ledger_by_run.get(run_id, [])]

    def put_run_step(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            if run_id not in self._state.runs:
                raise KeyError(f"unknown run_id: {run_id}")
            step_id = str(payload.get("step_id") or "")
            if not step_id:
                raise ValueError("run step requires step_id")
            self._state.run_steps_by_run.setdefault(run_id, {})[step_id] = dict(payload)
            return dict(self._state.run_steps_by_run[run_id][step_id])

    def list_run_steps(self, run_id: str) -> list[dict[str, Any]]:
        with self._lock:
            steps = self._state.run_steps_by_run.get(run_id, {})
            rows = [dict(s) for s in steps.values()]
            rows.sort(key=lambda r: (int(r.get("sequence_no", 0) or 0), str(r.get("step_id", ""))))
            return rows

    def enqueue_dispatch_job(
        self, job_id: str, run_id: str, body: dict[str, Any], *, created_at: str
    ) -> dict[str, Any]:
        with self._lock:
            if run_id not in self._state.runs:
                raise KeyError(f"unknown run_id: {run_id}")
            rec: dict[str, Any] = {
                "job_id": job_id,
                "run_id": run_id,
                "status": "queued",
                "body": dict(body),
                "result": None,
                "created_at": created_at,
                "started_at": None,
                "finished_at": None,
            }
            self._state.dispatch_records[job_id] = rec
            self._state.dispatch_order.append(job_id)
            return self._dispatch_job_public_view(rec)

    def get_dispatch_job(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            rec = self._state.dispatch_records.get(job_id)
            if not rec:
                return None
            return self._dispatch_job_public_view(rec)

    def claim_next_dispatch_job(self) -> dict[str, Any] | None:
        now_s = dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")
        with self._lock:
            for jid in self._state.dispatch_order:
                rec = self._state.dispatch_records.get(jid)
                if rec and rec["status"] == "queued":
                    rec["status"] = "running"
                    rec["started_at"] = now_s
                    body = dict(rec["body"])
                    return {"job_id": jid, "run_id": rec["run_id"], **body}
            return None

    def finish_dispatch_job(
        self,
        job_id: str,
        *,
        status: str,
        result: dict[str, Any] | None,
        finished_at: str,
    ) -> None:
        with self._lock:
            rec = self._state.dispatch_records.get(job_id)
            if not rec:
                return
            rec["status"] = status
            rec["result"] = dict(result) if result is not None else None
            rec["finished_at"] = finished_at

    def count_dispatch_jobs_queued(self) -> int:
        with self._lock:
            return sum(
                1 for rec in self._state.dispatch_records.values() if rec.get("status") == "queued"
            )

    @staticmethod
    def _dispatch_job_public_view(rec: dict[str, Any]) -> dict[str, Any]:
        out = {"job_id": rec["job_id"], "run_id": rec["run_id"], "status": rec["status"]}
        out.update(rec["body"])
        out["created_at"] = rec["created_at"]
        out["started_at"] = rec["started_at"]
        out["finished_at"] = rec["finished_at"]
        out["result"] = rec["result"]
        return out
