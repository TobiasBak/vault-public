#!/usr/bin/env python3
import argparse
import bisect
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timedelta, timezone
from html import escape
import json
import math
from pathlib import Path
import re
import sqlite3
import statistics
from string import Template
import subprocess
import sys
from zoneinfo import ZoneInfo


COS_THREAD_ID = Path(__file__).with_name("cos-thread").read_text().strip()
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


STORE_PATH = Path("/home/tb/.t3/userdata/statev2.sqlite")
LOCAL_ZONE = ZoneInfo("Europe/Copenhagen")


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
           WHERE role='user'
             AND ((thread_id=? AND instr(message_id, 'thread-send') > 0)
                  OR json_extract(payload_json, '$.senderThreadId')=?)
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
    leads = sorted(
        (lead for lead in threads if lead != COS_THREAD_ID and not threads[lead][1].get("parentThreadId")),
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


def report_kind(text):
    typed = re.match(r"^\s*\[(go[_-]request|merge[_-]ready|done|blocked|tobias[_-]decision)\]", text, re.I)
    return typed.group(1).lower().replace("_", "-") if typed else classify(text)


class Snapshot:
    def __init__(self, db, data):
        self.data = data
        self.threads = {
            thread_id: json.loads(raw)
            for thread_id, raw in db.execute("SELECT thread_id, payload_json FROM orchestration_v2_projection_threads")
        }
        self.leads = data[1]
        self.projects = dict(db.execute("SELECT project_id, title FROM projection_projects"))
        self.reports = defaultdict(list)
        for at, raw in db.execute(
            """SELECT created_at, payload_json FROM orchestration_v2_projection_messages
               WHERE thread_id=? AND role='user' AND instr(message_id, 'thread-send') > 0
               ORDER BY created_at, message_id""", (COS_THREAD_ID,),
        ):
            payload = json.loads(raw)
            self.reports[payload.get("senderThreadId")].append((timestamp(at), payload.get("text", "")))
        self.runs = defaultdict(list)
        self.run_by_id = {}
        self.running = set()
        self.queued = []
        for run_id, thread_id, status, requested, ended, raw in db.execute(
            "SELECT run_id, thread_id, status, requested_at, completed_at, payload_json FROM orchestration_v2_projection_runs"
        ):
            payload = json.loads(raw)
            start = timestamp(payload["startedAt"]) if payload.get("startedAt") else None
            end = timestamp(ended) if ended else None
            run = (run_id, start, end, status, timestamp(requested))
            self.runs[thread_id].append(run)
            self.run_by_id[run_id] = run
            if status == "running":
                self.running.add(thread_id)
            if status in {"queued", "pending"} or payload.get("queuePosition") is not None:
                self.queued.append((timestamp(requested), thread_id, run_id))
        self.last_assistant = {}
        for lead in self.leads:
            row = db.execute(
                """SELECT created_at, run_id, payload_json FROM orchestration_v2_projection_messages
                   WHERE thread_id=? AND role='assistant' AND streaming=0
                   ORDER BY created_at DESC, message_id DESC LIMIT 1""", (lead,),
            ).fetchone()
            if row:
                self.last_assistant[lead] = (timestamp(row[0]), row[1], json.loads(row[2]).get("text", ""))
        self.used_results = {}
        for child, parent, target_run, raw in db.execute(
            """SELECT source_thread_id, target_thread_id, target_run_id, payload_json
               FROM orchestration_v2_projection_context_transfers
               WHERE type='subagent_result' AND status='consumed'"""
        ):
            payload = json.loads(raw)
            consumed = timestamp(payload.get("consumedAt") or payload["updatedAt"])
            run = self.run_by_id.get(target_run)
            source_run = (payload.get("sourcePoint") or {}).get("runId")
            latest_child = max(self.runs[child], key=lambda entry: entry[4], default=None)
            if run and run[2] and run[2] >= consumed and latest_child and latest_child[0] == source_run:
                self.used_results[child] = (consumed, parent)
        self.consumed_children = {}
        for child, payload in self.threads.items():
            lineage = payload.get("lineage") or {}
            parent = lineage.get("parentThreadId")
            latest = max(self.runs[child], key=lambda run: run[4], default=None)
            if lineage.get("relationshipToParent") != "subagent" or not latest or latest[3] != "completed" or not latest[2]:
                continue
            ends = [end for _, start, end, status, _ in self.runs[parent]
                    if status == "completed" and start and start > latest[2] and end]
            if ends:
                self.consumed_children[child] = min(ends)
        self.children_today = []
        for subagent_id, parent, child, started in db.execute(
            "SELECT subagent_id, thread_id, child_thread_id, started_at FROM orchestration_v2_projection_subagents WHERE started_at IS NOT NULL"
        ):
            self.children_today.append((timestamp(started), self.root(parent), child or subagent_id))

    def root(self, thread_id):
        seen = set()
        while thread_id in self.threads and thread_id not in seen:
            seen.add(thread_id)
            lineage = self.threads[thread_id].get("lineage") or {}
            if lineage.get("rootThreadId"):
                return lineage["rootThreadId"]
            if not lineage.get("parentThreadId"):
                break
            thread_id = lineage["parentThreadId"]
        return thread_id

    def visible(self, thread_id):
        payload = self.threads[thread_id]
        return not payload.get("archivedAt") and not payload.get("deletedAt")

    def settled(self, thread_id):
        payload = self.threads[thread_id]
        return payload.get("settledOverride") == "settled" or (
            bool(payload.get("settledAt")) and payload.get("settledOverride") != "unsettled"
            and (not payload.get("unsettledAt") or timestamp(payload["settledAt"]) >= timestamp(payload["unsettledAt"]))
        )

    def done(self, lead):
        if self.settled(lead):
            return True
        if lead in self.running or not self.reports[lead]:
            return False
        at, text = self.reports[lead][-1]
        return report_kind(text) == "done" and not any(start and start > at for _, start, _, _, _ in self.runs[lead])

    def title(self, thread_id):
        return self.data[0].get(thread_id, (thread_id, {}))[0]


def one_line(text):
    return " ".join(text.split())


def age(at, now):
    return duration(max(0, (now - at).total_seconds()))


def send_hint(snapshot, thread):
    return f"{thread} send:{'steer' if thread in snapshot.running else 'auto'}"


def outside_runs(snapshot):
    return sorted(
        (start or requested, thread, run_id)
        for thread, runs in snapshot.runs.items() if snapshot.root(thread) != COS_THREAD_ID
        for run_id, start, _, status, requested in runs if status == "running"
    )


def restart_check(snapshot):
    live = outside_runs(snapshot)
    for _, thread, run_id in live:
        print(f"running | {snapshot.title(thread)} | {thread} | run {run_id}")
    if not live:
        print("No running runs outside CoS and its children; restart allowed.")
    return 1 if live else 0


def commit(message, paths):
    subprocess.run(["git", "add", "--", *paths], check=True)
    subprocess.run(["git", "commit", "-m", message, "--", *paths], check=True)
    subprocess.run(["git", "pull", "--rebase", "--autostash"], check=True)
    subprocess.run(["git", "push"], check=True)
    return 0


def census(snapshot, now):
    items = []
    state = Path(__file__).resolve().parent.parent / "state.md"
    holds = {}
    for line in state_lines(state, "Holds"):
        thread, reason = line.split(": ", 1)
        holds[thread] = reason
        if thread in snapshot.threads and snapshot.visible(thread):
            at = timestamp(snapshot.threads[thread]["updatedAt"])
            items.append((at, f"held {age(at, now)}: {reason} | {snapshot.title(thread)} | {send_hint(snapshot, thread)}"))
    for lead in snapshot.leads:
        if not snapshot.visible(lead) or snapshot.settled(lead):
            continue
        title = snapshot.title(lead)
        replies = snapshot.data[3][lead]
        for at, text in snapshot.reports[lead]:
            if not replies or replies[-1] <= at:
                items.append((at, f"unanswered report {age(at, now)} {report_kind(text)} | {title} | {send_hint(snapshot, lead)}"))
        if lead in holds:
            continue
        latest = max(snapshot.runs[lead], key=lambda run: run[4], default=None)
        if latest and latest[3] in {"failed", "interrupted", "cancelled"}:
            _, _, end, status, requested = latest
            at = end or requested
            items.append((at, f"dead lead {age(at, now)}: last run {status}; resume or settle | {title} | {send_hint(snapshot, lead)}"))
            continue
        if lead in snapshot.running:
            continue
        assistant = snapshot.last_assistant.get(lead)
        if assistant:
            at, run_id, text = assistant
            run = snapshot.run_by_id.get(run_id)
            start = (run[1] or run[4]) if run else at
            sent = any(report_at >= start for report_at, _ in snapshot.reports[lead])
            plan = re.search(r"\b(?:plan|question|approve|approval|permission)\b|\?", text, re.I)
            if not sent and (classify(text) == "merge-ready" or plan):
                kind = "merge-ready" if classify(text) == "merge-ready" else "plan/question"
                items.append((at, f"idle unreported {age(at, now)} {kind}: answer or merge | {title} | {send_hint(snapshot, lead)}"))
        ends = [end for _, _, end, _, _ in snapshot.runs[lead] if end]
        if ends:
            last_end = max(ends)
            for child, payload in snapshot.threads.items():
                lineage = payload.get("lineage") or {}
                if lineage.get("parentThreadId") != lead or not snapshot.visible(child) or child in holds:
                    continue
                completions = [end for _, _, end, status, _ in snapshot.runs[child] if status == "completed" and end and end > last_end]
                if completions:
                    at = min(completions)
                    items.append((at, f"idle unused child {age(at, now)}: nudge lead | {title} | {send_hint(snapshot, lead)} | child {send_hint(snapshot, child)}"))
    running_roots = {snapshot.root(thread) for thread in snapshot.running}
    for at, thread, run_id in snapshot.queued:
        root = snapshot.root(thread)
        if root in running_roots and root in snapshot.leads:
            items.append((at, f"queued message {age(at, now)}: promote to steer or cancel stale | {snapshot.title(thread)} | {send_hint(snapshot, thread)} | {run_id}"))
    for thread, payload in snapshot.threads.items():
        if thread == COS_THREAD_ID or not snapshot.visible(thread) or snapshot.settled(thread) or thread in snapshot.running:
            continue
        root = snapshot.root(thread)
        reason = None
        at = timestamp(payload["updatedAt"])
        lineage = payload.get("lineage") or {}
        latest = max(snapshot.runs[thread], key=lambda run: run[4], default=None)
        if (lineage.get("parentThreadId") == COS_THREAD_ID and lineage.get("relationshipToParent") == "subagent"
                and latest and latest[3] == "completed" and latest[2]):
            at = latest[2]
            reason = "CoS child completed with no later run; verify used"
        elif root in snapshot.leads and snapshot.done(root):
            reason = "root lead done"
        elif thread in snapshot.used_results:
            at, parent = snapshot.used_results[thread]
            reason = f"result consumed by completed parent run {parent}; verify used"
        elif thread in snapshot.consumed_children:
            at = snapshot.consumed_children[thread]
            reason = "child result consumed by parent's later run; verify used"
        if reason:
            items.append((at, f"settle candidate {age(at, now)}: {reason} | {snapshot.title(thread)} | {send_hint(snapshot, thread)}"))
    live = outside_runs(snapshot)
    if live:
        at = min(start for start, _, _ in live)
        details = "; ".join(f"{snapshot.title(thread)} [{send_hint(snapshot, thread)}]" for _, thread, _ in live)
        items.append((at, f"running outside CoS {age(at, now)}: {len(live)} runs; hold T3 restart | {details}"))
    for _, line in sorted(items, key=lambda item: (item[0], item[1])):
        print(line)


def wait_today(snapshot, lead, since, now):
    replies = snapshot.data[3][lead]
    total = 0
    settled_at = snapshot.threads[lead].get("settledAt") if snapshot.settled(lead) else None
    for at, _ in snapshot.reports[lead]:
        if not since <= at < now:
            continue
        index = bisect.bisect_left(replies, at)
        end = min(replies[index], now) if index < len(replies) else now
        if settled_at:
            end = min(end, timestamp(settled_at))
        total += max(0, (end - at).total_seconds())
    return total


def dead_today(snapshot, since, now):
    endings = []
    dead = []
    for thread, runs in snapshot.runs.items():
        for run_id, start, end, status, _ in runs:
            if status in {"cancelled", "interrupted"} and end and since <= end < now:
                endings.append((end, snapshot.root(thread), run_id))
            if status in {"cancelled", "interrupted", "failed"} and start and end and start < now and end > since:
                dead.append((run_id, snapshot.root(thread), max(0, (min(end, now) - max(start, since)).total_seconds())))
    endings.sort()
    clusters = set()
    left = 0
    for right, (end, _, _) in enumerate(endings):
        while (end - endings[left][0]).total_seconds() > 10:
            left += 1
        window = endings[left:right + 1]
        if len({root for _, root, _ in window}) >= 3:
            clusters.update(run_id for _, _, run_id in window)
    per_root = defaultdict(float)
    restart = other = 0
    for run_id, root, seconds in dead:
        per_root[root] += seconds
        if run_id in clusters:
            restart += seconds
        else:
            other += seconds
    return per_root, restart, other


def state_lines(path, heading):
    lines = path.read_text().splitlines()
    active = False
    result = []
    for line in lines:
        if re.match(r"^#{1,6} ", line):
            active = line.lstrip("#").strip().casefold() == heading.casefold()
        elif active and line.startswith("- "):
            text = line[2:].strip()
            status = text.replace("**", "").replace("`", "")
            if status.casefold() not in {"none", "none.", "nothing", "nothing."} and not re.fullmatch(r"(?:.+?:\s*)?done[.!]?", status, re.I):
                result.append(text)
    return result


def markdown_text(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return escape(text.replace("**", "").replace("`", ""))


def progress(text):
    match = re.search(r"^\s*progress:\s*(.+)$", text, re.I | re.M)
    if not match:
        return []
    result = []
    for step in match.group(1).split("|"):
        step = step.strip()
        marker = step[-1:] if step[-1:] in {"✓", "*", "!"} else ""
        label = step[:-1].strip() if marker else step
        if label:
            result.append((label, {"✓": "d", "*": "c", "!": "b", "": ""}[marker]))
    return result


def board_duration(seconds):
    if seconds < 60:
        return f"{seconds:.0f} s"
    if seconds < 3600:
        return f"{seconds / 60:.0f} min"
    return f"{seconds / 3600:.1f} h"


def write_board(snapshot, now, out):
    local_now = now.astimezone(LOCAL_ZONE)
    since = local_now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    recent = now - timedelta(hours=48)
    activity = {}
    for thread, payload in snapshot.threads.items():
        at = timestamp(payload["updatedAt"])
        for _, start, end, _, requested in snapshot.runs[thread]:
            at = max(at, start or requested, end or requested)
        root = snapshot.root(thread)
        activity[root] = max(at, activity.get(root, at))
    running_roots = {snapshot.root(thread) for thread in snapshot.running}
    reporting_leads = [lead for lead in snapshot.leads if snapshot.reports[lead]]
    leads = [lead for lead in reporting_leads if snapshot.visible(lead)
             and (lead in running_roots or not snapshot.settled(lead)) and activity.get(lead, since) >= recent]
    dead, restart, other = dead_today(snapshot, since, now)
    children = defaultdict(set)
    for at, root, child in snapshot.children_today:
        if since <= at < now:
            children[root].add(child)
    for thread, payload in snapshot.threads.items():
        if (payload.get("lineage") or {}).get("parentThreadId") and since <= timestamp(payload["createdAt"]) < now:
            children[snapshot.root(thread)].add(thread)
    rows = []
    for lead in leads:
        report_at, text = snapshot.reports[lead][-1]
        progress_text = next((report_text for _, report_text in reversed(snapshot.reports[lead]) if progress(report_text)), text)
        steps = progress(progress_text)
        track = '<div class="track">' + "".join(f'<div class="st {status}"><i></i><span>{escape(label)}</span></div>' for label, status in steps) + '</div>' if steps else '<div class="goal">no progress line yet</div>'
        current = next((index + 1 for index, (_, status) in enumerate(steps) if status in {"c", "b"}), None)
        next_step = current or next((index + 1 for index, (_, status) in enumerate(steps) if not status), len(steps))
        step_count = f'<span>step <b>{next_step} of {len(steps)}</b></span>' if steps else ""
        sentence = re.split(r"(?<=[.!?])\s+", one_line(text), maxsplit=1)[0]
        replies = snapshot.data[3][lead]
        answer_index = bisect.bisect_right(replies, report_at)
        now_class = "now"
        if answer_index < len(replies):
            answered_at = replies[answer_index].astimezone(LOCAL_ZONE).strftime("%H:%M")
            sentence = f"answered {answered_at}: {sentence}"
            now_class += " goal"
        running = lead in running_roots
        pill = "run" if running else "park"
        status = "running" if running else "parked"
        rows.append(
            f'<div class="team"><div><div class="nm">{escape(snapshot.title(lead))}<span class="pill {pill}">{status}</span></div>'
            f'<div class="rp">{escape(snapshot.projects.get(snapshot.threads[lead]["projectId"], ""))}</div></div><div>{track}<div class="{now_class}">{escape(sentence)}</div><div class="m">{step_count}'
            f'<span>wait on CoS <b>{board_duration(wait_today(snapshot, lead, since, now))}</b></span>'
            f'<span>children <b>{len(children[lead])}</b></span><span>dead runs <b>{dead[lead] / 60:.1f} min</b></span>'
            f'<span>last report <b>{escape(age(report_at, now))}</b></span></div></div></div>'
        )
    finished = []
    for lead in reporting_leads:
        payload = snapshot.threads[lead]
        settled_at = timestamp(payload["settledAt"]) if payload.get("settledAt") else None
        done_at = snapshot.reports[lead][-1][0] if snapshot.done(lead) and report_kind(snapshot.reports[lead][-1][1]) == "done" else None
        if (settled_at and since <= settled_at < now and snapshot.settled(lead)) or (done_at and since <= done_at < now):
            finished.append(f'<b>{escape(snapshot.title(lead))}</b>')
    state = Path(__file__).resolve().parent.parent / "state.md"
    needs = state_lines(state, "Needs Tobias")
    coming = state_lines(state, "Coming to you")
    html = Template(Path(__file__).with_name("board.html").read_text()).substitute(
        updated=local_now.strftime("%H:%M"), needs_count=len(needs),
        needs_lines="".join(f"<p>{markdown_text(line)}</p>" for line in needs) or "<p><b>Nothing waiting on you.</b></p>",
        coming=('<ul class="soon"><li><b>Coming to you</b></li>' + "".join(f"<li>{markdown_text(line)}</li>" for line in coming) + '</ul>') if coming else "",
        teams="".join(rows), wait=board_duration(sum(wait_today(snapshot, lead, since, now) for lead in leads)),
        restart_dead=board_duration(restart), other_dead=board_duration(other), finished=" · ".join(finished),
    )
    out.write_text(html)
    print(out)


def main():
    parser = argparse.ArgumentParser(description="Chief-of-staff control CLI; T3 reads are read-only.", allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    brief = commands.add_parser("brief", description="Print the one-source team-brief preamble.", allow_abbrev=False)
    brief.add_argument("--short", action="store_true", help="Print only the report-trigger restatement.")
    commands.add_parser("restart-check", description="Refuse a T3 restart while runs outside CoS and its children are running.", allow_abbrev=False)
    commit_parser = commands.add_parser("commit", description="Commit only named paths, pull/rebase with autostash, then push once.", allow_abbrev=False)
    commit_parser.add_argument("message", metavar="MSG")
    commit_parser.add_argument("paths", nargs="+", metavar="PATH")
    commands.add_parser(
        "census", description="Print unanswered reports, dead leads, unreported idle gates, unused child completions, queued messages, settle candidates and live runs. Oldest first; silence means no action. Report kinds and completion/usage candidates are heuristics.", allow_abbrev=False,
    )
    board = commands.add_parser(
        "board", description="Write the fixed-design board from T3 and state.md. Today is Europe/Copenhagen. Wait sums today's reports to their next CoS send, including pending waits ending at now or settlement; one reply may answer several reports. Dead-run time is clipped to today. Restart clusters have at least three distinct roots ending within ten seconds. Children count distinct tasks started today, including native subagents when stored. Done uses the latest report kind, not the status of a completed turn.", allow_abbrev=False,
    )
    board.add_argument("--out", type=Path, default=Path("/tmp/cos-board.html"), metavar="PATH")
    metrics = commands.add_parser(
        "metrics", description="Measure CoS messages, next-send delays, idle-lead gaps and turn durations from local T3 V2 SQLite.",
        epilog="Window is [since, until). ISO timestamps need a timezone. Defaults: first CoS report/run to now. No message text is printed.", allow_abbrev=False,
    )
    metrics.add_argument("--since", type=timestamp, metavar="ISO")
    metrics.add_argument("--until", type=timestamp, metavar="ISO")
    args = parser.parse_args()
    try:
        if args.command == "brief":
            text = Path(__file__).with_name("brief.md").read_text().replace("{cos_thread}", COS_THREAD_ID)
            if args.short:
                text = f"CoS-thread: {COS_THREAD_ID}\n\n" + text.split("## Report back\n", 1)[1].lstrip()
            print(text, end="")
            return 0
        if args.command == "commit":
            return commit(args.message, args.paths)
        with closing(open_readonly(STORE_PATH)) as db:
            data = load_data(db)
            snapshot = Snapshot(db, data) if args.command != "metrics" else None
        now = datetime.now(timezone.utc)
        if args.command == "restart-check":
            return restart_check(snapshot)
        if args.command == "census":
            census(snapshot, now)
        elif args.command == "board":
            write_board(snapshot, now, args.out)
        else:
            until = args.until or now
            reports = [at for entries in data[2].values() for at, _ in entries]
            starts = [start for start, _, _ in data[4][COS_THREAD_ID]]
            since = args.since or min(reports + starts, default=until)
            if since >= until:
                raise ValueError("--since must be earlier than --until")
            report(data, STORE_PATH, since, until)
    except subprocess.CalledProcessError as error:
        print(f"cos: git {error.cmd[1]} failed (exit {error.returncode}); stopped", file=sys.stderr)
        return error.returncode
    except (OSError, sqlite3.Error, ValueError, KeyError, TypeError) as error:
        print(f"cos: {type(error).__name__}; check the read-only T3 store, state.md and output path; use --help", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
