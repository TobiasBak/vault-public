#!/usr/bin/env python3
from __future__ import annotations

import ast
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HASH_SUFFIXES = {".sh", ".yaml", ".yml", ".toml"}
HASH_NAMES = {".gitignore", ".gitattributes"}
COMMENT_FREE_SUFFIXES = {".json"}
COMMENT_FREE_NAMES = {"LICENSE"}
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
HASH_COMMENT = re.compile(r"(?:^|\s)#")


def tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [Path(p) for p in out.decode().split("\0") if p]


def python_comments(text: str) -> list[int]:
    found = [
        token.start[0]
        for token in tokenize.generate_tokens(io.StringIO(text).readline)
        if token.type == tokenize.COMMENT and not (token.start[0] == 1 and token.string.startswith("#!"))
    ]
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node, clean=False) is not None:
                found.append(node.body[0].lineno)
    return found


def hash_comments(text: str) -> list[int]:
    return [
        number
        for number, line in enumerate(text.splitlines(), start=1)
        if not (number == 1 and line.startswith("#!")) and HASH_COMMENT.search(QUOTED.sub("", line))
    ]


def markup_comments(text: str, scripted: bool) -> list[int]:
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        if "<!--" in line or (scripted and ("/*" in line or line.lstrip().startswith("//"))):
            found.append(number)
    return found


def is_shell(path: Path) -> bool:
    with open(ROOT / path, "rb") as file:
        first = file.readline()
    return first.startswith(b"#!") and re.search(rb"\b(ba|z)?sh\b", first) is not None


def scan(path: Path) -> list[int] | None:
    text = lambda: (ROOT / path).read_text(encoding="utf-8")
    if path.suffix == ".py":
        return python_comments(text())
    if path.suffix in HASH_SUFFIXES or path.name in HASH_NAMES or (not path.suffix and is_shell(path)):
        return hash_comments(text())
    if path.suffix == ".md":
        return markup_comments(text(), scripted=False)
    if path.suffix == ".html":
        return markup_comments(text(), scripted=True)
    if path.suffix in COMMENT_FREE_SUFFIXES or path.name in COMMENT_FREE_NAMES:
        return []
    return None


def main() -> int:
    issues = []
    for path in tracked():
        if (ROOT / path).is_symlink():
            continue
        lines = scan(path)
        if lines is None:
            issues.append(f"{path}: no comment scanner for this format; add one to scripts/check-comments.py")
            continue
        issues += [f"{path}:{line}: comment" for line in sorted(set(lines))]
    for issue in issues:
        print(f"zero-comments: {issue}", file=sys.stderr)
    if issues:
        print(
            "Tracked files carry no comments or docstrings. Say it with a name, a check's failure\n"
            "message or CLI help, or put the reason in the note that owns it.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
