"""Installer regression for dependency metadata, not prompt/agent behavior tests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Final

import install_package

ROOT: Final = Path(__file__).resolve().parents[1]


def test_installed_manifest_retains_external_coordination_without_installing_it(
    tmp_path: Path,
) -> None:
    # Given: an isolated destination; no real user skill root is touched.
    target = tmp_path / "installed"

    # When: the real installer copies the package and its support manifest.
    result = install_package.install(
        target, repo_root=ROOT, exclude_derived_support=True,
    )

    # Then: consumers can discover the external prerequisite without it being
    # bundled, installed, or misrepresented as a verified runtime.
    installed_manifest = json.loads(
        (target / "video-production-assets/support/manifest.json").read_text(
            encoding="utf-8",
        ),
    )
    dependencies = [
        entry for entry in installed_manifest["external_dependencies"]
        if "ai-delegation-loop" in entry["skills"]
    ]
    assert len(dependencies) == 1
    dependency = dependencies[0]
    assert dependency["verified"] is False
    assert dependency["auto_install"] is False
    assert dependency["runtime"] is None
    assert dependency["auth"] is None
    assert dependency["upstream_version"] is None
    assert "ai-delegation-loop" not in installed_manifest["skills"]
    assert "ai-delegation-loop" not in {skill.name for skill in result.installed}
    assert not (target / "ai-delegation-loop").exists()
