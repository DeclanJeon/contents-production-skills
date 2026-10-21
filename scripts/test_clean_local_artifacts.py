#!/usr/bin/env python3
"""Tests for the local-artifact cleanup script."""
import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "clean_local_artifacts.py"
spec = importlib.util.spec_from_file_location("clean_local_artifacts", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CleanLocalArtifactsTests(unittest.TestCase):
    def test_backup_detection_helpers_target_only_backup_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md.from-backup").write_text("x", encoding="utf-8")
            (root / "a.md").write_text("x", encoding="utf-8")
            found = [p.name for p in root.rglob("*.from-backup")]
            self.assertEqual(found, ["a.md.from-backup"])
            self.assertNotIn("a.md", found)

    def test_stale_remote_refs_use_no_deref_semantics(self):
        # A symbolic ref must never delete the branch it points at.
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess = __import__("subprocess")
            def git(*args):
                return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
            git("init", "-q", "-b", "main")
            (repo / "f.txt").write_text("x", encoding="utf-8")
            git("add", "f.txt")
            git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
            git("update-ref", "refs/remotes/origin/main", "HEAD")
            git("symbolic-ref", "refs/remotes/origin/HEAD.from-backup", "refs/remotes/origin/main")
            out = git("for-each-ref", "--format=%(refname)", "refs/remotes").stdout
            self.assertIn("refs/remotes/origin/HEAD.from-backup", out)
            git("update-ref", "--no-deref", "-d", "refs/remotes/origin/HEAD.from-backup")
            self.assertTrue((repo / ".git" / "refs" / "remotes" / "origin" / "main").exists())
            self.assertFalse((repo / ".git" / "refs" / "remotes" / "origin" / "HEAD.from-backup").exists())

    def test_script_reports_dry_run_without_deleting(self):
        result = __import__("subprocess").run(
            ["python3", str(SCRIPT)], cwd=module.ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("dry run", result.stdout)
        self.assertIn("reclaimable", result.stdout)


if __name__ == "__main__":
    unittest.main()
