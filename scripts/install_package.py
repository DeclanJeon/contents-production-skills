#!/usr/bin/env python3
"""Manifest-driven installer for the contents-production-skills package.

Copies the skills listed in the repository ``manifest.json`` into a user
skill root, plus the package support files (manifest, examples, QA and
optional provenance metadata) under ``<support_skill>/support/``.

Contract:

* Every preflight check (source SKILL.md files, required support files,
  safe/unique skill IDs, root overlap, existing collisions, duplicate IDs
  in an explicitly supplied alias root) completes before the first
  destination write. Any problem aborts the run with zero writes.
* Existing destinations are never merged or silently overwritten.
  ``--replace`` requires ``--backup-dir`` and moves each conflicting
  managed folder (including managed duplicate IDs in the alias root) into
  the backup before copying. Unrelated directories are never touched.
* The alias root is only scanned when ``--alias-root`` is passed
  explicitly. Nothing infers or mutates a second root on its own.
* No dependency is ever auto-installed; ``external_dependencies`` in the
  manifest are informational records only.

Usage::

    python scripts/install_package.py [--skills-root PATH]
                                      [--replace --backup-dir PATH]
                                      [--alias-root PATH]

Default skills root: ``%CODEX_HOME%/skills`` when ``CODEX_HOME`` is set,
else ``~/.codex/skills``. Exit 0 means the installation completed;
nonzero means a preflight (2) or I/O (1) failure, with the actual applied
paths and retained backups reported honestly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "manifest.json"
SKILL_FILE_NAME = "SKILL.md"
SUPPORT_DIR_NAME = "support"
DEFAULT_SUPPORT_SKILL = "video-production-assets"

# Support payloads copied under <support_skill>/support/. Required entries
# must exist; optional provenance/metadata files are included when present
# but are never required at baseline.
REQUIRED_SUPPORT = (MANIFEST_NAME, "examples", "qa")
OPTIONAL_SUPPORT = ("CHANGELOG.md",)

SKILL_ID_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class PreflightError(Exception):
    """Every problem discovered before any destination write."""

    def __init__(self, problems):
        self.problems = [str(p) for p in problems]
        super().__init__("; ".join(self.problems))


class InstallError(Exception):
    """An I/O failure after writes began. Carries honest partial state."""

    def __init__(self, message, applied=None, backups=None):
        self.applied = list(applied or [])
        self.backups = list(backups or [])
        super().__init__(message)


@dataclass(frozen=True)
class CopyItem:
    source: Path
    target: Path
    label: str


@dataclass(frozen=True)
class BackupItem:
    existing: Path
    backup: Path
    origin: str  # "skills" or "alias"


@dataclass
class InstallPlan:
    repo_root: Path
    skills_root: Path
    support_root: Path
    package_version: str
    skills: list
    skill_copies: list = field(default_factory=list)
    support_copies: list = field(default_factory=list)
    backups: list = field(default_factory=list)
    replace: bool = False
    backup_dir: Path | None = None
    alias_root: Path | None = None


@dataclass
class InstallResult:
    installed: list
    support_root: Path
    skills_root: Path
    package_version: str
    backups: list = field(default_factory=list)
    alias_migrated: list = field(default_factory=list)


def _resolve(path) -> Path:
    raw = Path(path).expanduser().absolute()
    for candidate in (raw, *raw.parents):
        if _lexists(candidate) and _is_link(candidate):
            raise PreflightError([f"path crosses a symlink/junction: {candidate}"])
        if candidate != raw and _lexists(candidate) and not candidate.is_dir():
            raise PreflightError([f"path parent is not a directory: {candidate}"])
    return raw.resolve()


def _lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _is_link(path: Path) -> bool:
    """True for symlinks and, on Windows, junctions/other reparse points."""
    if path.is_symlink():
        return True
    if os.name == "nt":
        try:
            attrs = os.lstat(os.fspath(path)).st_file_attributes
        except (OSError, AttributeError):
            return False
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    return False


def _tree_link(root: Path):
    """Return the first symlink/junction inside ``root``, or None."""
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            candidate = Path(dirpath) / name
            if _is_link(candidate):
                return candidate
    return None


def _paths_overlap(a: Path, b: Path) -> bool:
    return a == b or a in b.parents or b in a.parents


def default_skills_root(env=None, home=None) -> Path:
    """Codex user skill root: $CODEX_HOME/skills else ~/.codex/skills."""
    env = os.environ if env is None else env
    codex_home = env.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return (Path(home) if home is not None else Path.home()) / ".codex" / "skills"


def load_manifest(repo_root: Path) -> dict:
    path = repo_root / MANIFEST_NAME
    if not path.is_file():
        raise PreflightError([f"missing package manifest: {path}"])
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreflightError([f"unreadable package manifest {path}: {exc}"])
    if not isinstance(manifest, dict):
        raise PreflightError([f"package manifest {path} is not a JSON object"])
    return manifest


def _check_skill_ids(manifest: dict, problems: list) -> list:
    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        problems.append("manifest 'skills' must be a non-empty list")
        return []
    seen = set()
    valid = []
    for skill_id in skills:
        if not isinstance(skill_id, str) or not SKILL_ID_RE.match(skill_id):
            problems.append(f"unsafe skill id rejected: {skill_id!r}")
            continue
        if skill_id in seen:
            problems.append(f"duplicate skill id in manifest: {skill_id!r}")
            continue
        seen.add(skill_id)
        valid.append(skill_id)
    entry = manifest.get("entry_skill")
    if entry is not None and (not isinstance(entry, str) or entry not in seen):
        problems.append(f"manifest 'entry_skill' is not in the skills list: {entry!r}")
    support_skill = manifest.get("support_skill", DEFAULT_SUPPORT_SKILL)
    if not isinstance(support_skill, str) or support_skill not in seen:
        problems.append(
            f"manifest 'support_skill' must name an installed skill: {support_skill!r}"
        )
    return valid


def _check_root(path: Path, name: str, problems: list, must_exist=False):
    if _is_link(path):
        problems.append(f"{name} is a symlink/junction and is refused: {path}")
    if must_exist and not path.is_dir():
        problems.append(f"{name} is not an existing directory: {path}")
    if _lexists(path) and not path.is_dir():
        problems.append(f"{name} is not a directory: {path}")


def build_plan(
    skills_root=None,
    *,
    repo_root=None,
    replace: bool = False,
    backup_dir=None,
    alias_root=None,
    env=None,
) -> InstallPlan:
    """Run the complete preflight and return an executable plan.

    Raises PreflightError listing every problem found; no destination is
    created or modified by this function.
    """
    problems: list = []
    repo_root = _resolve(repo_root) if repo_root is not None else PACKAGE_ROOT
    if not repo_root.is_dir():
        problems.append(f"repository source root is not a directory: {repo_root}")

    manifest: dict = {}
    if not problems:
        try:
            manifest = load_manifest(repo_root)
        except PreflightError as exc:
            problems.extend(exc.problems)

    skills = _check_skill_ids(manifest, problems)
    if problems:
        raise PreflightError(problems)
    support_skill = manifest.get("support_skill", DEFAULT_SUPPORT_SKILL)
    version = str(manifest.get("version", "unknown"))

    skills_root = _resolve(skills_root) if skills_root is not None else _resolve(
        default_skills_root(env=env)
    )
    alias_root = _resolve(alias_root) if alias_root is not None else None
    backup_dir = _resolve(backup_dir) if backup_dir is not None else None

    if replace and backup_dir is None:
        problems.append("--replace requires --backup-dir so replaced folders are preserved")
    if backup_dir is not None and not replace:
        problems.append("--backup-dir only makes sense together with --replace")

    # Root/link/overlap checks.
    if _lexists(skills_root):
        _check_root(skills_root, "skills root", problems)
    if backup_dir is not None and _lexists(backup_dir):
        _check_root(backup_dir, "backup directory", problems)
    if alias_root is not None:
        if _lexists(alias_root):
            _check_root(alias_root, "alias root", problems, must_exist=True)
        else:
            problems.append(f"alias root is not an existing directory: {alias_root}")

    if repo_root.is_dir() and _paths_overlap(repo_root, skills_root):
        problems.append(
            f"skills root overlaps the repository source root: {skills_root} vs {repo_root}"
        )
    if backup_dir is not None:
        if repo_root.is_dir() and _paths_overlap(backup_dir, repo_root):
            problems.append(
                f"backup directory overlaps the repository source root: {backup_dir}"
            )
        if _paths_overlap(backup_dir, skills_root):
            problems.append(f"backup directory overlaps the skills root: {backup_dir}")
    if alias_root is not None and alias_root.is_dir():
        if _paths_overlap(alias_root, skills_root):
            problems.append(f"alias root overlaps the skills root: {alias_root}")
        if repo_root.is_dir() and _paths_overlap(alias_root, repo_root):
            problems.append(
                f"alias root overlaps the repository source root: {alias_root}"
            )
        if backup_dir is not None and _paths_overlap(alias_root, backup_dir):
            problems.append(f"alias root overlaps the backup directory: {alias_root}")

    # Source checks.
    skill_copies: list = []
    for skill_id in skills:
        source = repo_root / skill_id
        if not source.is_dir() or _is_link(source):
            problems.append(f"missing skill source directory: {source}")
            continue
        if not (source / SKILL_FILE_NAME).is_file():
            problems.append(f"missing {SKILL_FILE_NAME} in skill source: {source}")
            continue
        link = _tree_link(source)
        if link is not None:
            problems.append(f"skill source contains a symlink/junction: {link}")
            continue
        skill_copies.append(CopyItem(source, skills_root / skill_id, skill_id))

    support_root = skills_root / support_skill / SUPPORT_DIR_NAME
    support_copies: list = []
    for rel in REQUIRED_SUPPORT:
        source = repo_root / rel
        if not _lexists(source) or _is_link(source):
            problems.append(f"missing required package support source: {source}")
            continue
        if (rel == MANIFEST_NAME and not source.is_file()) or (
            rel != MANIFEST_NAME and not source.is_dir()
        ):
            problems.append(f"wrong type for required package support source: {source}")
            continue
        if source.is_dir():
            link = _tree_link(source)
            if link is not None:
                problems.append(f"support source contains a symlink/junction: {link}")
                continue
        support_copies.append(CopyItem(source, support_root / rel, f"support:{rel}"))
    for rel in OPTIONAL_SUPPORT:
        source = repo_root / rel
        if _lexists(source) and not _is_link(source) and source.is_file():
            support_copies.append(CopyItem(source, support_root / rel, f"support:{rel}"))

    source_support = repo_root / support_skill / SUPPORT_DIR_NAME
    if _lexists(source_support) and not source_support.is_dir():
        problems.append(f"source support parent is not a directory: {source_support}")
    for item in support_copies:
        copied_destination = source_support / item.target.relative_to(support_root)
        if _lexists(copied_destination):
            problems.append(f"source skill would create a support collision: {copied_destination}")

    # Collision detection: managed skill targets, support targets, and
    # managed duplicate IDs under the explicitly supplied alias root.
    conflicts = [
        item for item in skill_copies + support_copies if _lexists(item.target)
    ]
    alias_duplicates: list = []
    if alias_root is not None and alias_root.is_dir():
        for skill_id in skills:
            candidate = alias_root / skill_id
            if _lexists(candidate):
                alias_duplicates.append(candidate)
    for item in conflicts:
        if _is_link(item.target):
            problems.append(f"managed destination is a symlink/junction: {item.target}")
    for candidate in alias_duplicates:
        if _is_link(candidate):
            problems.append(f"managed alias is a symlink/junction: {candidate}")

    backups: list = []
    if conflicts or alias_duplicates:
        if not replace:
            lines = [f"existing destination: {item.target}" for item in conflicts]
            lines += [f"duplicate managed id in alias root: {p}" for p in alias_duplicates]
            problems.append(
                "refusing to overwrite or merge existing destinations "
                "(rerun with --replace --backup-dir PATH to keep backups): "
                + "; ".join(lines)
            )
        elif backup_dir is not None:
            for item in conflicts:
                if item.label.startswith("support:"):
                    # Support lives inside its host skill folder, which is
                    # itself a conflicting managed folder that gets backed
                    # up wholesale; no separate support backup is needed.
                    continue
                backups.append(
                    BackupItem(item.target, backup_dir / "skills" / item.label, "skills")
                )
            for candidate in alias_duplicates:
                backups.append(
                    BackupItem(candidate, backup_dir / "alias" / candidate.name, "alias")
                )
            for item in backups:
                if _lexists(item.backup):
                    problems.append(f"backup destination already exists: {item.backup}")
                for parent in item.backup.parents:
                    if parent == backup_dir:
                        break
                    if _lexists(parent):
                        _check_root(parent, "backup parent", problems)

    if problems:
        raise PreflightError(problems)

    return InstallPlan(
        repo_root=repo_root,
        skills_root=skills_root,
        support_root=support_root,
        package_version=version,
        skills=list(skills),
        skill_copies=skill_copies,
        support_copies=support_copies,
        backups=backups,
        replace=replace,
        backup_dir=backup_dir,
        alias_root=alias_root,
    )


def execute_plan(plan: InstallPlan) -> InstallResult:
    """Apply a validated plan: backups first, then skill/support copies.

    On I/O failure, raises InstallError carrying the paths already applied
    and the backups retained so far. No atomicity is claimed.
    """
    done_backups: list = []
    attempted_targets: list = []
    attempted_backups: list = []
    try:
        plan.skills_root.mkdir(parents=True, exist_ok=True)
        for item in plan.backups:
            item.backup.parent.mkdir(parents=True, exist_ok=True)
            attempted_backups.append(item)
            shutil.move(os.fspath(item.existing), os.fspath(item.backup))
            done_backups.append(item)
        for item in plan.skill_copies:
            attempted_targets.append(item.target)
            shutil.copytree(
                os.fspath(item.source), os.fspath(item.target), ignore=COPY_IGNORE
            )
        plan.support_root.mkdir(parents=True, exist_ok=True)
        for item in plan.support_copies:
            attempted_targets.append(item.target)
            item.target.parent.mkdir(parents=True, exist_ok=True)
            if item.source.is_dir():
                shutil.copytree(
                    os.fspath(item.source), os.fspath(item.target), ignore=COPY_IGNORE
                )
            else:
                shutil.copy2(os.fspath(item.source), os.fspath(item.target))
    except OSError as exc:
        touched = [path for path in attempted_targets if _lexists(path)]
        retained = [item for item in attempted_backups if _lexists(item.backup)]
        raise InstallError(
            f"installation failed; destinations may contain partial files: {exc}",
            applied=touched, backups=retained
        )

    installed = [
        item.target for item in plan.skill_copies if (item.target / SKILL_FILE_NAME).is_file()
    ]
    return InstallResult(
        installed=installed,
        support_root=plan.support_root,
        skills_root=plan.skills_root,
        package_version=plan.package_version,
        backups=done_backups,
        alias_migrated=[b for b in done_backups if b.origin == "alias"],
    )


def install(skills_root=None, *, repo_root=None, replace=False, backup_dir=None,
            alias_root=None, env=None) -> InstallResult:
    """Preflight + execute in one call. Raises PreflightError/InstallError."""
    plan = build_plan(
        skills_root,
        repo_root=repo_root,
        replace=replace,
        backup_dir=backup_dir,
        alias_root=alias_root,
        env=env,
    )
    return execute_plan(plan)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="install_package",
        description="Install the manifest-listed skills and package support "
        "files into a user skill root. Fails before any write on missing "
        "sources, unsafe/duplicate IDs, overlapping roots, or existing "
        "collisions unless --replace --backup-dir is given.",
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=None,
        help="destination skill root (default: $CODEX_HOME/skills else ~/.codex/skills)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="move existing managed destinations to --backup-dir before copying",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=None,
        help="required with --replace; receives backed-up folders under skills/ and alias/",
    )
    parser.add_argument(
        "--alias-root",
        type=Path,
        default=None,
        help="explicit second skill root scanned for duplicate managed IDs; "
        "duplicates are backed up and removed only with --replace",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="package source root override (default: this script's repository)",
    )
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        plan = build_plan(
            args.skills_root,
            repo_root=args.repo_root,
            replace=args.replace,
            backup_dir=args.backup_dir,
            alias_root=args.alias_root,
        )
    except PreflightError as exc:
        print("installation preflight failed; nothing was written:", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return 2

    try:
        result = execute_plan(plan)
    except InstallError as exc:
        print(f"installation failed: {exc}", file=sys.stderr)
        if exc.applied:
            print("paths already applied:", file=sys.stderr)
            for path in exc.applied:
                print(f"  - {path}", file=sys.stderr)
        if exc.backups:
            print("retained backups:", file=sys.stderr)
            for item in exc.backups:
                print(f"  - {item.existing} -> {item.backup}", file=sys.stderr)
        return 1

    print(
        f"Installed {len(result.installed)} skill(s) into {result.skills_root} "
        f"(package version {result.package_version})."
    )
    for path in result.installed:
        print(f"  skill: {path}")
    print(f"  support: {result.support_root}")
    if result.backups:
        print(f"Backed up {len(result.backups)} existing folder(s) to {plan.backup_dir}:")
        for item in result.backups:
            print(f"  {item.origin}: {item.existing} -> {item.backup}")
    if result.alias_migrated:
        names = ", ".join(sorted(b.existing.name for b in result.alias_migrated))
        print(f"Removed duplicate managed id(s) from alias root {plan.alias_root}: {names}")
    print("Restart or refresh your agent so it scans the new skill directories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
