import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VERIFIER = Path(__file__).with_name("verify_staleness.py")


class VerifyStalenessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "vault"
        self.write("AGENTS.md", "# Instructions\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def run_verifier(self, *arguments):
        result = subprocess.run(
            [sys.executable, str(VERIFIER), "--vault", str(self.root), "--json", *arguments],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_expired_note_is_reported_without_failing(self):
        self.write("prices.md", "# Prices\n\nrecheck-after: 2026-09-01\n\n- Ten dollars.\n")
        self.write("fresh.md", "# Fresh\n\nrecheck-after: 2027-06-01\n\n- Twenty dollars.\n")

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 0)
        self.assertEqual([item["source"] for item in report["expired"]], ["prices.md"])
        self.assertEqual(report["expired"][0]["days_overdue"], 53)
        self.assertEqual(report["counts"]["marked"], 2)
        self.assertEqual(report["counts"]["next_due"], "2027-06-01")

    def test_note_due_today_is_not_expired(self):
        self.write("today.md", "# Today\n\nrecheck-after: 2026-10-24\n")

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 0)
        self.assertEqual(report["counts"]["expired"], 0)

    def test_malformed_date_fails_because_the_expiry_is_off(self):
        self.write("broken.md", "# Broken\n\nrecheck-after: soon\n")

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 1)
        self.assertEqual(report["malformed"][0]["source"], "broken.md")
        self.assertEqual(report["counts"]["marked"], 0)

    def test_duplicate_marker_fails(self):
        self.write("twice.md", "# Twice\n\nrecheck-after: 2027-01-01\n\nrecheck-after: 2028-01-01\n")

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 1)
        self.assertEqual(len(report["malformed"]), 1)
        self.assertEqual(report["counts"]["marked"], 1)

    def test_prose_about_the_convention_is_not_a_marker(self):
        self.write(
            "guide.md",
            "# Guide\n\n"
            "Volatile facts carry a `recheck-after: 2027-01-24` line near the top.\n"
            "- Write recheck-after: later when unsure\n",
        )

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 0)
        self.assertEqual(report["counts"]["marked"], 0)
        self.assertEqual(report["expired"], [])

    def test_expired_entries_are_ordered_and_source_paths_are_vault_relative(self):
        self.write("b-note.md", "# B\n\nrecheck-after: 2026-10-01\n")
        self.write("a/deep.md", "# Deep\n\nrecheck-after: 2026-09-01\n")

        code, report = self.run_verifier("--as-of", "2026-10-24")

        self.assertEqual(code, 0)
        self.assertEqual([item["source"] for item in report["expired"]], ["a/deep.md", "b-note.md"])

    def test_human_output_names_the_note_and_the_recheck(self):
        self.write("prices.md", "# Prices\n\nrecheck-after: 2026-09-01\n")

        result = subprocess.run(
            [sys.executable, str(VERIFIER), "--vault", str(self.root), "--as-of", "2026-10-24"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("[recheck] prices.md:3 due 2026-09-01", result.stdout)


if __name__ == "__main__":
    unittest.main()
