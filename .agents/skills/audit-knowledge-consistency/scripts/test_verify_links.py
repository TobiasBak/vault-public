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

    def run_verifier(self):
        result = subprocess.run(
            [sys.executable, str(VERIFIER), "--vault", str(self.root), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_hidden_targets_and_directories_resolve_without_scanning_hidden_notes(self):
        self.write("Guide.md", "# Guide\n")
        self.write(".agents/skills/demo/SKILL.md", "# Skill\n## Usage\n[[Absent hidden note]]\n")
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
        self.assertEqual(report["counts"]["files"], 3)
        self.assertEqual(report["counts"]["wikilinks"], 1)
        self.assertEqual(report["counts"]["valid"], 5)

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
