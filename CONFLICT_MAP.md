# Forge Council — Instruction Conflict Map

**Generated/refreshed by:** `bootstrap/fc-repo-ingestion.sh`
**Precedence contract:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`
**Last scan (UTC):** 2026-04-04T19:32:30Z

## Resolution order (summary)

1. Repo-local runtime and product facts
2. AIAST core (`AGENTS.md`, `_system/` core docs)
3. Forge Council extension (`_system/forge-council/`)
4. Tool overlays (`CODEX.md`, `.cursorrules`, …)
5. Prompt packs (`_system/prompt-packs/`)
6. Host orchestration context

## Detected conflicts (automation)

| Topic | Source | Severity | Resolution |
|-------|--------|----------|------------|
| (none) | `detect-instruction-conflicts.sh` | — | No heuristic findings |

## Raw scan output (reference)

```text
Instruction Conflict Report
===========================

Scanned surfaces: 77
Strict mode: off

No likely instruction conflicts detected.
```

## Manual review notes

- Add rows for subtle semantic conflicts not caught by heuristics.

