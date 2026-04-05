# Project Profile

Fill this file in immediately after copying the operating system into a real repo. The stronger and more specific this file is, the better every agent will perform.

## After scaffold (customize for your app)

1. Replace every `- App name:` / `- Repo purpose:` style blank with **your** product truth.
2. Keep `_system/` as the agent operating layer; put runtime code outside it (see `AGENTS.md`).
3. If you use governed ports, follow `_system/ports/PORT_POLICY.md` and record bindings under `registry/`.
4. Re-run `bootstrap/validate-system.sh . --strict` after meaningful edits.
5. See `_system/INSTALLER_AND_UPGRADE_CONTRACT.md` for how installs and upgrades preserve app-owned state.

## Completion status

- [ ] Identity filled
- [ ] Runtime boundaries filled
- [ ] Stack filled
- [ ] Components filled
- [ ] Build, packaging, and install filled
- [ ] Mobile and AI filled
- [ ] Validation commands filled
- [ ] Operations and deployment filled
- [ ] Security and compliance filled
- [ ] Observability filled
- [ ] Constraints filled
- [ ] MCP plan filled
- [ ] Canonical docs filled
- [ ] Experience targets filled
- [ ] Release model filled

## Identity

- App name: Forge Council
- App id: io.aiaast.forge.council
- Desktop entry id: io.aiaast.forge.council
- Android application id: io.aiaast.forge.council
- Repo purpose:
- Product category:
- Primary users:
- Main workflows:
- Primary success criteria:
- Non-goals:

## Runtime boundaries

- Runtime code roots: src/
- Test roots: tests/
- Scripts / tooling roots: tools/
- Packaging / deploy roots: ops/, packaging/, mobile/, ai/
- Infrastructure roots:
- Agent-system root: `_system/`
- No-touch zones:

## Stack

- Primary languages: Python
- Primary frameworks: FastAPI
- Components: backend service
- Datastores:
- Package managers: pyproject-based Python packaging
- Build tools: Python project tooling
- Runtime environments: Python
- Supported environments: server
- Deployment targets: Linux host

## Build and packaging

- Packaging targets: wheel, sdist
- Native package targets: .deb, .rpm
- Universal package targets:
- Packaging manifest paths: packaging/appimage.yml, packaging/flatpak-manifest.json, packaging/snapcraft.yaml
- Installer commands: ops/install/install.sh, ops/install/repair.sh, ops/install/uninstall.sh, ops/install/purge.sh
- Signing identity: Release owner placeholder; replace before shipping signed artifacts
- Minimum runtime versions: Python 3.10+
- System dependencies:
- Build entrypoints: python3 -m compileall src
- Release artifacts: python distributions

## Validation commands

- Format: `.venv/bin/ruff format src tests`
- Lint: `.venv/bin/ruff check src tests`
- Typecheck: mypy src/
- Unit tests: `.venv/bin/pytest`
- Integration tests:
- End-to-end or smoke:
- Build: python3 -m compileall src
- Install / launch verification: uvicorn app.main:app --host ${APP_BIND_ADDRESS:-127.0.0.1} --port ${APP_PORT:-8000}
- Packaging verification: python -m build
- Visual regression or design smoke:
- Security or policy checks: bootstrap/scan-security.sh /home/whyte/.MyAppZ/ForgeCouncil

## Mobile and AI

- Mobile targets:
- Android module path: mobile/flutter/
- Mobile release artifacts:
- Mobile build flavors:
- LLM config path: ai/llm_config.yaml
- Default LLM provider:
- Chatbot surfaces: CLI REPL, REST endpoint, GUI side panel when a UI exists
- Command bus or action registry:
- Local documentation sources:

## Operations and deployment

- Default ports: 8000
- Default port range:
- Bind model: bind to 127.0.0.1 by default
- Required background services:
- Service model: HTTP service
- Migration model:
- Database mode:
- Container runtime preference:
- Service account model:
- Required env vars:
- Optional providers:
- Known degraded modes:
- Backup location:
- Filesystem layout:
- Environment files:
- Reverse proxy or ingress:

## Security and compliance

- Safety / compliance:
- Security:
- Secret handling:
- Data classification:
- Audit or retention requirements:
- Threat model doc:

## Observability

- Structured logging surface:
- Metrics surface:
- Health or readiness surface:
- Tracing or profiling surface:
- Alerting or dashboards:

## Constraints

- Performance:
- UI / design:
- Accessibility expectations:
- Data integrity:
- Release / packaging:
- Repo workflow:
- Compatibility requirements:

## MCP plan

- Project-scoped servers:
- User-level shared servers:
- Read-only defaults:
- Elevation rules:
- Servers to avoid:

## Canonical docs

- Product spec:
- Architecture:
- Data model:
- Runbook:
- Standards:
- Threat model:
- Additional design docs:

## Experience targets

- Visual quality bar:
- Interaction quality bar:
- Performance quality bar:
- Accessibility expectations:
- Device targets:
- Brand or tone constraints:

## Release model

- Environments:
- Branch strategy: main for runtime code, system for copied AIAST updates, optional short-lived feature branches
- Rollout method:
- Backout method:
- Release signoff:
- Post-release verification:

## High-value conventions

- Naming conventions:
- Module boundary rules:
- Logging rules:
- Testing rules:
- Handoff expectations:
- Documentation update expectations:
