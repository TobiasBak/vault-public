import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

COPIED = (
    "The quick brown fox jumps over the lazy dog while the slow turtle watches "
    "from the river bank and counts every single one of its careful steps today."
)


class DuplicateAuthorityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        shutil.copytree(SCRIPTS, self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        self.git("init", "-q")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def git(self, *args):
        result = subprocess.run(
            ("git", *args), cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def check(self):
        self.git("add", "-A")
        return subprocess.run(
            ("python3", "scripts/check-duplicate-authority.py"),
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=60,
        )

    def test_distinct_prose_passes(self):
        self.write("agents/one.md", f"# One\n\n{COPIED}\n")
        self.write("agents/two.md", "# Two\n\nA different claim about another subject entirely.\n")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_shared_thirteen_words_fails_and_names_both_files(self):
        words = COPIED.split()[:13]
        self.write("agents/one.md", f"# One\n\n{' '.join(words)}\n")
        self.write("agents/two.md", f"# Two\n\nIntro.\n\n{' '.join(words)}\n")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("agents/one.md", result.stderr)
        self.assertIn("agents/two.md", result.stderr)
        self.assertIn("13 identical words", result.stderr)

    def test_twelve_shared_words_passes(self):
        words = COPIED.split()[:12]
        self.write("agents/one.md", f"# One\n\n{' '.join(words)}\n")
        self.write("agents/two.md", f"# Two\n\n{' '.join(words)}\n")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_attribution_notice_is_exempt(self):
        self.write("skills/alpha/SKILL.md", f"# Alpha\n\n{COPIED}\n")
        self.write("skills/alpha/SOURCE.md", f"# Source\n\n{COPIED}\n")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
