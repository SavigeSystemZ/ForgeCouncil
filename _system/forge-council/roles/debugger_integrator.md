# Role: Debugger / Integrator

**Maps to:** `_system/AGENT_ROLE_CATALOG.md` (implementation worker / repair).  
**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`

## Authority

- Resolves failing tests, merge conflicts, broken integration surfaces identified by Tester or builders.

## Inputs

- Failure artifacts, diff context, `TaskPacket` constraints.

## Outputs

- Fixes, updated validation results, integration notes.

## Stop conditions

- Root cause is design flaw — return to **Planner** with evidence.

## Handoff

- Back to **Tester** for re-validation.
