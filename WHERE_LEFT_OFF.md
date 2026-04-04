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

- Current phase: Master planning pack **landed** (canonical docs, FC OS tree, schemas, bootstrap, tests)
- Working branch or lane: `main`
- Completion status: planning-pack implementation complete; control-plane service not started
- Resume confidence: high for docs/automation; implementation TBD

## Last Completed Work

Implemented the **Forge Council Master Architecture and Planning Pack** in-repo:

- Product SSoT: `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`, `GPT54.md`, `EXTENSION_ROADMAP.md`, operational stubs (`DECISIONS`, `EVAL_REPORT`, etc.).
- Extension tree: `_system/forge-council/{roles,policies,skills,context,templates}`.
- Cursor rules: `.cursor/rules/fc-*.mdc`.
- Prompt packs: `_system/prompt-packs/forge-council/*` (master handoff, M0–M2).
- M1 automation: `tools/fc_repo_ingestion.py`, `bootstrap/fc-repo-ingestion.sh`.
- Schemas: `schemas/forge_council/v1/*.json`; package `src/forge_council/` (`models.py`, `otel.py`, `schema_check.py`).
- M5–M7 stubs: `bootstrap/fc-controlled-run.sh`, `fc-gate-check.sh`, `fc-export-resume-packet.sh`; docs under `docs/forge-council/`.
- Tests: `tests/test_schema_check.py` (pytest); use `.venv` for local dev (`python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"`).
- Regenerated `_system/SYSTEM_REGISTRY.json` and `_system/REPO_OPERATING_PROFILE.md`; `bootstrap/validate-system.sh .` passes.

## Files Changed

See git status — large multi-file addition across docs, `_system/`, `.cursor/`, `schemas/`, `src/`, `bootstrap/`, `tools/`, `tests/`, `pyproject.toml`, `README.md`.

## Validation Run

- Command: `bootstrap/validate-system.sh /home/whyte/.MyAppZ/ForgeCouncil`
- Result: pass (`system_ok`)
- Command: `.venv/bin/pytest` (after `pip install -e ".[dev]"`)
- Result: pass (2 tests)

## Decisions Made

- Namespaced Forge-specific OS under `_system/forge-council/` to preserve AIAST upgrade path.
- JSON Schema as interchange SSoT; Python package must not import `_system/`.

## Open Risks / Blockers

- Choose control-plane HTTP stack (e.g. FastAPI) and desktop shell before heavy UI work.
- After adding instruction files, run `bootstrap/fc-repo-ingestion.sh .` then `bootstrap/generate-operating-profile.sh . --write` as repo owner.

## Next Best Step

Implement a minimal **FastAPI** (or chosen) service with health check and `Run`/`LedgerEvent` persistence stub, wired to `schemas/forge_council/v1/run.json`, plus optional OTLP export using `src/forge_council/otel.py`.

## Handoff Packet

- Agent: Cursor / implementation pass
- Timestamp: 2026-04-04
- Objective: Land master planning pack per approved plan
- Files changed: (see git diff — broad)
- Commands run: `validate-system.sh`, `generate-system-registry.sh --write`, `pytest`, `fc-repo-ingestion.py`
- Result summary: Repo validates; schemas and ingestion automation in place; ready for control-plane coding milestone.
- Known blockers: none
- Next best step: (matches section above)

## Usage rules

- This is the first file an incoming agent should read on resume.
- Keep it concise, factual, and action-oriented.
- All claims must be grounded in evidence (see `_system/HANDOFF_PROTOCOL.md`).
- Run `bootstrap/check-working-file-staleness.sh` to verify this file is current.
- Run `bootstrap/check-evidence-quality.sh` to verify claims are grounded.
- In the AIAST source repo, maintainer-only handoff state belongs in the master-repo-only meta workspace instead of this installable file.
