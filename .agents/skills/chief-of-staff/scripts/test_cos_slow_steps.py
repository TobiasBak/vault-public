import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

with patch.object(Path, "read_text", return_value="test-cos"):
    import cos


class SlowStepTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.proc = Path(self.temporary.name)
        (self.proc / "uptime").write_text("10000.00 0.00\n")
        (self.proc / "locks").write_text("")
        self.status = {"pool_size": 4, "slots": [], "exclusive": [], "waiters": []}

    def process(self, pid, argv, elapsed=200, cpu=0, parent=1, wchan="0", environment=()):
        directory = self.proc / str(pid)
        directory.mkdir()
        ticks = os.sysconf("SC_CLK_TCK")
        fields = ["0"] * 50
        fields[0], fields[1] = "S", str(parent)
        fields[11] = str(int(cpu * ticks))
        fields[19] = str(int((10000 - elapsed) * ticks))
        (directory / "stat").write_text(f"{pid} (name with ) spaces) " + " ".join(fields))
        (directory / "cmdline").write_bytes("\0".join(argv).encode() + b"\0")
        (directory / "wchan").write_text(wchan)
        (directory / "environ").write_bytes(b"\0".join(environment))
        (directory / "cwd").symlink_to("/worktrees/orderready-topic")
        (directory / "fd").mkdir()
        return directory

    def output(self, status_error=None):
        result = subprocess.CompletedProcess([], 0, json.dumps(self.status), "")
        with patch.object(cos.subprocess, "run", side_effect=status_error, return_value=result) as run, contextlib.redirect_stdout(io.StringIO()) as out:
            cos.slow_steps(self.proc)
        if run.called:
            self.assertEqual(run.call_args.args[0], ["heavy-lease", "status", "--json"])
            self.assertLessEqual(run.call_args.kwargs["timeout"], .5)
        return out.getvalue()

    def test_slow_launchers_hooks_checks_and_descendants(self):
        commands = [
            ["/repo/tools/or", "static"], ["cargo", "xtask", "gate"],
            ["bash", "/repo/.githooks/pre-commit"], ["python", "scripts/check.py"],
            ["mise", "exec", "--", "python", "check.py"], ["mise", "env"],
        ]
        for pid, argv in enumerate(commands, 10):
            self.process(pid, argv, elapsed=200, cpu=100)
        self.process(20, ["compiler"], parent=10, environment=[b"T3_THREAD_ID=thread:test"])
        output = self.output()
        self.assertEqual(output.count("SLOW STEP"), 7)
        self.assertIn("pid=10 elapsed=200s cpu-life=50.0% cwd=/worktrees/orderready-topic", output)
        self.assertIn("T3_THREAD_ID=thread:test", output)

    def test_normal_short_preparation_and_unrelated_long_processes_are_silent(self):
        self.process(10, ["tools/or", "static"], elapsed=119)
        self.process(11, ["mise", "install", "--quiet"], elapsed=59)
        self.process(12, ["unrelated-daemon"], elapsed=9000)
        self.process(13, ["mise", "install"], elapsed=20, wchan="locks_lock_inode_wait")
        self.assertEqual(self.output(), "")

    def test_preparation_has_lower_threshold_and_inherits_agent_identity(self):
        self.process(10, ["tools/or", "static"], elapsed=100,
                     environment=[b"PI_SESSION_ID=session-123", b"PASSWORD=not-output"])
        self.process(11, ["mise", "install", "--quiet"], elapsed=61, cpu=60, parent=10)
        output = self.output()
        self.assertIn("SLOW STEP pid=11 elapsed=61s", output)
        self.assertIn("PI_SESSION_ID=session-123", output)
        self.assertNotIn("SLOW STEP pid=10", output)
        self.assertNotIn("not-output", output)

    def test_mise_global_option_values_do_not_hide_preparation(self):
        commands = [
            ["mise", "--cd", "/repo", "install"], ["mise", "-E", "dev", "install"],
            ["mise", "-j", "2", "install"], ["mise", "--cd=/repo", "install"],
            ["mise", "-Edev", "install"], ["mise", "--jobs=2", "install"],
        ]
        self.process(10, ["tools/or", "test"])
        for pid, argv in enumerate(commands, 20):
            self.process(pid, argv, elapsed=61, parent=10 if pid % 2 else 1)
        self.status["slots"] = [{"name": "slot-0", "holder": {"pid": 10}}]
        output = self.output()
        self.assertEqual(output.count("SLOW STEP"), len(commands))
        for pid in range(20, 20 + len(commands)):
            self.assertIn(f"SLOW STEP pid={pid} elapsed=61s", output)
        self.assertNotIn("SLOW STEP pid=10", output)

    def test_idle_watcher_and_waiting_launcher_are_excluded(self):
        self.process(10, ["tools/or", "__watch-payload", "--idle"])
        self.process(11, ["sleep", "infinity"], parent=10)
        self.process(12, ["mise", "exec", "--", "tools/or", "__watch-payload", "--idle"])
        self.assertEqual(self.output(), "")

    def test_admitted_jobs_and_waiting_wrappers_excluded_but_not_preparation(self):
        self.process(10, ["tools/or", "test"])
        self.process(11, ["cargo", "xtask", "test"], parent=10)
        self.process(12, ["test-binary"], parent=11, elapsed=500)
        self.process(13, ["mise", "install"], parent=11, elapsed=61)
        for resource in ("slots", "exclusive"):
            with self.subTest(resource=resource):
                self.status[resource] = [{"name": "slot-0" if resource == "slots" else "exclusive-win-vm",
                                          "holder": {"pid": 11}}]
                output = self.output()
                self.assertEqual(output.count("SLOW STEP"), 1)
                self.assertIn("pid=13", output)
                self.status[resource] = []
        self.status["waiters"] = [{"pid": 11}]
        self.assertIn("pid=11", self.output())

    def test_lock_wait_names_shared_file_and_holder(self):
        holder = self.process(10, ["mise", "install"], elapsed=360, cpu=355)
        waiter = self.process(11, ["mise", "install"], elapsed=45, wchan="locks_lock_inode_wait")
        lock = self.proc / "mise-install.lock"
        lock.touch()
        for directory in (holder, waiter):
            (directory / "fd/8").symlink_to(lock)
        stat = lock.stat()
        for mount_device in (os.minor(stat.st_dev), os.minor(stat.st_dev) + 100):
            with self.subTest(mount_device=mount_device):
                identity = f"{os.major(stat.st_dev):02x}:{mount_device:02x}:{stat.st_ino}"
                (self.proc / "locks").write_text(
                    f"1: FLOCK ADVISORY WRITE 10 {identity} 0 EOF\n"
                    f"1: -> FLOCK ADVISORY WRITE 11 {identity} 0 EOF\n")
                (waiter / "mountinfo").write_text(
                    f"58 25 {os.major(stat.st_dev)}:{mount_device} / /home rw - btrfs /dev/root rw\n")
                (waiter / "fdinfo").mkdir(exist_ok=True)
                (waiter / "fdinfo/8").write_text("pos: 0\nmnt_id:\t58\n")
                output = self.output()
                self.assertIn("LOCK WAIT pid=11 elapsed=45s", output)
                self.assertIn("wait-age=unknown (snapshot)", output)
                self.assertIn(f"lock={lock} holder=10", output)
                self.assertNotIn("SLOW STEP pid=11", output)

    def test_lock_wait_still_reports_when_lock_details_or_process_files_disappear(self):
        directory = self.process(10, ["tools/or"], elapsed=31, wchan="locks_lock_inode_wait")
        (directory / "cwd").unlink()
        (directory / "environ").unlink()
        (self.proc / "locks").unlink()
        vanished = self.proc / "11"
        vanished.mkdir()
        (vanished / "stat").write_text("gone")
        output = self.output()
        self.assertIn("LOCK WAIT pid=10", output)
        self.assertIn("lock=unknown holder=unknown", output)
        self.assertIn("cwd=unknown", output)

    def test_secrets_are_redacted_before_truncation_and_control_characters_removed(self):
        self.process(10, ["tools/or", "--token", "token-value with spaces", "--password=pass-value",
                          "API_KEY=key-value", "--key", "private-value", "https://user:url-password@example.test/path"])
        self.process(12, ["tools/or", "--database-url", "postgresql://user:db-password@example.test/db"])
        self.process(11, ["bash", ".githooks/pre-commit", "-c",
                          'run --password "quoted secret words"; TOKEN=shell-secret; auth Bearer bearer-secret\nnext'])
        output = self.output()
        for secret in ("token-value", "with spaces", "pass-value", "key-value", "private-value",
                       "url-password", "db-password", "quoted secret words", "shell-secret", "bearer-secret"):
            self.assertNotIn(secret, output)
        self.assertIn("[redacted]", output)
        self.assertEqual(len(output.splitlines()), 3)

    def test_shell_quoting_cannot_bypass_secret_redaction(self):
        payloads = [
            'tools/or "--token" "SYNTHETIC_SENTINEL"',
            'tools/or --token="prefix"SYNTHETIC_SENTINEL',
            "tools/or --password=prefix'quoted words'SYNTHETIC_SENTINEL",
        ]
        commands = [["bash", "-lc", payload, "SYNTHETIC_POSITIONAL"] for payload in payloads]
        commands.extend([
            ["busybox", "sh", "-c", payloads[0]],
            ["busybox", "ash", "-c", payloads[0]],
            ["unknown-shell", "-c", payloads[0]],
            ["python3", "-c", payloads[0]],
            ["fish", "--command=" + payloads[0]],
        ])
        for pid, argv in enumerate(commands, 20):
            self.process(pid, argv, parent=10)
        self.process(10, ["tools/or", "static"])
        output = self.output()
        self.assertNotIn("SYNTHETIC_", output)
        self.assertEqual(output.count("[payload omitted]"), len(commands))

    def test_scheduler_failure_is_visible_without_hiding_slow_steps(self):
        self.process(10, ["tools/or", "static"])
        output = self.output(subprocess.TimeoutExpired("heavy-lease", .3))
        self.assertIn("GAP slow-steps", output)
        self.assertIn("SLOW STEP pid=10", output)


if __name__ == "__main__":
    unittest.main()
