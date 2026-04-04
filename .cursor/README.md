# Cursor Overlays

This directory contains repo-local Cursor overlays for commands, rules, skills,
agents, and MCP configuration.

Use these files as a thin IDE host layer only. The authoritative operating
contract still lives in `AGENTS.md`, `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`,
and `_system/REPO_OPERATING_PROFILE.md`.

If the repo is used from multiple IDE hosts or orchestrators, also read
`_system/CURSOR_AND_MULTI_HOST.md` before changing Cursor-specific behavior.

For **Composer** multi-file work, use `rules/60-composer-orchestration.mdc`,
`commands/composer-session.md`, and `agents/composer-lead.md` as overlays.

Do not put product truth, secrets, or app runtime logic in this directory.
