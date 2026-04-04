from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_schema_check_exits_zero() -> None:
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, "-m", "forge_council.schema_check"],
        cwd=root,
        env={**dict(**__import__("os").environ), "PYTHONPATH": str(root / "src")},
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fc_repo_ingestion_runs() -> None:
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, str(root / "tools" / "fc_repo_ingestion.py"), str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert (root / "REPO_PROFILE.md").is_file()
