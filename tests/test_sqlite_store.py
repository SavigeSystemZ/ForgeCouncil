from __future__ import annotations

from pathlib import Path

from forge_council.sqlite_store import SqliteStore


def test_sqlite_run_and_ledger_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / "fc.db"
    store = SqliteStore(str(db))
    store.put_run(
        "r1",
        {
            "schema_version": "1",
            "run_id": "r1",
            "project_id": "p1",
            "status": "pending",
            "mode": "local",
            "started_at": "2026-04-04T12:00:00Z",
            "cost_summary_json": {},
        },
    )
    store2 = SqliteStore(str(db))
    got = store2.get_run("r1")
    assert got is not None
    assert got["project_id"] == "p1"

    store2.append_ledger_event(
        "r1",
        {
            "schema_version": "1",
            "event_id": "e1",
            "timestamp": "2026-04-04T12:01:00Z",
            "workspace_id": "w",
            "project_id": "p1",
            "run_id": "r1",
            "event_type": "gate_result",
            "actor": "system",
            "payload_json": {},
        },
    )
    events = store2.list_ledger_events("r1")
    assert len(events) == 1
    assert events[0]["event_type"] == "gate_result"


def test_sqlite_patch_preserves_ledger(tmp_path: Path) -> None:
    db = tmp_path / "fc.db"
    store = SqliteStore(str(db))
    store.put_run(
        "r1",
        {
            "schema_version": "1",
            "run_id": "r1",
            "project_id": "p1",
            "status": "pending",
            "mode": "local",
            "started_at": "2026-04-04T12:00:00Z",
            "cost_summary_json": {},
        },
    )
    store.append_ledger_event(
        "r1",
        {
            "schema_version": "1",
            "event_id": "e1",
            "timestamp": "2026-04-04T12:01:00Z",
            "workspace_id": "w",
            "project_id": "p1",
            "run_id": "r1",
            "event_type": "state_transition",
            "actor": "system",
            "payload_json": {},
        },
    )
    store.put_run(
        "r1",
        {
            "schema_version": "1",
            "run_id": "r1",
            "project_id": "p1",
            "status": "running",
            "mode": "local",
            "started_at": "2026-04-04T12:00:00Z",
            "cost_summary_json": {},
        },
    )
    assert len(store.list_ledger_events("r1")) == 1


def test_sqlite_unknown_run_ledger_raises(tmp_path: Path) -> None:
    store = SqliteStore(str(tmp_path / "x.db"))
    try:
        store.append_ledger_event(
            "missing",
            {
                "schema_version": "1",
                "event_id": "e",
                "timestamp": "2026-04-04T12:00:00Z",
                "workspace_id": "w",
                "project_id": "p",
                "run_id": "missing",
                "event_type": "state_transition",
                "actor": "system",
                "payload_json": {},
            },
        )
    except KeyError:
        return
    raise AssertionError("expected KeyError")
