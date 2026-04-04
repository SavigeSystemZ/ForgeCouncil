# Context: Security

LLM-app threats (injection, tool abuse, leakage, cross-project memory, cost DoS) are **in scope from day one**. Controls: `NFR.md`, `policies/tool_policy.md`, `policies/approval_policy.md`, `policies/memory_policy.md`.

Never log raw secrets or full prompts to shared telemetry.
