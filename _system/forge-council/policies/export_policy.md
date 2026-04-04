# Policy: Prompt and bundle export

**Related:** `_system/PROMPT_EMISSION_CONTRACT.md`, `_system/HOST_BUNDLE_CONTRACT.md`

## Rules

- Exports **reference** repo paths; avoid embedding full `AGENTS.md` unless target requires minimal excerpt.  
- Include startup preamble per prompt emission contract.  
- Label host-only instructions clearly when bundling.

## Versioning

- Exported packs include `schema_version` / pack version for reproducibility (`NFR-D02`).
