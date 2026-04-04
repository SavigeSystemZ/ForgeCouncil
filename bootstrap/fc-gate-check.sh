#!/usr/bin/env bash
# M6 stub: validation / review gate driver
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: fc-gate-check.sh [--gate validation|review] [--repo PATH] [--full-validate]

Runs lightweight repo checks. Emits gate_result-shaped JSON to stdout (informal).

Options:
  --gate           Gate id (default: validation)
  --repo           Repository root (default: parent of bootstrap/)
  --full-validate  Run bootstrap/validate-system.sh (stricter; may fail if profiles stale)
EOF
}

GATE="validation"
TARGET="${REPO_ROOT}"
FULL_VALIDATE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gate)
      GATE="${2:-}"
      shift 2
      ;;
    --repo)
      TARGET="${2:-}"
      shift 2
      ;;
    --full-validate)
      FULL_VALIDATE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

PASS=true
DETAILS=()

if [[ ! -f "${TARGET}/AGENTS.md" ]]; then
  PASS=false
  DETAILS+=("missing AGENTS.md")
fi

if [[ "${GATE}" == "validation" && "${FULL_VALIDATE}" -eq 1 ]]; then
  if [[ -x "${TARGET}/bootstrap/validate-system.sh" ]]; then
    if ! "${TARGET}/bootstrap/validate-system.sh" "${TARGET}" >/tmp/fc_gate_validate.log 2>&1; then
      PASS=false
      DETAILS+=("validate-system.sh failed — see /tmp/fc_gate_validate.log")
    fi
  else
    DETAILS+=("validate-system.sh not executable — skipped")
  fi
else
  DETAILS+=("light gate only; pass --full-validate for validate-system.sh")
fi

echo "{"
echo "  \"schema_version\": \"1\","
echo "  \"gate_id\": \"${GATE}\","
echo "  \"passed\": ${PASS},"
echo "  \"details\": \"$(printf '%s; ' "${DETAILS[@]}")\""
echo "}"

if [[ "${PASS}" != true ]]; then
  exit 1
fi
exit 0
