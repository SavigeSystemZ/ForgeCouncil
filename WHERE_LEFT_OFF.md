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

- Current phase: Onboarding
- Working branch or lane: `main`
- Completion status: not set yet — fill after meaningful work
- Resume confidence: low until updated

## Last Completed Work

Installed the local AI operating system for Forge Council and seeded the first working surfaces.
- Bad: "Made progress on the API"
- Good: "Implemented GET /users and POST /users with input validation. 4 pytest tests passing."

## Files Changed

List files changed in the last meaningful pass. Omit if recorded in the
Handoff Packet below.

## Validation Run

- Command: bootstrap/validate-system.sh /home/whyte/.MyAppZ/ForgeCouncil --strict
- Result: pass
- Scope: AIAST install integrity, required files, config syntax, and awareness validation

If no validation was run, write "No validation run this session" and note why.

## Decisions Made

Record durable decisions made during the last pass. Move decisions with
long-term significance to `_system/context/DECISIONS.md`.

## Open Risks / Blockers

Record anything that could change the next agent's approach. Include:
- Known failing tests or broken features
- External dependencies that are unavailable
- Permission or environment issues
- Partially completed migrations or refactors

## Next Best Step

State the single most valuable next action as a concrete instruction:
- Bad: "Continue working on the feature"
- Good: "Implement PATCH /users/:id with partial-update semantics, then add integration tests for the auth middleware"

## Handoff Packet

- Agent: (which agent or human performed the work)
- Timestamp: (date of handoff, e.g., 2026-01-15)
- Objective: (what the session set out to accomplish)
- Files changed: (list of modified files)
- Commands run: (key commands with results)
- Result summary: (1-3 sentence outcome)
- Known blockers: (what could stop the next agent, or "none")
- Next best step: (matches the section above)

## Usage rules

- This is the first file an incoming agent should read on resume.
- Keep it concise, factual, and action-oriented.
- All claims must be grounded in evidence (see `_system/HANDOFF_PROTOCOL.md`).
- Run `bootstrap/check-working-file-staleness.sh` to verify this file is current.
- Run `bootstrap/check-evidence-quality.sh` to verify claims are grounded.
- In the AIAST source repo, maintainer-only handoff state belongs in the master-repo-only meta workspace instead of this installable file.
