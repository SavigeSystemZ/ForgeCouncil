# System Awareness Protocol

The operating system must know which files it owns, which docs point to which surfaces, and whether its own structure is still truthful.

## Sources of truth

- `_system/SYSTEM_REGISTRY.json` — machine-readable list of AIAST-managed files
- `_system/CONTEXT_INDEX.md` — human-readable map of major surfaces
- `_system/LOAD_ORDER.md` — what to load first
- `_system/golden-examples/golden-example-manifest.json` — machine-readable map of the neutral example pack
- `bootstrap/check-system-awareness.sh` — structural awareness verification

## Rules

- Regenerate the registry whenever AIAST-managed files are added, removed, or renamed.
- Core docs must not reference paths that do not exist locally.
- Core docs must mention critical self-awareness and recovery commands so agents can find them under pressure.
- Golden-example discovery docs must stay aligned with the actual installed example files.
- Registry drift is a system problem, not a cosmetic issue.

## Commands

- `bootstrap/generate-system-registry.sh <repo> --write`
- `bootstrap/check-system-awareness.sh <repo>`
- `bootstrap/system-doctor.sh <repo>`
