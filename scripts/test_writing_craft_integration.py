"""Install/link/contract checks, not assertions about prompt prose or writing quality."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

import pytest
import install_package

ROOT = Path(__file__).resolve().parents[1]
LICENSE_SHA256 = "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5"


@pytest.fixture
def installed(tmp_path: Path) -> Path:
    target = tmp_path / "installed"
    _ = install_package.install(target, repo_root=ROOT, exclude_derived_support=True)
    return target


def test_shared_reference_and_anchor_routes_survive_temporary_install(installed: Path) -> None:
    # Given: a clean install without any separately installed Matt skills.
    shared = installed / "video-production-assets/references/writing-craft.md"
    # When: its fragment routes are resolved.
    assert shared.is_file()
    anchors = set(re.findall(r'<a id="([^"]+)"', shared.read_text()))
    # Then: all four documented entry points exist in the copied runtime.
    assert {"explore", "grounding", "shape", "interaction-and-handoff"} <= anchors


def test_pinned_license_and_provenance_are_distributed(installed: Path) -> None:
    # Given: the authorized immutable upstream license digest.
    upstream = installed / "video-production-assets/references/upstream"
    license_file = upstream / "matt-pocock-LICENSE.txt"
    provenance = upstream / "matt-pocock-writing-provenance.md"
    # When: the actual distribution files are inspected.
    assert license_file.is_file() and provenance.is_file()
    # Then: the complete license bytes, not a rewritten notice, were packaged.
    assert hashlib.sha256(license_file.read_bytes()).hexdigest() == LICENSE_SHA256


def test_new_references_resolve_inside_install_without_machine_paths(installed: Path) -> None:
    # Given: shared guidance and its portable provenance.
    refs = installed / "video-production-assets/references"
    files = [refs / "writing-craft.md", refs / "upstream/matt-pocock-writing-provenance.md"]
    # When: actual Markdown dependency paths are followed.
    for path in files:
        assert path.is_file()
        for href in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            relative = href.split("#")[0]
            if not relative or "://" in relative:
                continue
            target = (path.parent / relative).resolve()
            # Then: no author-machine path or external skill installation is needed.
            assert target.is_relative_to(installed.resolve()) and target.is_file(), (path, href)


def test_skill_registry_has_no_new_standalone_writing_owners(installed: Path) -> None:
    # Given: existing package owner registrations, not global user skills.
    manifest = json.loads((ROOT / "manifest.json").read_bytes())
    names = {p.parent.name for p in installed.glob("*/SKILL.md")}
    # When/Then: installation preserves the 22-owner public registry.
    assert len(names) == 22 and names == set(manifest["skills"])
    assert names.isdisjoint({"writing-craft", "writing-fragments", "writing-beats", "writing-shape", "grilling"})


def test_existing_project_contract_needs_no_writing_state_fields(installed: Path, tmp_path: Path) -> None:
    # Given: an existing minimal schema-1.1 plan without any new craft state.
    data = {"schema_version":"1.1", "project_id":"compat", "version":"1", "aspect_ratio":"16:9",
        "target_duration_s":2, "fps":24, "audio_mode":"no_audio", "characters":[],
        "scenes":[{"id":"S01", "purpose":"compare"}],
        "shots":[{"id":"SH01", "scene_id":"S01", "character_ids":[], "start_s":0, "end_s":2,
            "source_duration_s":2, "source_duration_status":"estimated", "purpose":"compare", "start_state":"before", "end_state":"after"}],
        "claims":[], "artifacts":[{"id":"A01", "type":"plan", "version":"1", "status":"draft", "dependencies":[], "dependency_versions":{}}]}
    project = tmp_path / "project.json"
    project.write_text(json.dumps(data))
    # When: the actually installed validator consumes the old contract.
    result = subprocess.run([sys.executable, str(installed / "video-production-assets/scripts/validate_project.py"), str(project)],
        capture_output=True, text=True, timeout=15)
    # Then: no writing-specific schema/required field was introduced.
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["valid"] is True
