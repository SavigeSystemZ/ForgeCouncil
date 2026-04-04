# Forge Council — Agent operating extension

This directory **extends** the AIAST core in `_system/`. It does not replace `AGENTS.md`, `INSTRUCTION_PRECEDENCE_CONTRACT.md`, or `AGENT_ROLE_CATALOG.md`.

## Precedence

1. Repo-local runtime facts (code, config).  
2. Product SSoT: `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`.  
3. AIAST core (`_system/` excluding this subtree for FC-specific rules).  
4. **`_system/forge-council/`** — Forge Council roles, policies, skills, templates.  
5. Tool overlays and prompt packs.  
6. Host orchestration context.

On conflict: **do not merge silently** — record in `CONFLICT_MAP.md` and follow `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`.

## Contents

| Path | Purpose |
|------|---------|
| `roles/` | Authority, stop conditions, handoff rules per council role |
| `policies/` | Tool, approval, memory, precedence, export, escalation |
| `skills/` | Repeatable procedures (checklist-style) |
| `context/` | Product/architecture/security/quality/UX/integration context |
| `templates/` | Task packet, decision, resume, review, milestone, profile, conflict |

## Related

- `_system/AGENT_ROLE_CATALOG.md` — generic role taxonomy  
- `_system/MULTI_AGENT_COORDINATION.md` — delegation patterns  
- `_system/VALIDATION_GATES.md` — gate philosophy  
- `_system/prompt-packs/forge-council/` — exported prompts  
- `schemas/forge_council/v1/` — JSON Schema interchange
