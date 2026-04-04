# Forge Council — Runbook

**SSoT:** Operator procedures, scripts, and incident handling. For requirements see `PRD.md` and `NFR.md`.

---

## 1. First-time setup (developers)

1. Clone the repository.  
2. Read `AGENTS.md`, `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`, `PRD.md` (skim), `ARCHITECTURE.md` (skim).  
3. Run AIAST validation:  
   `bootstrap/validate-system.sh .`  
4. Run Forge Council ingestion (repo profile + conflict map):  
   `bootstrap/fc-repo-ingestion.sh .`  
5. Review generated `REPO_PROFILE.md` and `CONFLICT_MAP.md`; resolve blocking conflicts before planning execution packets.

## 2. Daily operations

| Action | Command / location |
|--------|---------------------|
| System health | `bootstrap/system-doctor.sh` |
| Instruction layer | `bootstrap/validate-instruction-layer.sh .` |
| Repo ingestion refresh | `bootstrap/fc-repo-ingestion.sh .` then `bootstrap/generate-operating-profile.sh . --write` |
| Controlled run stub (dry) | `bootstrap/fc-controlled-run.sh --dry-run` |
| Gate check stub | `bootstrap/fc-gate-check.sh --help` (add `--full-validate` to run `validate-system.sh`) |
| Resume packet export | `bootstrap/fc-export-resume-packet.sh .` |
| Validate FC schemas | `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"` then `PYTHONPATH=src .venv/bin/python -m forge_council.schema_check` |

Full system validation: `bootstrap/validate-system.sh .` (expect `system_ok`).

## 3. Control plane HTTP API (M5+ stub)

Default bind: `127.0.0.1:8010` (override with `FC_API_HOST`, `FC_API_PORT`).

**Persistence:** unset `FC_STATE_DB` → in-memory (lost on restart). Set `FC_STATE_DB` to a file path (e.g. `data/forge-council/state.db`) for **SQLite** (WAL) runs + ledger events.

```bash
.venv/bin/pip install -e ".[api]"
export FC_STATE_DB="${PWD}/data/forge-council/state.db"
mkdir -p "$(dirname "$FC_STATE_DB")"
forge-council-api
# or: .venv/bin/python -m forge_council.server
```

- `GET /health` — liveness (`persistence`, `auth_required`, `dispatch_kill_switch`, `subprocess_dispatch_enabled`, `async_dispatch_enabled`, `artifact_root_configured`)  
- `POST /v1/runs` — create run (body validated against `schemas/forge_council/v1/run.json`)  
- `PATCH /v1/runs/{run_id}` — partial update (`status`, `mode`, `milestone_id`, `workspace_id`, `finished_at`, `started_at`, `trace_id`, `cost_summary_json`, `initiated_by`, `project_id`)  
- `GET /v1/runs/{run_id}` — fetch run  
- `GET /v1/runs` — list runs  
- `POST /v1/runs/{run_id}/ledger-events` — append ledger event (`ledger_event.json`)  
- `GET /v1/runs/{run_id}/ledger-events` — list events  
- `POST /v1/runs/{run_id}/dispatch` — always appends `dispatch_requested` to the ledger. Optional `execution`: `sync` (default) or `async`.  
  - `action`: `noop` or `subprocess_stub` → **202** (audit only; no subprocess).  
  - `action`: `subprocess` + `execution: sync` → **200** when the subprocess finishes **in the HTTP request** (same persistence as below).  
  - `action`: `subprocess` + `execution: async` → **202** with `job_id` (**requires** `FC_ALLOW_ASYNC_DISPATCH=1`); a background worker claims jobs from SQLite (or in-memory) and runs the same completion path. Poll `GET /v1/dispatch-jobs/{job_id}` or subscribe to **SSE** `GET /v1/dispatch-jobs/{job_id}/events` (stream ends in terminal state).  
  - Subprocess path: **no shell**, `run_step` + terminal run + `tool_invocation_meta` (snippets + byte counts; full logs optional under `FC_ARTIFACT_ROOT`). **Gated** (see below).  
- `GET /v1/runs/{run_id}/run-steps` — list persisted steps for the run  
- `GET /v1/dispatch-jobs/{job_id}` — job status (`queued` \| `running` \| `completed` \| `failed`) and `result` payload when finished  
- `GET /v1/dispatch-jobs/{job_id}/events` — **text/event-stream** (SSE): JSON snapshots on change until `completed` or `failed` (in-process only; not shared across API replicas)  

**Subprocess dispatch gates (secure default: off):**  

| Variable | Purpose |
|----------|---------|
| `FC_DISPATCH_KILL_SWITCH` | If `1`/`true`/`yes`/`on`, refuse `subprocess` dispatch (**503**) after logging `dispatch_requested`. |
| `FC_ALLOW_SUBPROCESS_DISPATCH` | Must be `1`/`true`/`yes`/`on` to allow `subprocess` (**403** otherwise). |
| `FC_EXEC_ALLOWLIST` | Comma-separated **absolute paths** permitted as `argv[0]` (**403** if empty or no match). |
| `FC_EXEC_WORKDIR` | Process working directory (default: `FORGE_COUNCIL_REPO_ROOT`, else cwd). |
| `FC_EXEC_TIMEOUT_SEC` | Wall-clock cap per subprocess (default 60, max 3600). |
| `FC_EXEC_INHERIT_ENV` | Default `1`: merge `env` from the request onto the server environment. Set `0` for a minimal `PATH`-only baseline plus request `env`. |
| `FC_ALLOW_ASYNC_DISPATCH` | Must be `1`/`true`/`yes`/`on` to use `execution: async` on subprocess dispatch (**403** otherwise). |
| `FC_DISPATCH_MAX_QUEUED` | Optional positive cap on **queued** jobs; enqueue returns **503** when full. |
| `FC_ARTIFACT_ROOT` | If set, writes full `stdout.log` / `stderr.log` under `{root}/{run_id}/{step_id}/` (16 MiB cap per stream); ledger carries `stdout_artifact_relpath` / `stderr_artifact_relpath`. |

**Backup:** copy the SQLite file while the process is stopped or use SQLite backup API; `data/` is gitignored by default.  

Set `OTEL_EXPORTER_OTLP_ENDPOINT` to enable OTLP export (optional `pip install -e ".[otel]"`).  
Optional CORS: `FC_CORS_ORIGINS=http://127.0.0.1:3000`.  
Optional auth: set `FC_API_TOKEN` to a long random secret; send `Authorization: Bearer <token>` on all `/v1/*` requests (`/health` remains open for load balancers). When the token is set, **OpenAPI** marks each `/v1/*` operation with `bearerAuth` security.  
Schemas resolve via `FORGE_COUNCIL_REPO_ROOT` (defaults to parent of `src/` in dev).

## 4. Kill-switch and escalation

1. **Stop new runs:** set `FC_DISPATCH_KILL_SWITCH=1` on the API host (refuses `subprocess` dispatch); set workspace flag (future UI); document in `WHERE_LEFT_OFF.md`.  
2. **Revoke API keys** at provider if abuse suspected.  
3. **Disable MCP servers** in workspace manifest.  
4. Follow `_system/forge-council/policies/escalation_policy.md`.

## 5. Backup and recovery

- **Git:** Canonical docs and `_system/forge-council/` are versioned; commit often.  
- **Control-plane state:** if using `FC_STATE_DB`, include that file in backups (see §3).  
- **Artifacts:** sync object store per operator policy.

## 6. Telemetry

- Set `OTEL_EXPORTER_OTLP_ENDPOINT` when OTLP backend available.  
- Use `src/forge_council/otel.py` helpers; never attach raw prompts to spans.

## 7. Incident response (secrets)

If a secret is committed:

1. Rotate the credential immediately.  
2. Purge from git history if required by policy (use org-standard tools).  
3. Record in `RISK_REGISTER.md` and governance notes.

## 8. Release checklist (high level)

- `bootstrap/validate-system.sh .` passes.  
- `REPO_PROFILE.md` / `CONFLICT_MAP.md` current.  
- `CHANGELOG.md` updated.  
- No secrets in diff.  
- `TEST_STRATEGY.md` reflects executed validations.

## 9. Contacts and ownership

- Product docs: repo maintainers per `AGENTS.md` handoff rules.  
- Security policy: `_system/forge-council/policies/`.

---

## Script index (Forge Council)

| Script | Purpose |
|--------|---------|
| `bootstrap/fc-repo-ingestion.sh` | Scan instructions; emit/update `REPO_PROFILE.md`, `CONFLICT_MAP.md`; refresh machine hints |
| `bootstrap/fc-controlled-run.sh` | Placeholder for single-milestone dispatch contract |
| `bootstrap/fc-gate-check.sh` | Placeholder validation/review gate driver |
| `bootstrap/fc-export-resume-packet.sh` | Emit `RESUME_PACKET.md` skeleton from repo state |
| `bootstrap/fc-api-smoke.sh` | `curl` `/health` (server must be running) |
