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

- Current phase: Control-plane API with **SQLite** persistence + **PATCH** runs
- Working branch or lane: `main`
- Completion status: `FC_STATE_DB`, `sqlite_store`, ledger preserved on run update; smoke script added
- Resume confidence: high

## Last Completed Work

- `SqliteStore`, `RunLedgerStore` protocol, `PATCH /v1/runs/{id}`, health `persistence`, UPSERT fix (ledger survives run updates).
- `tests/test_sqlite_store.py`, extended `test_api.py`; `bootstrap/fc-api-smoke.sh`.
- Docs: `RUNBOOK`, `ARCHITECTURE`, `DATA_MODEL`, `CHANGELOG`; `.gitignore` `data/`.

## Validation Run

- `.venv/bin/pytest` — pass
- `bootstrap/validate-system.sh .` — run after `generate-system-registry.sh --write` (expect `system_ok`)

## Next Best Step

Wire **dispatch** to a real **local runner** (subprocess or worker): consume `argv` / `env`, update run `status`, append `run_step` or artifact refs. Add **run_step** persistence in store if not only via ledger.

**Done recently:** `POST /v1/runs/{id}/dispatch` records `dispatch_requested` in ledger (execution still stubbed); optional `FC_API_TOKEN` on `/v1/*`.

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
