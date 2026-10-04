"""Tests for scripts/sync_installed.py.

Runs the synchronizer as a subprocess against a temporary fake package
and temporary skill roots, on both Windows (junctions) and POSIX
(symlinks). Nothing here touches the real installation roots.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
SYNC = SCRIPTS / "sync_installed.py"
SKILL_MD = "---\nname: {name}\nversion: 1.0.0\n---\n{name} body\n"


def load_module():
    spec = importlib.util.spec_from_file_location("sync_installed", SYNC)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(module)
    return module


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    for skill in ("skill-a", "skill-b"):
        skill_dir = repo / skill
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            SKILL_MD.format(name=skill), encoding="utf-8"
        )
    (repo / "manifest.json").write_text(
        json.dumps({
            "version": "1.0",
            "entry_skill": "skill-a",
            "support_skill": "skill-a",
            "skills": ["skill-a", "skill-b"],
        }),
        encoding="utf-8",
    )
    (repo / "examples").mkdir()
    (repo / "examples" / "demo.md").write_text("demo", encoding="utf-8")
    (repo / "qa").mkdir()
    (repo / "qa" / "check.json").write_text("{}", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## Unreleased\n\n- stuff\n\n## 1.0 2026-01-01\n\n- init\n",
        encoding="utf-8",
    )
    return repo


def run_sync(repo: Path, roots: list[Path], *extra: str):
    cmd = [sys.executable, str(SYNC), "--repo-root", str(repo)]
    for root in roots:
        cmd += ["--root", str(root)]
    cmd += list(extra)
    return subprocess.run(cmd, capture_output=True, text=True)


def summary_counts(output: str) -> dict:
    for line in output.splitlines():
        if line.startswith("summary:"):
            return dict(
                part.split("=", 1)
                for part in line.split(":", 1)[1].strip().split()
            )
    raise AssertionError(f"no summary line in output:\n{output}")


@pytest.fixture()
def env(tmp_path: Path):
    repo = make_repo(tmp_path)
    roots = [tmp_path / "root1", tmp_path / "root2"]
    backup = tmp_path / "backup"
    return repo, roots, backup


def test_creates_links_readable_through_link(env):
    repo, roots, backup = env
    module = load_module()

    proc = run_sync(repo, roots, "--backup-root", str(backup))
    assert proc.returncode == 0, proc.stderr

    for root in roots:
        for skill in ("skill-a", "skill-b"):
            link = root / skill
            assert link.is_dir()
            assert module._is_link(link), f"not a link: {link}"
            text = (link / "SKILL.md").read_text(encoding="utf-8")
            assert f"{skill} body" in text

    # The derived support payload exists inside the repo, not the roots.
    assert (repo / "skill-a" / "support" / "manifest.json").is_file()
    assert (repo / "skill-a" / "support" / "examples" / "demo.md").is_file()


def test_second_run_is_idempotent(env):
    repo, roots, backup = env
    first = run_sync(repo, roots, "--backup-root", str(backup))
    assert first.returncode == 0, first.stderr
    counts = summary_counts(first.stdout)
    assert counts == {"created": "4", "repointed": "0",
                      "skipped": "0", "backed_up": "0"}

    second = run_sync(repo, roots, "--backup-root", str(backup))
    assert second.returncode == 0, second.stderr
    counts = summary_counts(second.stdout)
    assert counts == {"created": "0", "repointed": "0",
                      "skipped": "4", "backed_up": "0"}


def test_real_dir_displaced_to_backup(env):
    repo, roots, backup = env
    module = load_module()

    occupied = roots[0] / "skill-a"
    occupied.mkdir(parents=True)
    (occupied / "OLD.txt").write_text("keep me", encoding="utf-8")

    proc = run_sync(repo, roots, "--backup-root", str(backup))
    assert proc.returncode == 0, proc.stderr

    assert module._is_link(roots[0] / "skill-a")
    saved = backup / roots[0].name / "skill-a" / "OLD.txt"
    assert saved.is_file()
    assert saved.read_text(encoding="utf-8") == "keep me"
    # The link now serves the repository content.
    text = (roots[0] / "skill-a" / "SKILL.md").read_text(encoding="utf-8")
    assert "skill-a body" in text


def test_dry_run_mutates_nothing(env):
    repo, roots, backup = env
    proc = run_sync(repo, roots, "--backup-root", str(backup), "--dry-run")
    assert proc.returncode == 0, proc.stderr
    assert "nothing written" in proc.stdout

    assert not (roots[0] / "skill-a").exists()
    assert not (roots[0]).exists() or not any(roots[0].iterdir())
    assert not (repo / "skill-a" / "support").exists()


def test_stale_link_is_repointed(env):
    repo, roots, _backup = env
    module = load_module()

    elsewhere = env[0].parent / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "SKILL.md").write_text("stale", encoding="utf-8")
    roots[0].mkdir(parents=True)
    module._create_link(roots[0] / "skill-a", elsewhere)

    proc = run_sync(repo, roots, "--backup-root", str(_backup))
    assert proc.returncode == 0, proc.stderr
    assert "repointed=1" in proc.stdout

    text = (roots[0] / "skill-a" / "SKILL.md").read_text(encoding="utf-8")
    assert "skill-a body" in text


def test_remove_link_never_deletes_target_content(env):
    repo, _roots, _backup = env
    module = load_module()

    link = repo.parent / "link-to-skill-a"
    module._create_link(link, repo / "skill-a")
    assert module._is_link(link)

    module._remove_link(link)

    assert not link.exists()
    assert (repo / "skill-a" / "SKILL.md").is_file()
    assert "skill-a body" in (repo / "skill-a" / "SKILL.md").read_text(
        encoding="utf-8"
    )


def test_remove_link_refuses_real_directory(env):
    repo, _roots, _backup = env
    module = load_module()
    with pytest.raises(module.SyncError):
        module._remove_link(repo / "skill-a")


def test_preflight_failure_writes_nothing(env):
    repo, roots, backup = env
    manifest = json.loads((repo / "manifest.json").read_text(encoding="utf-8"))
    manifest["skills"].append("missing-skill")
    (repo / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    proc = run_sync(repo, roots, "--backup-root", str(backup))
    assert proc.returncode == 2
    assert "missing skill source" in proc.stderr
    assert not (roots[0] / "skill-a").exists()
    assert not (repo / "skill-a" / "support").exists()


def test_summary_counts_parse(env):
    repo, roots, backup = env
    proc = run_sync(repo, roots, "--backup-root", str(backup))
    assert proc.returncode == 0, proc.stderr
    counts = summary_counts(proc.stdout)
    assert int(counts["created"]) == 4
