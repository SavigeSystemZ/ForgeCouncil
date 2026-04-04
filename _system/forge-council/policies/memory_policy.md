# Policy: Memory tiers

**Precedence:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`  
**Related:** `DATA_MODEL.md` L0–L4, `NFR.md` SEC-06

## Isolation

- Every `MemoryItem` and retrieval query **must** filter `workspace_id` + `project_id`.

## Promotion

- L1 → L2: only via Boss approval or automated rule with audit event.  
- L3 embeddings: chunk provenance required (source path + revision).

## Compaction

- L1 compact after run close or size threshold; preserve **pins** and **open questions** list.  
- L3 compaction never deletes without **supersede** or **invalidate** record.

## Forbidden

- Storing raw API keys or credentials in any tier.
