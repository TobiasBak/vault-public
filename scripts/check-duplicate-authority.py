#!/usr/bin/env python3
"""Root AGENTS.md must not restate what another file already owns.

Verbatim overlap is the decidable part of duplicate authority: a sentence that
appears in `AGENTS.md` and again in a skill or note gives the rule two owners,
and the copies drift. Semantic duplication ("this line repeats a skill's
charter in different words") still needs the per-line question in
`skills/theodore-kaczynski-nullifier/references/agent-context.md`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER = Path("AGENTS.md")
WINDOW = 8
WORD = re.compile(r"[a-z0-9][a-z0-9._/-]*")


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def shingles(text: str) -> set[tuple[str, ...]]:
    w = words(text)
    return {tuple(w[i : i + WINDOW]) for i in range(len(w) - WINDOW + 1)}


def tracked_markdown() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", "*.md"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [Path(p) for p in out.decode().split("\0") if p]


def main() -> int:
    owner_text = (ROOT / OWNER).read_text()
    owner_shingles = shingles(owner_text)
    # Line numbers in the owner, so the failure names where to look.
    owner_lines = {}
    for number, line in enumerate(owner_text.splitlines(), start=1):
        for shingle in shingles(line):
            owner_lines.setdefault(shingle, number)

    issues = []
    for path in tracked_markdown():
        if path == OWNER:
            continue
        text = (ROOT / path).read_text()
        shared = owner_shingles & shingles(text)
        for shingle in sorted(shared, key=lambda s: owner_lines.get(s, 0)):
            line = owner_lines.get(shingle)
            issues.append(f"{OWNER}:{line}: '{' '.join(shingle)}' also appears in {path}")

    for issue in issues:
        print(f"duplicate authority: {issue}", file=sys.stderr)
    if issues:
        print(
            "One owner per fact. Keep the rule in the file that is open when the rule\n"
            "is needed and let AGENTS.md link to it, or delete the copy.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
