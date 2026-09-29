import io
import json
import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import history_review as hr


class HistoryReviewTests(unittest.TestCase):
    def test_pi_selects_latest_active_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            rows = [
                {"id": "root", "role": "user", "content": "root"},
                {"id": "old", "parentId": "root", "role": "assistant", "content": "abandoned"},
                {"id": "new", "parentId": "root", "role": "assistant", "content": "active", "timestamp": "2026-07-14T01:00:00Z"},
            ]
            path.write_text("\n".join(json.dumps(x) for x in rows))
            messages, _ = hr.parse_pi(path)
            self.assertEqual([item["text"] for item in messages], ["root", "active"])

    def test_codex_payload_messages_and_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            rows = [
                {"timestamp": "2026-07-14T01:00:00Z", "payload": {"type": "session_meta", "id": "stable", "cwd": "/work", "thread_source": "main"}},
                {"payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "hello"}]}},
                {"payload": {"type": "function_call", "name": "secret_tool", "arguments": "do not include"}},
                {"payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "answer"}]}},
                {"payload": {"type": "message", "role": "system", "content": "ignore"}},
            ]
            path.write_text("\n".join(json.dumps(x) for x in rows))
            messages, _, child = hr.parse_codex(path)
            self.assertFalse(child)
            self.assertEqual([item["text"] for item in messages], ["hello", "answer"])
            self.assertEqual(hr.session_metadata(path)["session_id"], "stable")

    def test_codex_nested_session_metadata_marks_subagent(self):
        records = [{"payload": {"type": "session_meta", "id": "child", "thread_source": "subagent"}}]
        self.assertTrue(hr.codex_is_child(records))

    def test_redaction_common_credentials(self):
        text = "ghp_abcdefghijklmnopqrstuvwxyz xoxb-123456789012 bearer ABCDEFGHIJKLMNOP AKIA1234567890123456 -----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----"
        clean, warnings = hr.redact(text)
        self.assertNotIn("ghp_", clean)
        self.assertNotIn("xoxb-", clean)
        self.assertNotIn("AKIA", clean)
        self.assertNotIn("BEGIN PRIVATE KEY", clean)
        self.assertTrue(warnings)

    def test_first_run_selection_is_seven_days(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            since, basis = hr.select_since(Path(tmp), None, False)
            self.assertEqual(hr.iso(since), "2026-07-07T00:00:00Z")
            self.assertIn("first run", basis)

    def test_child_discovery_option(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "run-0" / "session.jsonl"
            child.parent.mkdir()
            child.write_text("{}\n")
            found, _ = hr.discover(root, "pi")
            self.assertEqual(found, [])
            found, _ = hr.discover(root, "pi", include_children=True)
            self.assertEqual(found, [child])

    def test_codex_discovery_ignores_unrelated_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sessions = root / "sessions"
            archived = root / "archived_sessions"
            sessions.mkdir()
            archived.mkdir()
            wanted = sessions / "rollout.jsonl"
            wanted.write_text("{}\n")
            (archived / "old.jsonl").write_text("{}\n")
            (root / "unrelated.jsonl").write_text("{}\n")
            found = []
            for subtree in (sessions, archived):
                paths, _ = hr.discover(subtree, "codex")
                found.extend(paths)
            self.assertEqual(sorted(found), sorted([wanted, archived / "old.jsonl"]))

    def test_exact_search_reports_routes_limits_and_truncation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex_home = root / "codex"
            sessions = codex_home / "sessions"
            sessions.mkdir(parents=True)
            path = sessions / "rollout.jsonl"
            rows = [
                {"timestamp": "2026-07-14T01:00:00Z", "payload": {"type": "session_meta", "id": "stable", "cwd": "/work"}},
                {"timestamp": "2026-07-14T01:01:00Z", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "first needle memory with surrounding words"}]}},
                {"timestamp": "2026-07-14T01:02:00Z", "payload": {"type": "function_call", "name": "needle_tool", "arguments": "needle must not leak"}},
                {"timestamp": "2026-07-14T01:03:00Z", "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "second needle memory"}]}},
            ]
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            output = io.StringIO()
            with redirect_stdout(output):
                result = hr.search(Namespace(
                    vault=str(root), pi_root=None, codex_root=str(codex_home), source="codex",
                    query="needle", since=None, until=None, include_children=False,
                    limit=1, excerpt_chars=16,
                ))
            self.assertEqual(result, 0)
            data = json.loads(output.getvalue())
            self.assertEqual(data["matches_total"], 2)
            self.assertEqual(data["matches_returned"], 1)
            self.assertTrue(data["truncated"])
            self.assertEqual(data["results"][0]["session_id"], "stable")
            self.assertEqual(data["results"][0]["path"], str(path.resolve()))
            self.assertLessEqual(len(data["results"][0]["excerpt"]), 16)
            self.assertNotIn("needle_tool", output.getvalue())

    def test_show_returns_exact_redacted_message_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            rows = [
                {"payload": {"type": "session_meta", "id": "stable", "cwd": "/work"}},
                {"payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "before"}]}},
                {"payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "exact remembered answer"}]}},
                {"payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "after"}]}},
            ]
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            output = io.StringIO()
            with redirect_stdout(output):
                result = hr.show(Namespace(path=str(path), source="codex", message_index=2, before=1, after=1))
            self.assertEqual(result, 0)
            data = json.loads(output.getvalue())
            self.assertEqual(data["session_id"], "stable")
            self.assertEqual([item["text"] for item in data["messages"]], ["before", "exact remembered answer", "after"])
            self.assertEqual([item["message_index"] for item in data["messages"]], [1, 2, 3])

    def test_out_of_layout_manifest_is_rejected_without_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normalized = root / "normalized"
            normalized.mkdir()
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"run_id": "run", "scan_started_at": "2026-07-14T00:00:00Z"}))
            result = hr.complete(Namespace(vault=str(root), manifest=str(manifest), review_complete=True))
            self.assertEqual(result, 1)
            self.assertTrue(normalized.exists())
            self.assertFalse((root / ".knowledge-bank").exists())

    def test_per_source_checkpoints_are_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / ".knowledge-bank" / "state").mkdir(parents=True)
            (vault / ".knowledge-bank" / "state" / "checkpoint.json").write_text(json.dumps({
                "pi": {"scan_started_at": "2026-07-01T00:00:00Z"},
                "codex": {"scan_started_at": "2026-07-10T00:00:00Z"},
            }))
            pi_since, _ = hr.select_since(vault, None, False, "pi")
            codex_since, _ = hr.select_since(vault, None, False, "codex")
            self.assertEqual(hr.iso(pi_since), "2026-07-01T00:00:00Z")
            self.assertEqual(hr.iso(codex_since), "2026-07-10T00:00:00Z")

    def test_pi_only_completion_does_not_advance_codex(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            run = vault / ".knowledge-bank" / "state" / "pi-run"
            run.mkdir(parents=True)
            manifest = run / "manifest.json"
            manifest.write_text(json.dumps({"run_id": "pi-run", "scan_started_at": "2026-07-14T00:00:00Z", "sources": ["pi"], "checkpoint_updates": {"pi": "2026-07-14T00:00:00Z"}, "extraction_errors": [], "sessions": [], "review_complete": False}))
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True)), 0)
            self.assertEqual(hr.checkpoint(vault, "pi"), hr.parse_time("2026-07-14T00:00:00Z"))
            self.assertIsNone(hr.checkpoint(vault, "codex"))

    def test_historical_until_does_not_create_checkpoint_updates(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            pi = vault / "pi"
            pi.mkdir()
            path = pi / "session.jsonl"
            path.write_text(json.dumps({"role": "user", "content": "old"}) + "\n")
            os.utime(path, (hr.parse_time("2026-07-10T00:00:00Z").timestamp(),) * 2)
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(hr.scan(Namespace(vault=str(vault), pi_root=str(pi), codex_root=str(vault / "none"), source="pi", since=None, until="2026-07-11T00:00:00Z", all=False, include_children=False)), 0)
            manifest = json.loads(output.getvalue())
            self.assertEqual(manifest["checkpoint_updates"], {})

    def test_malformed_jsonl_is_reported_and_blocks_completion(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            pi = vault / "pi"
            pi.mkdir()
            history = pi / "session.jsonl"
            history.write_text('{"role":"user","content":"valid"}\n{broken\n')
            os.utime(history, (hr.parse_time("2026-07-13T00:00:00Z").timestamp(),) * 2)
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(vault=str(vault), pi_root=str(pi), codex_root=str(vault / "none"), source="pi", since=None, until=None, all=False, include_children=False))
            data = json.loads(output.getvalue())
            self.assertEqual(data["extraction_errors"][0]["line"], 2)
            manifest = vault / ".knowledge-bank" / "state" / data["run_id"] / "manifest.json"
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True)), 1)
            self.assertTrue((manifest.parent / "normalized").exists())
            self.assertFalse((vault / ".knowledge-bank" / "state" / "checkpoint.json").exists())

    def test_scan_always_warns_about_incomplete_redaction(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(vault=str(vault), pi_root=str(vault / "pi"), codex_root=str(vault / "codex"), source="pi", since=None, until=None, all=False, include_children=False))
            manifest = json.loads(output.getvalue())
            self.assertIn(hr.PRIVACY_WARNING, manifest["warnings"])

    def test_pi_parent_session_is_excluded_and_included_children_marked(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            pi = vault / "pi"
            pi.mkdir()
            path = pi / "child.jsonl"
            path.write_text("\n".join([json.dumps({"type": "session", "id": "child", "parentSession": "parent"}), json.dumps({"role": "user", "content": "child"})]) + "\n")
            os.utime(path, (hr.parse_time("2026-07-13T00:00:00Z").timestamp(),) * 2)
            base = Namespace(vault=str(vault), pi_root=str(pi), codex_root=str(vault / "codex"), source="pi", since=None, until=None, all=False, include_children=False)
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(base)
            self.assertEqual(json.loads(output.getvalue())["counts"]["files"], 0)
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(**{**vars(base), "include_children": True}))
            manifest = json.loads(output.getvalue())
            self.assertTrue(manifest["sessions"][0]["child"])

    def test_explicit_since_gap_does_not_advance_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            state = vault / ".knowledge-bank" / "state"
            state.mkdir(parents=True)
            (state / "checkpoint.json").write_text(json.dumps({"pi": {"scan_started_at": "2026-07-01T00:00:00Z"}}))
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(vault=str(vault), pi_root=str(vault / "none"), codex_root=str(vault / "none"), source="pi", since="2026-07-10T00:00:00Z", until=None, all=False, include_children=False))
            manifest = json.loads(output.getvalue())
            self.assertEqual(manifest["checkpoint_updates"], {})
            self.assertTrue(any("unreviewed gap" in warning for warning in manifest["warnings"]))

    def test_compressed_history_and_missing_roots_block_completion(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(hr, "now", return_value=hr.parse_time("2026-07-14T00:00:00Z")):
            vault = Path(tmp)
            pi = vault / "pi"
            pi.mkdir()
            compressed = pi / "session.jsonl.zst"
            compressed.write_bytes(b"compressed")
            os.utime(compressed, (hr.parse_time("2026-07-13T00:00:00Z").timestamp(),) * 2)
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(vault=str(vault), pi_root=str(pi), codex_root=str(vault / "missing"), source="pi", since=None, until=None, all=False, include_children=False))
            data = json.loads(output.getvalue())
            self.assertIn("unsupported compressed JSONL history", data["extraction_errors"][0]["error"])
            manifest = vault / ".knowledge-bank" / "state" / data["run_id"] / "manifest.json"
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True)), 1)
            self.assertIsNone(hr.checkpoint(vault, "pi"))

            other_vault = vault / "other"
            output = io.StringIO()
            with redirect_stdout(output):
                hr.scan(Namespace(vault=str(other_vault), pi_root=str(vault / "absent"), codex_root=str(vault / "missing"), source="pi", since=None, until=None, all=False, include_children=False))
            missing = json.loads(output.getvalue())
            self.assertEqual(missing["extraction_errors"][0]["error"], "no history root was available")

    def test_non_object_jsonl_is_an_extraction_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            path.write_text('[]\n{"role":"user","content":"valid"}\n')
            records, errors = hr.parse_jsonl_diagnostics(path)
            self.assertEqual(len(records), 1)
            self.assertEqual(errors[0]["line"], 1)
            self.assertIn("not an object", errors[0]["error"])

    def test_manifest_checkpoint_invariants_and_monotonicity(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            state = vault / ".knowledge-bank" / "state"
            bad_run = state / "bad"
            bad_run.mkdir(parents=True)
            bad_manifest = bad_run / "manifest.json"
            bad_manifest.write_text(json.dumps({
                "run_id": "bad",
                "scan_started_at": "2026-07-14T00:00:00Z",
                "sources": ["pi"],
                "checkpoint_updates": {"pi": "2099-01-01T00:00:00Z"},
                "extraction_errors": [],
                "sessions": [],
                "review_complete": False,
            }))
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(bad_manifest), review_complete=True)), 1)
            self.assertIsNone(hr.checkpoint(vault, "pi"))

            (state / "checkpoint.json").write_text(json.dumps({"pi": {"scan_started_at": "2026-07-15T00:00:00Z"}}))
            old_run = state / "old"
            old_run.mkdir()
            old_manifest = old_run / "manifest.json"
            old_manifest.write_text(json.dumps({
                "run_id": "old",
                "scan_started_at": "2026-07-14T00:00:00Z",
                "sources": ["pi"],
                "checkpoint_updates": {"pi": "2026-07-14T00:00:00Z"},
                "extraction_errors": [],
                "sessions": [],
                "review_complete": False,
            }))
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(old_manifest), review_complete=True)), 0)
            self.assertEqual(hr.checkpoint(vault, "pi"), hr.parse_time("2026-07-15T00:00:00Z"))

    def test_complete_requires_matching_vault_and_generated_manifest_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vault = root / "vault"
            other = root / "other"
            run = vault / ".knowledge-bank" / "state" / "run"
            normalized = run / "normalized"
            normalized.mkdir(parents=True)
            orphan = normalized / "orphan.json"
            orphan.write_text("body")
            manifest = run / "manifest.json"
            manifest.write_text(json.dumps({
                "run_id": "run",
                "scan_started_at": "2026-07-14T00:00:00Z",
                "sources": ["pi"],
                "checkpoint_updates": {"pi": "2026-07-14T00:00:00Z"},
                "review_complete": False,
            }))
            self.assertEqual(hr.complete(Namespace(vault=str(other), manifest=str(manifest), review_complete=True)), 1)
            self.assertTrue(orphan.exists())
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True)), 1)
            self.assertTrue(orphan.exists())

    def test_invalid_checkpoint_blocks_scan_and_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            state = vault / ".knowledge-bank" / "state"
            state.mkdir(parents=True)
            checkpoint = state / "checkpoint.json"
            checkpoint.write_text("{broken")
            output = io.StringIO()
            with redirect_stdout(output):
                result = hr.scan(Namespace(vault=str(vault), pi_root=str(vault / "pi"), codex_root=str(vault / "codex"), source="pi", since=None, until=None, all=False, include_children=False))
            self.assertEqual(result, 1)
            self.assertEqual(output.getvalue(), "")

            run = state / "run"
            (run / "normalized").mkdir(parents=True)
            manifest = run / "manifest.json"
            manifest.write_text(json.dumps({
                "run_id": "run",
                "scan_started_at": "2026-07-14T00:00:00Z",
                "sources": ["pi"],
                "checkpoint_updates": {"pi": "2026-07-14T00:00:00Z"},
                "extraction_errors": [],
                "sessions": [],
                "review_complete": False,
            }))
            self.assertEqual(hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True)), 1)
            self.assertEqual(checkpoint.read_text(), "{broken")

    def test_portable_skill_invocation_is_documented(self):
        skill = Path(__file__).parents[1] / "SKILL.md"
        text = skill.read_text()
        self.assertIn('python "$SKILL_DIR/scripts/history_review.py" --vault "$VAULT_ROOT" scan', text)
        self.assertIn('python "$SKILL_DIR/scripts/history_review.py" --vault "$VAULT_ROOT" complete', text)
        self.assertNotIn("BASH_SOURCE", text)
        self.assertIn("whole-file mtime", text)

    def test_complete_checkpoint_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            run = vault / ".knowledge-bank" / "state" / "run"
            normalized = run / "normalized"
            normalized.mkdir(parents=True)
            (normalized / "one.json").write_text("body")
            manifest = run / "manifest.json"
            manifest.write_text(json.dumps({"run_id": "run", "scan_started_at": "2026-07-14T00:00:00Z", "sources": ["pi"], "checkpoint_updates": {"pi": "2026-07-14T00:00:00Z"}, "extraction_errors": [], "sessions": [{"normalized_path": str(normalized / "one.json")}], "review_complete": False}))
            result = hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=False))
            self.assertEqual(result, 2)
            self.assertFalse((vault / ".knowledge-bank" / "state" / "checkpoint.json").exists())
            result = hr.complete(Namespace(vault=str(vault), manifest=str(manifest), review_complete=True))
            self.assertEqual(result, 0)
            self.assertFalse(normalized.exists())
            self.assertEqual(hr.checkpoint(vault, "pi"), hr.parse_time("2026-07-14T00:00:00Z"))
            self.assertIsNone(hr.checkpoint(vault, "codex"))


if __name__ == "__main__":
    unittest.main()
