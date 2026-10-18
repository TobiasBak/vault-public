#!/usr/bin/env python3
import argparse
import bisect
from collections import Counter, defaultdict
from contextlib import closing
from datetime import datetime, timedelta, timezone
from html import escape
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import statistics
from string import Template
import subprocess
import sys
import tomllib
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


STATE_DIR = Path.home() / ".local/state/chief-of-staff"
COS_THREAD_ID = (STATE_DIR / "cos-thread").read_text().strip()
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
            if sender is None:
                continue
            if sender not in threads:
                raise ValueError("A CoS report has no stored sender thread")
            incoming[sender].append((at, report_kind(payload.get("text", ""))))
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
    print("Kinds: explicit [kind] first, then PR URL + 40-hex SHA, Tobias decision, blocked, go request, done; keyword heuristics.")
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
    print("\nBlocked time: each blocked report to the lead's next run start; clipped to the window.")
    print("Reports are summed separately; open intervals end at --until.")
    blocked_rows = []
    for lead in leads:
        intervals, open_count = blocked_intervals(incoming[lead], runs[lead], since, until)
        blocked_rows.append((threads[lead][0], len(intervals), duration(sum(intervals)), open_count))
    table(("Lead", "reports", "blocked", "open"), blocked_rows)
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


def blocked_intervals(reports, runs, since, until):
    starts = sorted(start for start, _, _ in runs)
    intervals = []
    open_count = 0
    for at, kind in reports:
        if kind != "blocked" or at >= until:
            continue
        index = bisect.bisect_right(starts, at)
        next_start = starts[index] if index < len(starts) else until
        end = min(next_start, until)
        start = max(at, since)
        if start < end:
            intervals.append((end - start).total_seconds())
            open_count += next_start >= until
    return intervals, open_count


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


def quota():
    try:
        credentials = json.loads((Path.home() / ".claude/.credentials.json").read_text())
        token = credentials["claudeAiOauth"]["accessToken"]
        if not isinstance(token, str) or not token:
            raise ValueError
    except Exception:
        print("opus_ui_team: unknown (credentials unavailable)")
        return 1
    try:
        request = Request(
            "https://api.anthropic.com/api/oauth/usage",
            headers={"Authorization": f"Bearer {token}", "anthropic-beta": "oauth-2025-04-20"},
        )
        with urlopen(request, timeout=15) as response:
            usage = json.load(response)
    except HTTPError as error:
        print(f"opus_ui_team: unknown (HTTP {error.code})")
        return 1
    except Exception:
        print("opus_ui_team: unknown (request failed)")
        return 1
    try:
        windows = []
        for name, window in usage.items():
            if window is None or not isinstance(window, dict) or "resets_at" not in window:
                continue
            utilization = window["utilization"]
            if (not re.fullmatch(r"[a-z][a-z0-9_]*", name)
                    or isinstance(utilization, bool) or not isinstance(utilization, (int, float))
                    or not math.isfinite(utilization) or utilization < 0):
                raise ValueError
            resets = timestamp(window["resets_at"]).isoformat(timespec="minutes").replace("+00:00", "Z")
            windows.append((name, utilization, resets))
        if not {"five_hour", "seven_day"} <= {name for name, _, _ in windows}:
            raise ValueError
    except Exception:
        print("opus_ui_team: unknown (invalid usage response)")
        return 1
    for name, utilization, resets in windows:
        print(f"{name} {utilization:g}% resets {resets}")
    limited = next(((name, utilization) for name, utilization, _ in windows if utilization >= 60), None)
    if limited:
        print(f"opus_ui_team: wait ({limited[0]} at {limited[1]:g}%)")
    else:
        teams = 1 if any(utilization >= 40 for _, utilization, _ in windows) else 2
        print(f"opus_ui_team: allowed (max {teams} live, 1 Opus child per team)")
    return 0


def commit(message, paths):
    subprocess.run(["git", "add", "--", *paths], check=True)
    subprocess.run(["git", "commit", "-m", message, "--", *paths], check=True)
    subprocess.run(["git", "pull", "--rebase", "--autostash"], check=True)
    subprocess.run(["git", "push"], check=True)
    return 0


def github_repositories(project_roots):
    repositories = defaultdict(set)
    for project, root in project_roots.items():
        try:
            result = subprocess.run(
                ["git", "-C", root, "remote", "-v"], capture_output=True, text=True, timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode:
            continue
        remotes = []
        for line in result.stdout.splitlines():
            fields = line.split()
            if len(fields) < 2:
                continue
            match = re.fullmatch(r"(?:https?://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/\s]+/[^/\s]+?)(?:\.git)?/?", fields[1], re.I)
            if match:
                remotes.append((fields[0] != "origin", match[1]))
        if remotes:
            repositories[min(remotes)[1]].add(project)
    return repositories


def gh_json(arguments, timeout=15):
    try:
        result = subprocess.run(["gh", *arguments], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ValueError("gh timed out") from None
    except OSError:
        raise ValueError("gh unavailable") from None
    if result.returncode:
        raise ValueError(f"gh failed (exit {result.returncode})")
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise ValueError("invalid gh response") from None


def capacity(snapshot, repositories):
    for repo, projects in sorted(repositories.items()):
        live = sum(snapshot.threads[lead].get("projectId") in projects
                   and snapshot.visible(lead) and not snapshot.settled(lead) for lead in snapshot.leads)
        try:
            issues = gh_json(["issue", "list", "--repo", repo, "--state", "open", "--label", "ready",
                              "--search", "-label:in-progress", "--limit", "10000", "--json", "number"])
            if not isinstance(issues, list) or len(issues) >= 10000:
                raise ValueError("issue result incomplete")
            numbers = sorted(int(issue["number"]) for issue in issues)
        except (ValueError, KeyError, TypeError) as error:
            reason = str(error) if isinstance(error, ValueError) else "invalid gh response"
            print(f"capacity {repo}: unknown ({reason})")
            continue
        if numbers:
            print(f"capacity {repo}: live={live} ready_unlaunched={len(numbers)} | " + " ".join(f"#{number}" for number in numbers[:5]))


MERGED_PRS_QUERY = """
query($search: String!, $endCursor: String) {
  search(query: $search, type: ISSUE, first: 25, after: $endCursor) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes { ... on PullRequest {
      mergedAt
      labels(first: 100) { nodes { name } pageInfo { hasNextPage } }
      closingIssuesReferences(first: 100) {
        pageInfo { hasNextPage }
        nodes { labels(first: 100) { nodes { name } pageInfo { hasNextPage } } }
      }
    } }
  }
}
"""


def merged_pr_counts(repo, since, until):
    # Search by UTC dates, then apply the exact half-open timestamp window locally.
    search = f"repo:{repo} is:pr is:merged merged:{since.date()}..{until.date()}"
    pages = gh_json(["api", "graphql", "--paginate", "--slurp", "-f", f"query={MERGED_PRS_QUERY}",
                     "-f", f"search={search}"], timeout=30)
    counts = Counter(product=0, infra=0)
    for page in pages:
        if page.get("errors"):
            raise ValueError("GitHub query failed")
        result = page["data"]["search"]
        if result["issueCount"] > 1000:
            raise ValueError("PR search exceeds GitHub's 1000-result limit")
        for pr in result["nodes"]:
            if not since <= timestamp(pr["mergedAt"]) < until:
                continue
            issues = pr["closingIssuesReferences"]
            label_sets = [pr["labels"], *(issue["labels"] for issue in issues["nodes"])]
            if issues["pageInfo"]["hasNextPage"] or any(labels["pageInfo"]["hasNextPage"] for labels in label_sets):
                raise ValueError("PR labels or closing issues incomplete")
            infra = any(label["name"].casefold() == "infra" for labels in label_sets for label in labels["nodes"])
            counts["infra" if infra else "product"] += 1
    return counts


def merged_pr_report(repositories, since, until):
    print("\nMerged PRs: infra when the PR or a closing issue carries the infra label; otherwise product.")
    rows = []
    total = Counter(product=0, infra=0)
    unknown = 0
    for repo in sorted(repositories):
        try:
            counts = merged_pr_counts(repo, since, until)
        except (ValueError, KeyError, TypeError) as error:
            reason = str(error) if isinstance(error, ValueError) else "invalid gh response"
            rows.append((repo, "unknown", "unknown", reason))
            unknown += 1
            continue
        total.update(counts)
        rows.append((repo, counts["product"], counts["infra"], sum(counts.values())))
    rows.append(("TOTAL" if not unknown else "TOTAL (known repos only)", total["product"], total["infra"], sum(total.values())))
    table(("Repository", "product", "infra", "total / error"), rows)


MAIN_HEALTH_REPOS = ("TobiasBak/orderready", "TobiasBak/orderready-platform")
HEALTH_QUERY = """
query($owner: String!, $name: String!, $endCursor: String) {
  repository(owner: $owner, name: $name) {
    ref(qualifiedName: "refs/heads/main") {
      branchProtectionRule { requiredStatusCheckContexts }
      target { ... on Commit {
        oid tree { oid }
        statusCheckRollup { contexts(first: 100) {
          pageInfo { hasNextPage }
          nodes {
            ... on CheckRun {
              name status conclusion databaseId startedAt completedAt
              checkSuite { app { slug } workflowRun { workflow { name } } }
            }
            ... on StatusContext { context state createdAt }
          }
        } }
      } }
    }
    pullRequests(states: OPEN, first: 50, after: $endCursor) {
      pageInfo { hasNextPage endCursor }
      nodes { number commits(last: 1) { nodes { commit {
        oid tree { oid }
        statusCheckRollup { contexts(first: 100) {
          pageInfo { hasNextPage }
          nodes {
            ... on CheckRun {
              name status conclusion databaseId startedAt completedAt
              checkSuite { app { slug } workflowRun { workflow { name } } }
            }
            ... on StatusContext { context state createdAt }
          }
        } }
      } } } }
    }
  }
}
"""


def recorded_checks(commit):
    rollup = commit["statusCheckRollup"]
    if rollup is None:
        return {}, False
    contexts = rollup["contexts"]
    latest = {}
    for node in contexts["nodes"]:
        name = node.get("name") or node["context"]
        at = node.get("createdAt") or node.get("startedAt") or node.get("completedAt") or ""
        if "context" in node:
            state = node["state"].lower()
            producer = ("status",)
            source = "GitHub commit status"
        else:
            state = "pending" if node["status"] != "COMPLETED" else (node["conclusion"] or "unknown").lower()
            suite = node.get("checkSuite") or {}
            app = (suite.get("app") or {}).get("slug", "unknown-app")
            workflow = ((suite.get("workflowRun") or {}).get("workflow") or {}).get("name", "")
            producer = ("check-run", app, workflow)
            source = f"GitHub check run {one_line(app + '/' + workflow)}"
        order = (node.get("databaseId") or 0, at)
        check = {"name": name, "state": state, "at": node.get("completedAt") or at,
                 "order": order, "source": source}
        key = (name, producer)
        if key not in latest or order >= latest[key]["order"]:
            latest[key] = check
    grouped = defaultdict(list)
    for (name, _), check in latest.items():
        grouped[name].append(check)
    return dict(grouped), contexts["pageInfo"]["hasNextPage"]


def read_git(root, *arguments):
    try:
        result = subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("local Git evidence unavailable") from None
    if result.returncode:
        raise ValueError("exact commit unavailable locally")
    return result.stdout.strip()


def orderready_static(commits):
    root = Path.home() / "code/orderready"
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "orderready/verdicts"
    directory = cache / ("static-" + hashlib.sha256(b"static").hexdigest())
    by_tree = defaultdict(list)
    trees = {commit["tree"]["oid"] for commit in commits}
    for path in directory.glob("*.json"):
        if path.name == "last-pass.json":
            continue
        record = json.loads(path.read_text())
        if record.get("tree") in trees:
            by_tree[record["tree"]].append((path, record))
    advisory_url = "https://github.com/RustSec/advisory-db"
    cargo_home = Path(os.environ.get("CARGO_HOME") or Path.home() / ".cargo")
    revisions = set()
    for database in (cargo_home / "advisory-dbs").glob("advisory-db-*"):
        if read_git(database, "config", "--get", "remote.origin.url").rstrip("/").removesuffix(".git") == advisory_url:
            revisions.add(read_git(database, "rev-parse", "HEAD"))
    results = {}
    for commit in commits:
        sha = commit["oid"]
        try:
            config = tomllib.loads(read_git(root, "show", f"{sha}:deny.toml")).get("advisories", {})
            if config.get("db-path") or config.get("db-urls", [advisory_url]) != [advisory_url]:
                raise ValueError("custom advisory database is not observed")
            if len(revisions) != 1:
                raise ValueError("current advisory revision unavailable or ambiguous")
            inputs = {f"advisory:{advisory_url}": next(iter(revisions))}
            matches = [(path, record) for path, record in by_tree[commit["tree"]["oid"]]
                       if {key: value for key, value in record["inputs"].items() if key.startswith("advisory:")} == inputs
                       and record["verdict"] in {"pass", "fail"}]
            if not matches:
                raise ValueError("no static receipt for exact tree and current local advisory revision")
            path, record = max(matches, key=lambda entry: entry[1]["created"])
            results[sha] = ({"name": "static", "state": "failure" if record["verdict"] == "fail" else "success",
                             "at": iso(datetime.fromtimestamp(record["created"], timezone.utc)), "source": str(path)}, None)
        except (ValueError, KeyError, TypeError) as error:
            results[sha] = (None, str(error) if isinstance(error, ValueError) else "invalid static receipt")
    return results


def print_main_health(repo, main, checks, required, prs, gaps):
    failed = {"failure", "error", "timed_out", "cancelled", "action_required", "startup_failure"}
    relevant = {name: evidence for name, evidence in checks.items()
                if name in required or re.search(r"static|cargo[-_ /:]?deny", name, re.I)}
    red = {name for name, evidence in relevant.items() if any(check["state"] in failed for check in evidence)}
    prefix = f"main-health {repo} main@{main['oid'][:12]}"
    for name, evidence in sorted(relevant.items()):
        for check in evidence:
            state = "RED" if check["state"] in failed else check["state"]
            at = check["at"] or "unknown"
            print(f"{prefix}: {state} {one_line(name)} since {at} (recorded result; earlier onset unknown) | {check['source']}")
    if not relevant:
        gaps.append("no recorded required/static result on main")
    for name in sorted(required - checks.keys()):
        gaps.append(f"required check {one_line(name)} has no result on main")
    groups = defaultdict(set)
    for number, pr_checks in prs:
        for name, evidence in pr_checks.items():
            if any(check["state"] in failed for check in evidence):
                groups[name].add(number)
    for name in sorted(red | groups.keys()):
        numbers = sorted(groups[name])
        detail = " ".join(f"#{number}" for number in numbers) or "none"
        print(f"main-health {repo}: failing PRs {one_line(name)}={len(numbers)} | {detail}")
        if name in red or len(numbers) >= 2:
            reason = "main red" if name in red else "same check fails on multiple PRs"
            print(f"SHARED BLOCKER {repo}: {one_line(name)} | {reason} | failing PRs={len(numbers)} {detail}")
    for gap in dict.fromkeys(gaps):
        print(f"GAP main-health {repo}: {gap}")


def main_health():
    print("Main health: existing results only; timestamps date recorded results, not continuous-red history.")
    for repo in MAIN_HEALTH_REPOS:
        try:
            owner, name = repo.split("/")
            pages = gh_json(["api", "graphql", "--paginate", "--slurp", "-f", f"query={HEALTH_QUERY}",
                             "-f", f"owner={owner}", "-f", f"name={name}"], timeout=30)
            main = None
            prs = {}
            required = {"gate"} if repo == "TobiasBak/orderready" else set()
            gaps = []
            for page in pages:
                if page.get("errors"):
                    raise ValueError("GitHub main-health query failed")
                repository = page["data"]["repository"]
                branch = repository["ref"]
                target = branch["target"]
                if main and target["oid"] != main["oid"]:
                    raise ValueError("main moved during census; retry")
                main = target
                protection = branch["branchProtectionRule"]
                required.update((protection or {}).get("requiredStatusCheckContexts") or [])
                for pr in repository["pullRequests"]["nodes"]:
                    prs[pr["number"]] = pr["commits"]["nodes"][-1]["commit"]
            if main is None:
                raise ValueError("main result unavailable")
            checks, truncated = recorded_checks(main)
            if truncated:
                gaps.append("main check list exceeds 100 results")
            pr_checks = []
            for number, commit in prs.items():
                found, truncated = recorded_checks(commit)
                pr_checks.append((number, found))
                if truncated or not found:
                    gaps.append(f"PR #{number} GitHub check results {'incomplete' if truncated else 'absent'}")
            if repo == "TobiasBak/orderready":
                try:
                    static = orderready_static([main, *prs.values()])
                    for commit, found in [(main, checks), *((prs[number], found) for number, found in pr_checks)]:
                        check, gap = static[commit["oid"]]
                        if check:
                            found.setdefault("static", []).append(check)
                        elif commit is main:
                            gaps.append(gap)
                except (OSError, ValueError, KeyError, TypeError):
                    gaps.append("local static receipts unavailable or invalid")
            else:
                gaps.append("scripts/check.py records no durable main result; promotion Actions do not establish main health")
            print_main_health(repo, main, checks, required, pr_checks, gaps)
        except (ValueError, KeyError, TypeError, IndexError) as error:
            reason = str(error) if isinstance(error, ValueError) else "invalid GitHub main-health response"
            print(f"GAP main-health {repo}: {reason}")


def stalled_queues(snapshot, now):
    for thread in snapshot.threads:
        if not snapshot.visible(thread) or snapshot.settled(thread) or thread in snapshot.running:
            continue
        latest = max(snapshot.runs[thread], key=lambda run: run[4], default=None)
        if latest and latest[3] == "queued" and now - latest[4] > timedelta(minutes=2):
            at = latest[4]
            yield at, f"stalled queue {age(at, now)}: latest run queued with nothing running; cancel the queued run and resend | {snapshot.title(thread)} | {send_hint(snapshot, thread)}"


def census(snapshot, now, repositories):
    main_health()
    capacity(snapshot, repositories)
    items = list(stalled_queues(snapshot, now))
    state = STATE_DIR / "state.md"
    state_size = state.stat().st_size
    if state_size > 10_240:
        print(f"WARNING: state.md is {state_size:,} bytes; exceeds the 10,240-byte budget")
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
            items.append((at, f"settle candidate {age(at, now)}: {reason} | {snapshot.title(thread)} | {send_hint(snapshot, thread)} | settle:{thread}"))
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
    state = STATE_DIR / "state.md"
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
    commands.add_parser("quota", description="Print Claude plan utilization and the live Opus UI team limit: two while every window is below 40%, one at 40% or above, none at 60% or above. Each team runs at most one Opus child. Non-UI leads always use Sol; check UI quota before launching and on every heartbeat.", allow_abbrev=False)
    commands.add_parser("restart-check", description="Refuse a T3 restart while runs outside CoS and its children are running.", allow_abbrev=False)
    commit_parser = commands.add_parser("commit", description="Commit only named paths, pull/rebase with autostash, then push once.", allow_abbrev=False)
    commit_parser.add_argument("message", metavar="MSG")
    commit_parser.add_argument("paths", nargs="+", metavar="PATH")
    commands.add_parser(
        "census", description="Print recorded main health and shared blockers, ready-issue capacity, unanswered reports, dead leads, unreported idle gates, unused child completions, stalled queues, queued messages, settle candidates and live runs. Oldest first; silence means no action. Report kinds and completion/usage candidates are heuristics.", allow_abbrev=False,
    )
    board = commands.add_parser(
        "board", description="Write the fixed-design board from T3 and state.md. Today is Europe/Copenhagen. Wait sums today's reports to their next CoS send, including pending waits ending at now or settlement; one reply may answer several reports. Dead-run time is clipped to today. Restart clusters have at least three distinct roots ending within ten seconds. Children count distinct tasks started today, including native subagents when stored. Done uses the latest report kind, not the status of a completed turn.", allow_abbrev=False,
    )
    board.add_argument("--out", type=Path, default=Path("/tmp/cos-board.html"), metavar="PATH")
    metrics = commands.add_parser(
        "metrics", description="Measure CoS messages, next-send delays, blocked time, idle-lead gaps and turn durations from local T3 V2 SQLite, plus merged product/infra PRs from GitHub's current labels.",
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
        if args.command == "quota":
            return quota()
        if args.command == "commit":
            return commit(args.message, args.paths)
        with closing(open_readonly(STORE_PATH)) as db:
            data = load_data(db)
            snapshot = Snapshot(db, data) if args.command != "metrics" else None
            project_roots = dict(db.execute("SELECT project_id, workspace_root FROM projection_projects WHERE deleted_at IS NULL"))
        now = datetime.now(timezone.utc)
        if args.command == "restart-check":
            return restart_check(snapshot)
        if args.command == "census":
            census(snapshot, now, github_repositories(project_roots))
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
            merged_pr_report(github_repositories(project_roots), since, until)
    except subprocess.CalledProcessError as error:
        print(f"cos: git {error.cmd[1]} failed (exit {error.returncode}); stopped", file=sys.stderr)
        return error.returncode
    except (OSError, sqlite3.Error, ValueError, KeyError, TypeError) as error:
        print(f"cos: {type(error).__name__}; check the read-only T3 store, state.md and output path; use --help", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
