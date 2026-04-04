# Policy: Escalation and kill-switch

**Related:** `RUNBOOK.md`, `NFR.md` SEC-10

## Escalate to human (Boss operator)

- Repeated gate failures &gt; threshold.  
- Cost surge beyond budget policy.  
- Suspected prompt injection or policy bypass.  
- Cross-project memory anomaly signals.

## Kill-switch

- Halt new **Run** creation; complete or cancel in-flight with audit reason.  
- Disable MCP and external tools at workspace level.  
- Rotate credentials if leakage suspected.

## Recording

- All escalations append L4 event with `trace_id` when available.
