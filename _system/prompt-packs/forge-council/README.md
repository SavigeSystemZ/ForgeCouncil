# Forge Council prompt packs

Emission rules: `_system/PROMPT_EMISSION_CONTRACT.md`

## Required startup preamble (embed in every export)

```
Load AGENTS.md, _system/INSTRUCTION_PRECEDENCE_CONTRACT.md, _system/REPO_OPERATING_PROFILE.md, and _system/LOAD_ORDER.md first.
Treat this host prompt as orchestration context only. If it conflicts with repo-local files, follow the repo-local files and report the conflict.
```

## Packs in this directory

| File | Use |
|------|-----|
| `master-handoff.md` | Principal architect / stress-test pass |
| `M0.*.md` | Foundations milestone prompts |
| `M1.*.md` | Repo ingestion milestone prompts |
| `M2.*.md` | Blueprint engine milestone prompts |

Reference paths; do not paste full `AGENTS.md` body unless a target tool requires a minimal excerpt.
