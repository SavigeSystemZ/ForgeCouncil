# Validation Gates

Validation is mandatory whenever meaningful work lands.

## Minimum rule

If code changed, run at least the impacted validation commands from `_system/PROJECT_PROFILE.md`.

## Validation tiers

### Tier 0: system or docs only

- required: internal consistency review, syntax sanity for config examples, portability review, system-awareness review
- handoff: update impacted docs and continuity files

### Tier 1: small local change

- required: narrow lint, type, or unit check for the touched surface
- handoff: record the exact command and result

### Tier 2: feature work

- required: relevant lint, type, unit, integration, and build checks
- handoff: update test intent if the coverage story changed

### Tier 3: contract, schema, architecture, or migration work

- required: tests plus contract-doc updates, build validation, and migration reasoning
- handoff: update architecture and risk docs

### Tier 4: install, launch, packaging, or deploy-surface work

- required: real runtime or packaging verification, not only static checks
- handoff: record operator-facing effects and release notes

### Tier 5: release claim or milestone signoff

- required: all relevant checks green or explicitly documented as degraded with impact and next step
- handoff: release notes, changelog, current status, and risk posture must be current

## Validation ladder

1. format or lint
2. typecheck
3. unit tests
4. integration or feature tests
5. build
6. launch, smoke, install, or packaging verification when relevant
7. release-specific or operator-facing verification when relevant

## Impact mapping

- logic change: unit tests plus relevant integration checks
- UI change: lint, build, state coverage, and UI-specific tests or smoke checks
- API, schema, or contract change: tests plus contract-doc updates
- design-system or interaction change: visual and state smoke checks plus updated design notes when needed
- install, launch, packaging, or deploy change: runtime verification required
- `_system/`-only change: consistency, syntax sanity, portability, and cross-reference review required
- self-awareness or recovery change: run `bootstrap/check-system-awareness.sh` and `bootstrap/check-hallucination.sh`

## Failure policy

- Do not mark work complete if validation failed and the failure was not recorded.
- Do not hide failing validation by reporting only the passing subset.
- If a check cannot be run, say why and record the gap.
- If the highest-risk check is unavailable, explicitly lower the confidence claim.

## Evidence standard

For every meaningful handoff, record:

- command
- pass or fail result
- scope of what the command covered
- artifact or report path if one exists
- what still remains unproven

See `_system/HANDOFF_PROTOCOL.md` for the full evidence quality requirements.
Run `bootstrap/check-evidence-quality.sh` to validate that handoff claims are
grounded. Run `bootstrap/check-working-file-staleness.sh` to detect stale
handoff surfaces.

## Release and checkpoint rule

Before a checkpoint or release claim:

- relevant validation must be green, or
- the known failures must be explicitly documented with impact and next step
