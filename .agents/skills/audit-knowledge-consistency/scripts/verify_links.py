#!/usr/bin/env python3
"""Verify internal links in a Markdown knowledge vault.

Checks Obsidian wikilinks, relative Markdown links, headings, and block references.
External URLs are counted but deliberately not fetched. Only visible Markdown
sources are scanned; explicit targets can be hidden files or directories. Fenced
or indented code, inline code, HTML comments, and Obsidian comments are excluded
from link extraction.
"""

from __future__ import annotations

import argparse
import bisect
import html
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULT_EXCLUDED_NAMES = {"node_modules", "__pycache__"}
SETEXT_UNDERLINE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
BLOCK_ID = re.compile(r"(?:^|[ \t])\^([A-Za-z0-9-]+)[ \t]*$")
REFERENCE_DEF = re.compile(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(.*)$", re.MULTILINE)
AUTOLINK = re.compile(r"(?<!\\)<((?:https?://|mailto:|obsidian:|file:|tel:|ftp:|//)[^>\n]+)>")


@dataclass
class HeadingIndex:
    names: set[str] = field(default_factory=set)
    slugs: set[str] = field(default_factory=set)
    blocks: dict[str, list[int]] = field(default_factory=dict)


@dataclass
class Note:
    path: Path
    relative: str
    text: str
    masked: str
    anchors: HeadingIndex


@dataclass
class Link:
    kind: str
    raw: str
    target: str
    offset: int


@dataclass
class Issue:
    code: str
    message: str
    source: str
    line: int
    column: int
    raw: str = ""
    target: str = ""
    candidates: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "source": self.source,
            "line": self.line,
            "column": self.column,
            "raw": self.raw,
            "target": self.target,
            "candidates": self.candidates,
        }


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, min(end, len(chars))):
        if chars[index] not in "\r\n":
            chars[index] = " "


def mask_ignored(text: str, *, mask_inline_code: bool = True) -> str:
    """Return same-length text with fenced code and comments replaced by spaces."""
    chars = list(text)
    offset = 0
    fence_char: str | None = None
    fence_length = 0
    in_indented_code = False
    previous_blank = True
    last_nonblank = ""

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        stripped = body.strip()
        if fence_char is not None:
            mask_range(chars, offset, offset + len(line))
            close = re.match(r"^ {0,3}([`~]+)[ \t]*$", body)
            if close and close.group(1)[0] == fence_char and len(close.group(1)) >= fence_length:
                fence_char = None
                fence_length = 0
            offset += len(line)
            previous_blank = not stripped
            if stripped:
                last_nonblank = body
            continue

        indent = re.match(r"^( +|\t+)", body)
        indent_width = 0
        if indent:
            indent_width = sum(4 if char == "\t" else 1 for char in indent.group(1))
        if in_indented_code:
            if not stripped or indent_width >= 4:
                mask_range(chars, offset, offset + len(line))
                offset += len(line)
                previous_blank = not stripped
                continue
            in_indented_code = False

        opener = re.match(r"^ {0,3}(`{3,}|~{3,})", body)
        if opener:
            run = opener.group(1)
            fence_char = run[0]
            fence_length = len(run)
            mask_range(chars, offset, offset + len(line))
        else:
            content = body.lstrip(" \t")
            nested_marker = bool(re.match(r"(?:[-+*>]|\d+[.)])(?:[ \t]+|$)", content))
            list_context = bool(re.match(r"^\s*(?:[-+*]|\d+[.)])(?:[ \t]+|$)", last_nonblank))
            if indent_width >= 4 and (previous_blank or offset == 0) and not nested_marker and not (list_context and indent_width <= 4):
                in_indented_code = True
                mask_range(chars, offset, offset + len(line))
        offset += len(line)
        previous_blank = not stripped
        if stripped:
            last_nonblank = body

    masked = "".join(chars)
    chars = list(masked)

    for pattern in (re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL), re.compile(r"%%.*?(?:%%|\Z)", re.DOTALL)):
        for match in pattern.finditer(masked):
            mask_range(chars, match.start(), match.end())

    masked = "".join(chars)
    if not mask_inline_code:
        return masked
    chars = list(masked)
    index = 0
    while index < len(masked):
        if masked[index] != "`" or is_escaped(masked, index):
            index += 1
            continue
        end_run = index
        while end_run < len(masked) and masked[end_run] == "`":
            end_run += 1
        delimiter = masked[index:end_run]
        close = masked.find(delimiter, end_run)
        if close == -1:
            index = end_run
            continue
        mask_range(chars, index, close + len(delimiter))
        index = close + len(delimiter)
    return "".join(chars)


def strip_heading_markup(value: str) -> str:
    value = re.sub(r"[ \t]+#+[ \t]*$", "", value.strip())
    value = re.sub(r"!?(?:\[([^\]]*)\])\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", value)
    value = re.sub(r"`+([^`]*)`+", r"\1", value)
    value = re.sub(r"[*_~]", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\\([\\`*{}\[\]()#+.!_>-])", r"\1", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def heading_slug(value: str) -> str:
    value = strip_heading_markup(value).casefold()
    value = "".join(ch for ch in value if ch.isalnum() or ch in " _-")
    return re.sub(r"[\s]+", "-", value).strip("-")


def build_anchor_index(masked: str) -> HeadingIndex:
    anchors = HeadingIndex()
    lines = masked.splitlines()
    for line_number, line in enumerate(lines, start=1):
        match = re.match(r"^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*$", line)
        if match:
            name = strip_heading_markup(match.group(1))
            if name:
                anchors.names.add(nfc(name).casefold())
                anchors.slugs.add(nfc(heading_slug(name)))
        if line_number > 1 and SETEXT_UNDERLINE.match(line):
            previous = lines[line_number - 2]
            looks_like_block = re.match(r"^\s*(?:[-+*>]|\d+[.)]\s)", previous)
            name = strip_heading_markup(previous)
            if name and not looks_like_block:
                anchors.names.add(nfc(name).casefold())
                anchors.slugs.add(nfc(heading_slug(name)))
        block = BLOCK_ID.search(line)
        if block:
            anchors.blocks.setdefault(block.group(1), []).append(line_number)
    return anchors


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_note(path: Path, root: Path) -> Note:
    text = path.read_text(encoding="utf-8")
    return Note(
        path,
        nfc(relative_posix(path, root)),
        text,
        mask_ignored(text),
        build_anchor_index(mask_ignored(text, mask_inline_code=False)),
    )


def path_is_excluded(relative: Path, extra: list[str]) -> bool:
    parts = relative.parts
    if any(part.startswith(".") or part in DEFAULT_EXCLUDED_NAMES for part in parts):
        return True
    rel = relative.as_posix().strip("/")
    for item in extra:
        normalized = item.strip("/")
        if not normalized:
            continue
        if "/" not in normalized and normalized in parts:
            return True
        if rel == normalized or rel.startswith(normalized + "/"):
            return True
    return False


def discover_files(root: Path, extra_excludes: list[str]) -> list[Path]:
    files: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept = []
        for directory in directories:
            candidate = current_path / directory
            if candidate.is_symlink():
                continue
            if path_is_excluded(candidate.relative_to(root), extra_excludes):
                continue
            kept.append(directory)
        directories[:] = kept
        for filename in filenames:
            candidate = current_path / filename
            if candidate.is_symlink() or path_is_excluded(candidate.relative_to(root), extra_excludes):
                continue
            files.append(candidate)
    return sorted(files)


def resolve_scopes(root: Path, scopes: list[str], visible_markdown: list[Path]) -> list[Path]:
    if not scopes:
        return visible_markdown
    allowed = set(visible_markdown)
    selected: set[Path] = set()
    for raw in scopes:
        candidate = (root / raw).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"scope escapes vault: {raw}") from exc
        if candidate.is_file():
            if candidate.suffix.lower() == ".md" and candidate in allowed:
                selected.add(candidate)
            continue
        if candidate.is_dir():
            selected.update(path for path in visible_markdown if candidate == path.parent or candidate in path.parents)
            continue
        raise ValueError(f"scope does not exist: {raw}")
    return sorted(selected)


def line_column(text: str, offset: int) -> tuple[int, int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer(r"\n", text))
    line_index = bisect.bisect_right(starts, offset) - 1
    return line_index + 1, offset - starts[line_index] + 1


def find_unescaped(text: str, needle: str, start: int) -> int:
    index = start
    while True:
        index = text.find(needle, index)
        if index == -1 or not is_escaped(text, index):
            return index
        index += len(needle)


def split_unescaped(value: str, delimiter: str) -> tuple[str, str | None]:
    for index, char in enumerate(value):
        if char == delimiter and not is_escaped(value, index):
            return value[:index], value[index + 1 :]
    return value, None


def unescape_target(value: str) -> str:
    return re.sub(r"\\([|#\\])", r"\1", value).strip()


def extract_wikilinks(original: str, masked: str) -> tuple[list[Link], list[tuple[int, int]]]:
    links: list[Link] = []
    spans: list[tuple[int, int]] = []
    index = 0
    while index < len(masked) - 1:
        embedded = masked.startswith("![[", index) and not is_escaped(masked, index)
        normal = masked.startswith("[[", index) and not is_escaped(masked, index)
        if not embedded and not normal:
            index += 1
            continue
        start = index
        content_start = index + (3 if embedded else 2)
        close = find_unescaped(masked, "]]", content_start)
        if close == -1:
            index += 1
            continue
        end = close + 2
        content = masked[content_start:close]
        destination, _alias = split_unescaped(content, "|")
        links.append(Link("wikilink", original[start:end], unescape_target(destination), start))
        spans.append((start, end))
        index = end
    return links, spans


def find_closing_bracket(text: str, start: int) -> int:
    depth = 1
    index = start
    while index < len(text):
        if is_escaped(text, index):
            index += 1
            continue
        if text[index] == "[":
            depth += 1
        elif text[index] == "]":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def parse_parenthesized_destination(text: str, open_paren: int) -> tuple[str, int] | None:
    index = open_paren + 1
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    if index >= len(text):
        return None
    if text[index] == "<":
        close = find_unescaped(text, ">", index + 1)
        if close == -1:
            return None
        cursor = close + 1
        while cursor < len(text) and text[cursor] in " \t\r\n":
            cursor += 1
        if cursor < len(text) and text[cursor] in "\"'(":
            opener = text[cursor]
            closer = ")" if opener == "(" else opener
            cursor += 1
            while cursor < len(text) and (text[cursor] != closer or is_escaped(text, cursor)):
                cursor += 1
            if cursor >= len(text):
                return None
            cursor += 1
            while cursor < len(text) and text[cursor] in " \t\r\n":
                cursor += 1
        if cursor >= len(text) or text[cursor] != ")":
            return None
        return text[index + 1 : close], cursor + 1

    destination_start = index
    depth = 0
    while index < len(text):
        char = text[index]
        if is_escaped(text, index):
            index += 1
        elif char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return text[destination_start:index].strip(), index + 1
            depth -= 1
        elif char in " \t\r\n" and depth == 0:
            destination = text[destination_start:index]
            cursor = index
            while cursor < len(text) and text[cursor] in " \t\r\n":
                cursor += 1
            if cursor < len(text) and text[cursor] in "\"'(":
                opener = text[cursor]
                closer = ")" if opener == "(" else opener
                cursor += 1
                while cursor < len(text) and (text[cursor] != closer or is_escaped(text, cursor)):
                    cursor += 1
                if cursor >= len(text):
                    return None
                cursor += 1
                while cursor < len(text) and text[cursor] in " \t\r\n":
                    cursor += 1
            if cursor < len(text) and text[cursor] == ")":
                return destination, cursor + 1
            return None
        index += 1
    return None


def parse_definition_destination(rest: str) -> str | None:
    value = rest.lstrip()
    if not value:
        return None
    if value.startswith("<"):
        close = find_unescaped(value, ">", 1)
        return value[1:close] if close != -1 else None
    result = []
    depth = 0
    for index, char in enumerate(value):
        if is_escaped(value, index):
            result.append(char)
        elif char == "(":
            depth += 1
            result.append(char)
        elif char == ")" and depth:
            depth -= 1
            result.append(char)
        elif char.isspace() and depth == 0:
            break
        else:
            result.append(char)
    return "".join(result) or None


def normalize_reference(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def markdown_unescape(value: str) -> str:
    return re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~ ])", r"\1", value)


def extract_markdown_links(original: str, masked: str, occupied: list[tuple[int, int]]) -> tuple[list[Link], int]:
    chars = list(masked)
    for start, end in occupied:
        mask_range(chars, start, end)
    working = "".join(chars)

    definitions: dict[str, tuple[str, int]] = {}
    definition_spans: list[tuple[int, int]] = []
    for match in REFERENCE_DEF.finditer(working):
        destination = parse_definition_destination(match.group(2))
        if destination:
            definitions.setdefault(normalize_reference(match.group(1)), (destination, match.start()))
        definition_spans.append((match.start(), match.end()))
    chars = list(working)
    for start, end in definition_spans:
        mask_range(chars, start, end)
    working = "".join(chars)

    links: list[Link] = []
    spans: list[tuple[int, int]] = []

    # Extract images first so an image nested inside a linked label is also checked.
    image_spans: dict[int, int] = {}
    image_index = 0
    while image_index < len(working) - 1:
        start = working.find("![", image_index)
        if start == -1:
            break
        if is_escaped(working, start):
            image_index = start + 2
            continue
        close = find_closing_bracket(working, start + 2)
        if close == -1:
            image_index = start + 2
            continue
        cursor = close + 1
        destination: str | None = None
        end = cursor
        if cursor < len(working) and working[cursor] == "(":
            parsed = parse_parenthesized_destination(working, cursor)
            if parsed:
                destination, end = parsed
        elif cursor < len(working) and working[cursor] == "[":
            ref_close = find_closing_bracket(working, cursor + 1)
            if ref_close != -1:
                label = working[start + 2 : close]
                reference = working[cursor + 1 : ref_close] or label
                entry = definitions.get(normalize_reference(reference))
                if entry:
                    destination = entry[0]
                    end = ref_close + 1
        if destination is not None:
            links.append(Link("markdown", original[start:end], destination.strip(), start))
            spans.append((start, end))
            image_spans[start] = end
            image_index = end
        else:
            image_index = close + 1

    index = 0
    while index < len(working):
        image = working.startswith("![", index) and not is_escaped(working, index)
        bracket = working[index] == "[" and not is_escaped(working, index)
        if not image and not bracket:
            index += 1
            continue
        if image and index in image_spans:
            index = image_spans[index]
            continue
        start = index
        open_bracket = index + 1 if image else index
        close = find_closing_bracket(working, open_bracket + 1)
        if close == -1:
            index += 1
            continue
        label = working[open_bracket + 1 : close]
        cursor = close + 1
        destination: str | None = None
        end = cursor
        if cursor < len(working) and working[cursor] == "(":
            parsed = parse_parenthesized_destination(working, cursor)
            if parsed:
                destination, end = parsed
        elif cursor < len(working) and working[cursor] == "[":
            ref_close = find_closing_bracket(working, cursor + 1)
            if ref_close != -1:
                reference = working[cursor + 1 : ref_close] or label
                entry = definitions.get(normalize_reference(reference))
                if entry:
                    destination = entry[0]
                    end = ref_close + 1
        else:
            entry = definitions.get(normalize_reference(label))
            if entry:
                destination = entry[0]
                end = cursor
        if destination is None:
            index = close + 1
            continue
        links.append(Link("markdown", original[start:end], destination.strip(), start))
        spans.append((start, end))
        index = max(end, close + 1)

    chars = list(working)
    for start, end in spans:
        mask_range(chars, start, end)
    remaining = "".join(chars)
    external_autolinks = len(AUTOLINK.findall(remaining))
    return links, external_autolinks


class Verifier:
    def __init__(self, root: Path, source_paths: list[Path], all_visible_files: list[Path]):
        self.root = root
        self.source_paths = source_paths
        self.all_visible_files = all_visible_files
        self.issues: list[Issue] = []
        self.counts = {
            "files": len(source_paths),
            "wikilinks": 0,
            "markdown_links": 0,
            "external_skipped": 0,
            "valid": 0,
            "missing": 0,
            "ambiguous": 0,
            "case_mismatch": 0,
            "scan_errors": 0,
        }
        self.notes: dict[str, Note] = {}
        self.unreadable_notes: set[str] = set()
        self.unreadable_stems: dict[str, list[str]] = {}
        self.path_casefold: dict[str, list[str]] = {}
        self.stems: dict[str, list[str]] = {}
        self.stems_casefold: dict[str, list[str]] = {}
        self.visible_paths = {nfc(relative_posix(path, root)): path for path in all_visible_files}
        self.visible_paths_casefold: dict[str, list[str]] = {}
        for relative in self.visible_paths:
            self.visible_paths_casefold.setdefault(relative.casefold(), []).append(relative)
        self._build_notes()

    def _build_notes(self) -> None:
        for path in (item for item in self.all_visible_files if item.suffix.lower() == ".md"):
            relative = nfc(relative_posix(path, self.root))
            try:
                note = read_note(path, self.root)
            except (OSError, UnicodeDecodeError) as exc:
                self.unreadable_notes.add(relative)
                self.unreadable_stems.setdefault(nfc(path.stem).casefold(), []).append(relative)
                if path in self.source_paths:
                    self._issue("scan-error", f"cannot read Markdown: {exc}", relative, 1, 1)
                continue
            self.notes[relative] = note
            without_suffix = relative[:-3]
            for key in (relative, without_suffix):
                self.path_casefold.setdefault(key.casefold(), []).append(relative)
            stem = nfc(path.stem)
            self.stems.setdefault(stem, []).append(relative)
            self.stems_casefold.setdefault(stem.casefold(), []).append(relative)

    def _issue(
        self,
        code: str,
        message: str,
        source: str,
        line: int,
        column: int,
        raw: str = "",
        target: str = "",
        candidates: list[str] | None = None,
    ) -> None:
        self.issues.append(Issue(code, message, source, line, column, raw, target, sorted(candidates or [])))
        if code.startswith("missing-") or code in {"outside-vault", "duplicate-block-id", "invalid-target", "unverifiable-target"}:
            self.counts["missing"] += 1
        elif code == "ambiguous-target":
            self.counts["ambiguous"] += 1
        elif code == "case-mismatch":
            self.counts["case_mismatch"] += 1
        elif code == "scan-error":
            self.counts["scan_errors"] += 1

    def _resolve_wiki_note(self, source: Note, raw_target: str) -> tuple[Note | None, str | None, list[str]]:
        try:
            target = nfc(unquote(raw_target.strip())).replace("\\", "/")
        except (UnicodeError, ValueError):
            return None, "invalid", []
        if "\x00" in target:
            return None, "invalid", []
        if not target:
            return source, None, []
        explicit_path = "/" in target or target.startswith(".") or target.endswith(".md")
        if explicit_path:
            base = source.path.parent if target.startswith("./") or target.startswith("../") else self.root
            try:
                candidate_path = (base / target.lstrip("/")).resolve()
                relative = nfc(candidate_path.relative_to(self.root).as_posix())
            except (OSError, RuntimeError, ValueError):
                try:
                    candidate_path.relative_to(self.root)
                except (UnboundLocalError, ValueError):
                    return None, "outside", []
                return None, "invalid", []
            if not relative.endswith(".md"):
                relative += ".md"
            if relative in self.notes:
                return self.notes[relative], None, []
            if relative in self.unreadable_notes:
                return None, "unreadable", [relative]
            matches = self.path_casefold.get(relative.casefold(), [])
            if len(matches) == 1:
                return self.notes[matches[0]], "case", matches
            if len(matches) > 1:
                return None, "ambiguous", matches
            return None, "missing", []

        stem = target[:-3] if target.endswith(".md") else target
        matches = self.stems.get(stem, [])
        if len(matches) == 1:
            return self.notes[matches[0]], None, []
        if len(matches) > 1:
            return None, "ambiguous", matches
        folded = self.stems_casefold.get(stem.casefold(), [])
        if len(folded) == 1:
            return self.notes[folded[0]], "case", folded
        if len(folded) > 1:
            return None, "ambiguous", folded
        unreadable = self.unreadable_stems.get(stem.casefold(), [])
        if len(unreadable) == 1:
            return None, "unreadable", unreadable
        if len(unreadable) > 1:
            return None, "ambiguous", unreadable
        return None, "missing", []

    def _check_anchor(self, source: Note, target_note: Note, fragment: str, link: Link) -> None:
        line, column = line_column(source.text, link.offset)
        decoded = nfc(unquote(fragment)).strip()
        if not decoded:
            return
        if decoded.startswith("^"):
            block_id = decoded[1:]
            lines = target_note.anchors.blocks.get(block_id, [])
            if not lines:
                self._issue("missing-block", f"block ^{block_id} does not exist in {target_note.relative}", source.relative, line, column, link.raw, link.target)
            elif len(lines) > 1:
                self._issue("ambiguous-target", f"block ^{block_id} occurs more than once in {target_note.relative}", source.relative, line, column, link.raw, link.target, [f"{target_note.relative}:{item}" for item in lines])
            else:
                self.counts["valid"] += 1
            return
        plain = strip_heading_markup(decoded)
        if nfc(plain).casefold() in target_note.anchors.names or nfc(decoded).casefold() in target_note.anchors.names or nfc(decoded).casefold() in target_note.anchors.slugs or nfc(heading_slug(decoded)) in target_note.anchors.slugs:
            self.counts["valid"] += 1
            return
        self._issue("missing-heading", f"heading '{decoded}' does not exist in {target_note.relative}", source.relative, line, column, link.raw, link.target)

    def _verify_wikilink(self, source: Note, link: Link) -> None:
        self.counts["wikilinks"] += 1
        note_part, fragment = split_unescaped(link.target, "#")
        note, status, candidates = self._resolve_wiki_note(source, unescape_target(note_part))
        line, column = line_column(source.text, link.offset)
        if status == "outside":
            self._issue("outside-vault", "wikilink target escapes the vault", source.relative, line, column, link.raw, link.target)
            return
        if status == "invalid":
            self._issue("invalid-target", "wikilink target is malformed", source.relative, line, column, link.raw, link.target)
            return
        if status == "case":
            self._issue("case-mismatch", f"target case differs from {candidates[0]}", source.relative, line, column, link.raw, link.target, candidates)
            return
        if status == "ambiguous":
            self._issue("ambiguous-target", "wikilink basename resolves to multiple notes", source.relative, line, column, link.raw, link.target, candidates)
            return
        if status == "unreadable":
            self._issue("unverifiable-target", "wikilink target exists but cannot be read", source.relative, line, column, link.raw, link.target, candidates)
            return
        if status == "missing" or note is None:
            self._issue("missing-note", "wikilink target does not exist", source.relative, line, column, link.raw, link.target)
            return
        if fragment is not None:
            self._check_anchor(source, note, fragment, link)
        else:
            self.counts["valid"] += 1

    def _resolve_markdown_path(self, source: Note, destination: str) -> tuple[Path | None, str | None, list[str], str]:
        destination = markdown_unescape(destination)
        try:
            parsed = urlsplit(destination)
        except ValueError:
            return None, "invalid", [], ""
        if parsed.scheme or destination.startswith("//"):
            return None, "external", [], parsed.fragment
        try:
            raw_path = unquote(parsed.path)
        except (UnicodeError, ValueError):
            return None, "invalid", [], ""
        if "\x00" in raw_path:
            return None, "invalid", [], unquote(parsed.fragment)
        if not raw_path:
            return source.path, None, [], unquote(parsed.fragment)
        try:
            candidate = (self.root / raw_path.lstrip("/")) if raw_path.startswith("/") else (source.path.parent / raw_path)
            candidate = candidate.resolve()
            relative = nfc(candidate.relative_to(self.root).as_posix())
        except (OSError, RuntimeError, ValueError):
            try:
                candidate.relative_to(self.root)
            except (UnboundLocalError, ValueError):
                return None, "outside", [], unquote(parsed.fragment)
            return None, "invalid", [], unquote(parsed.fragment)
        alternatives = [relative]
        if not Path(relative).suffix:
            alternatives.append(relative + ".md")
        for item in alternatives:
            path = self.visible_paths.get(item, self.root / item)
            if path.is_file() or path.is_dir():
                path = path.resolve()
                if not path.is_relative_to(self.root):
                    return None, "outside", [], unquote(parsed.fragment)
                return path, None, [], unquote(parsed.fragment)
        matches: list[str] = []
        for item in alternatives:
            matches.extend(self.visible_paths_casefold.get(item.casefold(), []))
        matches = sorted(set(matches))
        if len(matches) == 1:
            return self.visible_paths[matches[0]], "case", matches, unquote(parsed.fragment)
        if len(matches) > 1:
            return None, "ambiguous", matches, unquote(parsed.fragment)
        return None, "missing", [], unquote(parsed.fragment)

    def _verify_markdown(self, source: Note, link: Link) -> None:
        self.counts["markdown_links"] += 1
        path, status, candidates, fragment = self._resolve_markdown_path(source, link.target)
        line, column = line_column(source.text, link.offset)
        if status == "external":
            self.counts["external_skipped"] += 1
            return
        if status == "invalid":
            self._issue("invalid-target", "Markdown link target is malformed", source.relative, line, column, link.raw, link.target)
            return
        if status == "outside":
            self._issue("outside-vault", "Markdown link target escapes the vault", source.relative, line, column, link.raw, link.target)
            return
        if status == "case":
            self._issue("case-mismatch", f"target case differs from {candidates[0]}", source.relative, line, column, link.raw, link.target, candidates)
            return
        if status == "ambiguous":
            self._issue("ambiguous-target", "Markdown link resolves to multiple files", source.relative, line, column, link.raw, link.target, candidates)
            return
        if status == "missing" or path is None:
            self._issue("missing-file", "Markdown link target does not exist", source.relative, line, column, link.raw, link.target)
            return
        if fragment and path.is_file() and path.suffix.lower() == ".md":
            target = self.notes.get(nfc(relative_posix(path, self.root)))
            if target is None:
                try:
                    target = read_note(path, self.root)
                except (OSError, UnicodeDecodeError) as exc:
                    self._issue("unverifiable-target", f"Markdown target exists but cannot be read: {exc}", source.relative, line, column, link.raw, link.target)
                    return
            self._check_anchor(source, target, fragment, link)
            return
        self.counts["valid"] += 1

    def run(self) -> dict:
        for path in self.source_paths:
            relative = nfc(relative_posix(path, self.root))
            note = self.notes.get(relative)
            if note is None:
                continue
            for block_id, lines in note.anchors.blocks.items():
                if len(lines) > 1:
                    self._issue("duplicate-block-id", f"block ^{block_id} occurs more than once", relative, lines[1], 1, target=block_id, candidates=[f"{relative}:{item}" for item in lines])
            wikilinks, occupied = extract_wikilinks(note.text, note.masked)
            markdown_links, autolinks = extract_markdown_links(note.text, note.masked, occupied)
            self.counts["external_skipped"] += autolinks
            for link in wikilinks:
                self._verify_wikilink(note, link)
            for link in markdown_links:
                self._verify_markdown(note, link)

        self.issues.sort(key=lambda item: (item.source.casefold(), item.line, item.column, item.code, item.target))
        return {
            "schema_version": 1,
            "vault": str(self.root),
            "counts": {**self.counts, "issues": len(self.issues)},
            "issues": [issue.as_dict() for issue in self.issues],
        }


def find_vault_root(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file():
            return candidate
    return None


def render_human(report: dict) -> None:
    counts = report["counts"]
    for issue in report["issues"]:
        location = f"{issue['source']}:{issue['line']}:{issue['column']}"
        print(f"[{issue['code']}] {location} {issue['message']}")
        if issue["raw"]:
            print(f"  {issue['raw']}")
        if issue["candidates"]:
            print("  candidates: " + ", ".join(issue["candidates"]))
    print(
        f"\n{counts['files']} file(s), {counts['wikilinks']} wikilink(s), "
        f"{counts['markdown_links']} Markdown link(s), {counts['external_skipped']} external skipped, "
        f"{counts['issues']} issue(s)"
    )
    if not report["issues"]:
        print("All internal links resolve.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify internal Markdown and Obsidian links")
    parser.add_argument("--vault", help="vault root; defaults to nearest ancestor containing AGENTS.md")
    parser.add_argument("--scope", action="append", default=[], help="relative file or directory to scan; repeatable")
    parser.add_argument("--exclude", action="append", default=[], help="additional relative path or directory name to exclude")
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

    all_files = discover_files(root, args.exclude)
    markdown = [path for path in all_files if path.suffix.lower() == ".md"]
    try:
        sources = resolve_scopes(root, args.scope, markdown)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not sources:
        print("error: scope contains no visible Markdown files", file=sys.stderr)
        return 2

    report = Verifier(root, sources, all_files).run()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        render_human(report)
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
