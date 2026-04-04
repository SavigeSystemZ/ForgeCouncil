"""Optional API token auth (shared secret) with OpenAPI bearer scheme."""

from __future__ import annotations

import os

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=False)


async def require_api_token(
    cred: HTTPAuthorizationCredentials | None = Security(_bearer),
) -> None:
    """If ``FC_API_TOKEN`` is set, require a matching Bearer token."""
    expected = os.environ.get("FC_API_TOKEN", "").strip()
    if not expected:
        return
    if cred is None or cred.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="missing or invalid Authorization header (Bearer token required)",
        )
    if cred.credentials != expected:
        raise HTTPException(status_code=403, detail="invalid token")
