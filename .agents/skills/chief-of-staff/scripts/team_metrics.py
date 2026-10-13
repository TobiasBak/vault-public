#!/usr/bin/env python3
import argparse
import bisect
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import sqlite3
import statistics
import sys


COS_THREAD_ID = "b826766b-7e34-4c9d-bc2d-d3199e4744f6"
KINDS = ("go-request", "merge-ready", "done", "blocked", "tobias-decision", "other")
TABLES = {
    "orchestration_v2_projection_threads",
    "orchestration_v2_projection_messages",
    "orchestration_v2_projection_runs",
}
PR_URL = re.compile(r"https?://[^\s<>]+/(?:pull|pulls|merge_requests)/\d+", re.I)
SHA = re.compile(r"\b[0-9a-f]{40}\b", re.I)
KEYWORDS = (
    ("tobias-decision", r"\bneeds[- ]tobias\b|\btobias\b.{0,40}\b(?:decision|decide|choice|approval)\b|\b(?:decision|choice)\b.{0,40}\btobias\b"),
    ("blocked", r"\b(?:blocked|blocker|blocking|stalled)\b"),
    ("go-request", r"\bgo[- ]request\b|\b(?:request(?:ing)?|need|await(?:ing)?|waiting for|seeking)\b.{0,60}\b(?:go|approval|permission)\b|\b(?:plan|scope|protected[- ]surface)\b.{0,60}\bgate\b|\b(?:approve|go/no-go)\b"),
    ("done", r"\b(?:done|completed|finished|merged)\b"),
)


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("ISO timestamps must include a timezone")
    return result.astimezone(timezone.utc)


def iso(value):
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def open_readonly(path):
    db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=5)
    db.execute("PRAGMA query_only = ON")
    db.execute("BEGIN")
    return db


def discover_store():
    root = Path.home() / ".t3" / "userdata"
    candidates = sorted({*root.rglob("*.sqlite"), *root.rglob("*.sqlite3"), *root.rglob("*.db")})
    matches = []
    for path in candidates:
        with closing(open_readonly(path)) as db:
            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if TABLES <= tables and db.execute(
                "SELECT 1 FROM orchestration_v2_projection_threads WHERE thread_id=?",
                (COS_THREAD_ID,),
            ).fetchone():
                matches.append(path)
    if len(matches) != 1:
        raise ValueError(f"Expected one readable T3 V2 store containing the CoS thread; found {len(matches)}")
    return matches[0]


def classify(text):
    if PR_URL.search(text) and SHA.search(text):
        return "merge-ready"
    for kind, pattern in KEYWORDS:
        if re.search(pattern, text, re.I):
            return kind
    return "other"


def load_data(db):
    threads = {}
    for thread_id, title, raw in db.execute(
        "SELECT thread_id, title, payload_json FROM orchestration_v2_projection_threads"
    ):
        payload = json.loads(raw)
        safe_title = "".join(char if char.isprintable() else " " for char in title)
        threads[thread_id] = (" ".join(safe_title.split()), payload.get("lineage") or {})
    incoming, outgoing = defaultdict(list), defaultdict(list)
    for target, created_at, raw in db.execute(
        """SELECT thread_id, created_at, payload_json
           FROM orchestration_v2_projection_messages
           WHERE role='user' AND instr(message_id, 'thread-send') > 0
             AND (thread_id=? OR json_extract(payload_json, '$.senderThreadId')=?)
           ORDER BY created_at, message_id""",
        (COS_THREAD_ID, COS_THREAD_ID),
    ):
        payload = json.loads(raw)
        sender = payload.get("senderThreadId")
        at = timestamp(created_at)
        if target == COS_THREAD_ID:
            if sender not in threads:
                raise ValueError("A CoS report has no stored sender thread")
            incoming[sender].append((at, classify(payload.get("text", ""))))
        elif sender == COS_THREAD_ID:
            if target not in threads:
                raise ValueError("A CoS send has no stored destination thread")
            outgoing[target].append(at)
    contacts = incoming.keys() | outgoing.keys()
    leads = sorted(
        (lead for lead in contacts if lead != COS_THREAD_ID and not threads[lead][1].get("parentThreadId")),
        key=lambda lead: (threads[lead][0].casefold(), lead),
    )
    runs = defaultdict(list)
    child_completions = defaultdict(list)
    for thread_id, status, completed_at, raw in db.execute(
        "SELECT thread_id, status, completed_at, payload_json FROM orchestration_v2_projection_runs"
    ):
        payload = json.loads(raw)
        start = timestamp(payload["startedAt"]) if payload.get("startedAt") else None
        end = timestamp(completed_at) if completed_at else None
        if start is not None:
            if end is not None and end < start:
                raise ValueError("A stored run ends before it starts")
            if end is None and status != "running":
                raise ValueError("A terminal started run has no completion timestamp")
            runs[thread_id].append((start, end, status))
        lineage = threads.get(thread_id, ("", {}))[1]
        if status == "completed" and end is not None and lineage.get("relationshipToParent") == "subagent":
            child_completions[lineage["parentThreadId"]].append(end)
    for completions in child_completions.values():
        completions.sort()
    return threads, leads, incoming, outgoing, runs, child_completions


def idle_gaps(runs, completions, since, until):
    busy = []
    for start, end, _ in sorted(runs, key=lambda run: run[0]):
        if start >= until:
            continue
        end = min(end or until, until)
        if busy and start <= busy[-1][1]:
            busy[-1] = (busy[-1][0], max(busy[-1][1], end))
        else:
            busy.append((start, end))
    gaps = []
    open_count = 0
    for index, (_, end) in enumerate(busy):
        next_start = busy[index + 1][0] if index + 1 < len(busy) else until
        completion_index = bisect.bisect_right(completions, end)
        if completion_index == len(completions):
            continue
        start = max(completions[completion_index], since)
        if start < next_start:
            gaps.append((next_start - start).total_seconds())
            open_count += next_start == until
    return gaps, open_count


def duration(seconds):
    if seconds is None:
        return "pending"
    if seconds < 60:
        return f"{seconds:.3f}s"
    if seconds < 3600:
        return f"{seconds / 60:.2f}m"
    return f"{seconds / 3600:.2f}h"


def table(headers, rows):
    rows = [tuple(str(cell) for cell in row) for row in rows]
    widths = [max([len(header)] + [len(row[index]) for row in rows]) for index, header in enumerate(headers)]
    print("  ".join(header.ljust(width) for header, width in zip(headers, widths)))
    for row in rows:
        print("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())
    if not rows:
        print("(none)")


def summary(values):
    if not values:
        return ("0", "-", "-", "-")
    ordered = sorted(values)
    return (
        str(len(values)),
        duration(statistics.median(ordered)),
        duration(ordered[math.ceil(0.9 * len(ordered)) - 1]),
        duration(ordered[-1]),
    )


def report(data, path, since, until):
    threads, leads, incoming, outgoing, runs, child_completions = data
    print(f"Window: [{iso(since)}, {iso(until)}) UTC")
    print(f"Source: {path} (read-only snapshot)")
    print("Durations: s=seconds, m=minutes, h=hours; p90=nearest rank.")
    print("Kinds: PR URL + 40-hex SHA first, then Tobias decision, blocked, go request, done; keyword heuristics.")
    print("\nLead messages")
    message_rows = []
    gate_rows = []
    waits = []
    pending = 0
    for lead in leads:
        title = threads[lead][0]
        reports = sorted((at, kind) for at, kind in incoming[lead] if since <= at < until)
        replies = sorted(at for at in outgoing[lead] if since <= at < until)
        counts = Counter(kind for _, kind in reports)
        message_rows.append((title, len(reports), *(counts[kind] for kind in KINDS), len(replies)))
        lead_waits = []
        for at, _ in reports:
            reply_index = bisect.bisect_left(replies, at)
            wait = (replies[reply_index] - at).total_seconds() if reply_index < len(replies) else None
            lead_waits.append(duration(wait))
            if wait is None:
                pending += 1
            else:
                waits.append(wait)
        for index in range(0, len(lead_waits), 8):
            batch = lead_waits[index:index + 8]
            gate_rows.append((title if index == 0 else "", f"{index + 1}-{index + len(batch)}", ", ".join(batch)))
    table(("Lead", "sent", *KINDS, "CoS replies"), message_rows)
    print("\nGate latency: each report to the next CoS send to that lead within the window.")
    print("Reports are numbered chronologically per lead; one send can answer multiple reports.")
    print("This measures next-send delay, not whether the reply grants a gate or addresses the report.")
    table(("Lead", "Reports", "Delays in order"), gate_rows)
    table(("answered", "median", "p90", "max", "pending"), [(*summary(waits), pending)])
    print("\nIdle-lead gaps: first completed direct-child run after a lead run ends to its next run start.")
    print("Overlapping lead runs are merged; gaps are clipped to the window; open gaps end at --until.")
    gap_rows = []
    for lead in leads:
        gaps, open_count = idle_gaps(runs[lead], child_completions[lead], since, until)
        gap_rows.append((threads[lead][0], len(gaps), duration(sum(gaps)), duration(max(gaps, default=0)), open_count))
    table(("Lead", "count", "total", "max", "open"), gap_rows)
    cos_durations = []
    excluded = 0
    for start, end, _ in runs[COS_THREAD_ID]:
        if since <= start < until:
            if end is not None and end < until:
                cos_durations.append((end - start).total_seconds())
            else:
                excluded += 1
    print("\nCoS turn durations: runs starting and ending within the window, including failed/cancelled turns.")
    table(("turns", "median", "p90", "max", "unfinished at until"), [(*summary(cos_durations), excluded)])


def main():
    parser = argparse.ArgumentParser(
        description="Measure CoS messages, next-send delays, idle-lead gaps and turn durations from local T3 V2 SQLite.",
        epilog="Window is [since, until). ISO timestamps need a timezone. Defaults: first CoS report/run to now. No message text is printed.",
        allow_abbrev=False,
    )
    parser.add_argument("--since", type=timestamp, metavar="ISO")
    parser.add_argument("--until", type=timestamp, metavar="ISO")
    args = parser.parse_args()
    try:
        path = discover_store()
        with closing(open_readonly(path)) as db:
            data = load_data(db)
        until = args.until or datetime.now(timezone.utc)
        reports = [at for entries in data[2].values() for at, _ in entries]
        starts = [start for start, _, _ in data[4][COS_THREAD_ID]]
        since = args.since or min(reports + starts, default=until)
        if since >= until:
            raise ValueError("--since must be earlier than --until")
        report(data, path, since, until)
    except (OSError, sqlite3.Error, ValueError, KeyError, TypeError) as error:
        print(f"team_metrics: {type(error).__name__}; cannot read or interpret the T3 store safely", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
