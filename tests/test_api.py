from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from forge_council.api_app import create_app
from forge_council.memory_store import MemoryStore
from forge_council.sqlite_store import SqliteStore


def test_health() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["persistence"] == "memory"


def test_create_run_and_ledger() -> None:
    store = MemoryStore()
    client = TestClient(create_app(store))
    r = client.post("/v1/runs", json={"project_id": "proj-a", "workspace_id": "ws-a"})
    assert r.status_code == 201
    body = r.json()
    rid = body["run_id"]
    assert body["project_id"] == "proj-a"

    r2 = client.get(f"/v1/runs/{rid}")
    assert r2.status_code == 200

    r3 = client.post(
        f"/v1/runs/{rid}/ledger-events",
        json={
            "event_type": "policy_decision",
            "workspace_id": "ws-a",
            "project_id": "proj-a",
            "payload_json": {"decision": "allow"},
        },
    )
    assert r3.status_code == 201

    r4 = client.get(f"/v1/runs/{rid}/ledger-events")
    assert r4.status_code == 200
    assert len(r4.json()["events"]) == 1


def test_ledger_unknown_run() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.post(
        "/v1/runs/nope/ledger-events",
        json={
            "event_type": "state_transition",
            "workspace_id": "w",
            "project_id": "p",
        },
    )
    assert r.status_code == 404


def test_invalid_run_rejected() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.post("/v1/runs", json={"project_id": "ok", "mode": "not-a-mode"})
    assert r.status_code == 400


def test_patch_run_status(tmp_path: Path) -> None:
    db = tmp_path / "t.db"
    client = TestClient(create_app(SqliteStore(str(db))))
    r = client.post("/v1/runs", json={"project_id": "p"})
    rid = r.json()["run_id"]
    r2 = client.patch(f"/v1/runs/{rid}", json={"status": "running"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "running"
    r3 = client.get(f"/v1/runs/{rid}")
    assert r3.json()["status"] == "running"


def test_patch_unknown_run() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.patch("/v1/runs/nope", json={"status": "done"})
    assert r.status_code == 404
