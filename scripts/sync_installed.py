#!/usr/bin/env python3
"""Junction/symlink synchronizer for manifest-listed skills.

Links every skill listed in the package ``manifest.json`` from this
repository (the single source of truth) into one or more agent skill
roots, so Codex, Claude Code and OpenCode all read the same files and a
single repository change reaches every installed harness.

Contract:

* A full preflight runs before any destination mutation. Every problem
  is reported at once and the run aborts with exit 2 and zero writes.
* Existing links are verified: correct links are skipped (idempotent),
  stale links are repointed, real directories are displaced.
* A real directory found at a destination is moved whole into the
  backup root before its link is created; it is never merged or
  deleted in place.
* Links are removed only through ``_remove_link``, which refuses any
  path that is not actually a link; on Windows a junction is removed
  with ``os.rmdir`` so the target's contents can never be deleted.
* The derived ``<support_skill>/support/`` payload inside the
  repository is regenerated on every non-dry run; it is a build
  artifact and stays gitignored.
* ``--dry-run`` mutates nothing.

Usage::

    python scripts/sync_installed.py [--repo-root PATH] [--root PATH ...]
                                     [--dry-run] [--quiet]
                                     [--backup-root PATH]

Exit codes: 0 synced (or clean dry run), 2 preflight failure, 1 I/O
failure after mutations began (applied actions are reported honestly).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "manifest.json"
SKILL_FILE_NAME = "SKILL.md"
SUPPORT_DIR_NAME = "support"
DEFAULT_SUPPORT_SKILL = "video-production-assets"

# Support payloads copied under <repo>/<support_skill>/support/. Required
# entries must exist with the right type; optional ones are included when
# present but are never required at baseline.
REQUIRED_SUPPORT = (MANIFEST_NAME, "examples", "qa")
OPTIONAL_SUPPORT = ("CHANGELOG.md",)

COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
FILE_ATTRIBUTE_REPARSE_POINT = 0x400

# Agent skill roots fed by this repository, relative to the user home.
DEFAULT_ROOT_RELS = (os.path.join(".codex", "skills"),
                     os.path.join(".claude", "skills"),
                     os.path.join(".agents", "skills"))


class PreflightError(Exception):
    """Every problem discovered before any destination write."""

    def __init__(self, problems):
        self.problems = [str(p) for p in problems]
        super().__init__("; ".join(self.problems))


class SyncError(Exception):
    """An I/O failure after mutations began. Carries honest partial state."""

    def __init__(self, message, applied=None):
        self.applied = list(applied or [])
        super().__init__(message)


@dataclass(frozen=True)
class Action:
    kind: str  # create | repoint | displace | skip
    skill: str
    root: Path
    target: Path
    source: Path
    backup: Path | None = None


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


def _tree_link(root: Path) -> Path | None:
    """Return the first symlink/junction inside ``root``, or None."""
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            candidate = Path(dirpath) / name
            if _is_link(candidate):
                return candidate
    return None


def _paths_overlap(a: Path, b: Path) -> bool:
    return a == b or a in b.parents or b in a.parents


def _link_points_to(link: Path, source: Path) -> bool:
    try:
        return link.resolve() == source.resolve()
    except OSError:
        return False


def _remove_link(path: Path) -> None:
    """Remove a symlink/junction only. Never touches a real directory.

    On Windows a directory junction is removed with ``os.rmdir`` (which
    deletes just the reparse point). ``shutil.rmtree`` must never be
    used here: on a junction it would descend into and delete the
    target's contents.
    """
    if not _is_link(path):
        raise SyncError(f"refusing to remove a path that is not a link: {path}")
    if os.name == "nt":
        os.rmdir(os.fspath(path))
    else:
        os.unlink(os.fspath(path))


def _create_link(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        # Directory junctions need no admin rights and are local-volume
        # only; both properties hold for skill roots next to the repo.
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", os.fspath(link), os.fspath(target)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise SyncError(f"mklink failed for {link}: {detail}")
    else:
        os.symlink(os.fspath(target), os.fspath(link), target_is_directory=True)


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


def default_roots() -> list[Path]:
    home = Path.home()
    return [home / rel for rel in DEFAULT_ROOT_RELS]


def default_backup_root() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return Path.home() / ".skills-sync-backup" / stamp


def _resolve(path: Path) -> Path:
    return Path(path).expanduser().absolute().resolve()


def build_plan(repo_root: Path, roots: list[Path], backup_root: Path) -> list[Action]:
    """Run the complete preflight and return the planned actions.

    Raises PreflightError listing every problem found; nothing on disk
    is created or modified by this function.
    """
    problems: list[str] = []

    manifest = load_manifest(repo_root)
    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        raise PreflightError(["manifest 'skills' must be a non-empty list"])
    seen: set[str] = set()
    valid_skills: list[str] = []
    for skill_id in skills:
        if not isinstance(skill_id, str) or not skill_id:
            problems.append(f"unsafe skill id rejected: {skill_id!r}")
            continue
        if skill_id in seen:
            problems.append(f"duplicate skill id in manifest: {skill_id}")
            continue
        seen.add(skill_id)
        valid_skills.append(skill_id)

    support_skill = manifest.get("support_skill", DEFAULT_SUPPORT_SKILL)
    if not isinstance(support_skill, str) or support_skill not in seen:
        problems.append("manifest 'support_skill' must name a bundled skill")

    # Root sanity: deduplicate, reject overlap with the repository.
    unique_roots: list[Path] = []
    for root in roots:
        resolved = _resolve(root)
        if resolved not in unique_roots:
            unique_roots.append(resolved)
    for root in unique_roots:
        if _paths_overlap(repo_root, root):
            problems.append(f"skill root overlaps the repository: {root}")

    # Source checks.
    for skill_id in valid_skills:
        source = repo_root / skill_id
        if not source.is_dir():
            problems.append(f"missing skill source directory: {source}")
            continue
        if _is_link(source):
            problems.append(f"skill source is a symlink/junction: {source}")
            continue
        if not (source / SKILL_FILE_NAME).is_file():
            problems.append(f"missing {SKILL_FILE_NAME} in skill source: {source}")
            continue
        link = _tree_link(source)
        if link is not None:
            problems.append(f"skill source contains a symlink/junction: {link}")

    # Support payload sources.
    for rel in REQUIRED_SUPPORT:
        source = repo_root / rel
        if not _lexists(source):
            problems.append(f"missing required support source: {source}")
            continue
        if (rel == MANIFEST_NAME and not source.is_file()) or (
            rel != MANIFEST_NAME and not source.is_dir()
        ):
            problems.append(f"wrong type for required support source: {source}")

    # Backup destinations must be free and unique before anything moves.
    planned_backups: set[Path] = set()
    for root in unique_roots:
        for skill_id in valid_skills:
            target = root / skill_id
            if _lexists(target) and not _is_link(target):
                backup = backup_root / root.name / skill_id
                if backup in planned_backups:
                    problems.append(
                        f"two skill roots would back up {skill_id} to the same "
                        f"path: {backup}"
                    )
                planned_backups.add(backup)
    if planned_backups and _lexists(backup_root):
        problems.append(f"backup root already exists: {backup_root}")

    if problems:
        raise PreflightError(problems)

    actions: list[Action] = []
    for root in unique_roots:
        for skill_id in valid_skills:
            source = repo_root / skill_id
            target = root / skill_id
            if not _lexists(target):
                actions.append(Action("create", skill_id, root, target, source))
            elif _is_link(target):
                if _link_points_to(target, source):
                    actions.append(Action("skip", skill_id, root, target, source))
                else:
                    actions.append(Action("repoint", skill_id, root, target, source))
            else:
                backup = backup_root / root.name / skill_id
                actions.append(
                    Action("displace", skill_id, root, target, source, backup)
                )
    return actions


def regenerate_support(repo_root: Path, support_skill: str) -> Path:
    """Rebuild the derived support payload inside the repository."""
    support_dir = repo_root / support_skill / SUPPORT_DIR_NAME
    if _lexists(support_dir):
        if _is_link(support_dir):
            raise SyncError(f"support directory is a link, refusing to touch: {support_dir}")
        if not support_dir.is_dir():
            raise SyncError(f"support path is not a directory: {support_dir}")
        shutil.rmtree(os.fspath(support_dir))
    support_dir.mkdir(parents=True, exist_ok=True)
    for rel in REQUIRED_SUPPORT + tuple(
        rel for rel in OPTIONAL_SUPPORT if _lexists(repo_root / rel)
    ):
        source = repo_root / rel
        destination = support_dir / rel
        if source.is_dir():
            shutil.copytree(os.fspath(source), os.fspath(destination),
                            ignore=COPY_IGNORE)
        else:
            shutil.copy2(os.fspath(source), os.fspath(destination))
    return support_dir


def execute_plan(actions: list[Action], repo_root: Path, support_skill: str,
                 dry_run: bool) -> dict:
    """Apply the planned actions. Returns per-kind counts."""
    counts = {"created": 0, "repointed": 0, "skipped": 0, "backed_up": 0}
    applied: list[str] = []

    if dry_run:
        for action in actions:
            if action.kind == "create":
                counts["created"] += 1
            elif action.kind == "repoint":
                counts["repointed"] += 1
            elif action.kind == "displace":
                counts["backed_up"] += 1
            else:
                counts["skipped"] += 1
        print(f"dry run: created={counts['created']} "
              f"repointed={counts['repointed']} skipped={counts['skipped']} "
              f"backed_up={counts['backed_up']} (nothing written)")
        return counts

    try:
        regenerate_support(repo_root, support_skill)
        for action in actions:
            action.root.mkdir(parents=True, exist_ok=True)
            if action.kind == "skip":
                counts["skipped"] += 1
                continue
            if action.kind == "repoint":
                _remove_link(action.target)
                applied.append(f"repointed {action.target}")
            elif action.kind == "displace":
                action.backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(os.fspath(action.target), os.fspath(action.backup))
                applied.append(f"backed up {action.target} -> {action.backup}")
                counts["backed_up"] += 1
            _create_link(action.target, action.source)
            applied.append(f"created {action.target}")
            if action.kind == "create":
                counts["created"] += 1
            else:
                counts["repointed"] += 1
    except OSError as exc:
        raise SyncError(
            f"sync failed; destinations may be partially updated: {exc}",
            applied=applied,
        )
    return counts


def _print_actions(actions: list[Action], quiet: bool) -> None:
    if quiet:
        return
    for action in actions:
        verb = {"create": "create", "repoint": "repoint",
                "displace": "displace", "skip": "skip"}[action.kind]
        line = f"{verb:<9} {action.target} -> {action.source}"
        if action.backup is not None:
            line += f" (backup: {action.backup})"
        print(line)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sync_installed",
        description="Link every manifest-listed skill from this repository "
                    "into the installed agent skill roots. Preflight runs "
                    "first; real directories are backed up before being "
                    "replaced by links.",
    )
    parser.add_argument("--repo-root", type=Path, default=PACKAGE_ROOT,
                        help="package source root (default: this script's repository)")
    parser.add_argument("--root", type=Path, action="append", default=None,
                        help="destination skill root; repeatable; replaces the "
                             "default set of ~/.codex/skills, ~/.claude/skills "
                             "and ~/.agents/skills")
    parser.add_argument("--backup-root", type=Path, default=None,
                        help="where displaced real directories are moved "
                             "(default: ~/.skills-sync-backup/<timestamp>)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan without writing anything")
    parser.add_argument("--quiet", action="store_true",
                        help="print only the summary line")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)

    repo_root = _resolve(args.repo_root)
    if not repo_root.is_dir():
        print(f"repository source root is not a directory: {repo_root}",
              file=sys.stderr)
        return 2

    roots = [_resolve(p) for p in args.root] if args.root else default_roots()
    backup_root = (_resolve(args.backup_root) if args.backup_root
                   else default_backup_root())

    try:
        actions = build_plan(repo_root, roots, backup_root)
    except PreflightError as exc:
        print("sync preflight failed; nothing was written:", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return 2

    _print_actions(actions, args.quiet)

    try:
        counts = execute_plan(
            actions, repo_root,
            str(load_manifest(repo_root).get("support_skill",
                                             DEFAULT_SUPPORT_SKILL)),
            dry_run=args.dry_run,
        )
    except SyncError as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        for item in exc.applied:
            print(f"  applied: {item}", file=sys.stderr)
        return 1

    if not args.dry_run and not args.quiet:
        print(f"regenerated support payload: "
              f"{repo_root / load_manifest(repo_root).get('support_skill', DEFAULT_SUPPORT_SKILL) / SUPPORT_DIR_NAME}")
    print(f"summary: created={counts['created']} repointed={counts['repointed']} "
          f"skipped={counts['skipped']} backed_up={counts['backed_up']}")
    if not args.dry_run:
        print("Restart or refresh each agent so it rescans the skill roots.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
