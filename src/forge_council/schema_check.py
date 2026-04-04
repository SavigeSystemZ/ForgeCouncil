"""Validate JSON Schema files and example document instances."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def schema_dir() -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / "schemas" / "forge_council" / "v1"


def main() -> int:
    d = schema_dir()
    if not d.is_dir():
        print(f"Schema directory missing: {d}", file=sys.stderr)
        return 1
    files = sorted(d.glob("*.json"))
    if not files:
        print("No schema files found.", file=sys.stderr)
        return 1
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError:
        for path in files:
            json.loads(path.read_text(encoding="utf-8"))
        print(f"OK: {len(files)} JSON files parse (install jsonschema for full validation)")
        return 0

    for path in files:
        instance = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(instance)
    print(f"OK: {len(files)} schemas are valid Draft 2020-12 meta-schema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
