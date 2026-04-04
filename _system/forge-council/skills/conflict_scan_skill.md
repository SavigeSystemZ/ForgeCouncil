# Skill: Instruction conflict scan

**Related:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`

## Steps

1. Collect overlapping topics: tool policy, test requirements, boundaries.  
2. Classify severity: low / medium / high.  
3. Propose resolution per row in `CONFLICT_MAP.md`.  
4. **Block** execution packets on unresolved **high**.

## Tools

- `bootstrap/detect-instruction-conflicts.sh`, `bootstrap/validate-instruction-layer.sh`
