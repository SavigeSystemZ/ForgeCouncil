# Policy: Human approval

**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`  
**Related:** `NFR.md` SEC-05

## Requires explicit approval artifact (L4)

- Destructive filesystem operations outside temp dirs.  
- Force push, history rewrite, production deploy hooks.  
- Sending secrets or PII to external APIs.  
- Disabling security controls or expanding tool allowlist globally.

## Approval object (minimum)

- `approval_id`, `actor`, `timestamp`, `action_summary`, `risk_ack`, `expires_at` optional.

## Storage

- Append to governance ledger; human-readable summary may mirror in `DECISIONS.md` when durable.
