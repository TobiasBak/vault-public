import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = "---\nname: demo\ndescription: Use when testing.\n---\n\n# Demo\n\nSee [ref](references/ref.md).\n"


class CheckSkillsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(SCRIPTS, self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        self.write("skills/demo/SKILL.md", SKILL)
        self.write("skills/demo/references/ref.md", "# Ref\n")
        self.write("agents/note.md", "# Note\n")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def check(self):
        return subprocess.run(
            ("python3", "-I", "scripts/check-skills.py"),
            cwd=self.root, text=True, capture_output=True, timeout=30,
        )

    def assertRejected(self, message):
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def test_self_contained_global_skill_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_global_skill_link_to_a_vault_note_is_rejected(self):
        self.write("skills/demo/references/ref.md", "# Ref\n\n[Note](../../../agents/note.md)\n")
        self.assertRejected("skills/demo/references/ref.md: link escapes the skill directory (../../../agents/note.md)")

    def test_vault_only_skill_may_link_to_a_vault_note(self):
        self.write(".agents/skills/local/SKILL.md", SKILL.replace("references/ref.md", "../../../agents/note.md"))
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_description_is_rejected(self):
        self.write("skills/demo/SKILL.md", "---\nname: demo\n---\n\n# Demo\n")
        self.assertRejected("skills/demo: SKILL.md frontmatter has no description")

    def test_invocation_flag_is_rejected(self):
        self.write("skills/demo/SKILL.md", SKILL.replace("name: demo\n", "name: demo\ndisable-model-invocation: true\n"))
        self.assertRejected("skills/demo/SKILL.md: invocation flag on a model-invoked skill")

    def test_invocation_flag_in_a_vault_only_skill_is_rejected(self):
        self.write(".agents/skills/demo/SKILL.md", SKILL.replace("name: demo\n", "name: demo\ndisable-model-invocation: true\n"))
        self.assertRejected(".agents/skills/demo/SKILL.md: invocation flag on a model-invoked skill")

    def test_adapted_skill_without_license_is_rejected(self):
        self.write("skills/demo/SOURCE.md", "Adapted from upstream.\n")
        self.assertRejected("skills/demo: SOURCE.md without LICENSE")
        self.write("skills/demo/LICENSE", "MIT\n")
        self.assertEqual(self.check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
