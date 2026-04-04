#!/usr/bin/env python3
"""Emit RESUME_PACKET.md from PLAN.md and WHERE_LEFT_OFF.md snippets."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import sys


def _section(path: Path, start_prefix: str, max_lines: int = 40) -> str:
    if not path.is_file():
        return "(file missing)"
    lines = path.read_text(encoding="utf-8").splitlines()
    buf: list[str] = []
    capture = False
    for line in lines:
        if line.startswith(start_prefix):
            capture = True
            buf.append(line)
            continue
        if capture:
            if line.startswith("## ") and not line.startswith(start_prefix):
                break
            buf.append(line)
            if len(buf) >= max_lines:
                break
    return "\n".join(buf) if buf else "(section not found)"


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan_obj = _section(repo / "PLAN.md", "## Objective")
    snap = _section(repo / "WHERE_LEFT_OFF.md", "## Session Snapshot")
    nxt = _section(repo / "WHERE_LEFT_OFF.md", "## Next Best Step")
    body = f"""# Forge Council — Resume Packet

**Generated:** {now} (fc_export_resume.py)

## Objective (from PLAN.md)

{plan_obj}

## Session snapshot (from WHERE_LEFT_OFF.md)

{snap}

## Next best step

{nxt}

## Load first

1. `AGENTS.md`
2. `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`
3. `PLAN.md`, `TODO.md`, `CONFLICT_MAP.md`
4. `_system/forge-council/README.md`

## Next actions

- Continue from `PLAN.md` execution slices.
- Run `bootstrap/fc-repo-ingestion.sh` if instruction files changed.

## Validation

- Record last `bootstrap/validate-system.sh` outcome in `WHERE_LEFT_OFF.md`.
"""
    (repo / "RESUME_PACKET.md").write_text(body, encoding="utf-8")
    print(f"Wrote {repo / 'RESUME_PACKET.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
