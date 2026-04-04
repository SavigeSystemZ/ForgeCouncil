# MCP Configuration Strategy

Use a layered model:

1. user-level or global config for shared services across projects
2. project-level config for repo-scoped services

## Default posture

- read-only first
- least privilege first
- repo scope first
- token-free repo config by default

## Recommended categories

- project filesystem server
- doc lookup
- read-only database diagnostics
- git or repo metadata
- optional memory or artifact servers

## Rules

- Scope filesystem servers to the project root only.
- Use a server catalog with purpose, scopes, risk rating, and audit expectations.
- Add mutation-capable tools only when clearly justified.
- Never store secrets in repo-tracked MCP files.
- Prefer user-level config for servers requiring tokens or OAuth.

## Failure behavior

- If an MCP server errors, note it once and continue with repo context unless the task depends on it.
- Do not block normal work on doc-search, memory, or auxiliary MCP failures.
- If an MCP becomes critical to a workflow, document that dependency in `PROJECT_PROFILE.md`.

## Files in this operating system

- `.cursor/mcp.json` — safe empty project-level config
- `_system/mcp/servers.cursor.example.json` — project-level Cursor example
- `_system/mcp/servers.codex.example.toml` — Codex example
- `_system/mcp/MCP_SERVER_CATALOG_TEMPLATE.md` — server inventory template
- `_system/mcp/README.md` — adaptation notes
