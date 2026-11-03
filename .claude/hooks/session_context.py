#!/usr/bin/env python3
"""SessionStart hook: put docs/STATUS.md into Claude's context.

Plain stdout from a SessionStart hook is added to the conversation context.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    status = project / "docs" / "STATUS.md"

    if not status.exists():
        print(
            "docs/STATUS.md does not exist yet. The current stage of docs/project/realization.md is unknown."
        )
        return 0

    text = status.read_text(encoding="utf-8")
    print("Project progress tracker (docs/STATUS.md), loaded at session start:\n")
    print(text[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
