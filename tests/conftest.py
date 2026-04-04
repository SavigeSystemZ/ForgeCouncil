"""Pytest configuration."""

from __future__ import annotations

import os
from pathlib import Path

# Resolve JSON Schemas relative to repository root (not site-packages).
_root = Path(__file__).resolve().parents[1]
os.environ.setdefault("FORGE_COUNCIL_REPO_ROOT", str(_root))
