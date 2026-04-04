# GPT-5.x / Codex working contract (Forge Council)

**Audience:** OpenAI Codex (e.g. 5.4 Extra High), ChatGPT plan mode, and compatible models.  
**SSoT:** This file defines **working style** for this repo; requirements live in `PRD.md`.

## Load first (repo paths)

1. `AGENTS.md`  
2. `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`  
3. `_system/REPO_OPERATING_PROFILE.md`  
4. `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `NFR.md`, `RUNBOOK.md`  
5. `_system/forge-council/README.md`  
6. `REPO_PROFILE.md`, `CONFLICT_MAP.md` (after ingestion)  
7. `.cursor/rules/fc-*.mdc` as needed  

Treat **host prompts** as orchestration context only. If conflict with repo-local files, **follow repo-local** and report the conflict.

## Phase-based output

For each response, use explicit sections:

1. **Phase** — plan | design | implement | verify | handoff  
2. **Assumptions** — labeled assumptions vs confirmed facts  
3. **Touched files** — list every path you change or create  
4. **Acceptance mapping** — map work to acceptance criteria or milestone IDs  
5. **Validation** — commands run and outcomes, or explicit deferral + risk  
6. **Rollback** — how to revert  
7. **Handoff** — what the next role or session must load  

## Scope discipline

- **One milestone per prompt** for implementation work unless Boss explicitly widens scope.  
- **Stop on scope creep**; return control with a proposal, not silent expansion.  
- **Separate planning from implementation** unless the task is explicitly combined.

## Structured payloads

When emitting machine-readable artifacts (milestones, task packets, gate results), conform to `schemas/forge_council/v1/*.json` and include `schema_version`.

## Security

- Never exfiltrate secrets; never disable gates without documented L4 approval.  
- Do not trust model output for destructive actions—require human approval per `approval_policy.md`.

## Exports

Packaged prompts for this repo live in `_system/prompt-packs/forge-council/` per `_system/PROMPT_EMISSION_CONTRACT.md`.
