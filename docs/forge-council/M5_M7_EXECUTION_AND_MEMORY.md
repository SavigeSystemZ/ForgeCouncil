# M5–M7: Controlled execution, gates, memory, resume

## M5 — Controlled execution

- **Contract:** `bootstrap/fc-controlled-run.sh` (stub) documents dispatch steps.  
- **Implementation:** control-plane service opens OTel span (`src/forge_council/otel.py`), loads `TaskPacket`, verifies `CONFLICT_MAP.md` has no blocking rows, dispatches to runner adapter.  
- **Artifacts:** all outputs registered with `artifact.json` metadata; `run_step.json` per step.

## M6 — Validation and review gates

- **Validation:** `bootstrap/fc-gate-check.sh` — light mode by default; `--full-validate` runs `validate-system.sh`.  
- **Review:** `reviewer_security` role produces `evaluation_report.json`; gate_result with `gate_id: review`.

## M7 — Memory and resume

- **Tiers:** L0–L4 per `DATA_MODEL.md`.  
- **Resume:** `bootstrap/fc-export-resume-packet.sh` refreshes `RESUME_PACKET.md` from `PLAN.md` / `WHERE_LEFT_OFF.md`.  
- **Compaction:** batch jobs (future) honor `memory_policy.md`.

## Correlation

- Every `gate_result` and `ledger_event` should carry `trace_id` when OTEL is configured (`OTEL_EXPORTER_OTLP_ENDPOINT`).
