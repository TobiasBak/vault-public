import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

with patch.object(Path, "read_text", return_value="test-cos"):
    import cos


AT = "2026-10-18T12:00:00Z"
REPO = "TobiasBak/orderready"


def commit(state=None, checks=None):
    nodes = checks if checks is not None else ([{"context": "gate", "state": state, "createdAt": AT}] if state else [])
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
        with patch.object(cos, "MAIN_HEALTH_REPOS", (REPO,)), patch.object(cos, "gh_json", return_value=[page(main, prs)]), patch.object(cos, "orderready_static", return_value=evidence), contextlib.redirect_stdout(out):
            cos.main_health()
        return out.getvalue()

    def test_red_main_raises_without_any_pr(self):
        output = self.census_health(commit("FAILURE"))
        self.assertIn(f"SHARED BLOCKER {REPO}: gate | main red | failing PRs=0", output)
        self.assertIn(f"RED gate since {AT}", output)

    def test_green_main_and_pr_stay_silent(self):
        main = commit("SUCCESS")
        output = self.census_health(main, [(12, commit("SUCCESS"))], {
            main["oid"]: ({"name": "static", "state": "success", "at": AT, "source": "fixture"}, None),
        })
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("GAP", output)

    def test_same_check_on_two_prs_raises_with_green_main(self):
        output = self.census_health(commit("SUCCESS"), [(12, commit("FAILURE")), (34, commit("FAILURE"))])
        self.assertIn(f"SHARED BLOCKER {REPO}: gate | same check fails on multiple PRs | failing PRs=2 #12 #34", output)
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
        with patch.object(cos, "MAIN_HEALTH_REPOS", ("TobiasBak/orderready-platform",)), patch.object(cos, "gh_json", return_value=[response]), contextlib.redirect_stdout(io.StringIO()) as out:
            cos.main_health()
        self.assertIn("SHARED BLOCKER TobiasBak/orderready-platform: static", out.getvalue())

    def test_static_receipts_require_exact_tree_and_current_advisory(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            directory = home / ".cache/orderready/verdicts" / ("static-" + hashlib.sha256(b"static").hexdigest())
            directory.mkdir(parents=True)
            (home / ".cargo/advisory-dbs/advisory-db-fixture").mkdir(parents=True)
            main = commit()
            for name, tree, revision, verdict, created in [
                ("unrelated", "other-tree", "current", "fail", 30),
                ("old-advisory", main["tree"]["oid"], "old", "pass", 20),
                ("current", main["tree"]["oid"], "current", "fail", 10),
            ]:
                (directory / f"{name}.json").write_text(json.dumps({
                    "tree": tree, "verdict": verdict, "created": created,
                    "inputs": {"advisory:https://github.com/RustSec/advisory-db": revision},
                }))

            def git(root, *args):
                if args[0] == "config":
                    return "https://github.com/RustSec/advisory-db"
                if args[0] == "rev-parse":
                    return "current"
                return "[advisories]\n"

            with patch.object(Path, "home", return_value=home), patch.dict("os.environ", {"XDG_CACHE_HOME": "", "CARGO_HOME": ""}), patch.object(cos, "read_git", side_effect=git):
                found, gap = cos.orderready_static([main])[main["oid"]]
                self.assertIsNone(gap)
                self.assertEqual(found["state"], "failure")
                self.assertIn("current.json", found["source"])
                (directory / "current.json").unlink()
                found, gap = cos.orderready_static([main])[main["oid"]]
                self.assertIsNone(found)
                self.assertIn("current local advisory revision", gap)


class PlatformMainHealthTests(unittest.TestCase):
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
            with patch.object(Path, "home", return_value=home), patch.dict("os.environ", {"XDG_STATE_HOME": str(state) if xdg else ""}), patch.object(cos, "MAIN_HEALTH_REPOS", (self.repo,)), patch.object(cos, "gh_json", return_value=[page(commit())]), patch.object(cos.subprocess, "run", side_effect=AssertionError("census must only read receipts")), contextlib.redirect_stdout(io.StringIO()) as out:
                cos.main_health()
            return out.getvalue()

    def test_green_exact_main_in_xdg_and_default_state_home(self):
        for xdg in (True, False):
            with self.subTest(xdg=xdg):
                output = self.census_health(self.receipt(), xdg=xdg)
                self.assertIn(f"main-health {self.repo} main@{self.sha[:12]}: success scripts/check.py", output)
                self.assertNotIn("GAP", output)
                self.assertNotIn("SHARED BLOCKER", output)

    def test_failed_checks_raise_shared_blocker(self):
        receipt = self.receipt()
        receipt["result"] = "failed"
        receipt["checks"]["lint"] = {"status": "failed", "exit_code": 1}
        receipt["checks"]["tests"] = {"status": "failed", "exit_code": None, "error": "OSError"}
        output = self.census_health(receipt)
        self.assertIn("RED scripts/check.py", output)
        self.assertIn("failed checks: lint, tests", output)
        self.assertIn(f"SHARED BLOCKER {self.repo}: scripts/check.py | main red", output)
        self.assertNotIn("success", output)

    def test_running_is_pending(self):
        receipt = self.receipt()
        receipt.update(result="running", finished_at=None)
        receipt["checks"]["tests"] = {"status": "running", "exit_code": None}
        output = self.census_health(receipt)
        self.assertIn("pending scripts/check.py", output)
        self.assertNotIn("success", output)
        self.assertNotIn("SHARED BLOCKER", output)
        self.assertNotIn("GAP", output)

    def test_missing_receipt_is_gap(self):
        output = self.census_health(None)
        self.assertIn(f"GAP main-health {self.repo}: missing scripts/check.py receipt for main@{self.sha[:12]}", output)
        self.assertNotIn("success", output)

    def test_stale_receipt_never_establishes_current_main_health(self):
        stale = self.receipt()
        stale["head_sha"] = "c" * 40
        for file_sha in (self.sha, stale["head_sha"]):
            with self.subTest(file_sha=file_sha):
                output = self.census_health(stale, file_sha=file_sha)
                self.assertIn(f"GAP main-health {self.repo}", output)
                self.assertIn("stale SHA" if file_sha == self.sha else "missing scripts/check.py receipt", output)
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
                self.assertIn(f"GAP main-health {self.repo}", output)
                self.assertNotIn("success", output)
                self.assertNotIn("do-not-print-this", output)


if __name__ == "__main__":
    unittest.main()
