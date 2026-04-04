# Forge Council — Extension roadmap (M8–M12)

**Companion:** `ROADMAP.md` (horizons). This file expands **scale and ecosystem** milestones from the master plan.

## M8 — Multi-runner fabric

- Uniform job spec: image/command, env, mounts, resource limits, cancellation.  
- Adapters: local process, Docker/Podman, remote queue (e.g. Celery, K8s Job — TBD).  
- Artifact pull-back and log streaming contract.

## M9 — Comparative evaluation

- A/B harness for model mixes and agent lineups.  
- Dashboards: quality vs cost curves; statistical confidence bounds (lightweight).

## M10 — Release hardening

- Installers per `packaging/`; backup/restore for DB and artifact store.  
- Disaster recovery runbook section in `RUNBOOK.md`.  
- UX polish on desktop primary path.

## M11 — Governance and team mode

- Shared workspaces; role-based UI; approval inbox.  
- Richer audit dashboards; retention policies for L4.

## M12 — Extension ecosystem

- Plugin/workflow packs; domain templates (e.g. security review pack, API service pack).  
- Signed pack manifests; review gate before enablement.
