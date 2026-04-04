"""FastAPI control-plane stub: health, runs, ledger events."""

from __future__ import annotations

import datetime as dt
import os
import uuid
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from forge_council.auth import require_api_token
from forge_council.memory_store import MemoryStore
from forge_council.otel import configure_tracer, start_run_span
from forge_council.sqlite_store import SqliteStore
from forge_council.store_protocol import RunLedgerStore
from forge_council.schema_util import validate_instance_or_raise_http

_tracer: Any = None

ALLOWED_DISPATCH_BODY_KEYS = frozenset({"runner", "action", "note", "argv", "env"})

ALLOWED_RUN_PATCH_KEYS = frozenset(
    {
        "status",
        "mode",
        "milestone_id",
        "workspace_id",
        "finished_at",
        "started_at",
        "trace_id",
        "cost_summary_json",
        "initiated_by",
        "project_id",
    }
    )


def _normalize_dispatch_body(body: dict[str, Any]) -> dict[str, Any]:
    """Validate optional dispatch request; returns payload_json for ledger."""
    unknown = set(body) - ALLOWED_DISPATCH_BODY_KEYS
    if unknown:
        raise ValueError(f"unknown dispatch fields: {sorted(unknown)}")
    runner = (body.get("runner") or "local").strip() or "local"
    action = (body.get("action") or "noop").strip() or "noop"
    if action not in ("noop", "subprocess_stub"):
        raise ValueError("action must be 'noop' or 'subprocess_stub'")
    out: dict[str, Any] = {"runner": runner, "action": action}
    if "note" in body and body["note"] is not None:
        if not isinstance(body["note"], str):
            raise ValueError("note must be a string")
        out["note"] = body["note"]
    if "argv" in body and body["argv"] is not None:
        argv = body["argv"]
        if not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
            raise ValueError("argv must be a list of strings")
        out["argv"] = list(argv)
    if "env" in body and body["env"] is not None:
        env = body["env"]
        if not isinstance(env, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in env.items()
        ):
            raise ValueError("env must be an object of string keys and string values")
        out["env"] = dict(env)
    return out


def default_store() -> RunLedgerStore:
    """Use ``FC_STATE_DB`` for SQLite; otherwise in-memory (dev/tests)."""
    path = os.environ.get("FC_STATE_DB", "").strip()
    if path:
        return SqliteStore(path)
    return MemoryStore()


@asynccontextmanager
async def _make_lifespan() -> AsyncIterator[None]:
    global _tracer
    if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip():
        _tracer = configure_tracer("forge-council-api")
    yield


def create_app(store: RunLedgerStore | None = None) -> FastAPI:
    app = FastAPI(
        title="Forge Council Control Plane",
        version="0.1.0",
        lifespan=_make_lifespan,
    )
    app.state.store = store if store is not None else default_store()

    origins = os.environ.get("FC_CORS_ORIGINS", "").strip()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[o.strip() for o in origins.split(",") if o.strip()],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def otel_request_span(request: Request, call_next: Any) -> Any:
        if _tracer is None:
            return await call_next(request)
        route = request.scope.get("path", "/")
        with start_run_span(_tracer, f"http {request.method} {route}"):
            return await call_next(request)

    @app.get("/health")
    async def health(request: Request) -> dict[str, Any]:
        store = request.app.state.store
        mode = "sqlite" if isinstance(store, SqliteStore) else "memory"
        auth_on = bool(os.environ.get("FC_API_TOKEN", "").strip())
        return {
            "status": "ok",
            "service": "forge-council",
            "persistence": mode,
            "auth_required": auth_on,
        }

    v1 = APIRouter(prefix="/v1", dependencies=[Depends(require_api_token)])

    @v1.post("/runs", status_code=201)
    async def create_run(request: Request, body: dict[str, Any]) -> dict[str, Any]:
        store: RunLedgerStore = request.app.state.store
        now = dt.datetime.now(dt.timezone.utc)
        run_id = (body.get("run_id") or "").strip() or str(uuid.uuid4())
        payload: dict[str, Any] = {
            "schema_version": body.get("schema_version") or "1",
            "run_id": run_id,
            "project_id": body.get("project_id") or "default-project",
            "mode": body.get("mode") or "local",
            "status": body.get("status") or "pending",
            "started_at": body.get("started_at") or now.isoformat().replace("+00:00", "Z"),
            "cost_summary_json": body.get("cost_summary_json") or {},
        }
        if body.get("workspace_id") is not None:
            payload["workspace_id"] = body["workspace_id"]
        if body.get("milestone_id") is not None:
            payload["milestone_id"] = body["milestone_id"]
        if body.get("initiated_by") is not None:
            payload["initiated_by"] = body["initiated_by"]
        if body.get("finished_at") is not None:
            payload["finished_at"] = body["finished_at"]
        if body.get("trace_id") is not None:
            payload["trace_id"] = body["trace_id"]
        try:
            validate_instance_or_raise_http("run", payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        return store.put_run(run_id, payload)

    @v1.patch("/runs/{run_id}")
    async def patch_run(request: Request, run_id: str, body: dict[str, Any]) -> dict[str, Any]:
        store: RunLedgerStore = request.app.state.store
        current = store.get_run(run_id)
        if not current:
            raise HTTPException(status_code=404, detail="run not found")
        merged = dict(current)
        for key, value in body.items():
            if key in ALLOWED_RUN_PATCH_KEYS and value is not None:
                merged[key] = value
        merged["run_id"] = run_id
        merged.setdefault("schema_version", current.get("schema_version") or "1")
        try:
            validate_instance_or_raise_http("run", merged)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        return store.put_run(run_id, merged)

    @v1.get("/runs/{run_id}")
    async def get_run(request: Request, run_id: str) -> dict[str, Any]:
        store: RunLedgerStore = request.app.state.store
        r = store.get_run(run_id)
        if not r:
            raise HTTPException(status_code=404, detail="run not found")
        return r

    @v1.get("/runs")
    async def list_runs(request: Request) -> dict[str, list[dict[str, Any]]]:
        store: RunLedgerStore = request.app.state.store
        return {"runs": store.list_runs()}

    @v1.post("/runs/{run_id}/ledger-events", status_code=201)
    async def append_ledger_event(
        request: Request, run_id: str, body: dict[str, Any]
    ) -> dict[str, Any]:
        store: RunLedgerStore = request.app.state.store
        now = dt.datetime.now(dt.timezone.utc)
        event_id = (body.get("event_id") or "").strip() or str(uuid.uuid4())
        payload = {
            "schema_version": body.get("schema_version") or "1",
            "event_id": event_id,
            "timestamp": body.get("timestamp") or now.isoformat().replace("+00:00", "Z"),
            "workspace_id": body.get("workspace_id") or "default-workspace",
            "project_id": body.get("project_id") or "default-project",
            "run_id": run_id,
            "event_type": body.get("event_type") or "state_transition",
            "actor": body.get("actor") or "system",
            "payload_json": body.get("payload_json") or {},
        }
        if body.get("trace_id") is not None:
            payload["trace_id"] = body["trace_id"]
        if body.get("span_id") is not None:
            payload["span_id"] = body["span_id"]
        try:
            validate_instance_or_raise_http("ledger_event", payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        try:
            return store.append_ledger_event(run_id, payload)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e

    @v1.get("/runs/{run_id}/ledger-events")
    async def list_ledger(request: Request, run_id: str) -> dict[str, list[dict[str, Any]]]:
        store: RunLedgerStore = request.app.state.store
        if store.get_run(run_id) is None:
            raise HTTPException(status_code=404, detail="run not found")
        return {"events": store.list_ledger_events(run_id)}

    @v1.post("/runs/{run_id}/dispatch", status_code=202)
    async def dispatch_run(
        request: Request,
        run_id: str,
        body: dict[str, Any] | None = Body(default=None),
    ) -> dict[str, Any]:
        """Accept a dispatch request; persist audit via ledger (runner execution is stubbed)."""
        store: RunLedgerStore = request.app.state.store
        run = store.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="run not found")
        raw = body if body is not None else {}
        if not isinstance(raw, dict):
            raise HTTPException(status_code=400, detail="body must be a JSON object")
        try:
            dispatch_payload = _normalize_dispatch_body(raw)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        dispatch_id = str(uuid.uuid4())
        dispatch_payload["dispatch_id"] = dispatch_id
        now = dt.datetime.now(dt.timezone.utc)
        ws_id = str(run.get("workspace_id") or "default-workspace")
        proj_id = str(run.get("project_id") or "default-project")
        event = {
            "schema_version": "1",
            "event_id": str(uuid.uuid4()),
            "timestamp": now.isoformat().replace("+00:00", "Z"),
            "workspace_id": ws_id,
            "project_id": proj_id,
            "run_id": run_id,
            "event_type": "dispatch_requested",
            "actor": "system",
            "payload_json": dispatch_payload,
        }
        if run.get("trace_id"):
            event["trace_id"] = run["trace_id"]
        validate_instance_or_raise_http("ledger_event", event)
        store.append_ledger_event(run_id, event)
        return {
            "dispatch_id": dispatch_id,
            "run_id": run_id,
            "status": "accepted",
            "message": "Recorded dispatch_requested; local runner execution not started in this build.",
        }

    app.include_router(v1)

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    return app


app = create_app()
