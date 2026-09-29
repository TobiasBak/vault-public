#!/usr/bin/env python3
"""Safely scan Pi and Codex histories into reviewable, redacted run files.

The helper never edits source histories. It writes only under the vault's ignored
.knowledge-bank/state directory. File mtime is intentionally used for selection:
resumed sessions update their mtime, so they are reconsidered and older turns from
a touched session may appear.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

UTC = timezone.utc
DEFAULT_DAYS = 7
REVIEW_BATCH_SIZE = 10
PRIVACY_WARNING = "Deterministic redaction is incomplete; inspect every extracted candidate for secrets."
SOURCES = ("pi", "codex")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def now() -> datetime:
    return datetime.now(UTC)


def iso(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def atomic_write(path: Path, content: str) -> None:
    """Write content in the destination directory, then atomically replace path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def redact(text: str) -> tuple[str, list[str]]:
    """Redact common credentials; this deterministic set is deliberately conservative."""
    warnings: list[str] = []
    patterns = [
        (r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", "[REDACTED PRIVATE KEY]", re.S),
        (r"(?i)\b(?:ghp|github_pat)_[A-Za-z0-9_\-]{12,}\b", "[REDACTED TOKEN]", 0),
        (r"(?i)\bxox[baprs]-[A-Za-z0-9-]{12,}\b", "[REDACTED TOKEN]", 0),
        (r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}", "Bearer [REDACTED TOKEN]", 0),
        (r"\bAKIA[0-9A-Z]{16}\b", "[REDACTED AWS ACCESS KEY]", 0),
        (r"\b(?:sk|pk|rk|api)[_-]?[a-z0-9]{16,}\b", "[REDACTED TOKEN]", re.I),
        (r"(?im)\b(password|passwd|secret|token|api[_ -]?key)\s*[:=]\s*([^\s,;]+)", r"\1=[REDACTED]", 0),
    ]
    result = text
    changed = False
    for pattern, replacement, flags in patterns:
        result, count = re.subn(pattern, replacement, result, flags=flags)
        changed |= count > 0
    if changed:
        warnings.append("Common credential redaction was applied; deterministic redaction is not complete.")
    return result, warnings


def text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                kind = str(item.get("type", "")).lower()
                if kind in {"text", "input_text", "output_text", "message"}:
                    value = item.get("text", item.get("content", ""))
                    if isinstance(value, str):
                        parts.append(value)
        return "\n".join(parts)
    if isinstance(content, dict):
        return text_from_content(content.get("text", content.get("content", "")))
    return ""


def _message_object(record: dict[str, Any]) -> dict[str, Any]:
    message = record.get("message")
    if isinstance(message, dict):
        return message
    payload = record.get("payload")
    if isinstance(payload, dict) and payload.get("type") in {"message", "user_message", "assistant_message"}:
        return payload
    return record


def conversational(role: Any, record: dict[str, Any]) -> bool:
    message = _message_object(record)
    role = str(role or message.get("role", "")).lower()
    return role in {"user", "assistant"}


def record_text(record: dict[str, Any]) -> str:
    message = _message_object(record)
    return text_from_content(message.get("content", message.get("text", ""))).strip()


def _time_from(record: dict[str, Any]) -> str | None:
    for key in ("timestamp", "created_at", "createdAt", "time", "ts"):
        value = record.get(key)
        if isinstance(value, (int, float)):
            return iso(datetime.fromtimestamp(value / (1000 if value > 10**11 else 1), UTC))
        if isinstance(value, str):
            try:
                return iso(parse_time(value) or now())
            except ValueError:
                pass
    message = record.get("message")
    if isinstance(message, dict):
        return _time_from(message)
    return None


def parse_jsonl_diagnostics(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    records.append(item)
                else:
                    errors.append({"file": str(path.resolve()), "line": line_number, "error": "JSONL record is not an object"})
            except json.JSONDecodeError as exc:
                errors.append({"file": str(path.resolve()), "line": line_number, "error": f"malformed JSON: {exc.msg}"})
    return records, errors


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    """Compatibility parser; callers needing integrity diagnostics use the detailed form."""
    return parse_jsonl_diagnostics(path)[0]


def _parse_pi_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, str]], list[str]]:
    warnings: list[str] = []
    nodes: dict[str, dict[str, Any]] = {}
    ordered: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        node_id = record.get("id") or record.get("messageId") or record.get("uuid")
        parent = record.get("parentId") or record.get("parent_id")
        if node_id:
            nodes[str(node_id)] = {"record": record, "parent": str(parent) if parent else None, "index": index}
        ordered.append(record)
    selected = ordered
    if nodes and any(item["parent"] for item in nodes.values()):
        child_ids = {item["parent"] for item in nodes.values() if item["parent"] in nodes}
        leaves = [item for key, item in nodes.items() if key not in child_ids]
        if leaves:
            leaf = max(leaves, key=lambda item: (item.get("record", {}).get("timestamp", ""), item["index"]))
            chain = []
            current = leaf
            seen: set[str] = set()
            while current and id(current) not in seen:
                seen.add(id(current))
                chain.append(current["record"])
                parent = current["parent"]
                current = nodes.get(parent) if parent else None
            selected = list(reversed(chain))
    output: list[dict[str, str]] = []
    for record in selected:
        message = _message_object(record)
        role = record.get("role") or message.get("role")
        if conversational(role, record):
            text = record_text(record)
            if text:
                clean, redaction_warnings = redact(text)
                warnings.extend(redaction_warnings)
                output.append({"role": str(role).lower(), "text": clean, "timestamp": _time_from(record) or ""})
    return output, sorted(set(warnings))


def pi_is_child(records: Iterable[dict[str, Any]]) -> bool:
    """Recognize Pi's standard child session header as well as nested run paths."""
    for record in records:
        candidates: list[dict[str, Any]] = [record]
        payload = record.get("payload")
        if isinstance(payload, dict):
            candidates.append(payload)
        for candidate in candidates:
            parent = candidate.get("parentSession") or candidate.get("parent_session")
            if parent:
                return True
    return False


def parse_pi(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    records = parse_jsonl(path)
    return _parse_pi_records(records)


def codex_is_child(records: Iterable[dict[str, Any]]) -> bool:
    for record in records:
        payload = record.get("payload")
        candidates = [record]
        if isinstance(payload, dict):
            candidates.append(payload)
        for metadata in candidates:
            if str(metadata.get("thread_source", "")).lower() == "subagent":
                return True
    return False


def _parse_codex_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, str]], list[str], bool]:
    warnings: list[str] = []
    child = codex_is_child(records)
    output: list[dict[str, str]] = []
    for record in records:
        message = _message_object(record)
        role = record.get("role") or message.get("role")
        if record.get("payload") and not (isinstance(record.get("payload"), dict) and record["payload"].get("type") in {"message", "user_message", "assistant_message"}):
            continue
        if conversational(role, record):
            text = record_text(record)
            if text:
                clean, redaction_warnings = redact(text)
                warnings.extend(redaction_warnings)
                output.append({"role": str(role).lower(), "text": clean, "timestamp": _time_from(record) or ""})
    return output, sorted(set(warnings)), child


def parse_codex(path: Path) -> tuple[list[dict[str, str]], list[str], bool]:
    records = parse_jsonl(path)
    return _parse_codex_records(records)


def session_metadata_records(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Extract stable identity and cwd from the first session header, if present."""
    for record in list(records)[:8]:
        payload = record.get("payload")
        candidate = payload if isinstance(payload, dict) else record
        outer_kind = str(record.get("type", "")).lower()
        kind = str(candidate.get("type", "")).lower()
        if outer_kind in {"session_meta", "session_metadata"} or kind in {"session_meta", "session_metadata", "session"} or "session_id" in candidate:
            return {
                "session_id": candidate.get("id") or candidate.get("session_id") or candidate.get("sessionId"),
                "cwd": candidate.get("cwd") or candidate.get("working_directory"),
                "started_at": candidate.get("timestamp") or candidate.get("started_at") or candidate.get("created_at") or record.get("timestamp"),
                "thread_source": candidate.get("thread_source"),
                "parentSession": candidate.get("parentSession") or candidate.get("parent_session"),
            }
    return {}


def session_metadata(path: Path) -> dict[str, Any]:
    """Read only session header metadata, if present, for stable identity and cwd."""
    return session_metadata_records(parse_jsonl(path))


def discover(root: Path, source: str, include_children: bool = False) -> tuple[list[Path], list[Path]]:
    """Return readable JSONL paths and unsupported compressed JSONL paths."""
    if not root.exists():
        return [], []
    paths: list[Path] = []
    unsupported: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(path.name.endswith(f".jsonl{suffix}") for suffix in (".zst", ".gz", ".bz2", ".xz")):
            unsupported.append(path)
        elif path.suffix == ".jsonl":
            if source == "pi" and not include_children and re.search(r"(?:^|/)run-\d+/session\.jsonl$", path.as_posix()):
                continue
            paths.append(path)
    return sorted(paths), sorted(unsupported)


def roots(args: argparse.Namespace) -> tuple[list[Path], list[Path]]:
    if args.pi_root:
        pi = [Path(args.pi_root).expanduser()]
    elif os.environ.get("PI_CODING_AGENT_SESSION_DIR"):
        pi = [Path(os.environ["PI_CODING_AGENT_SESSION_DIR"]).expanduser()]
    elif os.environ.get("PI_CODING_AGENT_DIR"):
        pi = [Path(os.environ["PI_CODING_AGENT_DIR"]).expanduser() / "sessions"]
    else:
        pi = [Path.home() / ".pi" / "agent" / "sessions"]
    codex_home = Path(args.codex_root).expanduser() if args.codex_root else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    codex = [codex_home / "sessions", codex_home / "archived_sessions"]
    return pi, codex


def _search_roots(args: argparse.Namespace) -> list[tuple[str, Path]]:
    selected = {args.source} if args.source != "all" else set(SOURCES)
    pi_roots, codex_roots = roots(args)
    result: list[tuple[str, Path]] = []
    for source, candidates in (("pi", pi_roots), ("codex", codex_roots)):
        if source in selected:
            result.extend((source, path) for path in candidates if path.is_dir())
    return result


def _prefilter_history_paths(query: str, search_roots: list[tuple[str, Path]]) -> list[tuple[str, Path]]:
    """Use ripgrep to avoid parsing every history file for a narrow recall."""
    output: list[tuple[str, Path]] = []
    for source, root in search_roots:
        completed = subprocess.run(
            ["rg", "--files-with-matches", "--fixed-strings", "--ignore-case", "--null", "--", query, str(root)],
            capture_output=True,
            check=False,
        )
        if completed.returncode not in {0, 1}:
            detail = completed.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"ripgrep failed for {root}: {detail or f'exit {completed.returncode}'}")
        for raw_path in completed.stdout.split(b"\0"):
            if not raw_path:
                continue
            path = Path(os.fsdecode(raw_path))
            if path.suffix == ".jsonl" and path.is_file():
                output.append((source, path))
    return sorted(set(output), key=lambda item: (item[0], str(item[1])))


def _excerpt(text: str, query: str, max_chars: int) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    folded = text.casefold()
    match = folded.find(query.casefold())
    start = max(0, match - max_chars // 3) if match >= 0 else 0
    end = min(len(text), start + max_chars)
    start = max(0, end - max_chars)
    excerpt = text[start:end]
    if start > 0 and excerpt:
        excerpt = "…" + excerpt[1:]
    if end < len(text) and excerpt:
        excerpt = excerpt[:-1] + "…"
    return excerpt, True


def search(args: argparse.Namespace) -> int:
    query = args.query.strip()
    if not query:
        print("search requires a non-empty --query", file=sys.stderr)
        return 2
    if args.limit <= 0 or args.excerpt_chars <= 0:
        print("--limit and --excerpt-chars must be positive", file=sys.stderr)
        return 2
    lower = parse_time(args.since) if args.since else None
    upper = parse_time(args.until) if args.until else None
    if lower and upper and lower > upper:
        print("--since must not be later than --until", file=sys.stderr)
        return 2
    available = _search_roots(args)
    requested_sources = {args.source} if args.source != "all" else set(SOURCES)
    available_sources = {source for source, _ in available}
    warnings = [PRIVACY_WARNING]
    for source in sorted(requested_sources - available_sources):
        warnings.append(f"No available {source} history root was searched.")
    try:
        candidates = _prefilter_history_paths(query, available)
    except (OSError, RuntimeError) as exc:
        print(f"search failed: {exc}", file=sys.stderr)
        return 1
    matches: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    files_inspected = 0
    for source, path in candidates:
        modified = datetime.fromtimestamp(path.stat().st_mtime, UTC)
        if (lower and modified < lower) or (upper and modified > upper):
            continue
        records, parse_errors = parse_jsonl_diagnostics(path)
        errors.extend(parse_errors)
        metadata = session_metadata(path)
        if source == "pi":
            messages, parse_warnings = _parse_pi_records(records)
            child = pi_is_child(records) or bool(re.search(r"(?:^|/)run-\d+/session\.jsonl$", path.as_posix()))
        else:
            messages, parse_warnings, child = _parse_codex_records(records)
            child = child or str(metadata.get("thread_source", "")).lower() == "subagent"
        warnings.extend(parse_warnings)
        if child and not args.include_children:
            continue
        files_inspected += 1
        session_id = str(metadata.get("session_id") or hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16])
        for message_index, message in enumerate(messages, 1):
            if query.casefold() not in message["text"].casefold():
                continue
            excerpt, truncated = _excerpt(message["text"], query, args.excerpt_chars)
            matches.append({
                "source": source,
                "session_id": session_id,
                "path": str(path.resolve()),
                "cwd": metadata.get("cwd") or str(path.parent),
                "started_at": metadata.get("started_at"),
                "message_index": message_index,
                "role": message["role"],
                "timestamp": message["timestamp"],
                "excerpt": excerpt,
                "excerpt_truncated": truncated,
                "session_mtime": iso(modified),
            })
    matches.sort(key=lambda item: (item["timestamp"] or item["started_at"] or item["session_mtime"], item["session_id"], item["message_index"]), reverse=True)
    returned = matches[: args.limit]
    print(json.dumps({
        "query": query,
        "sources": sorted(requested_sources),
        "selection": {"since": iso(lower) if lower else None, "until": iso(upper) if upper else None},
        "limits": {"matches": args.limit, "excerpt_chars": args.excerpt_chars},
        "candidate_files": len(candidates),
        "files_inspected": files_inspected,
        "matches_total": len(matches),
        "matches_returned": len(returned),
        "truncated": len(returned) < len(matches),
        "warnings": sorted(set(warnings)),
        "extraction_errors": errors,
        "results": returned,
    }, ensure_ascii=False))
    return 0


def show(args: argparse.Namespace) -> int:
    requested_path = Path(args.path).expanduser()
    if args.message_index <= 0 or args.before < 0 or args.after < 0:
        print("--message-index must be positive; --before and --after must be non-negative", file=sys.stderr)
        return 2
    if requested_path.is_symlink():
        print("show requires a regular .jsonl history path", file=sys.stderr)
        return 2
    path = requested_path.resolve()
    if path.suffix != ".jsonl" or not path.is_file():
        print("show requires a regular .jsonl history path", file=sys.stderr)
        return 2
    records, errors = parse_jsonl_diagnostics(path)
    if args.source == "pi":
        messages, warnings = _parse_pi_records(records)
    else:
        messages, warnings, _ = _parse_codex_records(records)
    if args.message_index > len(messages):
        print(f"message index {args.message_index} exceeds session message count {len(messages)}", file=sys.stderr)
        return 2
    start = max(0, args.message_index - 1 - args.before)
    end = min(len(messages), args.message_index + args.after)
    selected = []
    for index in range(start, end):
        selected.append({"message_index": index + 1, **messages[index]})
    metadata = session_metadata(path)
    print(json.dumps({
        "source": args.source,
        "session_id": str(metadata.get("session_id") or hashlib.sha256(str(path).encode()).hexdigest()[:16]),
        "path": str(path),
        "cwd": metadata.get("cwd") or str(path.parent),
        "started_at": metadata.get("started_at"),
        "requested_message_index": args.message_index,
        "messages": selected,
        "warnings": sorted(set([PRIVACY_WARNING, *warnings])),
        "extraction_errors": errors,
    }, ensure_ascii=False))
    return 0


def state_dir(vault: Path) -> Path:
    return vault / ".knowledge-bank" / "state"


def _checkpoint_data(vault: Path) -> dict[str, Any]:
    path = state_dir(vault) / "checkpoint.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        raise ValueError(f"invalid checkpoint file {path}: {exc}") from exc
    if not isinstance(data, dict) or any(source not in SOURCES for source in data):
        raise ValueError(f"invalid checkpoint schema in {path}")
    for source, entry in data.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("scan_started_at"), str):
            raise ValueError(f"invalid {source} checkpoint in {path}")
        try:
            parse_time(entry["scan_started_at"])
        except ValueError as exc:
            raise ValueError(f"invalid {source} checkpoint timestamp in {path}") from exc
    return data


def checkpoint(vault: Path, source: str | None = None) -> datetime | dict[str, datetime | None] | None:
    data = _checkpoint_data(vault)
    def read_one(name: str) -> datetime | None:
        value = data.get(name)
        if isinstance(value, dict):
            value = value.get("scan_started_at")
        try:
            return parse_time(value) if isinstance(value, str) else None
        except ValueError:
            return None
    if source:
        return read_one(source)
    values = {name: read_one(name) for name in SOURCES}
    if values["pi"] == values["codex"]:
        return values["pi"]
    return values


def select_since(vault: Path, since: str | None, all_history: bool, source: str = "pi") -> tuple[datetime | None, str]:
    if all_history:
        return None, "all history"
    if since:
        return parse_time(since), f"explicit --since {since}"
    previous = checkpoint(vault, source)
    if isinstance(previous, datetime):
        return previous, f"last successful {source} checkpoint {iso(previous)}"
    return now() - timedelta(days=DEFAULT_DAYS), f"first run: last 7 days for {source} (no successful checkpoint)"


def scan(args: argparse.Namespace) -> int:
    vault = Path(args.vault).resolve()
    scan_started = now()
    upper = parse_time(args.until) if args.until else scan_started
    selected_sources = {args.source} if args.source != "all" else set(SOURCES)
    lowers: dict[str, datetime | None] = {}
    bases: dict[str, str] = {}
    previous_checkpoints: dict[str, datetime | None] = {}
    try:
        for source in SOURCES:
            if source in selected_sources:
                previous = checkpoint(vault, source)
                previous_checkpoints[source] = previous if isinstance(previous, datetime) else None
                lowers[source], bases[source] = select_since(vault, args.since, args.all, source)
    except ValueError as exc:
        print(f"scan failed without writing state: {exc}", file=sys.stderr)
        return 1
    basis = "; ".join(f"{source}: {bases[source]}" for source in sorted(selected_sources))
    candidates: list[tuple[str, Path, list[dict[str, str]], list[str], bool, dict[str, Any]]] = []
    warnings: list[str] = [PRIVACY_WARNING]
    extraction_errors: list[dict[str, Any]] = []
    pi_roots, codex_roots = roots(args)
    for source, source_roots in (("pi", pi_roots), ("codex", codex_roots)):
        if source not in selected_sources:
            continue
        inspected_root = False
        for root in source_roots:
            if not root.is_dir():
                warnings.append(f"History root is unavailable or not a directory: {root}")
                continue
            inspected_root = True
            paths, unsupported_paths = discover(root, source, args.include_children)
            lower = lowers[source]
            for path in unsupported_paths:
                modified = datetime.fromtimestamp(path.stat().st_mtime, UTC)
                if (lower and modified < lower) or (upper and modified > upper):
                    continue
                warning = f"Unsupported compressed history (not scanned): {path}"
                warnings.append(warning)
                extraction_errors.append({"file": str(path.resolve()), "error": "unsupported compressed JSONL history"})
            for path in paths:
                modified = datetime.fromtimestamp(path.stat().st_mtime, UTC)
                if (lower and modified < lower) or (upper and modified > upper):
                    continue
                records, errors = parse_jsonl_diagnostics(path)
                metadata = session_metadata(path)
                if source == "pi":
                    messages, parse_warnings = _parse_pi_records(records)
                    child = pi_is_child(records) or bool(re.search(r"(?:^|/)run-\d+/session\.jsonl$", path.as_posix()))
                else:
                    messages, parse_warnings, child = _parse_codex_records(records)
                    child = child or str(metadata.get("thread_source", "")).lower() == "subagent"
                if child and not args.include_children:
                    warnings.append(f"Excluded {source} child session: {path}")
                    continue
                extraction_errors.extend(errors)
                if not messages:
                    continue
                candidates.append((source, path, messages, parse_warnings, child, metadata))
        if not inspected_root:
            extraction_errors.append({
                "source": source,
                "roots": [str(root) for root in source_roots],
                "error": "no history root was available",
            })
    run_id = scan_started.strftime("%Y%m%dT%H%M%SZ") + "-" + hashlib.sha256(str(scan_started).encode()).hexdigest()[:8]
    run_dir = state_dir(vault) / run_id
    normalized_dir = run_dir / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    sessions = []
    for number, (source, path, messages, parse_warnings, child, metadata) in enumerate(candidates, 1):
        session_id = str(metadata.get("session_id") or hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16])
        normalized = normalized_dir / f"{number:04d}-{hashlib.sha256(session_id.encode()).hexdigest()[:16]}.json"
        payload = {"source": source, "session_id": session_id, "path": str(path.resolve()), "cwd": metadata.get("cwd") or str(path.parent), "started_at": metadata.get("started_at"), "messages": messages}
        atomic_write(normalized, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        sessions.append({"source": source, "session_id": session_id, "path": str(path.resolve()), "normalized_path": str(normalized), "cwd": metadata.get("cwd") or str(path.parent), "started_at": metadata.get("started_at"), "mtime": iso(datetime.fromtimestamp(path.stat().st_mtime, UTC)), "message_count": len(messages), "child": child, "warnings": parse_warnings})
        warnings.extend(parse_warnings)
    for index, session in enumerate(sessions):
        session["review_batch"] = index // REVIEW_BATCH_SIZE + 1
    historical = bool(args.until and upper and upper < scan_started)
    checkpoint_updates: dict[str, str] = {}
    if not historical:
        if args.all or args.since is None:
            checkpoint_updates = {source: iso(scan_started) for source in sorted(selected_sources)}
        else:
            explicit_lower = parse_time(args.since)
            for source in sorted(selected_sources):
                previous = previous_checkpoints[source]
                if previous is not None and explicit_lower is not None and explicit_lower <= previous:
                    checkpoint_updates[source] = iso(scan_started)
            if len(checkpoint_updates) != len(selected_sources):
                warnings.append(
                    "Explicit --since left an unreviewed gap for at least one source; "
                    "those source checkpoints will not advance."
                )
    manifest = {
        "run_id": run_id,
        "scan_started_at": iso(scan_started),
        "selection_basis": basis,
        "selection_details": {source: {"since": iso(lowers[source]) if lowers[source] else None, "basis": bases[source]} for source in sorted(selected_sources)},
        "since": iso(min((value for value in lowers.values() if value), default=scan_started)) if any(lowers.values()) else None,
        "until": iso(upper) if upper else None,
        "sources": sorted(selected_sources),
        "batch_size": REVIEW_BATCH_SIZE,
        "batch_count": (len(sessions) + REVIEW_BATCH_SIZE - 1) // REVIEW_BATCH_SIZE,
        "sessions": sessions,
        "warnings": sorted(set(warnings)),
        "extraction_errors": extraction_errors,
        "checkpoint_updates": checkpoint_updates,
        "counts": {"files": len(sessions), "messages": sum(item["message_count"] for item in sessions)},
        "review_complete": False,
    }
    manifest_path = run_dir / "manifest.json"
    atomic_write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


def status(args: argparse.Namespace) -> int:
    vault = Path(args.vault).resolve()
    data = _checkpoint_data(vault)
    checkpoints = {}
    for source in SOURCES:
        value = checkpoint(vault, source)
        checkpoints[source] = iso(value) if isinstance(value, datetime) else None
    runs = []
    root = state_dir(vault)
    if root.exists():
        for manifest in sorted(root.glob("*/manifest.json")):
            try:
                data = json.loads(manifest.read_text())
                runs.append({"run_id": data.get("run_id"), "manifest": str(manifest), "sessions": len(data.get("sessions", [])), "review_complete": data.get("review_complete", False)})
            except (OSError, json.JSONDecodeError):
                pass
    print(json.dumps({"checkpoints": checkpoints, "runs": runs}, ensure_ascii=False))
    return 0


def _manifest_layout(manifest_arg: str) -> tuple[Path, Path, Path, dict[str, Any]]:
    manifest_path = Path(manifest_arg).expanduser().resolve()
    if manifest_path.name != "manifest.json":
        raise ValueError("complete requires an explicit manifest.json path")
    run_dir = manifest_path.parent
    state_root = run_dir.parent
    knowledge_root = state_root.parent
    if state_root.name != "state" or knowledge_root.name != ".knowledge-bank" or not RUN_ID_RE.fullmatch(run_dir.name):
        raise ValueError("manifest must be exactly <vault>/.knowledge-bank/state/<run-id>/manifest.json")
    vault = knowledge_root.parent
    if state_dir(vault).resolve() != state_root:
        raise ValueError("manifest is outside the resolved vault state layout")
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError("manifest must be a regular file in the run directory")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read manifest: {exc}") from exc
    if not isinstance(data, dict) or data.get("run_id") != run_dir.name:
        raise ValueError("manifest run_id must match its run directory")
    return manifest_path, run_dir, vault, data


def _checkpoint_value(value: Any) -> str:
    if isinstance(value, str):
        parse_time(value)
        return value
    if isinstance(value, dict) and isinstance(value.get("scan_started_at"), str):
        parse_time(value["scan_started_at"])
        return value["scan_started_at"]
    raise ValueError("checkpoint_updates values must be timestamps or timestamp objects")


def complete(args: argparse.Namespace) -> int:
    try:
        manifest_path, run_dir, vault, data = _manifest_layout(args.manifest)
        requested_vault = Path(args.vault).expanduser().resolve()
        if vault != requested_vault:
            raise ValueError("manifest vault does not match --vault")
        if not args.review_complete:
            raise ValueError("refusing checkpoint advancement: pass --review-complete after the entire review succeeds")
        if data.get("review_complete") is not False:
            raise ValueError("manifest must represent an incomplete review")
        if "extraction_errors" not in data or not isinstance(data["extraction_errors"], list):
            raise ValueError("manifest extraction_errors must be a list")
        if data["extraction_errors"]:
            raise ValueError("refusing checkpoint advancement: manifest has extraction errors")
        if "sessions" not in data or not isinstance(data["sessions"], list):
            raise ValueError("manifest sessions must be a list")
        sources = data.get("sources")
        if not isinstance(sources, list) or not sources or any(source not in SOURCES for source in sources) or len(set(sources)) != len(sources):
            raise ValueError("manifest sources must be a nonempty unique list containing only pi or codex")
        updates = data.get("checkpoint_updates")
        if not isinstance(updates, dict) or any(source not in SOURCES for source in updates):
            raise ValueError("checkpoint_updates must name only pi or codex")
        if not set(updates).issubset(sources):
            raise ValueError("checkpoint_updates must be a subset of manifest sources")
        normalized = run_dir / "normalized"
        if normalized.exists() and (normalized.is_symlink() or not normalized.is_dir()):
            raise ValueError("normalized must be the run's direct directory")
        expected_normalized: set[Path] = set()
        for session in data["sessions"]:
            if not isinstance(session, dict) or not isinstance(session.get("normalized_path"), str):
                raise ValueError("every manifest session must name a normalized_path")
            candidate = Path(session["normalized_path"]).resolve()
            if candidate.parent != normalized.resolve() or not candidate.is_file() or candidate.is_symlink():
                raise ValueError("session normalized_path is outside the run normalized directory")
            expected_normalized.add(candidate)
        actual_normalized: set[Path] = set()
        if normalized.exists():
            for entry in normalized.iterdir():
                if entry.is_symlink() or not entry.is_file():
                    raise ValueError("normalized contains an unexpected non-file entry")
                actual_normalized.add(entry.resolve())
        if actual_normalized != expected_normalized:
            raise ValueError("normalized files do not exactly match manifest sessions")
        # Validate all update timestamps and stage both replacements before mutation.
        update_values = {source: _checkpoint_value(value) for source, value in updates.items()}
        scan_started = data.get("scan_started_at")
        if not isinstance(scan_started, str) or parse_time(scan_started) is None:
            raise ValueError("manifest scan_started_at is invalid")
        normalized_scan_started = iso(parse_time(scan_started))
        if any(iso(parse_time(value)) != normalized_scan_started for value in update_values.values()):
            raise ValueError("checkpoint update timestamps must equal manifest scan_started_at")
        until = data.get("until")
        if until and parse_time(until) < parse_time(scan_started) and update_values:
            raise ValueError("historical manifests must not advance checkpoints")
        checkpoint_path = state_dir(vault) / "checkpoint.json"
        checkpoint_data = _checkpoint_data(vault)
        actual_updates: dict[str, str] = {}
        for source, timestamp in update_values.items():
            existing = checkpoint(vault, source)
            chosen = timestamp
            if isinstance(existing, datetime) and existing > parse_time(timestamp):
                chosen = iso(existing)
            checkpoint_data[source] = {"scan_started_at": chosen, "run_id": data["run_id"]}
            actual_updates[source] = chosen
        completed = dict(data)
        completed["review_complete"] = True
        # Mark completion before cleanup. A failed checkpoint write leaves a completed
        # review that can safely be retried, rather than advancing an incomplete review.
        atomic_write(manifest_path, json.dumps(completed, ensure_ascii=False, indent=2) + "\n")
        if update_values:
            atomic_write(checkpoint_path, json.dumps(checkpoint_data, ensure_ascii=False, indent=2) + "\n")
        try:
            if normalized.exists():
                shutil.rmtree(normalized)
        except OSError as exc:
            print(f"review completed but normalized cleanup failed: {exc}", file=sys.stderr)
            print(json.dumps({"completed": data.get("run_id"), "cleanup_error": str(exc)}))
            return 1
        result = {"completed": data.get("run_id"), "checkpoint_updates": actual_updates}
        print(json.dumps(result))
        return 0
    except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"complete failed without advancing checkpoint: {exc}", file=sys.stderr)
        return 1 if args.review_complete else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument("--pi-root")
    scan_parser.add_argument("--codex-root")
    scan_parser.add_argument("--source", choices=["pi", "codex", "all"], default="all")
    scan_parser.add_argument("--since")
    scan_parser.add_argument("--until")
    scan_parser.add_argument("--all", action="store_true")
    scan_parser.add_argument("--include-children", action="store_true")
    scan_parser.set_defaults(func=scan)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("--pi-root")
    search_parser.add_argument("--codex-root")
    search_parser.add_argument("--source", choices=["pi", "codex", "all"], default="all")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--since")
    search_parser.add_argument("--until")
    search_parser.add_argument("--include-children", action="store_true")
    search_parser.add_argument("--limit", type=int, required=True)
    search_parser.add_argument("--excerpt-chars", type=int, required=True)
    search_parser.set_defaults(func=search)
    show_parser = sub.add_parser("show")
    show_parser.add_argument("path")
    show_parser.add_argument("--source", choices=SOURCES, required=True)
    show_parser.add_argument("--message-index", type=int, required=True)
    show_parser.add_argument("--before", type=int, default=0)
    show_parser.add_argument("--after", type=int, default=0)
    show_parser.set_defaults(func=show)
    status_parser = sub.add_parser("status")
    status_parser.set_defaults(func=status)
    complete_parser = sub.add_parser("complete")
    complete_parser.add_argument("manifest")
    complete_parser.add_argument("--review-complete", action="store_true")
    complete_parser.set_defaults(func=complete)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    raise SystemExit(parsed.func(parsed))
