#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: discover-plugins.sh <target-repo> [--json]

Scan _system/plugins/ for installed plugins and report their status.
EOF
}

TARGET=""
JSON_OUTPUT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_OUTPUT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [[ -z "${TARGET}" ]]; then
        TARGET="$1"; shift
      else
        echo "Unexpected argument: $1" >&2; exit 1
      fi
      ;;
  esac
done

if [[ -z "${TARGET}" ]]; then
  usage
  exit 1
fi

PLUGINS_DIR="${TARGET}/_system/plugins"

if [[ ! -d "${PLUGINS_DIR}" ]]; then
  if [[ ${JSON_OUTPUT} -eq 1 ]]; then
    echo '{"plugins":[],"count":0}'
  else
    echo "No plugins directory found."
  fi
  exit 0
fi

python3 - <<'PY' "${PLUGINS_DIR}" "${JSON_OUTPUT}"
from __future__ import annotations

import json
import sys
from pathlib import Path

plugins_dir = Path(sys.argv[1]).resolve()
json_output = sys.argv[2] == "1"

plugins: list[dict] = []

for plugin_json in sorted(plugins_dir.glob("*/plugin.json")):
    try:
        manifest = json.loads(plugin_json.read_text())
        has_runner = (plugin_json.parent / "run.sh").is_file()
        has_readme = (plugin_json.parent / "README.md").is_file()
        plugins.append({
            "name": manifest.get("name", plugin_json.parent.name),
            "version": manifest.get("version", "unknown"),
            "description": manifest.get("description", ""),
            "hooks": manifest.get("hooks", []),
            "capabilities": manifest.get("capabilities", []),
            "enabled": manifest.get("enabled", True),
            "has_runner": has_runner,
            "has_readme": has_readme,
            "path": str(plugin_json.parent.relative_to(plugins_dir.parent.parent)),
        })
    except Exception as exc:
        plugins.append({
            "name": plugin_json.parent.name,
            "version": "error",
            "description": f"Failed to parse: {exc}",
            "hooks": [],
            "enabled": False,
            "has_runner": False,
            "has_readme": False,
            "path": str(plugin_json.parent.relative_to(plugins_dir.parent.parent)),
        })

if json_output:
    print(json.dumps({"plugins": plugins, "count": len(plugins)}, indent=2))
else:
    if not plugins:
        print("No plugins found.")
    else:
        print(f"Discovered {len(plugins)} plugin(s):\n")
        for p in plugins:
            status = "enabled" if p["enabled"] else "disabled"
            runner = "executable" if p["has_runner"] else "metadata-only"
            print(f"  {p['name']} v{p['version']} [{status}, {runner}]")
            print(f"    {p['description']}")
            print(f"    Hooks: {', '.join(p['hooks']) if p['hooks'] else 'none'}")
            print(f"    Path:  {p['path']}")
            print()
    print(f"plugins_discovered: {len(plugins)}")
PY
)
            print()
    print(f"plugins_discovered: {len(plugins)}")
PY
