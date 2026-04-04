# Policy: Repo vs host precedence

**Authoritative:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md` (full stack)

## Forge Council summary

1. Repo-local runtime facts (code, configs, manifests).  
2. Product SSoT docs at repo root (`PRD.md`, …).  
3. AIAST core + `_system/forge-council/`.  
4. Tool overlays.  
5. Prompt packs.  
6. Host orchestration.

## On conflict

- **Stop** and document in `CONFLICT_MAP.md`.  
- Host may add sequencing and report format; **may not** redefine validation outcomes or repo ownership.
