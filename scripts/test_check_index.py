import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


class CheckIndexTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        shutil.copytree(SCRIPTS, self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        self.git("init", "-q")
        self.write("index.md", "# Index\n\n- [agents/note.md](agents/note.md)\n- [`demo`](skills/demo/SKILL.md)\n")
        self.write("agents/note.md", "# Note\n")
        self.write("skills/demo/SKILL.md", "# Demo\n")
        self.write("skills/demo/references/ref.md", "# Ref\n")
        self.write("README.md", "# Readme\n")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def git(self, *args):
        result = subprocess.run(("git", *args), cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)

    def check(self):
        self.git("add", "-A")
        return subprocess.run(
            ("python3", "-I", "scripts/check-index.py"),
            cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30,
        )

    def test_indexed_notes_and_skills_pass_and_references_and_routers_need_no_line(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unindexed_note_is_rejected(self):
        self.write("software/new-note.md", "# New\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("index.md: no line for software/new-note.md", result.stderr)

    def test_unindexed_vault_only_skill_is_rejected(self):
        self.write(".agents/skills/local/SKILL.md", "# Local\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("index.md: no line for .agents/skills/local/SKILL.md", result.stderr)

    def test_untracked_note_is_not_judged(self):
        self.write("tobias/draft.md", "# Draft\n")
        result = subprocess.run(
            ("python3", "-I", "scripts/check-index.py"),
            cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
