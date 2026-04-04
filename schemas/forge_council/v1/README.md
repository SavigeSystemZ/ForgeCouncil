# Forge Council JSON Schemas (v1)

Interchange contracts for orchestration, gates, ledger, and artifacts. **Normative** for HTTP/API and runner payloads.

| File | Purpose |
|------|---------|
| `milestone.json` | Milestone definition |
| `task_packet.json` | Role-scoped work packet |
| `approval_request.json` | L4 human approval |
| `run.json` | Execution run |
| `run_step.json` | Ordered step in a run |
| `run_summary.json` | Terminal summary + handoff |
| `artifact.json` | Stored artifact metadata |
| `gate_result.json` | Validation/review/approval gate |
| `evaluation_report.json` | Reviewer output |
| `ledger_event.json` | Append-only audit event |

Validate locally:

```bash
pip install -e ".[dev]"
PYTHONPATH=src python -m forge_council.schema_check
```
