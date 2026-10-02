#!/usr/bin/env python3
"""Deterministic unittest scenarios for scripts/install_package.py.

Runs entirely against temporary directories through the public installer
functions (build_plan/install/main); no real user skill root is touched.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
import shutil
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import install_package as ip


def write_file(root: Path, rel: str, text: str = "x") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_repo(
    root: Path,
    skills=("alpha-skill", "omega-skill"),
    *,
    support_skill="alpha-skill",
    with_support=True,
    version="0.0-test",
    extra_manifest=None,
) -> Path:
    """Create a minimal package repo: skill dirs + manifest + support."""
    for skill in skills:
        write_file(root / skill, "SKILL.md", f"# {skill}\n")
        write_file(root / skill, "references/ref.md", "ref\n")
    if with_support:
        write_file(root, "examples/demo/example.txt", "example\n")
        write_file(root, "qa/audit.json", '{"ok": true}\n')
    manifest = {
        "version": version,
        "skills": list(skills),
        "support_skill": support_skill,
        "entry_skill": skills[0],
        "examples": 1,
    }
    if extra_manifest:
        manifest.update(extra_manifest)
    write_file(root, "manifest.json", json.dumps(manifest))
    return root


def list_tree(root: Path):
    if not root.exists():
        return []
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))


class FreshInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = make_repo(self.base / "repo")
        self.root = self.base / "skills-root"

    def test_fresh_install_copies_skills_support_and_excludes_caches(self):
        write_file(
            self.repo / "alpha-skill" / "scripts" / "__pycache__",
            "mod.pyc",
            "bytecode\n",
        )
        result = ip.install(self.root, repo_root=self.repo)

        self.assertEqual(
            sorted(p.name for p in result.installed),
            ["alpha-skill", "omega-skill"],
        )
        self.assertTrue((self.root / "alpha-skill" / "SKILL.md").is_file())
        self.assertTrue(
            (self.root / "alpha-skill" / "references" / "ref.md").is_file()
        )
        self.assertTrue((self.root / "omega-skill" / "SKILL.md").is_file())
        self.assertFalse(
            (self.root / "alpha-skill" / "scripts" / "__pycache__").exists()
        )

        support = self.root / "alpha-skill" / "support"
        self.assertTrue((support / "manifest.json").is_file())
        self.assertTrue((support / "examples" / "demo" / "example.txt").is_file())
        self.assertEqual(json.loads((support / "manifest.json").read_text())["version"], "0.0-test")
        self.assertEqual(result.package_version, "0.0-test")
        self.assertEqual(result.support_root, support)



class PreflightFailureTests(unittest.TestCase):
    """Every failure mode below must leave the target root byte-identical."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = make_repo(self.base / "repo")
        self.root = self.base / "skills-root"

    def assert_no_writes(self, snapshot_before):
        self.assertEqual(list_tree(self.root), snapshot_before)

    def test_late_collision_aborts_with_zero_writes(self):
        # omega-skill is last in the manifest order; its existing target must
        # still prevent alpha-skill's copy.
        write_file(self.root / "omega-skill", "SKILL.md", "user-owned\n")
        before = list_tree(self.root)

        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.repo)
        self.assertTrue(
            any("omega-skill" in p for p in ctx.exception.problems),
            ctx.exception.problems,
        )
        self.assert_no_writes(before)
        self.assertEqual(
            (self.root / "omega-skill" / "SKILL.md").read_text(), "user-owned\n"
        )

    def test_missing_skill_source_aborts_with_zero_writes(self):
        for p in sorted((self.repo / "omega-skill").rglob("*"), reverse=True):
            p.rmdir() if p.is_dir() else p.unlink()
        (self.repo / "omega-skill").rmdir()

        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.repo)
        self.assertTrue(any("missing skill source" in p for p in ctx.exception.problems))
        self.assert_no_writes([])

    def test_missing_support_source_aborts_with_zero_writes(self):
        for p in sorted((self.repo / "qa").rglob("*"), reverse=True):
            p.rmdir() if p.is_dir() else p.unlink()
        (self.repo / "qa").rmdir()

        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.repo)
        self.assertTrue(
            any("support" in p for p in ctx.exception.problems),
            ctx.exception.problems,
        )
        self.assert_no_writes([])

    def test_unsafe_and_duplicate_ids_rejected(self):
        make_repo(
            self.base / "bad-repo",
            skills=("ok-skill",),
            extra_manifest={
                "skills": ["../evil", "ok-skill", "ok-skill"],
                "support_skill": "ok-skill",
            },
        )
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.base / "bad-repo")
        problems = "\n".join(ctx.exception.problems)
        self.assertIn("unsafe skill id", problems)
        self.assertIn("duplicate skill id", problems)
        self.assert_no_writes([])

    def test_overlapping_roots_rejected(self):
        # skills root inside the repo source.
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.build_plan(self.repo / "inner-root", repo_root=self.repo)
        self.assertTrue(any("overlaps the repository" in p for p in ctx.exception.problems))
        self.assertFalse((self.repo / "inner-root").exists())

        # backup dir inside the skills root.
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.build_plan(
                self.root,
                repo_root=self.repo,
                replace=True,
                backup_dir=self.root / "backups",
            )
        self.assertTrue(any("backup directory overlaps" in p for p in ctx.exception.problems))

        # alias root identical to skills root.
        (self.root).mkdir(parents=True)
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.build_plan(self.root, repo_root=self.repo, alias_root=self.root)
        self.assertTrue(any("alias root overlaps the skills root" in p for p in ctx.exception.problems))

    def test_replace_requires_backup_dir(self):
        write_file(self.root / "alpha-skill", "SKILL.md", "old\n")
        before = list_tree(self.root)
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.repo, replace=True)
        self.assertTrue(any("backup-dir" in p for p in ctx.exception.problems))
        self.assert_no_writes(before)

    def test_nonexistent_alias_root_rejected(self):
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.build_plan(
                self.root, repo_root=self.repo, alias_root=self.base / "no-such"
            )
        self.assertTrue(any("alias root" in p for p in ctx.exception.problems))

    def test_empty_manifest_is_rejected_before_target_creation(self):
        write_file(self.repo, "manifest.json", "{}")
        with self.assertRaises(ip.PreflightError):
            ip.install(self.root, repo_root=self.repo)
        self.assertFalse(self.root.exists())

    def test_malformed_manifest_roles_abort_without_writes(self):
        original = json.loads((self.repo / "manifest.json").read_text())
        for key in ("entry_skill", "support_skill"):
            with self.subTest(key=key):
                data = dict(original)
                data[key] = []
                write_file(self.repo, "manifest.json", json.dumps(data))
                with self.assertRaises(ip.PreflightError):
                    ip.install(self.root, repo_root=self.repo)
                self.assertFalse(self.root.exists())

    def test_support_directory_replaced_by_file_is_rejected(self):
        shutil.rmtree(self.repo / "qa")
        write_file(self.repo, "qa", "not a QA directory")
        with self.assertRaises(ip.PreflightError):
            ip.install(self.root, repo_root=self.repo)
        self.assertFalse(self.root.exists())

    def test_source_support_collisions_abort_before_backups_or_copies(self):
        for index, rel in enumerate(("support", "support/manifest.json", "support/examples/existing.txt")):
            with self.subTest(rel=rel):
                source = make_repo(self.base / f"source-{index}")
                write_file(source / "alpha-skill", rel, "source support bytes")
                target = self.base / f"target-{index}"
                backup = self.base / f"backup-{index}"
                write_file(target / "alpha-skill", "SKILL.md", "old installed bytes")
                with self.assertRaises(ip.PreflightError):
                    ip.install(target, repo_root=source, replace=True, backup_dir=backup)
                self.assertEqual((target / "alpha-skill" / "SKILL.md").read_text(),
                                 "old installed bytes")
                self.assertFalse((target / "omega-skill").exists())
                self.assertFalse(backup.exists())

    def test_existing_file_as_target_root_is_preflight_error(self):
        write_file(self.base, "skills-root", "user bytes")
        with self.assertRaises(ip.PreflightError):
            ip.install(self.root, repo_root=self.repo)
        self.assertEqual(self.root.read_text(), "user bytes")

    def test_linked_target_root_does_not_modify_external_directory(self):
        external = self.base / "external"
        external.mkdir()
        try:
            self.root.symlink_to(external, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"host cannot create directory symlinks: {exc}")
        with self.assertRaises(ip.PreflightError):
            ip.install(self.root, repo_root=self.repo)
        self.assertEqual(list(external.iterdir()), [])


class ReplaceAndMigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = make_repo(self.base / "repo")
        self.root = self.base / "skills-root"
        self.backup = self.base / "backup"

    def test_replace_backs_up_old_bytes(self):
        write_file(self.root / "alpha-skill", "SKILL.md", "old-alpha\n")
        write_file(self.root / "alpha-skill", "user-note.txt", "keep-me\n")

        result = ip.install(
            self.root,
            repo_root=self.repo,
            replace=True,
            backup_dir=self.backup,
        )
        self.assertEqual(len(result.installed), 2)
        backed = self.backup / "skills" / "alpha-skill"
        self.assertEqual((backed / "SKILL.md").read_text(), "old-alpha\n")
        self.assertEqual((backed / "user-note.txt").read_text(), "keep-me\n")
        self.assertEqual(
            (self.root / "alpha-skill" / "SKILL.md").read_text(), "# alpha-skill\n"
        )
        self.assertTrue((self.root / "alpha-skill" / "support" / "manifest.json").is_file())

    def test_replace_refuses_existing_backup_destination(self):
        write_file(self.root / "alpha-skill", "SKILL.md", "old-alpha\n")
        write_file(self.backup / "skills" / "alpha-skill", "SKILL.md", "earlier\n")
        before = list_tree(self.root)

        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(
                self.root,
                repo_root=self.repo,
                replace=True,
                backup_dir=self.backup,
            )
        self.assertTrue(any("backup destination" in p for p in ctx.exception.problems))
        self.assertEqual(list_tree(self.root), before)
        self.assertEqual((self.root / "alpha-skill" / "SKILL.md").read_text(), "old-alpha\n")
        self.assertEqual((self.backup / "skills" / "alpha-skill" / "SKILL.md").read_text(),
                         "earlier\n")

    def test_alias_duplicate_migrated_and_unrelated_preserved(self):
        alias = self.base / "alias-root"
        write_file(alias / "omega-skill", "SKILL.md", "alias-old\n")
        write_file(alias / "unrelated-skill", "SKILL.md", "not-managed\n")

        # Without --replace the duplicate is a hard preflight failure.
        with self.assertRaises(ip.PreflightError) as ctx:
            ip.install(self.root, repo_root=self.repo, alias_root=alias)
        self.assertTrue(any("alias root" in p for p in ctx.exception.problems))
        self.assertFalse(self.root.exists())
        self.assertTrue((alias / "omega-skill" / "SKILL.md").is_file())

        result = ip.install(
            self.root,
            repo_root=self.repo,
            replace=True,
            backup_dir=self.backup,
            alias_root=alias,
        )
        self.assertEqual(len(result.installed), 2)
        # Only the managed duplicate was moved; unrelated skill preserved.
        self.assertFalse((alias / "omega-skill").exists())
        self.assertEqual(
            (self.backup / "alias" / "omega-skill" / "SKILL.md").read_text(),
            "alias-old\n",
        )
        self.assertEqual(
            (alias / "unrelated-skill" / "SKILL.md").read_text(), "not-managed\n"
        )
        self.assertTrue((self.root / "omega-skill" / "SKILL.md").is_file())

    def test_copy_failure_reports_partial_path_and_retained_backup(self):
        write_file(self.root / "alpha-skill", "SKILL.md", "old-alpha")

        def interrupted_copy(source, target, **kwargs):
            write_file(Path(target), "partial.txt", "partial bytes")
            raise OSError("injected interruption")

        with patch.object(ip.shutil, "copytree", side_effect=interrupted_copy):
            with self.assertRaises(ip.InstallError) as ctx:
                ip.install(self.root, repo_root=self.repo, replace=True,
                           backup_dir=self.backup)
        self.assertIn(self.root / "alpha-skill", ctx.exception.applied)
        self.assertEqual((self.root / "alpha-skill" / "partial.txt").read_text(),
                         "partial bytes")
        self.assertEqual((self.backup / "skills" / "alpha-skill" / "SKILL.md").read_text(),
                         "old-alpha")
        self.assertEqual(ctx.exception.backups[0].existing, self.root / "alpha-skill")


class RootResolutionTests(unittest.TestCase):
    def test_default_root_prefers_codex_home(self):
        root = ip.default_skills_root(
            env={"CODEX_HOME": "C:/codex"}, home=Path("C:/home")
        )
        self.assertEqual(root, Path("C:/codex") / "skills")

    def test_default_root_falls_back_to_home_codex(self):
        root = ip.default_skills_root(env={}, home=Path("C:/home"))
        self.assertEqual(root, Path("C:/home") / ".codex" / "skills")

    def test_cli_preflight_failure_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = make_repo(base / "repo")
            root = base / "root"
            write_file(root / "alpha-skill", "SKILL.md", "old\n")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                rc = ip.main(
                    ["--repo-root", str(repo), "--skills-root", str(root)]
                )
            self.assertEqual(rc, 2)
            self.assertEqual(
                (root / "alpha-skill" / "SKILL.md").read_text(), "old\n"
            )
            self.assertFalse((root / "omega-skill").exists())


if __name__ == "__main__":
    unittest.main()
