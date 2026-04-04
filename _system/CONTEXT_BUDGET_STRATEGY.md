# Context Budget Strategy

Different AI models have different context windows. This strategy defines tiered loading so agents with smaller contexts can still operate effectively.

## Tiers

### Tier S: Infinite (1M+ tokens)
- Models: Gemini Pro 1.5, Gemini Flash 1.5, Gemini 2.0+
- Load: all files in `LOAD_ORDER.md` Tiers 0-3, plus broad repository source context.
- Use when: whole-repo analysis, cross-cutting architectural refactors, deep codebase investigations, finding scattered hallucinated dependencies.

### Tier A: Full (200K+ tokens)
- Models: Claude Opus, Claude Sonnet, GPT-4 Turbo, Gemini Pro 1.5
- Load: all files in `LOAD_ORDER.md` Tiers 0-3
- Use when: deep architecture work, system evolution, multi-file refactors

### Tier B: Standard (32K-128K tokens)
- Models: DeepSeek Coder, Codex, GPT-4o, Gemini Flash
- Load: Tier 0 (operating contract) + Tier 1 (working state) + targeted Tier 2 files for the task domain
- Use when: feature implementation, debugging, review

### Tier C: Compact (8K-32K tokens)
- Models: smaller cloud models, medium local models (13B-34B)
- Load: fast-path only (AGENTS.md, PROJECT_PROFILE.md, WHERE_LEFT_OFF.md, TODO.md, FIXME.md, PLAN.md, PRODUCT_BRIEF.md)
- Use when: focused single-file edits, quick fixes, inline completion

### Tier D: Minimal (4K-8K tokens)
- Models: small local models (7B and below)
- Load: AGENTS.md + PROJECT_PROFILE.md + WHERE_LEFT_OFF.md only
- Use when: simple edits with minimal context needed

## Usage

### Automatic detection
Adapter files in `_system/host-adapter-manifest.json` can declare a `context_tier` field. The `emit-tiered-context.sh` script reads this to produce the appropriate load sequence.

### Manual override
```bash
bootstrap/emit-tiered-context.sh . --tier B
bootstrap/emit-tiered-context.sh . --model deepseek-coder
```

### In adapters
Adapters for context-limited models should reference this document and the fast-path in `_system/LOAD_ORDER.md`.

## File classification by tier

Files in `_system/LOAD_ORDER.md` are tagged with their minimum tier:

| File | Min Tier | Purpose |
|------|----------|---------|
| AGENTS.md | D | Core contract |
| _system/PROJECT_PROFILE.md | D | Repo identity |
| WHERE_LEFT_OFF.md | D | Resume point |
| _system/INSTRUCTION_PRECEDENCE_CONTRACT.md | C | Conflict resolution |
| _system/MASTER_SYSTEM_PROMPT.md | C | Operating mission |
| _system/PROJECT_RULES.md | C | Behavioral rules |
| TODO.md, FIXME.md, PLAN.md, PRODUCT_BRIEF.md | C | Working state |
| _system/LOAD_ORDER.md, CONTEXT_INDEX.md | B | Navigation |
| _system/EXECUTION_PROTOCOL.md | B | Work protocol |
| _system/MULTI_AGENT_COORDINATION.md | B | Multi-agent rules |
| _system/VALIDATION_GATES.md | B | Quality gates |
| All Tier 2/3 files | A | Deep reference |

## Rules

- Never truncate or summarize governance files to fit a smaller tier. Load fewer files instead.
- Tier D agents should still respect the core contract in AGENTS.md.
- Tier C and D agents should note in WHERE_LEFT_OFF.md that they operated with limited context.
- Full-tier agents (A) should verify work done by limited-tier agents when taking over.
