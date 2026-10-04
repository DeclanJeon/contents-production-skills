#!/usr/bin/env python3
"""Version-consistency checker for the contents-production-skills package.

Validates that the package declares one coherent version everywhere it
matters, so a single bump reaches the manifest, the changelog and every
bundled skill:

* ``manifest.json`` parses and declares ``version`` as ``X.Y``.
* ``CHANGELOG.md`` contains a release heading for that version
  (a line starting ``## `` whose text starts with the version).
* Every skill listed in the manifest has its directory, a ``SKILL.md``,
  a YAML frontmatter block, a top-level ``name:`` field, and *some*
  version declaration: either a top-level ``version:`` field or a
  ``metadata:`` block containing ``version:`` (both house styles are
  accepted).

Pure helpers (``collect_problems``) are importable by tests. No
third-party dependencies.

Usage::

    python scripts/check_versions.py [--repo-root PATH]

Exit codes: 0 consistent, 2 unusable inputs (missing/invalid manifest),
1 one or more consistency problems found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "manifest.json"
CHANGELOG_NAME = "CHANGELOG.md"
SKILL_FILE_NAME = "SKILL.md"

PACKAGE_VERSION_RE = re.compile(r"^\d+\.\d+$")
FRONTMATTER_FENCE = "---"


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def parse_frontmatter(text: str) -> str | None:
    """Return the raw frontmatter body, or None when absent/unclosed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == FRONTMATTER_FENCE:
            return "\n".join(lines[1:index])
    return None


def frontmatter_field(frontmatter: str, name: str) -> str | None:
    """Read a top-level (unindented) scalar field from a frontmatter body."""
    pattern = re.compile(rf"^{re.escape(name)}:\s*(.+?)\s*$")
    for line in frontmatter.splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip("\"'")
    return None


def frontmatter_has_version(frontmatter: str) -> bool:
    """True when any indented-or-not ``version:`` field exists."""
    return any(re.match(r"^\s+version:\s*\S", line) or
               re.match(r"^version:\s*\S", line)
               for line in frontmatter.splitlines())


def changelog_has_version(changelog: str, version: str) -> bool:
    """True when a release heading names this version."""
    for line in changelog.splitlines():
        stripped = line.strip()
        if not stripped.startswith("## "):
            continue
        heading = stripped[3:].strip()
        if heading == version or heading.startswith(version + " "):
            return True
    return False


def collect_problems(repo_root: Path) -> list[str]:
    """Return every version-consistency problem (empty list = clean)."""
    problems: list[str] = []

    manifest_path = repo_root / MANIFEST_NAME
    raw = _read_text(manifest_path)
    if raw is None:
        return [f"missing or unreadable package manifest: {manifest_path}"]
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"package manifest is not valid JSON: {manifest_path}: {exc}"]
    if not isinstance(manifest, dict):
        return [f"package manifest is not a JSON object: {manifest_path}"]

    version = manifest.get("version")
    if not isinstance(version, str) or not PACKAGE_VERSION_RE.match(version):
        problems.append(
            f"manifest 'version' must be a two-part 'X.Y' string, got: {version!r}"
        )
        version = None

    changelog_path = repo_root / CHANGELOG_NAME
    changelog = _read_text(changelog_path)
    if changelog is None:
        problems.append(f"missing or unreadable changelog: {changelog_path}")
    elif version is not None and not changelog_has_version(changelog, version):
        problems.append(
            f"CHANGELOG.md has no release heading for manifest version {version} "
            f"(expected a line like '## {version} ...'); run scripts/bump_version.py"
        )

    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        problems.append("manifest 'skills' must be a non-empty list")
        return problems

    for skill_id in skills:
        if not isinstance(skill_id, str):
            problems.append(f"unsafe skill id in manifest: {skill_id!r}")
            continue
        skill_dir = repo_root / skill_id
        if not skill_dir.is_dir():
            problems.append(f"missing skill directory: {skill_dir}")
            continue
        skill_path = skill_dir / SKILL_FILE_NAME
        text = _read_text(skill_path)
        if text is None:
            problems.append(f"missing or unreadable {SKILL_FILE_NAME}: {skill_path}")
            continue
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            problems.append(f"missing or unclosed frontmatter: {skill_path}")
            continue
        name = frontmatter_field(frontmatter, "name")
        if name is None:
            problems.append(f"frontmatter has no top-level 'name:': {skill_path}")
        elif name != skill_id:
            problems.append(
                f"frontmatter name {name!r} does not match directory {skill_id!r} "
                f"in {skill_path}"
            )
        if not frontmatter_has_version(frontmatter):
            problems.append(
                f"frontmatter declares no version (top-level or under metadata): "
                f"{skill_path}"
            )
    return problems


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_versions",
        description="Verify manifest/changelog/skill-frontmatter version "
                    "consistency for the contents-production-skills package.",
    )
    parser.add_argument("--repo-root", type=Path, default=PACKAGE_ROOT,
                        help="package source root (default: this script's repository)")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().absolute().resolve()
    if not repo_root.is_dir():
        print(f"repository root is not a directory: {repo_root}", file=sys.stderr)
        return 2

    problems = collect_problems(repo_root)
    if problems:
        print(f"version check failed ({len(problems)} problem(s)):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    manifest = json.loads((repo_root / MANIFEST_NAME).read_text(encoding="utf-8"))
    print(f"version check OK: package {manifest['version']}, "
          f"{len(manifest['skills'])} skill(s) consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
