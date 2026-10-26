import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent


class CheckVaultTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        shutil.copytree(SCRIPTS, self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        self.write("AGENTS.md", "# Vault\n")
        self.write("index.md", "# Index\n\n[Note](agents/note.md)\n")
        self.fresh = "# Note\n\nrecheck-after: 9999-12-31\n\n[Index](../index.md)\n"
        self.write("agents/note.md", self.fresh)
        self.git("init", "-q")
        self.git("add", "-A")
        (self.root / ".git/hooks/pre-commit").symlink_to("../../scripts/check-vault")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_command(self, *args):
        return subprocess.run(args, cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30)

    def git(self, *args):
        result = self.run_command("git", *args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def hook(self):
        return self.run_command(str(self.root / ".git/hooks/pre-commit"))

    def test_hook_checks_staged_expiry_not_unstaged_content(self):
        self.assertEqual(self.hook().returncode, 0)
        self.write("agents/note.md", self.fresh.replace("9999-12-31", "2000-01-01"))
        self.git("add", "agents/note.md")
        self.write("agents/note.md", self.fresh)

        rejected = self.hook()
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("stale note edited: agents/note.md", rejected.stderr)

        self.git("add", "agents/note.md")
        self.write("agents/note.md", self.fresh.replace("9999-12-31", "2000-01-01"))
        self.assertEqual(self.hook().returncode, 0)

    def test_hook_checks_staged_links_and_direct_check_reads_worktree(self):
        self.write("agents/note.md", self.fresh + "[Missing](../missing.md)\n")
        self.git("add", "agents/note.md")
        self.write("agents/note.md", self.fresh)
        self.assertNotEqual(self.hook().returncode, 0)
        self.assertEqual(self.run_command("scripts/check-vault").returncode, 0)

        self.git("add", "agents/note.md")
        self.write("agents/note.md", self.fresh + "[Missing](../missing.md)\n")
        self.assertEqual(self.hook().returncode, 0)
        self.assertNotEqual(self.run_command("scripts/check-vault").returncode, 0)


if __name__ == "__main__":
    unittest.main()
