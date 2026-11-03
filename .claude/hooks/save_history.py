#!/usr/bin/env python3
"""Stop hook: append the last user/assistant exchange to .claude/history/YYYY-MM-DD.md.

Reads the hook JSON from stdin (transcript_path, session_id) and the transcript jsonl.
Everything is written as UTF-8 so Russian text is preserved.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def text_of(content: object) -> str:
    """Extract plain text from a message content (str or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "\n".join(p for p in parts if p).strip()
    return ""


def is_real_user_text(text: str) -> bool:
    return bool(text) and not text.startswith(
        ("<system-reminder>", "<command-", "<local-command")
    )


def last_exchange(transcript: Path) -> tuple[str, str]:
    user, assistant = "", ""
    with transcript.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = entry.get("type")
            text = text_of(entry.get("message", {}).get("content"))
            if kind == "user" and is_real_user_text(text):
                user, assistant = text, ""
            elif kind == "assistant" and text:
                assistant = text
    return user, assistant


def main() -> int:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    transcript = Path(data.get("transcript_path", ""))
    if not transcript.is_file():
        return 0

    user, assistant = last_exchange(transcript)
    if not user:
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    now = datetime.now()
    history = project / ".claude" / "history"
    history.mkdir(parents=True, exist_ok=True)
    day_file = history / f"{now:%Y-%m-%d}.md"

    session = str(data.get("session_id", ""))[:8]
    entry = (
        f"## {now:%H:%M:%S} (сессия {session})\n\n"
        f"**Вопрос:**\n\n{user}\n\n"
        f"**Ответ:**\n\n{assistant or '(без текстового ответа)'}\n\n---\n\n"
    )

    # Stop can fire again for the same turn: skip if this exact exchange is the last record.
    if day_file.exists():
        existing = day_file.read_text(encoding="utf-8")
        tail = existing.rsplit("## ", 1)[-1]
        if (
            f"**Вопрос:**\n\n{user}\n\n" in tail
            and f"**Ответ:**\n\n{assistant}" in tail
        ):
            return 0

    with day_file.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
