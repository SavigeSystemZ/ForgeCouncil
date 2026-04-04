# M8–M12: Scale, evaluation, governance, extensions

See `EXTENSION_ROADMAP.md` for milestone themes. This note ties **implementation hooks** to repo layout.

## M8 — Multi-runner fabric

- **Interface:** job spec shared by local process, container, and remote queue workers.  
- **Code home (future):** `src/forge_council/runners/` — must not import `_system/`.

## M9 — Comparative evaluation

- **Inputs:** fixed milestone fixtures + `EvaluationReport` dimensions.  
- **Telemetry:** cost and latency from OTel + provider usage APIs.

## M10 — Release hardening

- **Surfaces:** `packaging/`, `ops/install/`, `RUNBOOK.md` DR section (expand when DB exists).

## M11 — Governance / team mode

- **L4 growth:** retention policies, approval inbox UI, shared workspace ACLs on `Workspace` entity.

## M12 — Extensions

- **Signed workflow packs** under vendor namespace; enablement requires `Reviewer/Security` + Boss approval artifact.
