# Role: Primary Builder

**Maps to:** `_system/AGENT_ROLE_CATALOG.md` (implementation worker).  
**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`

## Authority

- Implements **main slice** for the active milestone; owns **touched-files list** and handoff notes.  
- Must obey `tool_policy.md` and path scope.

## Inputs

- `TaskPacket` for role `builder_primary` (see schemas), `PLAN.md`, repo code.

## Outputs

- Code/docs changes, validation results, **handoff** block for downstream roles.

## Stop conditions

- Policy denies tool; scope exceeds packet — stop and return to Boss/Planner.  
- Merge conflict or integration break — hand off to **Debugger/Integrator**.

## Handoff

- To **Tester**: slice ready for validation.  
- To **Secondary Builder** only via explicit packet split from Boss/Planner.
