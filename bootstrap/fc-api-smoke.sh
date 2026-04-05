#!/usr/bin/env bash
# Quick smoke: control-plane /health (requires server running).
set -euo pipefail

HOST="${FC_API_HOST:-127.0.0.1}"
PORT="${FC_API_PORT:-46124}"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl required" >&2
  exit 1
fi

curl -fsS "http://${HOST}:${PORT}/health"
echo
