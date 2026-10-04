#!/usr/bin/env python3
"""Single-command package version bump.

Keeps the package's declared version coherent in one move:

* updates ``manifest.json`` ``version`` (two-part ``X.Y``),
* promotes the current ``## Unreleased`` changelog bullets under a new
  ``## <X.Y> <date>`` release heading and leaves ``## Unreleased``
  ready for the next cycle,
* optionally (``--bump-skills``) increments the *minor* component of
  every bundled skill's ``SKILL.md`` version frontmatter in lockstep
  (``0.13.0 -> 0.14.0``, ``metadata.version "1.4.1" -> "1.5.0"``),
  preserving quote style and field location.

Usage::

    python scripts/bump_version.py 2.1
    python scripts/bump_version.py --part minor
    python scripts/bump_version.py 2.1 --bump-skills

Exit codes: 0 bumped, 2 invalid arguments or the target version already
exists in the changelog (nothing written).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "manifest.json"
CHANGELOG_NAME = "CHANGELOG.md"

PACKAGE_VERSION_RE = re.compile(r"^\d+\.\d+$")
UNRELEASED_HEADING = "## Unreleased"
SKILL_VERSION_RE = re.compile(
    r"^(?P<prefix>\s*version:\s*[\"']?)(?P<major>\d+)\.(?P<minor>\d+)"
    r"(?:\.(?P<patch>\d+))?(?P<suffix>[\"']?)\s*$"
)
METADATA_VERSION_RE = re.compile(
    r"^(?P<indent>\s+)version:\s*(?P<q1>[\"']?)(?P<major>\d+)\.(?P<minor>\d+)"
    r"(?:\.(?P<patch>\d+))?(?P<q2>[\"']?)\s*$"
)


def bump_two_part(version: str, part: str) -> str:
    major, minor = (int(x) for x in version.split("."))
    if part == "major":
        major += 1
    else:
        minor += 1
    return f"{major}.{minor}"


def derive_version(current: str, explicit: str | None, part: str | None) -> str:
    if explicit is not None:
        if not PACKAGE_VERSION_RE.match(explicit):
            raise ValueError(f"version must match 'X.Y': {explicit!r}")
        return explicit
    if not PACKAGE_VERSION_RE.match(current):
        raise ValueError(f"current manifest version is not 'X.Y': {current!r}")
    return bump_two_part(current, part or "minor")


def split_changelog(text: str) -> tuple[list[str], list[str], list[str]]:
    """Split into (lines before Unreleased body, Unreleased body, rest).

    ``rest`` starts at the next ``## `` heading after Unreleased, or is
    empty when Unreleased is the last section.
    """
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if line.strip() == UNRELEASED_HEADING:
            start = index
            break
    if start is None:
        raise ValueError("CHANGELOG.md has no '## Unreleased' heading")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    head = lines[: start + 1]
    body = lines[start + 1: end]
    rest = lines[end:]
    return head, body, rest


def changelog_has_version(text: str, version: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            if heading == version or heading.startswith(version + " "):
                return True
    return False


def rewrite_changelog(text: str, version: str, release_date: str) -> str:
    if changelog_has_version(text, version):
        raise ValueError(f"CHANGELOG.md already has a heading for {version}")
    head, body, rest = split_changelog(text)
    body_text = "".join(body).strip("\n")
    if not body_text:
        body_text = f"- Release {version}."
    block = f"## {version} {release_date}\n\n{body_text}\n\n"
    return "".join(head) + "\n" + block + "".join(rest)


def _is_indented(line: str) -> bool:
    return line.startswith((" ", "\t"))


def bump_skill_version(text: str) -> tuple[str, bool]:
    """Increment the minor component of the first version field found.

    Top-level ``version:`` fields are preferred; an indented
    ``metadata:`` version is used when no top-level field exists.
    Quote style and field indentation are preserved, and a third
    component is only kept when the original declared one.
    """
    lines = text.splitlines(keepends=True)

    for index, line in enumerate(lines):
        stripped = line.rstrip("\n")
        if _is_indented(stripped):
            continue
        match = SKILL_VERSION_RE.match(stripped)
        if match:
            patch = f".{match.group('patch')}" if match.group("patch") else ""
            lines[index] = (
                f"{match.group('prefix')}{match.group('major')}."
                f"{int(match.group('minor')) + 1}{patch}"
                f"{match.group('suffix')}\n"
            )
            return "".join(lines), True

    for index, line in enumerate(lines):
        stripped = line.rstrip("\n")
        if not _is_indented(stripped):
            continue
        match = METADATA_VERSION_RE.match(stripped)
        if match:
            patch = f".{match.group('patch')}" if match.group("patch") else ""
            lines[index] = (
                f"{match.group('indent')}version: {match.group('q1')}"
                f"{match.group('major')}.{int(match.group('minor')) + 1}"
                f"{patch}{match.group('q2')}\n"
            )
            return "".join(lines), True

    return text, False


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bump_version",
        description="Bump the package version in manifest.json and promote "
                    "the Unreleased changelog section to a dated release.",
    )
    parser.add_argument("version", nargs="?", default=None,
                        help="explicit new version, e.g. 2.1")
    parser.add_argument("--part", choices=("major", "minor"), default=None,
                        help="derive the new version from the current one")
    parser.add_argument("--bump-skills", action="store_true",
                        help="also increment the minor of every bundled "
                             "skill's SKILL.md version frontmatter")
    parser.add_argument("--repo-root", type=Path, default=PACKAGE_ROOT,
                        help="package source root (default: this script's repository)")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().absolute().resolve()

    manifest_path = repo_root / MANIFEST_NAME
    changelog_path = repo_root / CHANGELOG_NAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        current = str(manifest.get("version", ""))
        new_version = derive_version(current, args.version, args.part)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"cannot determine new version: {exc}", file=sys.stderr)
        return 2

    changelog = changelog_path.read_text(encoding="utf-8")
    try:
        new_changelog = rewrite_changelog(changelog, new_version,
                                          date.today().isoformat())
    except ValueError as exc:
        print(f"cannot update changelog: {exc}", file=sys.stderr)
        return 2

    skill_changes: list[str] = []
    if args.bump_skills:
        for skill_id in manifest.get("skills", []):
            skill_path = repo_root / str(skill_id) / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            updated, changed = bump_skill_version(text)
            if changed:
                skill_path.write_text(updated, encoding="utf-8")
                skill_changes.append(str(skill_id))
            else:
                print(f"warning: no version field in {skill_path}", file=sys.stderr)

    manifest["version"] = new_version
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    changelog_path.write_text(new_changelog, encoding="utf-8")

    print(f"version: {current} -> {new_version}")
    print(f"changelog: promoted Unreleased under '## {new_version} "
          f"{date.today().isoformat()}'")
    if args.bump_skills:
        print(f"skill frontmatter bumped: {len(skill_changes)} "
              f"({', '.join(skill_changes) if skill_changes else 'none'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
