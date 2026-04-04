# Policy: Tool use

**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`  
**Related:** `NFR.md` SEC-02, SEC-03, SEC-04

## Principles

- **Allowlist-first:** only declared tools per `AgentProfile`.  
- **Path-scoped** filesystem: workspace roots from project config only.  
- **Branch-scoped** git: explicit branch names; no force-push without L4 approval.

## Denylist (examples)

- Arbitrary `curl` to unknown hosts without approval.  
- Package publish, infra destroy, production DB drop.

## MCP servers

- Registered in workspace manifest; disabled until operator enables and policy binds.

## Enforcement

- Orchestrator rejects tool calls outside policy; log **policy decision** to ledger (metadata only).
