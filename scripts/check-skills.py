#!/usr/bin/env python3
"""Mechanical skill-shape rules for `skills/` and `.agents/skills/`.

A global skill is self-contained, so its instructional links stay inside its own
directory; a vault-only skill may point at vault notes, which is what it is for.
Judgment rules (when a skill earns its place, whether a description is useful)
stay with the agent context skill. These are the parts a program can decide, so
AGENTS.md does not restate them.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION = re.compile(r"^description:\s*\S", re.MULTILINE)
FLAG = re.compile(r"^\s*(disable-model-invocation|policy\.allow_implicit_invocation)\s*:", re.MULTILINE)
LINK = re.compile(r"\]\(([^)\s]+)\)")
# The one skill Tobias invokes himself, so it is the one that keeps the flag.
TOBIAS_ONLY = Path(".agents/skills/chief-of-staff")


def skill_dirs() -> list[Path]:
    found = []
    for parent in (ROOT / "skills", ROOT / ".agents" / "skills"):
        if not parent.is_dir():
            continue
        found += sorted(p for p in parent.iterdir() if p.is_dir())
    return found


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[: end if end != -1 else len(text)]


def check() -> list[str]:
    issues = []
    for skill in skill_dirs():
        rel = skill.relative_to(ROOT)
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            issues.append(f"{rel}: no SKILL.md")
            continue

        text = skill_md.read_text()
        if not DESCRIPTION.search(frontmatter(text)):
            issues.append(f"{rel}: SKILL.md frontmatter has no description")

        global_skill = rel.parts[0] == "skills"
        for path in sorted(skill.rglob("*.md")):
            body = path.read_text()
            for match in LINK.finditer(body) if global_skill else ():
                target = match.group(1).split("#")[0]
                if not target or target.startswith(("http", "mailto:")):
                    continue
                resolved = (path.parent / target).resolve()
                if resolved.suffix == ".md" and not resolved.is_relative_to(skill.resolve()):
                    issues.append(
                        f"{path.relative_to(ROOT)}: link escapes the skill directory ({target})"
                    )
            if FLAG.search(body) and skill.relative_to(ROOT) != TOBIAS_ONLY:
                issues.append(
                    f"{path.relative_to(ROOT)}: invocation flag on a model-invoked skill"
                )

        if (skill / "SOURCE.md").is_file() and not (skill / "LICENSE").is_file():
            issues.append(f"{rel}: SOURCE.md without LICENSE")

    return issues


def main() -> int:
    issues = check()
    for issue in issues:
        print(f"skill: {issue}", file=sys.stderr)
    if issues:
        print(
            "Fix the shape: one description per SKILL.md, no invocation flags outside\n"
            f"{TOBIAS_ONLY}, instructional links inside the skill directory, and LICENSE\n"
            "beside SOURCE.md for adapted skills.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
