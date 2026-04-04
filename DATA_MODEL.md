# Forge Council — Data Model

**SSoT:** Entity definitions, relationships, and memory tiers. JSON Schemas live in `schemas/forge_council/v1/`.

---

## 1. Design principle

The system is **workflow-state-shaped**, not **message-shaped**. Authoritative records: milestones, task packets, decisions, approvals, artifacts, evaluations, resume packets.

## 2. Core entities (relational)

| Entity | Description |
|--------|-------------|
| **Workspace** | Top-level tenant boundary; owns policies and agent profiles. |
| **Project** | Product effort within a workspace; links repos, docs, runs. |
| **Repository** | Path or URL, branch, detected stack, validation command hints. |
| **CanonicalDocument** | Typed doc (`prd`, `architecture`, `data_model`, `nfr`, `runbook`, …) with version, checksum, status, supersedes_id. |
| **Milestone** | Sequenced objective with acceptance criteria JSON, rollback notes, priority, status. |
| **TaskPacket** | Role-scoped work unit: inputs, constraints, deliverables, validation hooks, handoff template ref. |
| **AgentProfile** | Role name, model target, reasoning level, tool_policy_id, autonomy level. |
| **Run** | Single execution attempt for a milestone (or sub-run); cost summary, status, trace_id. |
| **RunStep** | Ordered step within a run: agent_role, action_type, input_ref, output_ref, status, timestamps. |
| **Artifact** | Blob or file reference with type, title, storage_uri, checksum, metadata, provenance. |
| **DecisionRecord** | Category, text, rationale, approver, timestamps, superseded_by. |
| **MemoryItem** | Tier, content_ref, embedding_ref, status, confidence, last_used_at. |
| **Policy** | Named rules JSON, approval requirements JSON, scope. |
| **EvaluationReport** | Quality score, security findings JSON, defects JSON, recommendation, linked run_id. |

## 3. Key relationships

- Workspace **1—*** Project  
- Project **1—*** Repository, CanonicalDocument, Milestone, Run, DecisionRecord, MemoryItem  
- Milestone **1—*** TaskPacket  
- Run **1—*** RunStep, Artifact (many)  
- CanonicalDocument: optional **supersedes** chain for versioning  

## 4. Event ledger

**Append-only** events for: state transitions, policy decisions, approvals, overrides, tool invocations (metadata only), gate outcomes. Each event stores:

- `event_id`, `timestamp`, `workspace_id`, `project_id`, `run_id?`, `trace_id?`, `event_type`, `payload_json` (schema-validated subset), `actor` (human | agent | system).

Correlate with **OpenTelemetry** `trace_id` / `span_id` for replay and debugging.

## 5. Memory tiers (L0–L4)

| Tier | Name | Content | Durability |
|------|------|---------|------------|
| L0 | Session | UI/thread scratch | Ephemeral |
| L1 | Working set | Active milestone, hot artifacts, open questions | Checkpointed per run |
| L2 | Durable project | Accepted decisions, conventions, validated commands | Long-lived; mirrored in `DECISIONS.md` where human-edited |
| L3 | Retrieval | Embeddings, chunk refs, prior runs, external packs | Long-lived |
| L4 | Governance | Approvals, exceptions, audit annotations | Append-mostly; immutable policy events |

## 6. Memory operations

- **capture** — Write to appropriate tier with provenance.  
- **summarize** — Produce compact narrative + structured pins.  
- **compact** — Merge/prune L1/L3 per policy thresholds.  
- **pin** — Promote to L2 or sticky L1.  
- **supersede** — Link new record to old (`superseded_by`).  
- **invalidate** — Mark stale; block use in new packets until refreshed.  
- **retrieve** — Query L3/L2 with project isolation **mandatory**.  
- **export_resume_packet** — Generate `RESUME_PACKET.md` + machine JSON sidecar (future: `artifacts/resume/*.json`).

## 7. Structured payloads

The following **must** validate against JSON Schema when exchanged between orchestrator and runners/UI:

- `milestone.json`, `task_packet.json`, `approval_request.json`, `run_summary.json`, `evaluation_report.json`, `gate_result.json` — see `schemas/forge_council/v1/`.

## 8. Canonical document lifecycle

Statuses: `draft` | `in_review` | `canonical` | `deprecated`.  
Transitions require gate metadata (who reviewed, run_id optional). Checksum (SHA-256) stored on promotion to `canonical`.

## 9. Cross-project isolation

All MemoryItem, Run, Artifact, and ledger events **must** include `workspace_id` and `project_id`. Queries default-filter on both.

---

## Document references

- Runtime types: `src/forge_council/models.py` (mirrors schema intent; schemas remain normative for interchange).
