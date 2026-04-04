"""Load JSON Schemas from the repo and validate payloads."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def _repo_root() -> Path:
    env = os.environ.get("FORGE_COUNCIL_REPO_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]


def schema_path(name: str) -> Path:
    return _repo_root() / "schemas" / "forge_council" / "v1" / f"{name}.json"


@lru_cache(maxsize=32)
def _validator_for(name: str) -> Draft202012Validator:
    path = schema_path(name)
    if not path.is_file():
        raise FileNotFoundError(f"Schema not found: {path}")
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(raw)
    return Draft202012Validator(raw)


def validate_instance(name: str, instance: dict[str, Any]) -> None:
    """Raise jsonschema.ValidationError on failure."""
    validator = _validator_for(name)
    validator.validate(instance)


def validate_instance_or_raise_http(name: str, instance: dict[str, Any]) -> None:
    """Convert validation errors to ValueError with message (for HTTP 400)."""
    from jsonschema import ValidationError

    try:
        validate_instance(name, instance)
    except ValidationError as e:
        raise ValueError(e.message) from e
