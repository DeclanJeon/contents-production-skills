"""Tests for scripts/check_versions.py.

Builds minimal temporary packages to exercise each validation rule.
Nothing here reads the real repository manifest.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

CHECK = Path(__file__).resolve().parent / "check_versions.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_versions", CHECK)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(module)
    return module


def make_package(
    tmp_path: Path,
    *,
    version: str = "1.0",
    changelog_version: str | None = "1.0",
    skill_version: str | None = "1.0.0",
    metadata_style: bool = False,
    name: str = "skill-a",
    manifest_json: str | None = None,
) -> Path:
    repo = tmp_path / "pkg"
    skill_dir = repo / "skill-a"
    skill_dir.mkdir(parents=True)

    if skill_version is None:
        frontmatter = f"---\nname: {name}\n---\nbody\n"
    elif metadata_style:
        frontmatter = (
            f'---\nname: {name}\nmetadata:\n  version: "{skill_version}"\n---\nbody\n'
        )
    else:
        frontmatter = f"---\nname: {name}\nversion: {skill_version}\n---\nbody\n"
    (skill_dir / "SKILL.md").write_text(frontmatter, encoding="utf-8")

    if manifest_json is None:
        manifest_json = json.dumps({
            "version": version,
            "entry_skill": "skill-a",
            "support_skill": "skill-a",
            "skills": ["skill-a"],
        })
    (repo / "manifest.json").write_text(manifest_json, encoding="utf-8")

    heading = f"## {changelog_version} 2026-01-01" if changelog_version else None
    sections = ["# Changelog", "", "## Unreleased", "", "- stuff", ""]
    if heading:
        sections += [heading, "", "- release", ""]
    (repo / "CHANGELOG.md").write_text("\n".join(sections), encoding="utf-8")
    return repo


def test_valid_package_has_no_problems(tmp_path):
    module = load_module()
    repo = make_package(tmp_path)
    assert module.collect_problems(repo) == []


def test_missing_changelog_heading_is_reported(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, changelog_version="0.9")
    problems = module.collect_problems(repo)
    assert any("no release heading" in p for p in problems)


def test_missing_skill_version_is_reported(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, skill_version=None)
    problems = module.collect_problems(repo)
    assert any("declares no version" in p for p in problems)


def test_metadata_style_version_is_accepted(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, skill_version="1.4.1", metadata_style=True)
    assert module.collect_problems(repo) == []


def test_invalid_manifest_json_is_fatal(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, manifest_json="{not json")
    problems = module.collect_problems(repo)
    assert len(problems) == 1
    assert "not valid JSON" in problems[0]


def test_bad_package_version_format_is_reported(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, version="1.0.0")
    problems = module.collect_problems(repo)
    assert any("two-part" in p for p in problems)


def test_name_mismatch_is_reported(tmp_path):
    module = load_module()
    repo = make_package(tmp_path, name="other-name")
    problems = module.collect_problems(repo)
    assert any("does not match directory" in p for p in problems)


def test_missing_frontmatter_is_reported(tmp_path):
    module = load_module()
    repo = make_package(tmp_path)
    (repo / "skill-a" / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
    problems = module.collect_problems(repo)
    assert any("frontmatter" in p for p in problems)


def test_frontmatter_helpers():
    module = load_module()
    text = "---\nname: demo\nversion: 0.13.0\n---\nbody\n"
    frontmatter = module.parse_frontmatter(text)
    assert frontmatter is not None
    assert module.frontmatter_field(frontmatter, "name") == "demo"
    assert module.frontmatter_has_version(frontmatter)
    assert not module.frontmatter_has_version("name: demo")
    assert module.changelog_has_version("## 2.0 2026-10-02\n", "2.0")
    assert not module.changelog_has_version("## 1.9 2026-01-01\n", "2.0")
