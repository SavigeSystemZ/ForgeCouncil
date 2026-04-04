#!/usr/bin/env bash
# Forge Council M1: refresh REPO_PROFILE.md and CONFLICT_MAP.md
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: fc-repo-ingestion.sh [target-repo]

Scan instruction surfaces and regenerate REPO_PROFILE.md and CONFLICT_MAP.md.
Default target is the repository containing this script.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

TARGET="${1:-${REPO_ROOT}}"
if [[ ! -d "${TARGET}" ]]; then
  echo "Target repo does not exist: ${TARGET}" >&2
  exit 1
fi

python3 "${REPO_ROOT}/tools/fc_repo_ingestion.py" "${TARGET}"
echo ""
echo "Note: refresh machine profile with:"
echo "  bootstrap/generate-operating-profile.sh ${TARGET} --write"
