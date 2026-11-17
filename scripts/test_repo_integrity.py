"""Repository integrity: every git-tracked file must exist in the worktree.

This exists because a whole tracked directory (`docs/`, 196 files) was found
missing from the worktree during the 2026-11-17 routing work. Nothing in the
test suite noticed, because every test only reads the files it already knows
about. This check notices.

It is deliberately cheap and offline. When git is unavailable it skips rather
than fails, so the suite still runs in an exported tarball.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]


def _tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT, capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:  # pragma: no cover
        pytest.skip(f"git unavailable: {error}")
    return [name for name in result.stdout.decode("utf-8").split("\0") if name]


def test_no_tracked_file_is_missing_from_the_worktree() -> None:
    # Given: the files git believes are in this repository
    tracked = _tracked_files()
    assert tracked, "git reported no tracked files"

    # When/Then: none of them has silently vanished or been moved away
    missing = [name for name in tracked if not (ROOT / name).exists()]
    assert not missing, (
        f"{len(missing)} tracked file(s) missing from the worktree, e.g. "
        f"{missing[:5]}"
    )


def test_tracked_docs_tree_is_present() -> None:
    """The docs tree specifically: it is audit evidence, not scratch space."""
    tracked_docs = [name for name in _tracked_files() if name.startswith("docs/")]
    if not tracked_docs:
        pytest.skip("no tracked docs in this checkout")

    missing = [name for name in tracked_docs if not (ROOT / name).exists()]
    assert not missing, f"docs evidence missing: {missing[:5]}"


def test_skill_directories_match_the_manifest() -> None:
    """Every manifest skill must be a real directory carrying a SKILL.md."""
    import json

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    missing = [
        name for name in manifest["skills"]
        if not (ROOT / name / "SKILL.md").is_file()
    ]
    assert not missing, f"manifest skills without SKILL.md: {missing}"


def test_qa_tree_has_no_symlinks_because_qa_ships() -> None:
    """`qa/` is a required support source, so the installer rejects links in it.

    A pytest run once left its numbered basetemp directories (34 symlinks) under
    `qa/`, and every installer test then failed with "support source contains a
    symlink". The message blamed the installer for something pytest had written,
    so fail here first and name the real cause.
    """
    qa = ROOT / "qa"
    if not qa.is_dir():
        pytest.skip("no qa directory")
    offenders = sorted(
        str(path.relative_to(ROOT)) for path in qa.rglob("*") if path.is_symlink())
    assert not offenders, (
        "qa/ ships with the package and must contain no symlinks; "
        f"these look like leftover pytest basetemp output: {offenders[:5]}")
