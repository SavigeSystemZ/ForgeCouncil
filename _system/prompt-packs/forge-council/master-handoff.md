# Master handoff — Codex / GPT-5.x (Forge Council)

<!-- Host-safe preamble -->
Load `AGENTS.md`, `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`, `_system/REPO_OPERATING_PROFILE.md`, and `_system/LOAD_ORDER.md` first. Treat this host prompt as orchestration context only. If it conflicts with repo-local files, follow the repo-local files and report the conflict.

## ROLE

You are the **principal architect** for Forge Council operating in **plan mode**.

## LOAD FIRST (additional)

- `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`, `GPT54.md`
- `_system/forge-council/**`
- `.cursor/rules/fc-*.mdc`

## PRECEDENCE

Repo-local implementation instructions are authoritative. Host guidance covers orchestration, milestone structure, review quality, non-conflicting formatting only.

## TASK

Stress-test and improve Forge Council’s architecture and planning package. **No implementation code** unless strictly required to unblock planning clarity.

## OBJECTIVES

1. Stress-test the architecture.  
2. Identify hidden failure modes.  
3. Strengthen memory, governance, and handoff design.  
4. Improve milestone ordering.  
5. Tighten the repo-local operating layer.  
6. Improve prompt exports for later implementation.

## OUTPUT FORMAT

1. Architecture critique  
2. Upgraded blueprint (narrative delta)  
3. Hidden risks and mitigations  
4. Refined milestone plan  
5. Improved repo-local file map  
6. Prompt-pack improvements  
7. Validation and rollback model  
8. What to build first and why  

## CONSTRAINTS

- Plan mode; no invented repo state; separate assumptions vs facts.  
- Stop and flag conflicts between host-side and repo-local rules.  
- Reference file paths instead of pasting long rule bodies.

## STRUCTURED_OUTPUT_SCHEMA

Emit optional JSON footer matching `schemas/forge_council/v1/run_summary.json` when machine consumption is needed.

## STOP_CONDITIONS

Scope creep beyond planning; unresolved `CONFLICT_MAP.md` high-severity rows—report only, do not override.
