# Where Left Off

This is the primary resume surface for the next agent or human in an **installed
app repo**. Read this file first on session start. See `_system/HANDOFF_PROTOCOL.md`
for quality requirements.

## AIAST source repository

If you are working in **`_AI_AGENT_SYSTEM_TEMPLATE`** (master template repo),
maintainer continuity and validation evidence live in **`_META_AGENT_SYSTEM/WHERE_LEFT_OFF.md`**
instead of this file. Update this file only for work that ships to downstream
app repositories.

## Session Snapshot

- Current phase: Control-plane API with **async dispatch queue**, **log artifacts**, **OpenAPI Bearer on /v1**
- Working branch or lane: `main`
- Completion status: `dispatch_jobs` + worker loop, `execution: async`, `FC_ARTIFACT_ROOT`, per-route OpenAPI security when `FC_API_TOKEN` set
- Resume confidence: high

## Last Completed Work

- `RunLedgerRunStepJobStore`, `dispatch_jobs` (SQLite + memory), `dispatch_worker` + app `lifespan`, `GET /v1/dispatch-jobs/{id}`.
- `POST .../dispatch` with `execution: async` + `FC_ALLOW_ASYNC_DISPATCH`; sync path uses shared `dispatch_execution.execute_subprocess_dispatch`.
- `FC_ARTIFACT_ROOT` log files, ledger `stdout_artifact_relpath` / `stderr_artifact_relpath`, `FC_DISPATCH_MAX_QUEUED`.
- OpenAPI attaches `bearerAuth` to each `/v1/*` operation when the API token env is set; health flags for async + artifact root.

## Validation Run

- `.venv/bin/pytest` — 26 passed
- `bootstrap/validate-system.sh .` — run after `generate-system-registry.sh --write` (expect `system_ok`)

## Next Best Step

- **SSE or WebSocket** for job completion instead of polling `GET /v1/dispatch-jobs/{id}`.  
- **Multi-instance** queue (Redis / separate worker process) — current worker is in-process with SQLite row locking.  
- **Rate limits** and **per-project** queue quotas.

**Done recently:** In-process async queue + artifacts + OpenAPI per-route Bearer when token configured.

## Handoff Packet

- Timestamp: 2026-04-04
- Next best step: (matches section above)

## Usage rules

- This is the first file an incoming agent should read on resume.
- Keep it concise, factual, and action-oriented.
- All claims must be grounded in evidence (see `_system/HANDOFF_PROTOCOL.md`).
- Run `bootstrap/check-working-file-staleness.sh` to verify this file is current.
- Run `bootstrap/check-evidence-quality.sh` to verify claims are grounded.
- In the AIAST source repo, maintainer-only handoff state belongs in the master-repo-only meta workspace instead of this installable file.
