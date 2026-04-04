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
