# Product Brief — Forge Council

## Product frame

- **Product name:** Forge Council  
- **Product category:** AI-orchestrated software-factory control plane (artifact-first, policy-governed)  
- **One-line summary:** A desktop-first hybrid control plane that turns ideas and repos into canonical docs, gated milestones, task packets, and resumable agent execution—not a chat shell.  
- **Why it should exist:** Solo operators and small teams need **work organization** (memory, handoffs, verification, governance) more than raw model throughput; current tools optimize chat, not factory discipline.  
- **Primary users:** Solo builders, security-conscious engineers, architects, maintainers, small team leads, AI-augmented consultants.  
- **Primary workflows:** New project from idea; repo ingestion; canonical doc generation; milestone approval; packet export; controlled execution; resume; strategy comparison (later).  
- **Success indicators:** Time to safe task packet after ingestion; milestone acceptance rate; resume success without chat history; operator-rated export quality.  
- **Non-goals (MVP):** Autonomous prod deploys, custom training, full IDE replacement, unbounded swarms, marketplace/billing complexity.

## Experience bar

- **Visual direction:** Professional control-plane UX (dense information, clear state—not playful chat UI).  
- **Interaction bar:** Explicit states matching orchestration state machine; low-friction approvals.  
- **Performance bar:** Responsive shell; heavy work isolated to runners.  
- **Reliability bar:** Degraded modes when models/tools unavailable; honest capability claims.  
- **Trust and safety bar:** Policy-gated tools, repo precedence, audit trail, no secret logging.

## Build shape (selected)

- **Recommended starter blueprint:** Hybrid Build Fabric — **selected** for this repo.  
- **Recommendation confidence:** high (locked in master plan).  
- **Rationale:** Pure SaaS weak for local repos/secrets; pure local weak for dashboards and remote runners. Hybrid preserves local-first execution and optional hosted orchestration.  
- **Selected starter blueprint:** Hybrid Build Fabric (desktop primary, optional web companion, multi-runner).  
- **Why this blueprint fits:** Matches control-plane + isolated runners architecture and NFR posture.  
- **Planned repo shape:** Monorepo — docs + `_system/forge-council/` + `schemas/` + `src/forge_council/` + `bootstrap/fc-*.sh`.  
- **First milestone:** M0/M1 complete — canonical docs, extension tree, ingestion automation, schemas, prompt packs (current phase).  
- **Initial validation focus:** `bootstrap/validate-system.sh`, `fc-repo-ingestion.sh`, schema check module.  
- **Next decision gates:** Control-plane HTTP framework; desktop shell technology; DB for multi-user.

## Usage rules

- Keep aligned with `PRD.md`, `ARCHITECTURE.md`, `PLAN.md`, `ROADMAP.md`, `_system/PROJECT_PROFILE.md`.  
- **SSoT split:** `PRODUCT_BRIEF.md` = intent and build shape; `PRD.md` = requirements; `PLAN.md` = active execution slice.
