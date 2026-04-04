# Forge Council — Product Requirements Document

**SSoT:** This file is durable product truth for what Forge Council *is* and *must do*. For the active execution slice, use `PLAN.md`. For narrative intent and build-shape choices, use `PRODUCT_BRIEF.md`.

**Version:** 0.1 (MVP definition)  
**Product id:** `io.aiaast.forge.council`

---

## 1. Vision

Forge Council is a **hybrid software-factory control plane**: desktop-first, optional web companion, with **local / self-hosted / cloud runners** under one orchestration model. It is **not** a chat application. It is an **artifact-driven, policy-governed, memory-backed** system that turns briefs and repositories into **canonical documents**, **risk-ranked milestones**, **role-scoped task packets**, **validation gates**, **resumable state**, and **exportable prompt packs** for external tools (Codex, Cursor, ChatGPT, Gemini, etc.).

## 2. Goals

| Goal | Description |
|------|-------------|
| G1 | Convert ambiguous product intent into **governed** plans and execution packets. |
| G2 | **Repo-safe** operation: discover instructions, map conflicts, honor repo-local precedence before execution. |
| G3 | **Durable memory** (L0–L4) that survives session breaks and model context limits. |
| G4 | **Policy-gated** tool use and autonomy; destructive actions require explicit approval artifacts. |
| G5 | **Inspectable** runs: ledger, traces, artifacts, evaluation reports. |
| G6 | **Provider-agnostic** model and tool layers; **MCP** as primary integration surface where applicable. |

## 3. Non-goals (MVP)

- Fully autonomous production deployment.
- Enterprise HR / org-wide identity products.
- Custom model training.
- Full IDE replacement.
- Unbounded background agent swarms.
- Marketplace, billing, or multi-tenant SaaS complexity in v1.

## 4. Personas

- Solo builder / founder.
- Security-conscious engineer.
- Product architect / planner.
- Repo maintainer and reviewer.
- Small team lead.
- AI-augmented consultant or agency operator.

## 5. Core user journeys

1. **New project from idea** — Intake → context capture → blueprint → milestones → approval → packets → optional controlled execution.
2. **Existing repo ingestion** — Attach repo → runtime/instruction discovery → `REPO_PROFILE.md` / `CONFLICT_MAP.md` → safe planning.
3. **Canonical doc maintenance** — Versioned PRD/architecture/data model/NFR/runbook with review and supersession.
4. **Milestone execution** — Dispatch to runner → capture artifacts → validation gate → review gate → accept / reject / split / retry.
5. **Resume** — Cold start from `RESUME_PACKET.md`, L1 snapshot, and pinned L2 decisions.
6. **Export** — Emit tool-specific prompt packs from task packets and canonical context.
7. **Compare strategies** — (post-MVP core) evaluate model mixes and agent lineups against quality and cost metrics.

## 6. Functional requirements (MVP)

### 6.1 Workspace and project

- FR-WP-1: Create and list **workspaces** and **projects** with metadata (name, owner, risk level, phase).
- FR-WP-2: Associate one or more **repositories** (path or URL) with a project.

### 6.2 Ingestion and safety

- FR-IN-1: Scan repo for instruction files (e.g. `AGENTS.md`, `.cursor/rules`, `_system/**`, tool adapters).
- FR-IN-2: Produce **`REPO_PROFILE.md`** (human) and align **`_system/REPO_OPERATING_PROFILE.md`** (machine-oriented summary) where applicable.
- FR-IN-3: Produce **`CONFLICT_MAP.md`** classifying instruction collisions and precedence per `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`.

### 6.3 Planning and artifacts

- FR-PL-1: Maintain versioned **canonical documents** (`PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`) with status and checksum semantics (see `DATA_MODEL.md`).
- FR-PL-2: Generate **milestones** with acceptance criteria, rollback notes, and dependencies.
- FR-PL-3: Generate **task packets** per role with inputs, constraints, deliverables, and validation hooks.

### 6.4 Execution and gates

- FR-EX-1: **Controlled execution**: single-milestone runs with captured **artifacts** and **run steps** (see schemas).
- FR-EX-2: **Validation gate**: tie to test/CI adapters; record pass/fail and logs as artifacts.
- FR-EX-3: **Review gate**: security/correctness checklist; record `EVAL_REPORT`-shaped output.

### 6.5 Memory and governance

- FR-MEM-1: Support memory tiers L0–L4 and operations: capture, summarize, compact, pin, supersede, invalidate, retrieve, export resume (see `DATA_MODEL.md`).
- FR-GOV-1: Record **approvals** and **policy decisions** in append-only governance trail (L4).

### 6.6 Observability

- FR-OBS-1: Correlate runs with **OpenTelemetry** trace IDs; emit metrics for cost, latency, gate outcomes (implementation phases M5+).

### 6.7 Exports

- FR-XP-1: Export **prompt packs** from `_system/prompt-packs/forge-council/` per `_system/PROMPT_EMISSION_CONTRACT.md`.

## 7. Success metrics

- Time from idea to **approved** milestone plan.
- Time from repo ingestion to **safe** task packet (conflict map present, no unresolved blocking collisions).
- Milestone acceptance rate; resume success rate; token/cost per accepted milestone.
- Operator-rated usefulness of exports.

## 8. Dependencies and assumptions

- Operators may use multiple LLM providers; **Responses API**-style interfaces are the reference for OpenAI-shaped backends (adapters abstract differences).
- Local execution requires explicit filesystem and git permissions; **path-scoped** tools are mandatory.
- **Assumption:** First implementation language for the control-plane service is **Python 3.12+** unless superseded by `ARCHITECTURE.md`.

## 9. Out of scope clarifications

- Forge Council **orchestrates** work; it does not replace human judgment for high-risk approvals.
- Chat transcripts are **not** authoritative; **artifacts and ledger events** are.

---

## Document division

| File | Role |
|------|------|
| `PRD.md` | Requirements and scope (this file) |
| `ARCHITECTURE.md` | Components, boundaries, deployment |
| `DATA_MODEL.md` | Entities, memory, events |
| `NFR.md` | Quality, security, performance attributes |
| `RUNBOOK.md` | Operator procedures and scripts |
| `PLAN.md` | Current milestone execution |
