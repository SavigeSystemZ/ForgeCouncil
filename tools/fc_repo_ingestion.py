#!/usr/bin/env python3
"""Generate REPO_PROFILE.md and CONFLICT_MAP.md for Forge Council (M1 ingestion)."""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

INSTRUCTION_GLOBS = [
    "AGENTS.md",
    "GPT54.md",
    "PRD.md",
    "ARCHITECTURE.md",
    "DATA_MODEL.md",
    "NFR.md",
    "RUNBOOK.md",
    "CODEX.md",
    "CLAUDE.md",
    "GEMINI.md",
    "WINDSURF.md",
    ".cursorrules",
    ".windsurfrules",
    ".github/copilot-instructions.md",
    ".cursor/rules/**/*",
    ".cursor/agents/**/*",
    "_system/**/*.md",
    "_system/prompt-packs/**/*.md",
]

STACK_MARKERS = [
    ("Python", "pyproject.toml", "pip install / pytest"),
    ("Python", "setup.py", "python setup.py"),
    ("Node", "package.json", "npm test / npm run build"),
    ("Go", "go.mod", "go test ./..."),
    ("Rust", "Cargo.toml", "cargo test"),
    ("Ruby", "Gemfile", "bundle exec rake"),
]


def _glob_files(repo: Path, pattern: str) -> list[Path]:
    if "**" in pattern:
        return sorted(p for p in repo.glob(pattern) if p.is_file())
    p = repo / pattern
    return [p] if p.is_file() else []


def collect_instruction_files(repo: Path) -> list[str]:
    seen: set[Path] = set()
    out: list[str] = []
    for pat in INSTRUCTION_GLOBS:
        for f in _glob_files(repo, pat):
            rp = f.resolve()
            if rp not in seen:
                seen.add(rp)
                try:
                    rel = rp.relative_to(repo)
                except ValueError:
                    continue
                out.append(str(rel).replace("\\", "/"))
    return sorted(out)


def detect_stack(repo: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for name, marker, hint in STACK_MARKERS:
        if (repo / marker).is_file():
            rows.append((name, marker, hint))
    return rows


def run_conflict_scan(repo: Path) -> tuple[list[str], str]:
    script = repo / "bootstrap" / "detect-instruction-conflicts.sh"
    if not script.is_file():
        return [], "detect-instruction-conflicts.sh not found"
    proc = subprocess.run(
        ["bash", str(script), str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    raw = (proc.stdout or "") + (proc.stderr or "")
    findings: list[str] = []
    in_findings = False
    for line in raw.splitlines():
        if line.strip() == "Findings":
            in_findings = True
            continue
        if in_findings and line.startswith("- "):
            findings.append(line[2:].strip())
        elif in_findings and line.strip() and not line.startswith("-"):
            break
    return findings, raw


def build_repo_profile(repo: Path, instructions: list[str], stack: list[tuple[str, str, str]]) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Forge Council — Repository Operating Profile (human)",
        "",
        "**Generated/refreshed by:** `bootstrap/fc-repo-ingestion.sh`",
        "**Machine-oriented summary:** `_system/REPO_OPERATING_PROFILE.md`",
        f"**Last scan (UTC):** {now}",
        "",
        "## Summary",
        "",
        "- **Product:** Forge Council — software-factory control plane.",
        f"- **Instruction files discovered:** {len(instructions)}",
        "",
        "## Detected stack",
        "",
    ]
    if stack:
        lines.append("| Stack | Marker | Suggested validation |")
        lines.append("|-------|--------|----------------------|")
        for name, marker, hint in stack:
            lines.append(f"| {name} | `{marker}` | {hint} |")
    else:
        lines.append("- No common stack markers found (add manually if applicable).")
    lines.extend(["", "## Instruction inventory", "", "| Path |", "|------|"])
    for p in instructions:
        lines.append(f"| `{p}` |")
    lines.extend(
        [
            "",
            "## Validation commands",
            "",
            "| Command | Purpose |",
            "|---------|---------|",
            "| `bootstrap/validate-system.sh .` | AIAST system validation |",
            "| `bootstrap/validate-instruction-layer.sh .` | Instruction layer |",
            "| `bootstrap/detect-instruction-conflicts.sh .` | Conflict heuristics |",
        ]
    )
    if (repo / "pyproject.toml").is_file():
        lines.append("| `python -m pytest` | Tests (if configured) |")
        lines.append("| `python -m forge_council.schema_check` | FC schema validation |")
    lines.extend(
        [
            "",
            "## Deploy / packaging surfaces",
            "",
            "- `packaging/`, `ops/install/`, `mobile/`, `ai/` (AIAST runtime foundations)",
            "",
            "## Known risks",
            "",
            "- Re-run ingestion after adding languages, adapters, or new instruction roots.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def build_conflict_map(repo: Path, findings: list[str], raw_report: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Forge Council — Instruction Conflict Map",
        "",
        "**Generated/refreshed by:** `bootstrap/fc-repo-ingestion.sh`",
        "**Precedence contract:** `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`",
        f"**Last scan (UTC):** {now}",
        "",
        "## Resolution order (summary)",
        "",
        "1. Repo-local runtime and product facts",
        "2. AIAST core (`AGENTS.md`, `_system/` core docs)",
        "3. Forge Council extension (`_system/forge-council/`)",
        "4. Tool overlays (`CODEX.md`, `.cursorrules`, …)",
        "5. Prompt packs (`_system/prompt-packs/`)",
        "6. Host orchestration context",
        "",
        "## Detected conflicts (automation)",
        "",
        "| Topic | Source | Severity | Resolution |",
        "|-------|--------|----------|------------|",
    ]
    if findings:
        for f in findings:
            topic = f[:80] + ("…" if len(f) > 80 else "")
            lines.append(f"| `{topic}` | heuristic scan | medium | Review; align adapters with AGENTS.md |")
    else:
        lines.append("| (none) | `detect-instruction-conflicts.sh` | — | No heuristic findings |")
    lines.extend(
        [
            "",
            "## Raw scan output (reference)",
            "",
            "```text",
        ]
    )
    # Trim huge output
    snippet = raw_report.strip()
    if len(snippet) > 12000:
        snippet = snippet[:12000] + "\n... (truncated)"
    lines.append(snippet or "(empty)")
    lines.extend(["```", "", "## Manual review notes", "", "- Add rows for subtle semantic conflicts not caught by heuristics.", ""])
    return "\n".join(lines) + "\n"


def main() -> int:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not (repo / "AGENTS.md").is_file():
        print(f"Not a Forge Council / AIAST repo root (missing AGENTS.md): {repo}", file=sys.stderr)
        return 1
    instructions = collect_instruction_files(repo)
    stack = detect_stack(repo)
    findings, raw = run_conflict_scan(repo)
    (repo / "REPO_PROFILE.md").write_text(build_repo_profile(repo, instructions, stack), encoding="utf-8")
    (repo / "CONFLICT_MAP.md").write_text(build_conflict_map(repo, findings, raw), encoding="utf-8")
    print(f"Wrote {repo / 'REPO_PROFILE.md'}")
    print(f"Wrote {repo / 'CONFLICT_MAP.md'}")
    print(f"Instruction files: {len(instructions)}; heuristic findings: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
