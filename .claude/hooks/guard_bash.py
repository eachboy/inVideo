#!/usr/bin/env python3
"""PreToolUse hook: block destructive shell commands.

Reads the hook JSON from stdin. Exit code 2 blocks the tool call and shows
stderr to Claude. Exit code 0 leaves the decision to the normal permission flow.
Standard library only, so it runs under `uv run --no-project python`.
"""

from __future__ import annotations

import json
import re
import sys

# (regex, human-readable reason)
RULES: list[tuple[str, str]] = [
    (
        r"\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r|-r\s+-f|-f\s+-r)\b",
        "recursive force delete (rm -rf)",
    ),
    (
        r"Remove-Item\b.*(-Recurse.*-Force|-Force.*-Recurse)",
        "recursive force delete (Remove-Item)",
    ),
    (r"\bgit\s+push\b.*(--force|--force-with-lease|\s-f\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean -f"),
    (r"\bgit\s+branch\s+-D\s+main\b", "deleting the main branch"),
    (
        r"\bdocker\s+compose\b.*\bdown\b.*(\s-v\b|--volumes)",
        "docker compose down with volumes (data loss)",
    ),
    (r"\bdocker\s+volume\s+(rm|prune)\b", "docker volume removal (data loss)"),
    (r"\bdocker\s+system\s+prune\b", "docker system prune"),
    (r"\b(DROP\s+(DATABASE|SCHEMA|TABLE)|TRUNCATE\s+TABLE)\b", "destructive SQL"),
    (
        r"\balembic\s+downgrade\s+base\b",
        "alembic downgrade base (drops the whole schema)",
    ),
    (r"\bchmod\s+-R\s+777\b", "chmod -R 777"),
    (r"\b(curl|wget)\b[^|]*\|\s*(ba|z)?sh\b", "piping a download into a shell"),
    (
        r"\b(cat|type|less|more|head|tail|Get-Content)\s+[^|;&]*\.env(?!\.example)\b",
        "reading a secrets file (.env); only .env.example may be read",
    ),
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    command = (data.get("tool_input") or {}).get("command") or ""
    for pattern, reason in RULES:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                f"Blocked by project guard: {reason}. "
                "If this is really needed, ask the user to run it manually.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
