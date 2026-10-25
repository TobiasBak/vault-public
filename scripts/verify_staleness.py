#!/usr/bin/env python3
"""Report vault notes whose dated facts are due for a recheck.

A note carrying a `recheck-after` line holds facts that decay: prices, model
catalogs, host behavior, vendor terms. The line states when that note is due to
be re-derived rather than followed. An expired note is guidance asking to be
rechecked, not an error: expiry exits 0 and is reported only.

A marker that is malformed, duplicated, or missing its date does exit non-zero,
because then the expiry is silently switched off and nobody notices.

The marker is a line whose content begins with `recheck-after:` and a
YYYY-MM-DD date. Mentioning the marker mid-sentence or inside code does not
count, so prose about the convention is safe. Scanned files come from
`verify_links.discover_files`, so both checks cover the same surface.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from verify_links import discover_files, find_vault_root, relative_posix

MARKER = re.compile(r"^[ \t]*recheck-after:[ \t]*(.*?)[ \t]*$", re.MULTILINE)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Marker:
    source: str
    line: int
    value: str
    parsed: date | None


def read_markers(path: Path, root: Path) -> tuple[list[Marker], str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [], str(exc)
    markers: list[Marker] = []
    for match in MARKER.finditer(text):
        value = match.group(1)
        line = text.count("\n", 0, match.start()) + 1
        parsed = date.fromisoformat(value) if ISO_DATE.match(value) else None
        markers.append(Marker(relative_posix(path, root), line, value, parsed))
    return markers, None


def scan(root: Path, as_of: date) -> dict:
    expired: list[dict] = []
    malformed: list[dict] = []
    marked = 0
    upcoming: date | None = None
    for path in discover_files(root, []):
        if path.suffix.lower() != ".md":
            continue
        markers, error = read_markers(path, root)
        if error is not None:
            malformed.append({"source": relative_posix(path, root), "line": 1, "reason": f"cannot read note: {error}"})
            continue
        if len(markers) > 1:
            for marker in markers[1:]:
                malformed.append({"source": marker.source, "line": marker.line, "reason": "note carries more than one recheck-after line"})
        if not markers:
            continue
        marker = markers[0]
        if marker.parsed is None:
            malformed.append({"source": marker.source, "line": marker.line, "reason": f"not a YYYY-MM-DD date: {marker.value!r}"})
            continue
        marked += 1
        if marker.parsed < as_of:
            expired.append(
                {
                    "source": marker.source,
                    "line": marker.line,
                    "recheck_after": marker.parsed.isoformat(),
                    "days_overdue": (as_of - marker.parsed).days,
                }
            )
        elif upcoming is None or marker.parsed < upcoming:
            upcoming = marker.parsed
    expired.sort(key=lambda item: (item["recheck_after"], item["source"]))
    malformed.sort(key=lambda item: (item["source"], item["line"]))
    return {
        "schema_version": 1,
        "vault": str(root),
        "as_of": as_of.isoformat(),
        "counts": {
            "marked": marked,
            "expired": len(expired),
            "malformed": len(malformed),
            "next_due": upcoming.isoformat() if upcoming else None,
        },
        "expired": expired,
        "malformed": malformed,
    }


def render_human(report: dict) -> None:
    for item in report["malformed"]:
        print(f"[malformed] {item['source']}:{item['line']} {item['reason']}")
    for item in report["expired"]:
        print(f"[recheck] {item['source']}:{item['line']} due {item['recheck_after']}, {item['days_overdue']} day(s) ago")
    counts = report["counts"]
    print(f"\n{counts['marked']} note(s) carry an expiry, {counts['expired']} due for recheck, {counts['malformed']} malformed")
    if counts["expired"]:
        print("Re-derive those facts before relying on them; update the date or the claim.")
    elif counts["next_due"]:
        print(f"Next due {counts['next_due']}.")
    else:
        print("No dated facts are due for recheck.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report notes due for a fact recheck")
    parser.add_argument("--vault", help="vault root; defaults to nearest ancestor containing AGENTS.md")
    parser.add_argument("--as-of", help="treat this YYYY-MM-DD as today; defaults to the current date")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    args = parser.parse_args(argv)

    if args.vault:
        root = Path(args.vault).expanduser().resolve()
    else:
        found = find_vault_root(Path.cwd())
        if found is None:
            print("error: no ancestor containing AGENTS.md; pass --vault", file=sys.stderr)
            return 2
        root = found
    if not root.is_dir() or not (root / "AGENTS.md").is_file():
        print(f"error: invalid vault root: {root}", file=sys.stderr)
        return 2
    try:
        as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    except ValueError:
        print(f"error: --as-of is not a YYYY-MM-DD date: {args.as_of}", file=sys.stderr)
        return 2

    report = scan(root, as_of)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        render_human(report)
    return 1 if report["malformed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
