#!/usr/bin/env python3
"""No file may copy another file's prose. One owner per fact, others link.

Verbatim reuse is the decidable part of duplicate authority: thirteen identical
consecutive words is a copied passage, and the copies drift. Shorter overlaps are
usually the same policy named twice, or ordinary vocabulary, and need the per-line
question in `.agents/skills/audit-knowledge-consistency/SKILL.md`.

Attribution notices (`skills/*/SOURCE.md`) and the index's one-line note
summaries quote by design, so they are exempt.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW = 6
MINIMUM_WORDS = 13
EXEMPT = re.compile(r"^(index\.md|.*/SOURCE\.md)$")
WORD = re.compile(r"[a-z0-9][a-z0-9._/-]*")


def tracked_markdown() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", "*.md"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    return [Path(p) for p in out.decode().split("\0") if p and not EXEMPT.match(p)]


class Note:
    def __init__(self, path: Path) -> None:
        self.path = path
        text = path.read_text(encoding="utf-8")
        self.words: list[str] = []
        self.lines: list[int] = []
        for number, line in enumerate(text.splitlines(), start=1):
            for word in WORD.findall(line.lower()):
                self.words.append(word)
                self.lines.append(number)
        self.shingles: dict[tuple[str, ...], list[int]] = defaultdict(list)
        for start in range(len(self.words) - WINDOW + 1):
            self.shingles[tuple(self.words[start : start + WINDOW])].append(start)

    def line(self, word: int) -> int:
        return self.lines[word]


def passages(a: Note, b: Note) -> list[tuple[int, int, int]]:
    """Maximal runs of identical words, as (words, start in a, start in b)."""
    shared = a.shingles.keys() & b.shingles.keys()
    if not shared:
        return []
    diagonals: dict[int, list[int]] = defaultdict(list)
    for shingle in shared:
        for start in a.shingles[shingle]:
            for other in b.shingles[shingle]:
                diagonals[start - other].append(start)
    found = []
    for starts in diagonals.values():
        starts.sort()
        run_start = previous = starts[0]
        for start in starts[1:] + [None]:
            if start is not None and start == previous + 1:
                previous = start
                continue
            words = previous - run_start + WINDOW
            if words >= MINIMUM_WORDS:
                found.append((words, run_start, run_start - (previous - run_start + WINDOW - 1)))
            if start is not None:
                run_start = previous = start
    found.sort(reverse=True)
    kept: list[tuple[int, int, int]] = []
    for words, start, _ in found:
        if all(abs(start - kept_start) >= kept_words for kept_words, kept_start, _ in kept):
            kept.append((words, start, 0))
    return kept


def main() -> int:
    notes = [Note(path) for path in tracked_markdown()]
    issues = []
    for index, first in enumerate(notes):
        for second in notes[index + 1 :]:
            for words, start, _ in passages(first, second):
                text = " ".join(first.words[start : start + words])
                issues.append(
                    f"{first.path}:{first.line(start)} ↔ {second.path}: "
                    f"{words} identical words: \"{text}\""
                )

    if issues:
        for issue in issues:
            print(f"duplicate authority: {issue}", file=sys.stderr)
        print(
            "One owner per fact. Keep the fact in the file that is open when it is\n"
            "needed and let the other name the idea with a link, or delete the copy.\n"
            "Rules: .agents/skills/audit-knowledge-consistency/SKILL.md",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
