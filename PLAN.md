# Plan — Active execution slice

## Objective

- **Current target outcome:** Land the **Master Architecture and Planning Pack** in-repo: canonical docs, Forge Council OS tree, Cursor rules, Codex prompt packs, ingestion automation, JSON schemas + Python mirror, bootstrap stubs for execution/gates/resume, and extension roadmap documentation.  
- **Why it matters now:** Establishes SSoT and automation before control-plane service implementation.  
- **Forcing function:** Single cohesive baseline for all subsequent milestones.

## Success criteria

- **Operator outcome:** A new contributor can read `PRD.md` / `RUNBOOK.md` and run ingestion + validation without guesswork.  
- **Technical outcome:** Schemas validate; scripts are executable; no runtime imports from `_system/`.  
- **Quality outcome:** AGENTS.md and precedence contract honored; conflicts surfaced in `CONFLICT_MAP.md`.

## Scope lock

- **In scope:** Documentation, `_system/forge-council/`, `.cursor/rules/fc-*.mdc`, `schemas/`, `src/forge_council/`, `bootstrap/fc-*.sh`, `EXTENSION_ROADMAP.md`, stub operational files.  
- **Out of scope:** Full desktop UI, production DB deployment, live multi-runner cluster.  
- **Dependencies:** Python 3.12+, shell, git.  
- **Known unknowns:** Exact FastAPI vs alternative for first API; desktop framework TBD.

## Assumptions

- AIAST upgrade path preserved by namespacing Forge files under `_system/forge-council/` and `fc-` Cursor rules.

## Execution slices

1. ~~Canonical docs + PRODUCT_BRIEF / PLAN / ROADMAP alignment~~  
2. ~~Forge Council OS tree (roles, policies, skills, context, templates)~~  
3. ~~fc Cursor rules + GPT54 + prompt packs~~  
4. ~~Ingestion script + profile/conflict refresh~~  
5. ~~Schemas + `forge_council` package + OTel stub~~  
6. ~~fc bootstrap stubs (run, gate, resume)~~  
7. ~~Minimal FastAPI control plane + SQLite (`FC_STATE_DB`) + `PATCH /v1/runs` + optional Bearer auth + dispatch stub (`POST /v1/runs/{id}/dispatch`)~~ — OAuth, real runner process, OpenAPI security text polish

## Validation plan

- `bootstrap/validate-system.sh .`  
- `bootstrap/fc-repo-ingestion.sh .`  
- `pip install -e ".[dev]" && pytest` and `python -m forge_council.schema_check`  
- `shellcheck bootstrap/fc-*.sh` (if available)

## Risks

- Cursor rule count may slow IDE; mitigated by focused `fc-*.mdc` files.  
- Schema drift vs Python models — mitigated by `schema_check` loading JSON Schema.

## Done definition

- All master-plan to-dos completed; handoff updated in `RESUME_PACKET.md` and `WHERE_LEFT_OFF.md`.

## Notes

- Long-term sequencing: `ROADMAP.md`, `EXTENSION_ROADMAP.md`.
