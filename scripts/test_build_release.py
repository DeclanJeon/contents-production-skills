"""Release archive contract: one installed skill root, wrapped in a versioned directory."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "build_release.py"
sys.path.insert(0, str(REPO / "scripts"))

VERSION = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))["version"]
PREFIX = f"contents-production-skills-{VERSION}"


def _run(*args: str, repo: Path = REPO) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "build_release.py"), *args],
        capture_output=True, text=True, cwd=repo,
    )


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    from build_release import build_release

    out = tmp_path_factory.mktemp("dist")
    return build_release(REPO, out)


def test_archive_layout(built):
    tar_path, _ = built
    assert tar_path.name == f"{PREFIX}.tar.gz"
    manifest = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))
    with tarfile.open(tar_path) as tar:
        names = tar.getnames()
    assert all(n == PREFIX or n.startswith(PREFIX + "/") for n in names)
    assert f"{PREFIX}/video-production-assets/support/manifest.json" in names
    for skill in manifest["skills"]:
        assert f"{PREFIX}/{skill}/SKILL.md" in names
    for banned in ("/.git/", "/qa/", "/.worktrees/", "__pycache__"):
        assert not any(banned in n + "/" for n in names if not n.startswith(f"{PREFIX}/video-production-assets/support/"))


def test_archive_is_reproducible(built, tmp_path):
    from build_release import build_release

    again, _ = build_release(REPO, tmp_path)
    assert again.read_bytes() == built[0].read_bytes()


def test_sha256_file(built):
    tar_path, sha_path = built
    assert sha_path.name == f"{PREFIX}.sha256"
    digest = hashlib.sha256(tar_path.read_bytes()).hexdigest()
    assert sha_path.read_text(encoding="utf-8") == f"{digest}  {PREFIX}.tar.gz\n"


def test_tag_mismatch_exit_2(tmp_path):
    result = _run("--out", str(tmp_path), "--tag", "v0.0")
    assert result.returncode == 2
    assert not list(tmp_path.iterdir())


def test_missing_notes_exit_3(tmp_path):
    copy = tmp_path / "repo"
    shutil.copytree(REPO, copy, ignore=shutil.ignore_patterns(".git", ".worktrees", "qa", "node_modules"))
    shutil.rmtree(copy / "docs" / "release-notes", ignore_errors=True)
    result = _run("--out", str(tmp_path / "dist"), "--tag", f"v{VERSION}", repo=copy)
    assert result.returncode == 3
