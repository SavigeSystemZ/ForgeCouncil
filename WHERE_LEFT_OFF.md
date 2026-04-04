# Where Left Off

This is the primary resume surface for the next agent or human in an **installed
app repo**. Read this file first on session start. See `_system/HANDOFF_PROTOCOL.md`
for quality requirements.

## AIAST source repository

If you are working in **`_AI_AGENT_SYSTEM_TEMPLATE`** (master template repo),
maintainer continuity and validation evidence live in **`_META_AGENT_SYSTEM/WHERE_LEFT_OFF.md`**
instead of this file. Update this file only for work that ships to downstream
app repositories.

## Session snapshot

- **Phase:** Forge Council control-plane API (FastAPI): async dispatch, **SSE** job stream, artifacts, Bearer `/v1`, **host install + desktop launcher**, **Ruff** lint/format.
- **Branch:** `main` (local commits ahead of `origin/main`; **push when ready**).
- **Resume confidence:** high.

## Last completed work

- **API:** `GET /v1/dispatch-jobs/{job_id}/events` (SSE); `dispatch_job_broadcaster.py`; worker publishes snapshots after claim and after `finish_dispatch_job`.
- **Install:** `bootstrap/fc-host-install.sh` (venv, `pip install -e '.[dev,api]'`, user desktop entry, hicolor SVG icon); `ops/install/launch-forge-council-api.sh` replaces generic `http.server` for desktop/systemd `Exec=`.
- **Quality:** Ruff in `pyproject.toml` `[dev]` + `tool.ruff`; `sqlite_store` / `dispatch_worker` / OpenAPI tag cleanups; per-file `B008` ignores for FastAPI deps.
- **Docs:** `README.md` host install section, `RUNBOOK.md` SSE line, `CHANGELOG.md`, `_system/PROJECT_PROFILE.md` validation commands, `packaging/io.aiaast.forge.council.desktop` template note.

## Validation run (evidence)

- `.venv/bin/pytest` — 29 passed
- `.venv/bin/ruff check src tests` — clean
- `bootstrap/fc-host-install.sh` + `ops/install/launch-forge-council-api.sh` + `curl http://127.0.0.1:8010/health` — OK (run installer as **desktop user** so `~/.local/share/applications` is yours, not root)
- `bootstrap/validate-system.sh .` — run after `generate-system-registry.sh --write` when touching registry/system files (expect `system_ok`)

## Next best step

- **Redis** (or similar) for SSE / queue when **multiple API replicas** exist.
- **Multi-instance** worker (separate process) + external queue.
- **Rate limits** and **per-project** dispatch quotas.
- **Push** `main` to `origin` when you want remote backup: `git push origin main`.

## Stopping now

- Working tree saved in **git** (single commit after this update). No further edits queued for this session.
- Re-open with: read this file → `PLAN.md` → `TODO.md` → run validation from `_system/PROJECT_PROFILE.md`.

## Handoff packet

- Timestamp: 2026-04-04
- Git: commit on `main` with message describing SSE + install + Ruff (see `git log -1`)

## Usage rules

- This is the first file an incoming agent should read on resume.
- Keep it concise, factual, and action-oriented.
- All claims must be grounded in evidence (see `_system/HANDOFF_PROTOCOL.md`).
- Run `bootstrap/check-working-file-staleness.sh` to verify this file is current.
- Run `bootstrap/check-evidence-quality.sh` to verify claims are grounded.
- In the AIAST source repo, maintainer-only handoff state belongs in the master-repo-only meta workspace instead of this installable file.
