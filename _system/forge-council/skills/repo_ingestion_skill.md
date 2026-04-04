# Skill: Repository ingestion

**Runs:** `bootstrap/fc-repo-ingestion.sh <repo>`  
**Outputs:** `REPO_PROFILE.md`, `CONFLICT_MAP.md`, hints for `_system/REPO_OPERATING_PROFILE.md`

## Steps

1. Enumerate instruction roots: `AGENTS.md`, `_system/**`, `.cursor/**`, `*.md` adapters.  
2. Detect stack signals: `pyproject.toml`, `package.json`, `go.mod`, etc.  
3. List validation commands from manifests or `REPO_PROFILE` template.  
4. Run `bootstrap/detect-instruction-conflicts.sh` if available.  
5. Refresh human + machine profiles.

## Done when

- `REPO_PROFILE.md` lists inventory and validation table.  
- `CONFLICT_MAP.md` has severity table (or explicit none).
