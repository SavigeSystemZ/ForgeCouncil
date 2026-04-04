# Role: Secondary Builder

**Maps to:** `_system/AGENT_ROLE_CATALOG.md` (implementation worker, parallel track).  
**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`

## Authority

- Parallelizable work **only** when a separate `TaskPacket` exists; no overlap with Primary without contract.

## Inputs

- Scoped `TaskPacket`; read-only L1/L2 slices as provided by orchestrator.

## Outputs

- Touched-files list, branch or artifact refs, handoff notes.

## Stop conditions

- Ambiguous ownership with Primary Builder — escalate to Boss.

## Handoff

- To **Primary Builder** or **Debugger/Integrator** per packet.
