# Test Strategy

Use this file to define the repo's confidence model, validation lanes, and known coverage gaps.

## Confidence model

- required confidence for local changes: run the smallest impacted validation lane plus any touched bootstrap or system checks
- required confidence for risky changes: run unit, integration, and any relevant smoke, build, packaging, or security lanes before handoff
- required confidence for release candidates: run every defined lane in this file and record exact outcomes in release-facing notes or handoff

## Validation lanes

- format: `.venv/bin/ruff format src tests` (after `pip install -e ".[dev]"`)
- lint: `.venv/bin/ruff check src tests`
- typecheck: no mypy/pyright lane configured yet; optional follow-up
- unit tests: `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]" && .venv/bin/pytest` (schema check, FastAPI `TestClient` routes, SQLite store)
- integration tests: no integration-test command inferred yet; confirm manually
- end-to-end or smoke: no smoke command inferred yet; confirm manually
- build or packaging checks: no build or packaging command inferred yet; confirm manually
- security or policy checks: bootstrap/scan-security.sh /home/whyte/.MyAppZ/ForgeCouncil

## Coverage expectations

- critical flows that must be proven: primary user flow, startup or install path, and any high-risk surface touched by the change
- areas allowed to rely on lighter validation: docs, prompt wording, and low-risk content-only changes after targeted checks
- expected evidence for high-risk changes: exact commands run, pass or fail outcomes, notable warnings, and any skipped lanes with reasons

## Known gaps

- Confirm the seeded validation lanes against the first real repo-local run and record any missing coverage explicitly.

## Usage rules

- Keep this aligned with `RISK_REGISTER.md` and `RELEASE_NOTES.md`.
- Record what confidence is required, not just what happens to exist today.
