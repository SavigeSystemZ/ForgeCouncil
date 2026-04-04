# Changelog

Use this file for meaningful repo-visible change history. Keep transient task chatter in `TODO.md` or `WHERE_LEFT_OFF.md`.

## Unreleased

### Added

- SQLite persistence via `FC_STATE_DB` (`sqlite_store.py`), `RunLedgerStore` protocol, `PATCH /v1/runs/{id}`, health `persistence` field; tests `test_sqlite_store.py`
- `.gitignore` `data/` and `.forge-council/` for local state files
- `bootstrap/fc-api-smoke.sh` for `/health` curl smoke
- Optional `FC_API_TOKEN` Bearer auth for `/v1/*` (`auth.py`, OpenAPI security via `HTTPBearer`)
- `POST /v1/runs/{id}/dispatch` (202) + ledger `event_type` `dispatch_requested`
- Gated local `subprocess` dispatch (`local_runner.py`): `FC_ALLOW_SUBPROCESS_DISPATCH`, `FC_EXEC_ALLOWLIST`, `FC_DISPATCH_KILL_SWITCH`, `FC_EXEC_*`; `GET /v1/runs/{id}/run-steps`; `run_steps` table in SQLite; `RunLedgerRunStepStore`
- OpenAPI `components.securitySchemes.bearerAuth` for documented Bearer usage with `FC_API_TOKEN`
- FastAPI control-plane stub: `GET /health`, `POST/GET /v1/runs`, ledger event routes; `forge-council-api` CLI; `schema_util`, `memory_store`; tests in `tests/test_api.py`
- Optional `[api]` extra (`fastapi`, `uvicorn`, `jsonschema`); `tests/conftest.py` sets `FORGE_COUNCIL_REPO_ROOT`
- Forge Council product SSoT docs: `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`, `GPT54.md`, `EXTENSION_ROADMAP.md`
- `_system/forge-council/` operating extension (roles, policies, skills, context, templates)
- `.cursor/rules/fc-*.mdc` and `_system/prompt-packs/forge-council/` (M0–M2 + master handoff)
- `schemas/forge_council/v1/` JSON Schemas and `src/forge_council/` package (`models`, `otel`, `schema_check`)
- `bootstrap/fc-*.sh` automation and `tools/fc_repo_ingestion.py`, `tools/fc_export_resume.py`
- `docs/forge-council/` notes for M5–M7 and M8–M12; `tests/test_schema_check.py`
- `pyproject.toml` for editable install with optional `dev` and `otel` extras
- `_system/KEY.md` as an exhaustive installable system key
- `bootstrap/generate-system-key.sh` as the generator for that key

### Changed

- core discovery and validation flows now treat the system key as a first-class
  installable surface
- Flutter mobile guidance now tells agents to run
  `flutter create --platforms=android .` around the copied minimal foundation
  before expecting Flutter analyze, test, or APK build commands to work
- Python starter-blueprint guidance now tells agents to use a `src/` layout or
  explicit package discovery in `pyproject.toml` inside scaffolded repos
  instead of relying on flat setuptools auto-discovery

### Fixed

- the system-key generator now resolves relative target paths correctly
- `bootstrap/validate-system.sh` now catches stale
  `_system/instruction-precedence.json.template_version` values instead of
  letting that metadata drift silently
- mobile campaign smoke now covers the copied Flutter bootstrap guidance and the
  wrapper still rewrites moved repo-local paths after staging under `apps/`

### Removed

- None recorded yet.
