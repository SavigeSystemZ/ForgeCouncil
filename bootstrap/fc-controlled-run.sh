#!/usr/bin/env bash
# M5 stub: single-milestone controlled execution contract (no remote dispatch yet)
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: fc-controlled-run.sh [--dry-run] [--milestone CODE]

Placeholder for controlled execution dispatch. Records intent only; does not
invoke external runners. Wire to control-plane service in M5+.

Options:
  --dry-run     Print planned actions (default)
  --milestone   Milestone code label for ledger metadata
EOF
}

DRY_RUN=1
MILESTONE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --milestone)
      MILESTONE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

echo "Forge Council fc-controlled-run (stub)"
echo "Repo: ${REPO_ROOT}"
echo "Milestone: ${MILESTONE:-unspecified}"
echo "Mode: dry-run (no side effects)"
echo
echo "Planned steps:"
echo "  1. Load task_packet schema + CONFLICT_MAP.md (no high-severity blocks)"
echo "  2. Open OTel span forge_council.run (see src/forge_council/otel.py)"
echo "  3. Dispatch to runner adapter (local | remote) — not implemented"
echo "  4. Capture artifacts + emit ledger_event + run_summary JSON"
exit 0
