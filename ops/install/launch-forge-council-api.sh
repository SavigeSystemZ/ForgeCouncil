#!/usr/bin/env bash
# Forge Council control-plane API (uvicorn). Used by desktop entry and systemd.
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${ROOT_DIR}/ops/env/.env"
VENV_PY="${ROOT_DIR}/.venv/bin/python"
VENV_API="${ROOT_DIR}/.venv/bin/forge-council-api"

if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090,SC1091
  source "${ENV_FILE}"
  set +a
fi

: "${FC_API_HOST:=${APP_BIND_ADDRESS:-127.0.0.1}}"
: "${FC_API_PORT:=${APP_PORT:-8010}}"
export FC_API_HOST FC_API_PORT

cd "${ROOT_DIR}"

if [[ -x "${VENV_API}" ]]; then
  exec "${VENV_API}"
fi
if [[ -x "${VENV_PY}" ]]; then
  exec "${VENV_PY}" -m forge_council.server
fi

printf '%s\n' "[forge-council] missing venv at ${ROOT_DIR}/.venv; run: bootstrap/fc-host-install.sh" >&2
exit 1
