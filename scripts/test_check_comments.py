import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
CLEAN = {
    "tool.py": '#!/usr/bin/env python3\nvalue = "# not a comment"\n\n\ndef run():\n    return value\n',
    "run.sh": '#!/usr/bin/env bash\nitems=(a b)\necho "${#items[@]} # quoted"\n',
    "check": "#!/usr/bin/env bash\necho ok\n",
    "agents/openai.yaml": 'interface:\n  prompt: "Use #tag"\n',
    "note.md": "# Heading\n\nText.\n",
    "page.html": "<p>https://example.com</p>\n",
    "data.json": '{"a": "# b"}\n',
    "LICENSE": "MIT # License\n",
}


class CheckCommentsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        shutil.copytree(SCRIPTS, self.root / "scripts", ignore=shutil.ignore_patterns("__pycache__", "test_*"))
        self.git("init", "-q")
        for path, text in CLEAN.items():
            self.write(path, text)
        (self.root / "linked").symlink_to("note.md")

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
            ("python3", "-I", "scripts/check-comments.py"),
            cwd=self.root, env=self.env, text=True, capture_output=True, timeout=30,
        )

    def assertRejected(self, path, text, location):
        self.write(path, text)
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"zero-comments: {location}", result.stderr)

    def test_clean_formats_shebangs_quoted_hashes_and_symlinks_pass(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_python_line_and_inline_comments_are_rejected(self):
        self.assertRejected("tool.py", "value = 1  # why\n", "tool.py:1: comment")

    def test_python_docstrings_are_rejected(self):
        self.assertRejected("tool.py", 'def run():\n    """Explain."""\n    return 1\n', "tool.py:2: comment")
        self.assertRejected("tool.py", '"""Module."""\nvalue = 1\n', "tool.py:1: comment")

    def test_shell_comments_in_extensionless_scripts_are_rejected(self):
        self.assertRejected("check", "#!/usr/bin/env bash\n# why\necho ok\n", "check:2: comment")
        self.assertRejected("run.sh", "#!/usr/bin/env bash\necho ok # why\n", "run.sh:2: comment")

    def test_yaml_and_markup_comments_are_rejected(self):
        self.assertRejected("agents/openai.yaml", "a: 1 # why\n", "agents/openai.yaml:1: comment")
        self.write("agents/openai.yaml", CLEAN["agents/openai.yaml"])
        self.assertRejected("note.md", "Text <!-- hidden -->\n", "note.md:1: comment")
        self.write("note.md", CLEAN["note.md"])
        self.assertRejected("page.html", "<script>\n  // why\n</script>\n", "page.html:2: comment")

    def test_format_without_a_scanner_is_rejected(self):
        self.assertRejected("config.ini", "a=1\n", "config.ini: no comment scanner for this format")


if __name__ == "__main__":
    unittest.main()
