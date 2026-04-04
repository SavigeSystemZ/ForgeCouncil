"""Shared interface for run + ledger persistence."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RunLedgerStore(Protocol):
    def put_run(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...

    def get_run(self, run_id: str) -> dict[str, Any] | None: ...

    def list_runs(self) -> list[dict[str, Any]]: ...

    def append_ledger_event(self, run_id: str, event: dict[str, Any]) -> dict[str, Any]: ...

    def list_ledger_events(self, run_id: str) -> list[dict[str, Any]]: ...


@runtime_checkable
class RunLedgerRunStepStore(RunLedgerStore, Protocol):
    """Persistence for runs, ledger, and per-run execution steps (M5+ runner)."""

    def put_run_step(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...

    def list_run_steps(self, run_id: str) -> list[dict[str, Any]]: ...


@runtime_checkable
class RunLedgerRunStepJobStore(RunLedgerRunStepStore, Protocol):
    """Adds durable dispatch job queue for async subprocess execution."""

    def enqueue_dispatch_job(
        self, job_id: str, run_id: str, body: dict[str, Any], *, created_at: str
    ) -> dict[str, Any]: ...

    def get_dispatch_job(self, job_id: str) -> dict[str, Any] | None: ...

    def claim_next_dispatch_job(self) -> dict[str, Any] | None: ...

    def finish_dispatch_job(
        self,
        job_id: str,
        *,
        status: str,
        result: dict[str, Any] | None,
        finished_at: str,
    ) -> None: ...

    def count_dispatch_jobs_queued(self) -> int: ...
