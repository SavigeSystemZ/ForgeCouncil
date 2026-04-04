#!/usr/bin/env bash
# User-mode install: Python venv, editable package, desktop entry, app icon.
# Run from repo root: bash bootstrap/fc-host-install.sh
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

LAUNCH="${ROOT}/ops/install/launch-forge-council-api.sh"
ICON_SRC="${ROOT}/packaging/icons/hicolor/scalable/apps/io.aiaast.forge.council.svg"
ICON_DEST="${HOME}/.local/share/icons/hicolor/scalable/apps/io.aiaast.forge.council.svg"

log() { printf '[fc-host-install] %s\n' "$*"; }

if ! command -v python3 >/dev/null 2>&1; then
  printf '[fc-host-install][error] python3 not found\n' >&2
  exit 1
fi

chmod +x "${LAUNCH}" 2>/dev/null || true
chmod +x "${ROOT}/ops/install/install.sh" 2>/dev/null || true

if [[ ! -d "${ROOT}/.venv" ]]; then
  log "creating venv at ${ROOT}/.venv"
  python3 -m venv "${ROOT}/.venv"
fi
# shellcheck disable=SC1091
source "${ROOT}/.venv/bin/activate"
python -m pip install -U pip wheel setuptools
log "pip install -e .[dev,api]"
pip install -e "${ROOT}[dev,api]"

log "ops/install/install.sh --mode user --skip-service --port 8010"
bash "${ROOT}/ops/install/install.sh" --mode user --skip-service --port 8010

if [[ -f "${ROOT}/ops/env/.env" ]]; then
  APP_P="$(awk -F= '$1=="APP_PORT" {print $2}' "${ROOT}/ops/env/.env" | tail -n 1 | tr -d '"' | tr -d "'")"
  if [[ -n "${APP_P}" ]]; then
    if grep -q '^FC_API_PORT=' "${ROOT}/ops/env/.env"; then
      sed -i.bak "s/^FC_API_PORT=.*/FC_API_PORT=${APP_P}/" "${ROOT}/ops/env/.env" && rm -f "${ROOT}/ops/env/.env.bak"
    else
      printf '\nFC_API_PORT=%s\n' "${APP_P}" >>"${ROOT}/ops/env/.env"
    fi
    if grep -q '^APP_HEALTHCHECK_URL=' "${ROOT}/ops/env/.env"; then
      sed -i.bak "s|^APP_HEALTHCHECK_URL=.*|APP_HEALTHCHECK_URL=http://127.0.0.1:${APP_P}/health|" "${ROOT}/ops/env/.env" && rm -f "${ROOT}/ops/env/.env.bak"
    fi
  fi
fi

if [[ -f "${ICON_SRC}" ]]; then
  log "installing icon -> ${ICON_DEST}"
  mkdir -p "$(dirname "${ICON_DEST}")"
  cp -f "${ICON_SRC}" "${ICON_DEST}"
  if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t "${HOME}/.local/share/icons/hicolor" 2>/dev/null || true
  fi
else
  log "warn: icon missing at ${ICON_SRC}"
fi

log "done. Launch from app menu (Forge Council) or: ${LAUNCH}"
log "health: http://127.0.0.1:8010/health (if APP_PORT is 8010)"
