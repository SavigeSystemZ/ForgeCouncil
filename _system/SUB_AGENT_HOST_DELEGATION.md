# Sub-Agent And Host CLI Delegation

This contract explains how a **primary** agent (any supported IDE or CLI host: Cursor, Windsurf,
Claude Code, Gemini CLI, Codex CLI, etc.) may use **auxiliary** agents—and when it must **not**
rely on them.

## What is not automated here

AIAST does **not** ship a built-in MCP server or daemon that spawns Gemini, Claude, or Codex in
the background. Parallel “sub-agents” depend on **your host environment**: installed CLIs,
logged-in sessions, API keys, and **your** approval to run additional processes. Treat any
pattern below as **optional** orchestration guidance, not a guaranteed platform feature.

## Goals

- Allow up to **two** auxiliary workers **in parallel** when the host supports it **and** write
  scopes stay disjoint.
- Keep **one primary** accountable for integration, handoff quality, and final validation.
- Ensure the primary can **continue alone** if sub-agents fail, hang, refuse, or produce
  incompatible output.

## Roles

- **Primary** — The active session you are in (e.g. Cursor Composer, Windsurf agent, or a single
  CLI chat). Owns coherence, merge conflicts, and `WHERE_LEFT_OFF.md`.
- **Auxiliary (sub-agent)** — A **separate** process: another terminal tab running `claude`,
  `gemini`, `codex`, or another tool, **or** a second IDE window. Must have an explicit,
  non-overlapping write scope unless read-only.

Any combination is allowed **in principle** (e.g. primary Cursor + aux Codex + aux Gemini), as
long as the **single-writer rule** in `MULTI_AGENT_COORDINATION.md` is respected per file.

## Preconditions before involving auxiliaries

1. **User consent** — The operator must agree to extra terminals, API usage, and cost.
2. **Explicit brief** — Each auxiliary gets a frozen prompt: inputs, outputs, files allowed,
   forbidden paths, and success criteria.
3. **Disjoint scopes** — Example: auxiliary A edits `src/api/`, auxiliary B edits `tests/` only;
   primary owns `PLAN.md` and integration.
4. **Secrets** — Never paste credentials into shared logs; use env vars and host keychains.

## Parallelism limit

- Prefer **at most two** concurrent auxiliaries to limit merge pain and context drift.
- If more capacity is needed, serialize or split by milestone.

## Failure and takeover

If an auxiliary fails or diverges:

1. Primary **stops** waiting, records the failure in `WHERE_LEFT_OFF.md` (command, symptom).
2. Primary either **repairs** the auxiliary’s branch of work or **reverts** those edits and
   completes the task alone.
3. Do not claim auxiliary output was merged without review.

## Relation to MCP

MCP servers are **optional accelerators**. A custom MCP that runs shell commands could invoke CLIs,
but that is **high risk** (injection, policy, sandboxing). Default AIAST guidance: prefer **manual**
or **explicitly approved** terminal sessions over opaque MCP shell bridges unless the repo adds
its own hardened MCP with a documented threat model.

## Auxiliary brief template (copy-paste)

Give each auxiliary a **frozen** message before it starts writing. Primary keeps the canonical
plan in `PLAN.md` / `WHERE_LEFT_OFF.md`; auxiliaries execute only their slice.

```markdown
## Role
You are an auxiliary worker. Primary session: <tool name>. Read-only unless stated.

## Allowed writes
- Paths: <e.g. `src/api/` only> OR read-only review.

## Forbidden
- Do not edit: <e.g. `PLAN.md`, `WHERE_LEFT_OFF.md`, `package-lock.json`>
- Do not run: <e.g. `rm -rf`, production deploys, secret-exporting commands>

## Inputs
- Branch / commit: <sha or branch>
- Spec / ticket: <link or paragraph>

## Deliverables
- <e.g. patch + short summary of files touched>
- Stop when: <acceptance criteria>

## Hand back
- Post summary to primary; primary merges and validates.
```

## Canonical cross-references

- `MULTI_AGENT_COORDINATION.md` — single writer, checkpoints, handoffs.
- `AGENT_ROLE_CATALOG.md` — named roles and write scopes.
- `HOST_ADAPTER_POLICY.md` — tool entrypoints; do not confuse adapters with live sub-processes.
- `.cursor/agents/` — optional role overlays for Cursor-like hosts; not a substitute for host CLI
  processes.
