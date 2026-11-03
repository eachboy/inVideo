#!/usr/bin/env python3
"""PostToolUse hook: format and lint Python files under backend/ after Edit/Write.

Runs `ruff format` and `ruff check --fix` through uv. Remaining lint errors are
printed to stderr with exit code 2, so Claude sees them and fixes them.
Silently does nothing until backend/pyproject.toml exists (before Stage 1 setup).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path or not file_path.endswith(".py"):
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    backend = project / "backend"
    target = Path(file_path).resolve()

    try:
        target.relative_to(backend)
    except ValueError:
        return 0

    if not (backend / "pyproject.toml").exists() or not target.exists():
        return 0

    def ruff(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["uv", "run", "ruff", *args, str(target)],
            cwd=backend,
            capture_output=True,
            text=True,
            timeout=60,
        )

    try:
        ruff("format")
        result = ruff("check", "--fix", "--quiet")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 0

    if result.returncode != 0:
        output = (result.stdout or result.stderr).strip()[:3000]
        print(
            f"ruff found issues that need manual fixing in {target.name}:\n{output}",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
