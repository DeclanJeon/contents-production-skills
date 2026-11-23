import json
from pathlib import Path

import pytest

import install_package as installer
from build_cineforge_inventory import ROOT, build
from test_install_package import make_repo, write_file


@pytest.mark.parametrize("relative", ["integrations/cineforge/files.json", "../outside.json"])
def test_installer_copies_inventory_or_refuses_escape(tmp_path: Path, relative: str) -> None:
    source = make_repo(tmp_path / "repo", extra_manifest={"integrations": {"cineforge": {"inventory": relative}}})
    inventory = write_file(source, "integrations/cineforge/files.json", json.dumps({"alpha-skill/SKILL.md": "digest"}))
    installed = tmp_path / "installed"
    if relative.startswith("../"):
        with pytest.raises(installer.PreflightError, match="inventory"):
            installer.install(installed, repo_root=source)
        assert not installed.exists()
    else:
        installer.install(installed, repo_root=source)
        assert (installed / "alpha-skill/support" / relative).read_bytes() == inventory.read_bytes()


def test_missing_inventory_does_not_install(tmp_path: Path) -> None:
    source = make_repo(tmp_path / "repo", extra_manifest={
        "integrations": {"cineforge": {"inventory": "integrations/cineforge/files.json"}}
    })
    with pytest.raises(installer.PreflightError, match="inventory"):
        installer.install(tmp_path / "installed", repo_root=source)
    assert not (tmp_path / "installed").exists()


def test_inventory_collision_requires_explicit_derived_exclusion(tmp_path: Path) -> None:
    relative = installer.CINEFORGE_INVENTORY.as_posix()
    source = make_repo(tmp_path / "repo", extra_manifest={"integrations": {"cineforge": {"inventory": relative}}})
    inventory = write_file(source, relative, '{"current": "digest"}')
    prior = write_file(source / 'alpha-skill/support', relative, '{"prior": "digest"}')
    target = tmp_path / 'installed'
    with pytest.raises(installer.PreflightError, match='support collision'):
        installer.install(target, repo_root=source)
    assert not target.exists()
    installer.install(target, repo_root=source, exclude_derived_support=True)
    assert (target / 'alpha-skill/support' / relative).read_bytes() == inventory.read_bytes()
    assert 'prior' in prior.read_text()


def test_checked_in_inventory_tracks_skill_bytes() -> None:
    path = ROOT / installer.CINEFORGE_INVENTORY
    assert path.read_bytes() == build(ROOT).encode("utf-8")
