# Local development ports (Docker Compose)

This repository assigns a **unique default host port** for the app service in
`ops/compose/compose.yml` so multiple stacks from `~/.MyAppZ/` can run on one
machine without binding the same port.

| Setting | Default | Override |
|--------|---------|----------|
| `APP_PORT` | **38208** | Set in `ops/env/.env` |

PostgreSQL/Redis host ports (when published) use their own variables in the
same compose file; this document only tracks the **HTTP** default.

**Recorded:** 2026-04-06 — workspace-wide unique defaults (SavigeSystemZ MyAppZ).
