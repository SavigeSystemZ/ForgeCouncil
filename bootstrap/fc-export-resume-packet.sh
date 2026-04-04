#!/usr/bin/env bash
# M7 helper: refresh RESUME_PACKET.md from working files
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

TARGET="${1:-${REPO_ROOT}}"
exec python3 "${REPO_ROOT}/tools/fc_export_resume.py" "${TARGET}"
