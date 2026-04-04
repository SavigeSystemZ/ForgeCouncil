from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

from forge_council.api_app import create_app
from forge_council.memory_store import MemoryStore
from forge_council.sqlite_store import SqliteStore


def test_health(monkeypatch) -> None:
    monkeypatch.delenv("FC_DISPATCH_KILL_SWITCH", raising=False)
    monkeypatch.delenv("FC_ALLOW_SUBPROCESS_DISPATCH", raising=False)
    client = TestClient(create_app(MemoryStore()))
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["persistence"] == "memory"
    assert data.get("auth_required") is False
    assert data.get("dispatch_kill_switch") is False
    assert data.get("subprocess_dispatch_enabled") is False


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


def test_dispatch_run_appends_ledger() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.post("/v1/runs", json={"project_id": "p1", "workspace_id": "w1"})
    rid = r.json()["run_id"]
    d = client.post(
        f"/v1/runs/{rid}/dispatch",
        json={"runner": "local", "action": "noop", "note": "test"},
    )
    assert d.status_code == 202
    data = d.json()
    assert data["run_id"] == rid
    assert data["status"] == "accepted"
    assert "dispatch_id" in data

    ev = client.get(f"/v1/runs/{rid}/ledger-events").json()["events"]
    assert len(ev) == 1
    assert ev[0]["event_type"] == "dispatch_requested"
    assert ev[0]["payload_json"]["dispatch_id"] == data["dispatch_id"]


def test_dispatch_unknown_run() -> None:
    client = TestClient(create_app(MemoryStore()))
    r = client.post("/v1/runs/nope/dispatch", json={})
    assert r.status_code == 404


def test_dispatch_rejects_unknown_field() -> None:
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={}).json()["run_id"]
    r = client.post(f"/v1/runs/{rid}/dispatch", json={"evil": 1})
    assert r.status_code == 400


def test_list_run_steps_empty() -> None:
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={"project_id": "p"}).json()["run_id"]
    r = client.get(f"/v1/runs/{rid}/run-steps")
    assert r.status_code == 200
    assert r.json()["steps"] == []


def test_dispatch_subprocess_forbidden_without_opt_in() -> None:
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={"project_id": "p"}).json()["run_id"]
    r = client.post(
        f"/v1/runs/{rid}/dispatch",
        json={"action": "subprocess", "argv": [sys.executable, "-c", "print(1)"]},
    )
    assert r.status_code == 403


def test_dispatch_subprocess_runs_when_opt_in(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FC_ALLOW_SUBPROCESS_DISPATCH", "1")
    monkeypatch.setenv("FC_EXEC_ALLOWLIST", str(Path(sys.executable).resolve()))
    monkeypatch.setenv("FC_EXEC_WORKDIR", str(tmp_path))
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={"project_id": "p"}).json()["run_id"]
    r = client.post(
        f"/v1/runs/{rid}/dispatch",
        json={
            "action": "subprocess",
            "argv": [sys.executable, "-c", "print('fc_ok')"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "completed"
    assert body["exit_code"] == 0
    assert "fc_ok" in body["stdout_snip"]

    steps = client.get(f"/v1/runs/{rid}/run-steps").json()["steps"]
    assert len(steps) == 1
    assert steps[0]["status"] == "succeeded"
    assert client.get(f"/v1/runs/{rid}").json()["status"] == "completed"


def test_dispatch_kill_switch(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FC_DISPATCH_KILL_SWITCH", "1")
    monkeypatch.setenv("FC_ALLOW_SUBPROCESS_DISPATCH", "1")
    monkeypatch.setenv("FC_EXEC_ALLOWLIST", str(Path(sys.executable).resolve()))
    monkeypatch.setenv("FC_EXEC_WORKDIR", str(tmp_path))
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={"project_id": "p"}).json()["run_id"]
    r = client.post(
        f"/v1/runs/{rid}/dispatch",
        json={"action": "subprocess", "argv": [sys.executable, "-c", "print(1)"]},
    )
    assert r.status_code == 503


def test_dispatch_subprocess_requires_argv() -> None:
    client = TestClient(create_app(MemoryStore()))
    rid = client.post("/v1/runs", json={"project_id": "p"}).json()["run_id"]
    r = client.post(f"/v1/runs/{rid}/dispatch", json={"action": "subprocess"})
    assert r.status_code == 400


def test_openapi_lists_bearer_security_scheme() -> None:
    client = TestClient(create_app(MemoryStore()))
    spec = client.get("/openapi.json").json()
    assert "bearerAuth" in spec["components"]["securitySchemes"]


def test_bearer_token_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("FC_API_TOKEN", "test-secret")
    client = TestClient(create_app(MemoryStore()))
    r = client.post("/v1/runs", json={"project_id": "p"})
    assert r.status_code == 401
    r2 = client.post(
        "/v1/runs",
        json={"project_id": "p"},
        headers={"Authorization": "Bearer test-secret"},
    )
    assert r2.status_code == 201
    h = client.get("/health").json()
    assert h.get("auth_required") is True
