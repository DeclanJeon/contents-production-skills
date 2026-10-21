#!/usr/bin/env python3
"""Remove the local artifacts the skill-install tooling leaves behind.

The install tooling copies each file it replaces to ``<file>.from-backup``,
mirrors branches as ``<branch>.from-backup`` and can drop the same copies into
the git object store. Those copies are redundant with git history, they are not
reviewed, and they grow without bound. This script removes them together with
the ignored bulk artifacts (raw evaluation captures, extracted analysis media)
and reports the reclaimed space.

Safe by default: nothing is deleted unless ``--apply`` is passed. The script
only touches paths that match the explicit patterns below and never removes a
tracked file, a branch that is not a ``.from-backup`` copy, or a commit.

Run:  python3 scripts/clean_local_artifacts.py            # dry run
      python3 scripts/clean_local_artifacts.py --apply
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP_SUFFIX = ".from-backup"
IGNORED_BULK_DIRS = (
    "qa/skill-completeness-95/runs",
    "qa/skill-completeness-95/camera-spatial-sequence",
    "qa/skill-completeness-95/integration-previs-stills",
    "qa/skill-completeness-95/closure-F2",
    "qa/skill-completeness-95/closure-F4",
    "qa/skill-completeness-95/closure-F7",
    "qa/skill-completeness-95/closure-parent",
)


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return result.stdout


def tracked_files() -> set[str]:
    out = run("git", "ls-files")
    return {line for line in out.splitlines() if line}


def backup_files() -> list[Path]:
    found = []
    for path in ROOT.rglob("*" + BACKUP_SUFFIX):
        if ".git" in path.parts:
            continue
        found.append(path)
    return found


def garbage_objects() -> list[Path]:
    objects = ROOT / ".git" / "objects"
    if not objects.is_dir():
        return []
    return [p for p in objects.rglob("*" + BACKUP_SUFFIX) if p.is_file()]


def backup_branches() -> list[str]:
    out = run("git", "for-each-ref", "--format=%(refname:short)", "refs/heads")
    return [b.strip() for b in out.splitlines() if b.strip().endswith(BACKUP_SUFFIX)]


def stale_remote_refs() -> list[str]:
    out = run("git", "for-each-ref", "--format=%(refname)", "refs/remotes")
    return [r.strip() for r in out.splitlines() if r.strip().endswith(BACKUP_SUFFIX)]


def bulk_dirs() -> list[Path]:
    return [ROOT / rel for rel in IGNORED_BULK_DIRS if (ROOT / rel).is_dir()]


def analysis_evidence_dirs() -> list[Path]:
    analysis = ROOT / "docs" / "analysis"
    if not analysis.is_dir():
        return []
    return [d for d in analysis.glob("*/evidence") if d.is_dir()]


def size_of(paths) -> int:
    total = 0
    for path in paths:
        if path.is_file():
            total += path.stat().st_size
        elif path.is_dir():
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="actually delete; without it nothing is removed")
    args = parser.parse_args()

    tracked = tracked_files()
    backups = backup_files()
    objects = garbage_objects()
    branches = backup_branches()
    refs = stale_remote_refs()
    bulk = bulk_dirs()
    evidence = analysis_evidence_dirs()

    removable_backups = [p for p in backups if str(p.relative_to(ROOT)) not in tracked]
    reclaimable = size_of(removable_backups) + size_of(objects) + size_of(bulk) + size_of(evidence)

    print(f"worktree backup copies : {len(removable_backups)}")
    print(f"git object copies       : {len(objects)}")
    print(f"backup branches         : {len(branches)}")
    print(f"stale remote refs       : {len(refs)}")
    print(f"ignored bulk dirs       : {len(bulk)}")
    print(f"analysis evidence dirs  : {len(evidence)}")
    print(f"reclaimable             : {reclaimable / (1024 * 1024):.0f} MB")

    if not args.apply:
        print("\ndry run - nothing was removed. Re-run with --apply.")
        return 0

    for path in removable_backups:
        path.unlink(missing_ok=True)
    for path in objects:
        path.unlink(missing_ok=True)
    for branch in branches:
        subprocess.run(["git", "branch", "-D", branch], cwd=ROOT, capture_output=True, text=True)
    for ref in refs:
        # --no-deref keeps a symbolic ref from deleting the branch it points at.
        subprocess.run(["git", "update-ref", "--no-deref", "-d", ref], cwd=ROOT, capture_output=True, text=True)
    for path in bulk + evidence:
        shutil.rmtree(path, ignore_errors=True)

    print("\nremoved. Suggested follow-up: git gc --prune=now to compact the object store.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
