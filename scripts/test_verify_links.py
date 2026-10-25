import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VERIFIER = Path(__file__).with_name("verify_links.py")


class VerifyLinksTests(unittest.TestCase):
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

    def run_verifier_error(self, *arguments):
        return subprocess.run(
            [sys.executable, str(VERIFIER), "--vault", str(self.root), "--json", *arguments],
            capture_output=True,
            text=True,
        )

    def test_hidden_targets_and_directories_resolve(self):
        self.write("Guide.md", "# Guide\n")
        self.write(".agents/skills/demo/SKILL.md", "# Skill\n## Usage\n")
        self.write(".agents/skills/demo/references.md", "# References\nA receipt. ^receipt\n")
        (self.root / "resources").mkdir()
        self.write(
            "README.md",
            "[[Guide]]\n"
            "[Skill](.agents/skills/demo/SKILL.md#usage)\n"
            "[Receipt](.agents/skills/demo/references.md#^receipt)\n"
            "[Skills](.agents/skills)\n"
            "[Resources](resources)\n",
        )

        code, report = self.run_verifier()

        self.assertEqual(code, 0)
        self.assertEqual(report["issues"], [])
        self.assertEqual(report["counts"]["files"], 5)
        self.assertEqual(report["counts"]["wikilinks"], 1)
        self.assertEqual(report["counts"]["valid"], 5)

    def test_broken_link_inside_agents_note_is_reported(self):
        self.write("Guide.md", "# Guide\n")
        self.write(
            ".agents/skills/demo/SKILL.md",
            "# Skill\n[Guide](../../../Guide.md)\n[Broken](./absent.md)\n[[Absent hidden note]]\n",
        )

        code, report = self.run_verifier()

        self.assertEqual(code, 1)
        self.assertEqual(
            [(issue["code"], issue["source"], issue["line"], issue["target"]) for issue in report["issues"]],
            [
                ("missing-file", ".agents/skills/demo/SKILL.md", 3, "./absent.md"),
                ("missing-note", ".agents/skills/demo/SKILL.md", 4, "Absent hidden note"),
            ],
        )
        self.assertEqual(report["counts"]["markdown_links"], 2)
        self.assertEqual(report["counts"]["wikilinks"], 1)
        self.assertEqual(report["counts"]["valid"], 1)

    def test_explicit_agents_scope_scans_only_that_hidden_directory(self):
        self.write("Guide.md", "[Broken](absent.md)\n")
        self.write(".agents/skills/demo/SKILL.md", "[Absent](./absent.md)\n")

        code, report = self.run_verifier("--scope", ".agents/skills/demo")

        self.assertEqual(code, 1)
        self.assertEqual(report["counts"]["files"], 1)
        self.assertEqual([issue["source"] for issue in report["issues"]], [".agents/skills/demo/SKILL.md"])

    def test_hidden_runtime_state_is_never_scanned_or_selectable(self):
        self.write("Guide.md", "# Guide\n")
        self.write(".git/cache.md", "[Absent](absent.md)\n")
        self.write(".pi-subagents/raw-session.md", "[Absent](absent.md)\n")

        code, report = self.run_verifier()

        self.assertEqual(code, 0)
        self.assertEqual(report["counts"]["files"], 2)
        self.assertEqual(report["counts"]["markdown_links"], 0)

        rejected = self.run_verifier_error("--scope", ".pi-subagents")
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("scope contains no scanned Markdown files", rejected.stderr)

    def test_missing_hidden_files_directories_and_anchors_report_the_source(self):
        self.write(".agents/skills/demo/SKILL.md", "# Skill\n## Usage\n")
        self.write(
            "README.md",
            "# Links\n"
            "[Missing skill](.agents/skills/absent/SKILL.md)\n"
            "[Missing directory](absent-directory)\n"
            "[Missing heading](.agents/skills/demo/SKILL.md#absent)\n",
        )

        code, report = self.run_verifier()

        self.assertEqual(code, 1)
        self.assertEqual(
            [(issue["code"], issue["source"], issue["line"]) for issue in report["issues"]],
            [
                ("missing-file", "README.md", 2),
                ("missing-file", "README.md", 3),
                ("missing-heading", "README.md", 4),
            ],
        )

    def test_visible_target_case_mismatch_still_fails(self):
        self.write("Guide.md", "# Guide\n")
        self.write("README.md", "[Guide](guide.md)\n")

        code, report = self.run_verifier()

        self.assertEqual(code, 1)
        self.assertEqual(report["issues"][0]["code"], "case-mismatch")
        self.assertEqual(report["issues"][0]["candidates"], ["Guide.md"])

    def test_direct_and_extensionless_symlink_targets_cannot_escape_the_vault(self):
        outside = self.root.parent / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        hidden = self.root / ".agents"
        hidden.mkdir()
        (hidden / "outside.md").symlink_to(outside)
        self.write("README.md", "[Direct](../outside.md)\n[Symlink](.agents/outside)\n")

        code, report = self.run_verifier()

        self.assertEqual(code, 1)
        self.assertEqual([issue["code"] for issue in report["issues"]], ["outside-vault", "outside-vault"])


if __name__ == "__main__":
    unittest.main()
