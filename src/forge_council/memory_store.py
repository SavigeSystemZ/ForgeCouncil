"""In-memory Run and LedgerEvent store (M5 persistence stub)."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunStoreState:
    runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    ledger_by_run: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    run_steps_by_run: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)


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
