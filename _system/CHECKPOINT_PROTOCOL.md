# Checkpoint Protocol

Run this at the end of a milestone, at risky turning points, or before switching tools after meaningful work.

## Goals

- prevent loss of work
- keep changes reviewable
- ensure important work ends verified
- leave a clean resumption point

## Trigger examples

- milestone or phase completion
- risky refactor landing
- architecture or design direction shift
- install, launch, packaging, or release-path change
- handoff between tools or humans after meaningful work

## Steps

1. Confirm the intended scope is actually complete enough to checkpoint.
2. Review the current state and ensure the changed files are intentional.
3. Run the relevant validation gates.
4. Update:
   - `TODO.md`
   - `FIXME.md`
   - `PRODUCT_BRIEF.md` when product direction or starter-blueprint choice changed
   - `PLAN.md` when the active execution picture changed
   - `TEST_STRATEGY.md` when validation expectations changed
   - `RISK_REGISTER.md` when delivery confidence changed
   - `WHERE_LEFT_OFF.md`
   - `CHANGELOG.md`
   - `RELEASE_NOTES.md` for release-facing changes
   - `_system/context/CURRENT_STATUS.md` when the overall state shifted
   - `_system/context/DECISIONS.md` when a durable choice was made
5. Create or refresh the project backup if the repo's workflow requires it.
6. Record blockers and next step honestly.

## Stop conditions

- do not checkpoint as "complete" if validation failed and that failure is undocumented
- do not snapshot secrets or machine-local credentials
- do not hand off ambiguous partial work without saying exactly what remains
