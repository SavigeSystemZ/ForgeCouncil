# TODO

This is the active execution queue. Keep it tight, factual, and ordered.
Use priority signals: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW** (see
`_system/HANDOFF_PROTOCOL.md` for definitions).

## Bootstrap

- [ ] HIGH: Fill in `_system/PROJECT_PROFILE.md`
- [ ] HIGH: Refine `PRODUCT_BRIEF.md` for Forge Council so the product frame and first build shape are explicit
- [ ] HIGH: Review the recommended starter blueprint and explicitly apply it if the repo is still greenfield
- [ ] MEDIUM: Confirm runtime roots, validation commands, packaging targets, and deployment surfaces
- [ ] MEDIUM: Confirm MCP server set and scope
- [ ] MEDIUM: Establish the first real milestone in `PLAN.md`
- [ ] MEDIUM: Review and refine the seeded first-pass risks in `RISK_REGISTER.md`

## Current Priority

- [ ] HIGH: Establish the first validated baseline for Forge Council

## Immediate Queue

Use short, reviewable tasks with priority signals.

- [ ] MEDIUM: Finish onboarding and confirm the first working validation path for Forge Council

## Next Queue

- [ ] MEDIUM: Begin the first product or platform milestone once onboarding is complete

## Validation Debt

- [ ] MEDIUM: Record the repo's real validation lane in `TEST_STRATEGY.md` after the first successful repo-local check

## Documentation Debt

- [ ] LOW: Keep design, architecture, research, risk, and release surfaces aligned with repo reality

## Completed

Move completed items here at session end.

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
