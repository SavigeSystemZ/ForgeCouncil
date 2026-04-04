# Forge Council — Non-Functional Requirements

**SSoT:** Quality, security, performance, and operability attributes.

---

## 1. Security (LLM-app native)

### 1.1 Threat classes (in scope)

- Prompt injection and instruction override attempts.  
- Malicious or conflicting **repo-local** instructions.  
- Insecure or over-privileged **tool** invocation.  
- Destructive actions without approval.  
- Sensitive data leakage (logs, traces, exports).  
- Cross-project **memory** contamination.  
- Cost / token DoS and runaway retry loops.  
- Supply-chain and poisoned dependencies in runners.  
- Over-trusted model output driving state transitions.  
- Policy bypass via layered prompts (host + repo + tool).

### 1.2 Required controls (MVP)

| ID | Requirement |
|----|-------------|
| SEC-01 | Instruction **discovery** and **CONFLICT_MAP** before execution packet issuance. |
| SEC-02 | Tool **allowlist** / denylist per `AgentProfile` / workspace policy. |
| SEC-03 | Filesystem access **path-scoped** to declared workspace roots. |
| SEC-04 | Git operations **branch-scoped** and explicit (no implicit force-push to default). |
| SEC-05 | Destructive operations require **human approval** artifact in L4. |
| SEC-06 | **Per-project** isolation for memory and retrieval indices. |
| SEC-07 | Secret scanning on committed artifacts; **redaction** in logs and traces. |
| SEC-08 | Structured outputs for state transitions; reject malformed payloads. |
| SEC-09 | Budget and **retry ceilings**; circuit breaker on repeated tool failures. |
| SEC-10 | **Kill-switch** stops new runs; documented in `RUNBOOK.md` and escalation policy. |
| SEC-11 | HTTP control plane: if `FC_API_TOKEN` is set, all `/v1/*` routes require `Authorization: Bearer <token>`; `/health` stays unauthenticated for probes. |

### 1.3 Posture

**Secure-by-default, autonomy-by-permission.** Not a fully autonomous unsupervised coder in MVP.

## 2. Reliability and resumability

- NFR-R01: Cold start must rehydrate from **RESUME_PACKET** + L2 pins + L1 snapshot without requiring chat history.  
- NFR-R02: Runs are **idempotent** where possible; explicit retry policy with caps.  
- NFR-R03: Artifact storage uses **checksums**; verifier on download.

## 3. Observability

- NFR-O01: **OpenTelemetry** traces for run and subagent spans; baggage includes `project_id`, `run_id` where safe.  
- NFR-O02: Metrics: latency, gate pass/fail, token estimates, cost aggregates, queue depth.  
- NFR-O03: Logs must not contain secrets or raw credentials; PII minimized.

## 4. Performance (control plane)

- NFR-P01: Desktop UI remains responsive; long work runs on runners/async jobs.  
- NFR-P02: Ingestion of medium repos (&lt;100k files) completes within practical interactive time using incremental indexing (future).

## 5. Portability

- NFR-V01: Control plane runs on **Linux** first; macOS/Windows dev supported.  
- NFR-V02: Packaged install paths align with `ops/install/` and `packaging/` stubs.

## 6. Accessibility and UX

- NFR-A01: Web companion targets WCAG-oriented patterns (full audit post-MVP UI).  
- NFR-A02: Keyboard-navigable critical flows on desktop (target).

## 7. Determinism and exports

- NFR-D01: Prompt pack exports are **deterministic** given same packet version and template set (byte-stable optional; logical stable required).  
- NFR-D02: Schema versions pinned in exports (`schema_version` field).

## 8. Compliance and audit

- NFR-C01: Append-only governance events retained per retention policy (configurable).  
- NFR-C02: Artifact **provenance** JSON on promoted canonical docs.

## 9. Dependencies

- Third-party model APIs: operator-supplied keys; never committed.  
- MCP servers: declared in workspace manifest; disabled by default until approved.
