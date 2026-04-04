# Skill: Milestone and task packetization

## Steps

1. Define milestone with acceptance JSON matching `schemas/forge_council/v1/milestone.json`.  
2. Emit role packets using `templates/task_packet.template.md`.  
3. Map each acceptance criterion to validation command or review step.  
4. Attach rollback notes and stale-artifact list.

## Gate

- Boss approval on `ApprovalGate` before execution dispatch.
