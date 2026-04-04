# Forge Council — Architecture Decision Records

**SSoT:** Durable L2 decisions (mirror of database `DecisionRecord` where applicable).  
Use `_system/forge-council/templates/decision_record.template.md` for new entries.

## Active decisions

| ID | Date | Title | Status |
|----|------|-------|--------|
| ADR-001 | 2026-04-04 | Hybrid Build Fabric (desktop-first, optional web, multi-runner) | accepted |
| ADR-002 | 2026-04-04 | Modular monolith control plane + isolated runners | accepted |
| ADR-003 | 2026-04-04 | Forge-specific OS under `_system/forge-council/` (AIAST extension) | accepted |
| ADR-004 | 2026-04-04 | JSON Schema as interchange SSoT under `schemas/forge_council/v1/` | accepted |

## Template

```markdown
## ADR-XXX: Title

- **Status:** proposed | accepted | superseded
- **Date:** YYYY-MM-DD
- **Context:** …
- **Decision:** …
- **Consequences:** …
- **Supersedes:** (optional)
```
