#!/usr/bin/env python3
"""Build or check the byte inventory distributed with the CineForge adapter."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from install_package import CINEFORGE_INVENTORY, OPTIONAL_SUPPORT, REQUIRED_SUPPORT, _is_link

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"__pycache__", ".pytest_cache", ".git", ".worktrees"}


def build(root: Path) -> str:
    manifest = json.loads((root / "manifest.json").read_bytes())
    support = root / manifest["support_skill"] / "support"
    inventory: dict[str, str] = {}
    for skill in manifest["skills"]:
        skill_root = root / skill
        if not skill_root.is_dir() or _is_link(skill_root):
            raise ValueError(f"missing or linked skill: {skill}")
        for directory, folders, files in os.walk(skill_root):
            parent = Path(directory)
            folders[:] = [name for name in folders if name not in EXCLUDED
                          and not (parent == support and name in REQUIRED_SUPPORT)]
            for name in folders + files:
                path = parent / name
                if parent == support and name in REQUIRED_SUPPORT + OPTIONAL_SUPPORT:
                    continue
                if path == support / CINEFORGE_INVENTORY or path.suffix in {".pyc", ".pyo"}:
                    continue
                if _is_link(path):
                    raise ValueError(f"linked inventory path: {path}")
                if name in files:
                    if not path.is_file():
                        raise ValueError(f"non-regular inventory file: {path}")
                    inventory[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / CINEFORGE_INVENTORY
    data = build(ROOT).encode("utf-8")
    if args.check:
        if not target.is_file() or target.read_bytes() != data:
            print(f"stale inventory: {target}; run {Path(__file__).name}")
            return 1
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
