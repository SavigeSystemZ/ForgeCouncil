# Forge Council — Resume Packet

**Purpose:** Cold-start handoff for the next human or agent session (L1 + L2 pointers).  
**Do not** rely on chat history alone.

## Last updated

- **Date:** 2026-04-04  
- **By:** (initial scaffold)

## What was done

- Master planning pack implemented: canonical docs, `_system/forge-council/`, schemas, bootstrap scripts, prompt packs.

## Current milestone focus

- Complete M0–M1 automation hardening and first control-plane service slice (see `PLAN.md`).

## Files to load first

1. `AGENTS.md`  
2. `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`  
3. `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`  
4. `_system/forge-council/README.md`  
5. `PLAN.md`, `WHERE_LEFT_OFF.md`

## Open questions

- Desktop framework choice (Tauri vs Qt) — decision gate before UI work.

## Next actions

1. Run `bootstrap/fc-repo-ingestion.sh .` after substantive instruction changes.  
2. Implement FastAPI control plane skeleton per `PLAN.md`.  
3. Wire OTel in first long-running service.

## Validation last run

- `bootstrap/validate-system.sh .` — (record outcome when run)

## Blockers

- (none recorded)
