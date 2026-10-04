#!/usr/bin/env python3
"""Install the package's git hooks into ``<repo>/.git/hooks``.

The four hook sources live in ``scripts/hooks/`` and are copied (not
symlinked) so git always executes a plain local file:

* ``pre-commit`` runs ``check_versions.py`` and blocks inconsistent
  commits (``git commit --no-verify`` is the documented escape).
* ``post-commit`` / ``post-merge`` / ``post-rewrite`` run
  ``sync_installed.py --quiet`` so every local change or pull refreshes
  the installed skill roots.

Contract:

* Idempotent: hooks already carrying the managed marker are refreshed;
  a missing hook is written.
* A pre-existing *foreign* hook (no marker) is never clobbered — the
  managed block is appended after it and reported.
* Every installed file ends up executable (0o755).

Usage::

    python scripts/install_hooks.py [--repo-root PATH]

Exit codes: 0 installed/updated, 2 no usable git directory.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
HOOK_SOURCE_DIR = Path(__file__).resolve().parent / "hooks"
MARKER = "contents-production-skills managed hook"
HOOK_NAMES = ("pre-commit", "post-commit", "post-merge", "post-rewrite")

# Fallback logic for appending into a foreign hook, per hook family.
APPENDED_BLOCK = {
    "pre-commit": (
        f"# {MARKER} (appended)\n"
        'if ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then\n'
        '  python "$ROOT/scripts/check_versions.py" || exit 1\n'
        "fi\n"
    ),
    "post-commit": (
        f"# {MARKER} (appended)\n"
        'if ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then\n'
        '  python "$ROOT/scripts/sync_installed.py" --quiet || '
        'echo "contents-production-skills: sync_installed failed (non-fatal)" >&2\n'
        "fi\n"
    ),
    "post-merge": (
        f"# {MARKER} (appended)\n"
        'if ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then\n'
        '  python "$ROOT/scripts/sync_installed.py" --quiet || '
        'echo "contents-production-skills: sync_installed failed (non-fatal)" >&2\n'
        "fi\n"
    ),
    "post-rewrite": (
        f"# {MARKER} (appended)\n"
        'if ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then\n'
        '  python "$ROOT/scripts/sync_installed.py" --quiet || '
        'echo "contents-production-skills: sync_installed failed (non-fatal)" >&2\n'
        "fi\n"
    ),
}


def _make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install(repo_root: Path) -> tuple[list[str], list[str]]:
    """Install/refresh hooks. Returns (installed, appended) reports."""
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        raise ValueError(f"not a git repository (missing .git): {repo_root}")
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    appended: list[str] = []
    for name in HOOK_NAMES:
        source = HOOK_SOURCE_DIR / name
        destination = hooks_dir / name
        content = source.read_text(encoding="utf-8")

        if not destination.exists():
            destination.write_text(content, encoding="utf-8")
            installed.append(name)
        elif MARKER in destination.read_text(encoding="utf-8"):
            destination.write_text(content, encoding="utf-8")
            installed.append(name)
        else:
            existing = destination.read_text(encoding="utf-8")
            block = APPENDED_BLOCK[name]
            if block not in existing:
                separator = "" if existing.endswith("\n") else "\n"
                destination.write_text(existing + separator + block,
                                       encoding="utf-8")
            appended.append(name)

        _make_executable(destination)
    return installed, appended


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="install_hooks",
        description="Install the package git hooks (version check before "
                    "commits, skill-root sync after commits/merges).",
    )
    parser.add_argument("--repo-root", type=Path, default=PACKAGE_ROOT,
                        help="package source root (default: this script's repository)")
    return parser


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().absolute().resolve()
    try:
        installed, appended = install(repo_root)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for name in installed:
        print(f"installed: {repo_root / '.git' / 'hooks' / name}")
    for name in appended:
        print(f"appended managed block to existing foreign hook: "
              f"{repo_root / '.git' / 'hooks' / name}")
    if not installed and not appended:
        print("hooks already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
