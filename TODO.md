# TODO

This is the active execution queue. Keep it tight, factual, and ordered.
Use priority signals: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW** (see
`_system/HANDOFF_PROTOCOL.md` for definitions).

## Bootstrap

- [ ] HIGH: Finish filling `_system/PROJECT_PROFILE.md` (stack, ports, ops — validation lines now list ruff/pytest)
- [ ] HIGH: Refine `PRODUCT_BRIEF.md` for Forge Council so the product frame and first build shape are explicit
- [ ] HIGH: Review the recommended starter blueprint and explicitly apply it if the repo is still greenfield
- [ ] MEDIUM: Confirm packaging targets (Flatpak/Snap/AppImage) against current control-plane-only shape
- [ ] MEDIUM: Confirm MCP server set and scope
- [ ] MEDIUM: Review and refine the seeded first-pass risks in `RISK_REGISTER.md`

## Current priority

- [ ] MEDIUM: Push `main` to `origin` when remote backup is desired (branch was ahead of origin)

## Immediate queue

- [ ] MEDIUM: Redis or shared bus for dispatch notifications across **multiple API instances**
- [ ] MEDIUM: Rate limits + per-project queue quotas for `/v1/.../dispatch`

## Next queue

- [ ] LOW: Optional **mypy** strict lane in `pyproject.toml` + `TEST_STRATEGY.md`

## Validation debt

- [x] MEDIUM: Record ruff + pytest in `TEST_STRATEGY.md` and `PROJECT_PROFILE.md` (done 2026-04-04)

## Documentation debt

- [ ] LOW: Align `RELEASE_NOTES.md` Forge Council section with next tagged release

## Completed

- Host install path: `bootstrap/fc-host-install.sh`, `launch-forge-council-api.sh`, desktop + icon, `README` section (2026-04-04)
- Ruff configured; `ruff check` / `ruff format` clean on `src` + `tests` (2026-04-04)
- SSE `GET /v1/dispatch-jobs/{job_id}/events` + broadcaster + tests (2026-04-04)

## Usage rules

- Keep this file current enough that another tool can pick up immediately.
- Use priority signals so the next agent knows what to work on first:
  - **CRITICAL**: blocks users, breaks production, or creates security exposure
  - **HIGH**: blocks the current milestone or other high-priority work
  - **MEDIUM**: planned work that should happen this milestone
  - **LOW**: improvement or cleanup that can wait
- Mark items `[x]` only when fully done, not "mostly done."
- Add discovered work before handoff even if it is low priority.
- Keep product framing in `PRODUCT_BRIEF.md`, product sequencing in `ROADMAP.md`, and active execution structure in `PLAN.md`.
- In the AIAST source repo, maintainer-only template-planning state belongs in the master-repo-only meta workspace instead of this installable file.
