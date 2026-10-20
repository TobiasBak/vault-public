import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

with patch.object(Path, "read_text", return_value="test-cos"):
    import cos


AT = "2026-10-18T12:00:00Z"
REPO = "TobiasBak/orderready"


def commit(state=None, checks=None):
    nodes = checks if checks is not None else ([{"context": "static", "state": state, "createdAt": AT}] if state else [])
    return {"oid": "a" * 40, "tree": {"oid": "b" * 40}, "statusCheckRollup": {
        "contexts": {"nodes": nodes, "pageInfo": {"hasNextPage": False}},
    }}


def page(main, prs=()):
    return {"data": {"repository": {
        "ref": {"target": main, "branchProtectionRule": None},
        "pullRequests": {"nodes": [
            {"number": number, "commits": {"nodes": [{"commit": result}]}}
            for number, result in prs
        ], "pageInfo": {"hasNextPage": False, "endCursor": None}},
    }}}


class MainHealthTests(unittest.TestCase):
    def census_health(self, main, prs=(), static=None):
        evidence = static or {main["oid"]: (None, "no static receipt")}
        out = io.StringIO()
        with patch.object(cos, "gah_repositories", return_value=({}, [])), patch.object(cos, "MAIN_HEALTH_REPOS", (REPO,)), patch.object(cos, "gh_json", return_value=[page(main, prs)]), patch.object(cos, "orderready_static", return_value=evidence), contextlib.redirect_stdout(out):
            cos.main_health()
        return out.getvalue()

    def test_red_main_raises_without_any_pr(self):
        output = self.census_health(commit("FAILURE"))
        self.assertIn(f"SHARED BLOCKER {REPO}: static | main red | failing PRs=0", output)
        self.assertIn(f"RED static since {AT}", output)

    def test_green_main_and_pr_stay_silent(self):
        main = commit("SUCCESS")
        output = self.census_health(main, [(12, commit("SUCCESS"))], {
            main["oid"]: ({"name": "static", "state": "success", "at": AT, "source": "fixture"}, None),
        })
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("GAP", output)

    def test_same_check_on_two_prs_raises_with_green_main(self):
        output = self.census_health(commit("SUCCESS"), [(12, commit("FAILURE")), (34, commit("FAILURE"))])
        self.assertIn(f"SHARED BLOCKER {REPO}: static | same check fails on multiple PRs | failing PRs=2 #12 #34", output)
        self.assertNotIn("SHARED BLOCKER", self.census_health(commit("SUCCESS"), [(12, commit("FAILURE"))]))

    def test_local_pass_cannot_hide_github_static_failures(self):
        main = commit(checks=[{"context": "static", "state": "FAILURE", "createdAt": AT}])
        local = {main["oid"]: ({"name": "static", "state": "success", "at": "2026-10-18T11:00:00Z", "source": "local receipt"}, None)}
        output = self.census_health(main, [(12, main), (34, main)], local)
        self.assertIn(f"RED static since {AT}", output)
        self.assertIn("success static since 2026-10-18T11:00:00Z", output)
        self.assertIn(f"SHARED BLOCKER {REPO}: static | main red | failing PRs=2 #12 #34", output)

    def test_github_check_run_cannot_hide_commit_status_failure(self):
        main = commit(checks=[
            {"name": "static", "status": "COMPLETED", "conclusion": "SUCCESS", "databaseId": 10,
             "startedAt": "2026-10-18T11:00:00Z", "completedAt": "2026-10-18T11:00:00Z"},
            {"context": "static", "state": "FAILURE", "createdAt": AT},
        ])
        output = self.census_health(main, [(12, main), (34, main)])
        self.assertIn(f"RED static since {AT}", output)
        self.assertIn("GitHub commit status", output)
        self.assertIn("GitHub check run", output)
        self.assertIn(f"SHARED BLOCKER {REPO}: static | main red | failing PRs=2 #12 #34", output)

    def test_same_named_checks_from_different_workflows_remain_visible(self):
        checks = [{"name": "static", "status": "COMPLETED", "conclusion": conclusion, "databaseId": index,
                   "startedAt": AT, "completedAt": AT,
                   "checkSuite": {"app": {"slug": "github-actions"}, "workflowRun": {"workflow": {"name": workflow}}}}
                  for index, workflow, conclusion in [(1, "Required", "FAILURE"), (2, "Other", "SUCCESS")]]
        output = self.census_health(commit(checks=checks))
        self.assertIn(f"SHARED BLOCKER {REPO}: static | main red", output)
        self.assertIn("github-actions/Required", output)
        self.assertIn("github-actions/Other", output)

    def test_same_check_groups_failures_across_sources(self):
        main = commit("SUCCESS")
        first = commit(checks=[{"context": "static", "state": "FAILURE", "createdAt": AT}])
        first["oid"] = "c" * 40
        second = commit(checks=[{"context": "static", "state": "SUCCESS", "createdAt": AT}])
        second["oid"] = "d" * 40
        local = {result["oid"]: ({"name": "static", "state": state, "at": AT, "source": "local receipt"}, None)
                 for result, state in [(main, "success"), (first, "success"), (second, "failure")]}
        output = self.census_health(main, [(12, first), (34, second)], local)
        self.assertIn(f"SHARED BLOCKER {REPO}: static | same check fails on multiple PRs | failing PRs=2 #12 #34", output)

    def test_absent_main_results_are_a_gap_not_green(self):
        output = self.census_health(commit())
        self.assertIn("GAP main-health", output)
        self.assertIn("no recorded required/static result on main", output)
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("success", output)

    def test_pending_rerun_replaces_old_failure_and_required_action_check_is_red(self):
        checks = [
            {"name": "static", "status": "COMPLETED", "conclusion": "FAILURE", "databaseId": 1, "startedAt": AT, "completedAt": AT},
            {"name": "static", "status": "QUEUED", "conclusion": None, "databaseId": 2, "startedAt": None, "completedAt": None},
        ]
        self.assertNotIn("SHARED BLOCKER", self.census_health(commit(checks=checks)))
        response = page(commit(checks=checks[:1]))
        response["data"]["repository"]["ref"]["branchProtectionRule"] = {"requiredStatusCheckContexts": ["static"]}
        with patch.object(cos, "gah_repositories", return_value=({}, [])), patch.object(cos, "MAIN_HEALTH_REPOS", ("TobiasBak/orderready-platform",)), patch.object(cos, "gh_json", return_value=[response]), contextlib.redirect_stdout(io.StringIO()) as out:
            cos.main_health()
        self.assertIn("SHARED BLOCKER TobiasBak/orderready-platform: static", out.getvalue())

class PlatformQualificationTests(unittest.TestCase):
    repo = "TobiasBak/orderready-platform"
    sha = "a" * 40

    def receipt(self):
        return {
            "format_version": 1, "head_sha": self.sha,
            "started_at": "2026-10-18T11:00:00Z", "finished_at": AT,
            "result": "passed", "worktree_clean": True,
            "checks": {name: {"status": "passed", "exit_code": 0}
                       for name in ("lint", "format", "types", "openapi", "promotion_config", "tests")},
        }

    def census_health(self, receipt, file_sha=None, xdg=True):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            state = home / "state" if xdg else home / ".local/state"
            path = state / "orderready-platform/checks" / f"{file_sha or self.sha}.json"
            if receipt is not None:
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps(receipt))
            with patch.object(Path, "home", return_value=home), patch.dict("os.environ", {"XDG_STATE_HOME": str(state) if xdg else ""}), patch.object(cos, "gah_repositories", return_value=({}, [])), patch.object(cos, "MAIN_HEALTH_REPOS", (self.repo,)), patch.object(cos, "gh_json", return_value=[page(commit())]), patch.object(cos.subprocess, "run", side_effect=AssertionError("census must only read receipts")), contextlib.redirect_stdout(io.StringIO()) as out:
                cos.main_health()
            return out.getvalue()

    def test_green_exact_main_in_xdg_and_default_state_home(self):
        for xdg in (True, False):
            with self.subTest(xdg=xdg):
                output = self.census_health(self.receipt(), xdg=xdg)
                self.assertIn(f"PROMOTION/FULL-SUITE {self.repo} main@{self.sha[:12]}: success scripts/check.py", output)
                self.assertIn("not required on main; production health unknown", output)
                self.assertNotIn("SHARED BLOCKER", output)

    def test_full_suite_failure_is_visible_but_does_not_make_main_red(self):
        receipt = self.receipt()
        receipt["result"] = "failed"
        receipt["checks"]["lint"] = {"status": "failed", "exit_code": 1}
        receipt["checks"]["tests"] = {"status": "failed", "exit_code": None, "error": "OSError"}
        output = self.census_health(receipt)
        self.assertIn(f"PROMOTION/FULL-SUITE {self.repo} main@{self.sha[:12]}: failure scripts/check.py", output)
        self.assertIn("failed checks: lint, tests", output)
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("main red", output)
        self.assertNotIn("success", output)

    def test_running_is_pending(self):
        receipt = self.receipt()
        receipt.update(result="running", finished_at=None)
        receipt["checks"]["tests"] = {"status": "running", "exit_code": None}
        output = self.census_health(receipt)
        self.assertIn("pending scripts/check.py", output)
        self.assertNotIn("success", output)
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertIn("not required on main", output)

    def test_missing_full_suite_is_unobserved_not_required_on_main(self):
        output = self.census_health(None)
        self.assertIn(f"PROMOTION/FULL-SUITE {self.repo} main@{self.sha[:12]}: unobserved", output)
        self.assertIn("not required on main", output)
        self.assertNotIn(f"GAP main-health {self.repo}: missing scripts/check.py", output)
        self.assertNotIn("success", output)

    def test_stale_receipt_never_establishes_current_main_health(self):
        stale = self.receipt()
        stale["head_sha"] = "c" * 40
        for file_sha in (self.sha, stale["head_sha"]):
            with self.subTest(file_sha=file_sha):
                output = self.census_health(stale, file_sha=file_sha)
                self.assertIn(f"PROMOTION/FULL-SUITE {self.repo} main@{self.sha[:12]}: unobserved", output)
                self.assertIn("stale SHA" if file_sha == self.sha else "missing scripts/check.py full-suite receipt", output)
                self.assertNotIn("success", output)

    def test_invalid_receipts_cannot_report_green_or_leak_field_contents(self):
        mutations = [
            lambda r: r.update(format_version=2),
            lambda r: r.update(format_version=True),
            lambda r: r.update(finished_at=None),
            lambda r: r.update(finished_at="do-not-print-this"),
            lambda r: r.update(worktree_clean=False),
            lambda r: r.update(result="invalid"),
            lambda r: r["checks"].pop("types"),
            lambda r: r["checks"]["tests"].update(exit_code=1),
            lambda r: r["checks"]["tests"].update(exit_code=False),
            lambda r: r["checks"]["tests"].update(status="not_run", exit_code=None),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                receipt = self.receipt()
                mutate(receipt)
                output = self.census_health(receipt)
                self.assertIn(f"PROMOTION/FULL-SUITE {self.repo} main@{self.sha[:12]}: unobserved", output)
                self.assertNotIn("success", output)
                self.assertNotIn("do-not-print-this", output)


class ReaderCliTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.state = self.home / ".local/state/chief-of-staff"
        self.state.mkdir(parents=True)
        (self.state / "state.md").write_text("")
        self.store = self.home / "synthetic.sqlite"
        self.db = sqlite3.connect(self.store)
        self.addCleanup(self.db.close)
        self.db.executescript("""
            CREATE TABLE orchestration_v2_projection_threads (thread_id, title, payload_json);
            CREATE TABLE orchestration_v2_projection_messages
                (thread_id, created_at, payload_json, role, message_id, run_id, streaming);
            CREATE TABLE orchestration_v2_projection_runs
                (run_id, thread_id, status, completed_at, payload_json, requested_at);
            CREATE TABLE projection_projects (project_id, title, workspace_root, deleted_at);
            CREATE TABLE orchestration_v2_projection_context_transfers
                (source_thread_id, target_thread_id, target_run_id, payload_json, type, status);
            CREATE TABLE orchestration_v2_projection_subagents (subagent_id, thread_id, child_thread_id, started_at);
        """)
        self.thread(cos.COS_THREAD_ID, "fixture-chief")
        self.health = {}

    def git(self, root, *args):
        environment = {**os.environ, "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                       "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        return subprocess.run(["git", "-C", str(root), *args], env=environment,
                              check=True, capture_output=True, text=True).stdout.strip()

    def repository(self, path, remote, marker="owned"):
        path.mkdir(parents=True)
        self.git(path, "init", "-q", "-b", "main")
        (path / "deny.toml").write_text("[advisories]\n")
        (path / "gah.toml").write_text('check = "synthetic-static-check"\n')
        (path / "fixture.txt").write_text(marker)
        self.git(path, "add", ".")
        tree = self.git(path, "write-tree")
        sha = self.git(path, "commit-tree", tree, "-m", "Synthetic reader fixture")
        self.git(path, "update-ref", "refs/heads/main", sha)
        self.git(path, "remote", "add", "origin", remote)
        result = commit()
        result.update(oid=sha, tree={"oid": tree})
        return result

    def owned(self, name, repo):
        root = self.home / "git-at-home" / name / "main"
        result = self.repository(root, f"https://github.com/{repo}.git")
        (root.parent / "config.toml").write_text('branch = "main"\nmode = "direct"\n')
        self.log(root, [{"op": "merge", "at": cos.timestamp(AT).timestamp(),
                         "result": f"merged {result['oid']}", "check_path": "fast-path"}])
        self.db.execute("INSERT INTO projection_projects VALUES (?, ?, ?, NULL)", (name, name, str(root)))
        self.health[repo] = result
        return root, result

    def log(self, root, rows):
        (root.parent / "log.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))

    def thread(self, thread, title, **payload):
        payload = {"projectId": "fixture", "createdAt": AT, "updatedAt": AT, **payload}
        self.db.execute("INSERT INTO orchestration_v2_projection_threads VALUES (?, ?, ?)",
                        (thread, title, json.dumps(payload)))

    def message(self, sender, target, at, text):
        self.db.execute("INSERT INTO orchestration_v2_projection_messages VALUES (?, ?, ?, 'user', ?, NULL, 0)",
                        (target, at, json.dumps({"senderThreadId": sender, "text": text}),
                         f"thread-send:cos-synthetic-{sender}-{at}"))

    def stored_run(self, thread, start, end):
        self.db.execute("INSERT INTO orchestration_v2_projection_runs VALUES (?, ?, 'completed', ?, ?, ?)",
                        (f"run-{thread}", thread, end, json.dumps({"startedAt": start}), start))

    def cli(self, *arguments):
        self.db.commit()

        def github(args, **kwargs):
            if args[0] == "issue":
                return []
            if any(arg.startswith("search=") for arg in args):
                return [{"data": {"search": {"issueCount": 0, "nodes": []}}}]
            name = next(arg.removeprefix("name=") for arg in args if arg.startswith("name="))
            repo = next(repo for repo in self.health if repo.split("/")[1] == name)
            response = page(self.health[repo])
            # Even a legacy full-suite context must not invent a main-suite obligation.
            response["data"]["repository"]["ref"]["branchProtectionRule"] = {
                "requiredStatusCheckContexts": ["full-suite"]}
            return [response]

        with patch.object(Path, "home", return_value=self.home), patch.dict(os.environ, {
            "GAH_ROOT": str(self.home / "git-at-home"), "XDG_CACHE_HOME": "", "XDG_STATE_HOME": "", "CARGO_HOME": "",
        }), patch.object(cos, "STATE_DIR", self.state), patch.object(cos, "STORE_PATH", self.store), patch.object(cos, "gh_json", side_effect=github), patch.object(cos, "slow_steps"), patch.object(sys, "argv", ["cos.py", *arguments]), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cos.main(), 0)
        return out.getvalue()

    def test_metrics_show_typed_activity_and_local_landings_without_historical_noise(self):
        root, main = self.owned("fixture", "Example/reader-fixture")
        child_sha = main["oid"]
        failed_sha = self.git(root, "commit-tree", main["tree"]["oid"], "-p", child_sha, "-m", "Synthetic intermediate")
        main["oid"] = self.git(root, "commit-tree", main["tree"]["oid"], "-p", failed_sha, "-m", "Synthetic main landing")
        self.git(root, "update-ref", "refs/heads/main", main["oid"])
        detached = self.git(root, "commit-tree", main["tree"]["oid"], "-m", "Unlanded synthetic fixture")
        at = cos.timestamp("2026-10-18T12:01:00Z").timestamp()
        self.log(root, [
            {"op": "merge", "at": at, "result": result, "check_path": "fast-path"}
            for result in [f"merged {main['oid']}", f"merged {main['oid']}",
                           f"error: rejected {failed_sha}", f"landed {child_sha} on fixture's line",
                           "opened https://example.invalid/pull/1", "updated https://example.invalid/pull/1",
                           f"merged {detached}"]
        ])
        self.thread("reporter", "settled-reporter", settledAt=AT)
        self.thread("historical", "irrelevant-history")
        self.thread("blocker", "prewindow-blocker")
        self.thread("idle", "prewindow-idle")
        self.thread("child", "synthetic-child", lineage={"parentThreadId": "idle", "relationshipToParent": "subagent"})
        self.message("reporter", cos.COS_THREAD_ID, "2026-10-18T12:01:00Z", "[done] synthetic")
        self.message("reporter", cos.COS_THREAD_ID, "2026-10-18T12:02:00Z", "[go_request] synthetic")
        self.message(cos.COS_THREAD_ID, "reporter", "2026-10-18T12:03:00Z", "synthetic reply")
        self.message("historical", cos.COS_THREAD_ID, "2026-10-17T12:00:00Z", "[done] synthetic")
        self.message("blocker", cos.COS_THREAD_ID, "2026-10-18T11:30:00Z", "[blocked] synthetic")
        self.stored_run("idle", "2026-10-18T11:00:00Z", "2026-10-18T11:20:00Z")
        self.stored_run("child", "2026-10-18T11:25:00Z", "2026-10-18T11:40:00Z")
        output = self.cli("metrics", "--since", AT, "--until", "2026-10-18T12:10:00Z")
        self.assertIn(f"CoS-thread: {cos.COS_THREAD_ID} | fixture-chief", output)
        self.assertNotIn("irrelevant-history", output)
        messages = output.split("Lead messages\n")[1].split("Gate latency:")[0]
        for title in ("settled-reporter", "TOTAL"):
            self.assertIn([title, "2", "1", "0", "1", "0", "0", "0", "0", "1"],
                          [line.split() for line in messages.splitlines()])
        self.assertNotIn("prewindow-blocker", messages)
        self.assertRegex(output, r"prewindow-blocker\s+1\s+10.00m\s+1")
        self.assertRegex(output, r"prewindow-idle\s+1\s+10.00m\s+10.00m\s+1")
        prs, landings = output.split("Merged PRs:")[1].split("LOCAL GAH LANDING OBSERVATION")
        self.assertRegex(prs, r"TOTAL\s+0\s+0\s+0")
        self.assertRegex(landings, r"Example/reader-fixture\s+1\s+")
        self.assertRegex(landings, r"TOTAL \(local observations only\)\s+1")
        self.assertIn("not complete remote shipping", landings)
        self.assertIn("unclassified", landings)

    def test_finding_is_counted_without_becoming_blocked_or_done(self):
        self.thread("finder", "synthetic-finder")
        self.message("finder", cos.COS_THREAD_ID, "2026-10-18T12:01:00Z",
                     "[finding] The blocked check failed because its comparison was wrong; diagnosis is done.")
        self.message("finder", cos.COS_THREAD_ID, "2026-10-18T12:02:00Z",
                     "[finding] Diagnosis is done; the comparison used the wrong input.")
        output = self.cli("metrics", "--since", AT, "--until", "2026-10-18T12:10:00Z")
        messages = output.split("Lead messages\n")[1].split("Gate latency:")[0]
        rows = [line.split() for line in messages.splitlines() if line.strip()]
        self.assertEqual(rows[0], ["Lead", "sent", "go-request", "merge-ready", "done", "blocked",
                                   "tobias-decision", "finding", "other", "CoS", "replies"])
        for title in ("synthetic-finder", "TOTAL"):
            self.assertIn([title, "2", "0", "0", "0", "0", "0", "2", "0", "0"], rows)
        blocked = output.split("Blocked time:")[1].split("Idle-lead gaps:")[0]
        self.assertNotIn("synthetic-finder", blocked)
        self.assertIn(["TOTAL", "0", "0.000s", "0"], [line.split() for line in blocked.splitlines()])
        with patch.object(cos, "MAIN_HEALTH_REPOS", ()):
            census = self.cli("census")
        reports = [line for line in census.splitlines() if "unanswered report" in line]
        self.assertEqual(len(reports), 2)
        for line in reports:
            self.assertIn(" finding | synthetic-finder | finder send:auto", line)
        self.assertNotIn("settle candidate", census)

    def static_fixture(self):
        root, main = self.owned("fixture", REPO)
        retired = self.home / "code/orderready"
        self.repository(retired, f"https://github.com/{REPO}.git", marker="retired")
        with self.assertRaises(ValueError):
            cos.read_git(retired, "show", f"{main['oid']}:deny.toml")
        advisory = self.home / ".cargo/advisory-dbs/advisory-db-fixture"
        revision = self.repository(advisory, "https://github.com/RustSec/advisory-db")["oid"]
        directory = self.home / ".cache/orderready/verdicts" / ("static-" + hashlib.sha256(b"static").hexdigest())
        directory.mkdir(parents=True)
        record = {"tree": main["tree"]["oid"], "verdict": "pass", "created": cos.timestamp(AT).timestamp(),
                  "inputs": {"advisory:https://github.com/RustSec/advisory-db": revision}}
        path = directory / "current.json"
        path.write_text(json.dumps(record))
        return main, path, record

    def test_census_reads_owned_exact_static_tree_and_keeps_promotion_unobserved(self):
        main, _, _ = self.static_fixture()
        self.owned("platform-fixture", cos.MAIN_HEALTH_REPOS[1])
        output = self.cli("census")
        self.assertIn(f"main-health {REPO} main@{main['oid'][:12]}: success static", output)
        self.assertEqual(output.count(": configured landing check completed"), 2)
        self.assertIn("exact commit/tree; not full-suite evidence", output)
        self.assertEqual(output.count(": unobserved |"), 2)
        self.assertIn("not required on main; production health unknown", output)
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("GAP main-health", output)
        self.assertNotIn("required check full-suite", output)

    def test_census_rejects_wrong_tree_or_advisory_but_preserves_exact_static_failure(self):
        main, path, record = self.static_fixture()
        with patch.object(cos, "MAIN_HEALTH_REPOS", (REPO,)):
            for field, value in [("tree", "unrelated-tree"), ("inputs", {"advisory:https://github.com/RustSec/advisory-db": "old"})]:
                with self.subTest(field=field):
                    path.write_text(json.dumps({**record, field: value}))
                    output = self.cli("census")
                    self.assertIn("no static receipt for exact tree and current local advisory revision", output)
                    self.assertNotIn(": success static", output)
            path.write_text(json.dumps({**record, "verdict": "fail"}))
            output = self.cli("census")
            self.assertIn(f"SHARED BLOCKER {REPO}: static | main red", output)
            self.assertIn(f"main-health {REPO} main@{main['oid'][:12]}: RED static", output)


if __name__ == "__main__":
    unittest.main()
