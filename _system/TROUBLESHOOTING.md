# Troubleshooting

Common issues and their solutions, organized by symptom.

## Agent ignores project rules

**Symptom**: Agent acts as if `_system/PROJECT_RULES.md` does not exist.

**Diagnosis**: The agent may not have loaded the startup sequence, or host-level instructions are overriding repo-local rules.

**Fix**:
1. Verify the agent loaded `AGENTS.md` first.
2. Check `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md` — repo-local truth wins.
3. Run `bootstrap/validate-instruction-layer.sh .` to check for adapter conflicts.
4. If using a host orchestrator, ensure it defers to repo-local files.

## Validation fails after upgrade

**Symptom**: `bootstrap/validate-system.sh . --strict` fails after updating AIAST.

**Fix**:
1. Run `bootstrap/install-missing-files.sh .` to add any new required files.
2. Run `bootstrap/system-doctor.sh . --heal` to auto-repair.
3. Run `bootstrap/detect-drift.sh . --source <template>` to see what drifted.
4. If version mismatch: check `AIAST_VERSION.md` matches `_system/.template-version`.

## Missing files after install

**Symptom**: `validate-system.sh` reports missing required files.

**Fix**:
1. Run `bootstrap/install-missing-files.sh . --source <template-root>`.
2. Run `bootstrap/repair-system.sh .` for safe file restoration.
3. Check that the source template is at the expected version.

## Agent hallucinates about features

**Symptom**: Agent claims something was tested/built/deployed when it was not.

**Fix**:
1. Run `bootstrap/check-hallucination.sh .` to detect claim-evidence mismatches.
2. Check `_system/HALLUCINATION_DEFENSE_PROTOCOL.md` for verification rules.
3. Verify `WHERE_LEFT_OFF.md` matches actual repo state.

## Adapter files are stale

**Symptom**: `check-host-adapter-alignment.sh` reports stale adapters.

**Fix**:
1. Run `bootstrap/generate-host-adapters.sh . --write` to regenerate from manifest.
2. Run `bootstrap/check-host-adapter-alignment.sh .` to verify.
3. Do not hand-edit adapter files — update the manifest instead.

## Plugin fails

**Symptom**: A plugin produces errors during system-doctor runs.

**Fix**:
1. Run `bootstrap/validate-plugin.sh _system/plugins/<name>` to check manifest.
2. Plugin failures are warnings, not fatal errors.
3. Set `"enabled": false` in `plugin.json` to disable a broken plugin.

## Environment check warns about missing tools

**Symptom**: `check-environment.sh` warns about tools referenced in profile.

**Fix**:
1. Install the missing tools, or
2. Remove the tool references from `_system/PROJECT_PROFILE.md` if not needed.
3. Stack-specific tools are warnings, not failures.

## Context too large for my model

**Symptom**: Small-context model cannot load the full startup sequence.

**Fix**:
1. Use `bootstrap/emit-tiered-context.sh . --model <model-name>` for appropriate tier.
2. See `_system/CONTEXT_BUDGET_STRATEGY.md` for tier definitions.
3. Adapters for local models (`LOCAL_MODELS.md`) reference the fast-path automatically.

## Multi-agent conflicts

**Symptom**: Two agents edit the same files, causing conflicts.

**Fix**:
1. Check `_system/MULTI_AGENT_COORDINATION.md` — single active writer model.
2. Read `WHERE_LEFT_OFF.md` to see if another agent left unfinished work.
3. Follow the takeover protocol: verify state before building on it.

## Integrity manifest mismatch

**Symptom**: `verify-integrity.sh --check` reports hash mismatches.

**Fix**:
1. If you intentionally modified system files, regenerate: `bootstrap/verify-integrity.sh --generate --target .`
2. If unexpected: run `bootstrap/detect-drift.sh .` to understand what changed.
3. Use `bootstrap/system-doctor.sh . --heal` for safe recovery.

## System-doctor reports drift

**Symptom**: `detect-drift.sh` reports version or structural drift.

**Fix**:
1. Compare installed version with source template version.
2. Run `bootstrap/update-template.sh . --source <template> --dry-run` to preview changes.
3. Apply with `bootstrap/update-template.sh . --source <template> --strict`.

## Bootstrap script not found or not executable

**Symptom**: `bash: bootstrap/validate-system.sh: No such file or directory`

**Fix**:
1. Check you are running from the repo root.
2. Run `chmod +x bootstrap/*.sh` to fix permissions.
3. If files are missing, run `bootstrap/install-missing-files.sh .`.

## How to get more help

1. Run `bootstrap/system-doctor.sh . --report` for a full diagnostic.
2. Check `_system/DEBUG_REPAIR_PLAYBOOK.md` for structured debugging.
3. Check `_system/FAILURE_MODES_AND_RECOVERY.md` for recovery paths.
