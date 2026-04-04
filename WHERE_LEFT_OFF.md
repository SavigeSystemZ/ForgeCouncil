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

- Current phase: Control-plane API with **SQLite** + **gated subprocess dispatch** + **run steps**
- Working branch or lane: `main`
- Completion status: `FC_STATE_DB`, ledger-safe upsert, `FC_ALLOW_SUBPROCESS_DISPATCH` + allowlist runner, `run_steps` persistence
- Resume confidence: high

## Last Completed Work

- `RunLedgerRunStepStore`, `run_steps` in `SqliteStore` / `MemoryStore`, `GET /v1/runs/{id}/run-steps`.
- `POST /v1/runs/{id}/dispatch` with `action=subprocess` (async subprocess, ledger `tool_invocation_meta`, run status terminal); `noop` / `subprocess_stub` remain audit-only (202).
- `local_runner.py`, `NFR` SEC-12, `RUNBOOK` operator env table; tests for gates and SQLite steps.

## Validation Run

- `.venv/bin/pytest` — pass
- `bootstrap/validate-system.sh .` — run after `generate-system-registry.sh --write` (expect `system_ok`)

## Next Best Step

- **Async job queue** (background worker) so long subprocesses do not block the HTTP request; poll or SSE for step status.  
- **Artifact refs** for full stdout/stderr (object store or workspace path) instead of only ledger snippets.  
- **OpenAPI** `securitySchemes` when `FC_API_TOKEN` is set (dynamic schema) and richer route descriptions.

**Done recently:** Gated in-process subprocess dispatch, `run_steps` API + SQLite, health flags for operator posture.

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
