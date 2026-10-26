#!/usr/bin/env python3
"""Check that the index lists tracked notes and skills."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = Path("index.md")
# Directories whose notes are content, and so must appear in the index.
CONTENT_DIRS = ("agents", "software", "hardware", "tobias")
SKILL_PARENTS = (Path("skills"), Path(".agents") / "skills")


def tracked(suffix: str) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", f"*{suffix}"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [Path(p) for p in out.decode().split("\0") if p]


def check_index() -> list[str]:
    text = (ROOT / INDEX).read_text()
    issues = []
    for path in tracked(".md"):
        if path.parts[0] in CONTENT_DIRS:
            needed = True
        elif len(path.parts) == 2 and path.parent in SKILL_PARENTS:
            needed = path.name == "SKILL.md"
        elif len(path.parts) == 3 and path.parent.parent in SKILL_PARENTS:
            needed = path.name == "SKILL.md"
        else:
            continue
        if needed and path.as_posix() not in text:
            issues.append(f"{INDEX}: no line for {path}")
    return issues


def main() -> int:
    issues = check_index()
    for issue in issues:
        print(f"index: {issue}", file=sys.stderr)
    if issues:
        print(f"Give every note and skill a line in {INDEX}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
