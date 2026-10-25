#!/usr/bin/env python3
"""Shape of the always-loaded file, and whether the index still lists everything.

`AGENTS.md` is read on every task, so it stays small and keeps one order of
sections; a value that is not ranked against the others never settles a
tradeoff. `index.md` is the only map, so a note missing from it is findable
only by search — a shape nobody notices until they need the note.

Judgment (which section a line belongs in, whether a note earns its place)
stays with the design principles; this is the decidable part.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS = Path("AGENTS.md")
INDEX = Path("index.md")
MAX_LINES = 80
MAX_VALUES = 5
SECTIONS = ["Purpose", "Values", "Loop", "Areas", "Boundaries"]
# Directories whose notes are content, and so must appear in the index.
CONTENT_DIRS = ("agents", "software", "hardware", "tobias")
SKILL_PARENTS = (Path("skills"), Path(".agents") / "skills")
HEADING = re.compile(r"^##\s+(.+?)\s*$")
VALUE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+(.+)$")


def tracked(suffix: str) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", f"*{suffix}"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [Path(p) for p in out.decode().split("\0") if p]


def check_agents() -> list[str]:
    text = (ROOT / AGENTS).read_text()
    lines = text.splitlines()
    issues = []
    if len(lines) > MAX_LINES:
        issues.append(f"{AGENTS}: {len(lines)} lines, limit {MAX_LINES}")

    headings = [(number, match.group(1)) for number, line in enumerate(lines, 1)
                if (match := HEADING.match(line))]
    names = [name for _, name in headings]
    unknown = [name for name in names if name not in SECTIONS]
    if unknown:
        issues.append(f"{AGENTS}: section outside {SECTIONS}: {', '.join(unknown)}")
    known = [name for name in names if name in SECTIONS]
    if known != sorted(known, key=SECTIONS.index):
        issues.append(f"{AGENTS}: sections out of order: {', '.join(known)}")

    values_at = next((number for number, name in headings if name == "Values"), None)
    if values_at is not None:
        body = lines[values_at:]
        body = body[: next((i for i, line in enumerate(body) if HEADING.match(line)), len(body))]
        values = [line for line in body if VALUE.match(line)]
        numbered = [int(VALUE.match(line).group(1)) for line in values]
        if len(values) > MAX_VALUES:
            issues.append(f"{AGENTS}: {len(values)} values, limit {MAX_VALUES}")
        if numbered != list(range(1, len(values) + 1)):
            issues.append(f"{AGENTS}: values are not numbered from 1 in order")
        for line in values:
            if not re.search(r"\bbeats?\b", line):
                issues.append(f"{AGENTS}: value does not name what it beats: {line[:60]}")
    return issues


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
    issues = check_agents() + check_index()
    for issue in issues:
        print(f"context shape: {issue}", file=sys.stderr)
    if issues:
        print(
            f"Keep {AGENTS} under {MAX_LINES} lines with the sections in {SECTIONS} order and\n"
            f"at most {MAX_VALUES} ranked values, and give every note and skill a line in {INDEX}.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
