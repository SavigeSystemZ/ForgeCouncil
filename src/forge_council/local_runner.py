"""Gated local subprocess execution for control-plane dispatch (no shell)."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

_OUTPUT_CAP = 65536
_ARTIFACT_MAX_BYTES = 16 * 1024 * 1024  # per stream cap when writing to disk


def dispatch_kill_switch_active() -> bool:
    """When true, dispatch must refuse new execution (operator kill-switch)."""
    v = os.environ.get("FC_DISPATCH_KILL_SWITCH", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def async_dispatch_enabled() -> bool:
    """Opt-in for ``execution: async`` queued subprocess dispatch."""
    v = os.environ.get("FC_ALLOW_ASYNC_DISPATCH", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def subprocess_dispatch_enabled() -> bool:
    """Explicit opt-in for real subprocess execution."""
    v = os.environ.get("FC_ALLOW_SUBPROCESS_DISPATCH", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _truthy(name: str, default: bool = True) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def parse_exec_allowlist() -> list[str]:
    """Comma-separated absolute paths to executables permitted as argv[0]."""
    raw = os.environ.get("FC_EXEC_ALLOWLIST", "").strip()
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def exec_timeout_sec() -> float:
    raw = os.environ.get("FC_EXEC_TIMEOUT_SEC", "60").strip()
    try:
        return max(1.0, min(float(raw), 3600.0))
    except ValueError:
        return 60.0


def resolve_artifact_root() -> Path | None:
    """Directory for full stdout/stderr logs; unset → no files (snippets only in ledger)."""
    p = os.environ.get("FC_ARTIFACT_ROOT", "").strip()
    if not p:
        return None
    root = Path(p).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def dispatch_max_queued() -> int | None:
    raw = os.environ.get("FC_DISPATCH_MAX_QUEUED", "").strip()
    if not raw:
        return None
    try:
        n = int(raw)
        return max(1, min(n, 100_000))
    except ValueError:
        return None


def resolve_workdir() -> Path:
    for key in ("FC_EXEC_WORKDIR", "FORGE_COUNCIL_REPO_ROOT"):
        p = os.environ.get(key, "").strip()
        if p:
            return Path(p).resolve()
    return Path.cwd().resolve()


def validate_subprocess_argv(argv: list[str]) -> None:
    """Require allowlisted argv[0] (resolved path match)."""
    if not argv:
        raise ValueError("argv must be non-empty for subprocess dispatch")
    allowlist = parse_exec_allowlist()
    if not allowlist:
        raise PermissionError(
            "FC_EXEC_ALLOWLIST must list allowed executable paths (comma-separated)"
        )
    exe = argv[0]
    try:
        candidate = Path(exe).resolve()
    except OSError as e:
        raise PermissionError(f"invalid executable path: {exe}") from e
    allowed_resolved: set[str] = set()
    for entry in allowlist:
        try:
            allowed_resolved.add(str(Path(entry).resolve()))
        except OSError:
            allowed_resolved.add(entry)
    c_str = str(candidate)
    if c_str not in allowed_resolved and exe not in allowlist:
        raise PermissionError(f"executable not allowlisted: {exe}")


def write_dispatch_log_artifacts(
    *,
    run_id: str,
    step_id: str,
    stdout_text: str,
    stderr_text: str,
) -> tuple[str | None, str | None]:
    """Write full logs under FC_ARTIFACT_ROOT/{run_id}/{step_id}/; return repo-relative refs."""
    root = resolve_artifact_root()
    if root is None:
        return None, None
    base = root / run_id / step_id
    try:
        base.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None, None
    rel_prefix = f"{run_id}/{step_id}"
    out_path = base / "stdout.log"
    err_path = base / "stderr.log"
    try:
        out_b = stdout_text.encode("utf-8", errors="replace")[:_ARTIFACT_MAX_BYTES]
        err_b = stderr_text.encode("utf-8", errors="replace")[:_ARTIFACT_MAX_BYTES]
        out_path.write_bytes(out_b)
        err_path.write_bytes(err_b)
    except OSError:
        return None, None
    try:
        out_path.resolve().relative_to(root)
        err_path.resolve().relative_to(root)
    except ValueError:
        return None, None
    return f"{rel_prefix}/stdout.log", f"{rel_prefix}/stderr.log"


def truncate_output(text: str, limit: int = _OUTPUT_CAP) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 20] + "\n... [truncated]"


def build_child_env(overlay: dict[str, str] | None) -> dict[str, str]:
    """Merge environment: optional full inherit, else PATH-only baseline."""
    overlay = overlay or {}
    if _truthy("FC_EXEC_INHERIT_ENV", default=True):
        base = dict(os.environ)
    else:
        base = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
    merged = {**base, **overlay}
    return merged


async def run_subprocess_async(
    argv: list[str],
    *,
    cwd: Path,
    env_overlay: dict[str, str] | None,
    timeout: float,
) -> tuple[int, str, str]:
    """Run argv with no shell; returns (exit_code, stdout, stderr) as strings."""
    child_env = build_child_env(env_overlay)
    proc = await asyncio.create_subprocess_exec(
        *argv,
        cwd=str(cwd),
        env=child_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        out_b, err_b = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        proc.kill()
        await proc.wait()
        return 124, "", "forge_council: subprocess timed out"
    code = proc.returncode if proc.returncode is not None else -1
    return (
        int(code),
        out_b.decode(errors="replace"),
        err_b.decode(errors="replace"),
    )
