"""SQLite-backed Run and LedgerEvent store (durable M5+)."""

from __future__ import annotations

import datetime as dt
import json
import sqlite3
import threading
from pathlib import Path
from typing import Any


class SqliteStore:
    """Thread-safe store using SQLite (WAL). Set ``FC_STATE_DB`` to a file path."""

    def __init__(self, db_path: str) -> None:
        self._path = db_path
        parent = Path(db_path).parent
        if parent.as_posix() not in ("", "."):
            parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def _init_schema(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS runs (
                        run_id TEXT PRIMARY KEY,
                        body_json TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS ledger_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                        body_json TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_ledger_run ON ledger_events(run_id, id);
                    CREATE TABLE IF NOT EXISTS run_steps (
                        run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                        step_id TEXT NOT NULL,
                        body_json TEXT NOT NULL,
                        PRIMARY KEY (run_id, step_id)
                    );
                    CREATE INDEX IF NOT EXISTS idx_run_steps_run ON run_steps(run_id);
                    CREATE TABLE IF NOT EXISTS dispatch_jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_id TEXT NOT NULL UNIQUE,
                        run_id TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
                        status TEXT NOT NULL,
                        body_json TEXT NOT NULL,
                        result_json TEXT,
                        created_at TEXT NOT NULL,
                        started_at TEXT,
                        finished_at TEXT
                    );
                    CREATE INDEX IF NOT EXISTS idx_dispatch_jobs_q ON dispatch_jobs(status, id);
                    """
                )

    def put_run(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Upsert run row without deleting the row (preserves ledger FK)."""
        body = json.dumps(payload, sort_keys=True)
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute("SELECT 1 FROM runs WHERE run_id = ?", (run_id,))
                if cur.fetchone():
                    conn.execute(
                        "UPDATE runs SET body_json = ? WHERE run_id = ?",
                        (body, run_id),
                    )
                else:
                    conn.execute(
                        "INSERT INTO runs (run_id, body_json) VALUES (?, ?)",
                        (run_id, body),
                    )
        return dict(payload)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT body_json FROM runs WHERE run_id = ?", (run_id,)
                ).fetchone()
        if row is None:
            return None
        return json.loads(row["body_json"])

    def list_runs(self) -> list[dict[str, Any]]:
        with self._lock:
            with self._connect() as conn:
                rows = conn.execute("SELECT body_json FROM runs ORDER BY run_id").fetchall()
        return [json.loads(r["body_json"]) for r in rows]

    def append_ledger_event(self, run_id: str, event: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(event, sort_keys=True)
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute("SELECT 1 FROM runs WHERE run_id = ?", (run_id,))
                if cur.fetchone() is None:
                    raise KeyError(f"unknown run_id: {run_id}")
                conn.execute(
                    "INSERT INTO ledger_events (run_id, body_json) VALUES (?, ?)",
                    (run_id, body),
                )
        return dict(event)

    def list_ledger_events(self, run_id: str) -> list[dict[str, Any]]:
        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT body_json FROM ledger_events WHERE run_id = ? ORDER BY id",
                    (run_id,),
                ).fetchall()
        return [json.loads(r["body_json"]) for r in rows]

    def put_run_step(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        step_id = str(payload.get("step_id") or "")
        if not step_id:
            raise ValueError("run step requires step_id")
        body = json.dumps(payload, sort_keys=True)
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute("SELECT 1 FROM runs WHERE run_id = ?", (run_id,))
                if cur.fetchone() is None:
                    raise KeyError(f"unknown run_id: {run_id}")
                conn.execute(
                    """
                    INSERT INTO run_steps (run_id, step_id, body_json) VALUES (?, ?, ?)
                    ON CONFLICT(run_id, step_id) DO UPDATE SET body_json = excluded.body_json
                    """,
                    (run_id, step_id, body),
                )
        return dict(payload)

    def list_run_steps(self, run_id: str) -> list[dict[str, Any]]:
        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT body_json FROM run_steps
                    WHERE run_id = ?
                    ORDER BY COALESCE(CAST(json_extract(body_json, '$.sequence_no') AS INTEGER), 0), step_id
                    """,
                    (run_id,),
                ).fetchall()
        return [json.loads(r["body_json"]) for r in rows]

    def enqueue_dispatch_job(
        self, job_id: str, run_id: str, body: dict[str, Any], *, created_at: str
    ) -> dict[str, Any]:
        body_j = json.dumps(body, sort_keys=True)
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute("SELECT 1 FROM runs WHERE run_id = ?", (run_id,))
                if cur.fetchone() is None:
                    raise KeyError(f"unknown run_id: {run_id}")
                conn.execute(
                    """
                    INSERT INTO dispatch_jobs (job_id, run_id, status, body_json, created_at)
                    VALUES (?, ?, 'queued', ?, ?)
                    """,
                    (job_id, run_id, body_j, created_at),
                )
        return self.get_dispatch_job(job_id) or {}

    def get_dispatch_job(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT job_id, run_id, status, body_json, result_json, created_at, started_at, finished_at "
                    "FROM dispatch_jobs WHERE job_id = ?",
                    (job_id,),
                ).fetchone()
        if row is None:
            return None
        body = json.loads(row["body_json"])
        result = json.loads(row["result_json"]) if row["result_json"] else None
        out: dict[str, Any] = {
            "job_id": row["job_id"],
            "run_id": row["run_id"],
            "status": row["status"],
            "created_at": row["created_at"],
            "started_at": row["started_at"],
            "finished_at": row["finished_at"],
            "result": result,
        }
        out.update(body)
        return out

    def claim_next_dispatch_job(self) -> dict[str, Any] | None:
        now_s = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
        with self._lock:
            with self._connect() as conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT job_id, run_id, body_json FROM dispatch_jobs WHERE status = 'queued' ORDER BY id ASC LIMIT 1"
                ).fetchone()
                if row is None:
                    conn.commit()
                    return None
                job_id = row["job_id"]
                cur = conn.execute(
                    "UPDATE dispatch_jobs SET status = 'running', started_at = ? WHERE job_id = ? AND status = 'queued'",
                    (now_s, job_id),
                )
                if cur.rowcount != 1:
                    conn.commit()
                    return None
                conn.commit()
                body = json.loads(row["body_json"])
                return {"job_id": job_id, "run_id": row["run_id"], **body}

    def finish_dispatch_job(
        self,
        job_id: str,
        *,
        status: str,
        result: dict[str, Any] | None,
        finished_at: str,
    ) -> None:
        res_j = json.dumps(result, sort_keys=True) if result is not None else None
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "UPDATE dispatch_jobs SET status = ?, result_json = ?, finished_at = ? WHERE job_id = ?",
                    (status, res_j, finished_at, job_id),
                )

    def count_dispatch_jobs_queued(self) -> int:
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT COUNT(*) AS c FROM dispatch_jobs WHERE status = 'queued'"
                ).fetchone()
        return int(row["c"]) if row else 0
