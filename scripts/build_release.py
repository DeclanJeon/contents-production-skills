#!/usr/bin/env python3
"""Build the published release archive of the skill pack.

The archive is exactly what ``install_package.py`` writes to an empty skill
root, wrapped in ``contents-production-skills-<version>/``. Members are sorted
and timestamps zeroed so the same commit always yields the same bytes.

Exit codes: 0 ok, 2 tag does not match manifest version, 3 release notes missing.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import sys
import tarfile
import tempfile
from pathlib import Path

NAME = "contents-production-skills"
REQUIRED_HEADINGS = ("## 요약", "## Summary")


def manifest_version(repo_root: Path) -> str:
    return json.loads((repo_root / "manifest.json").read_text(encoding="utf-8"))["version"]


def notes_problem(repo_root: Path, version: str) -> str | None:
    path = repo_root / "docs" / "release-notes" / f"{version}.md"
    if not path.is_file():
        return f"missing release notes: {path}"
    text = path.read_text(encoding="utf-8")
    if not any(line.strip() in REQUIRED_HEADINGS for line in text.splitlines()):
        return f"{path} has no '## 요약' or '## Summary' section"
    return None


def _install_to(repo_root: Path, target: Path) -> None:
    sys.path.insert(0, str(repo_root / "scripts"))
    try:
        from install_package import install
    finally:
        sys.path.pop(0)
    install(target, repo_root=repo_root)


def _reset(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mode = 0o755 if info.isdir() or info.mode & 0o111 else 0o644
    return info


def build_release(repo_root: Path, out_dir: Path) -> tuple[Path, Path]:
    version = manifest_version(repo_root)
    prefix = f"{NAME}-{version}"
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_path = out_dir / f"{prefix}.tar.gz"
    sha_path = out_dir / f"{prefix}.sha256"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / prefix
        _install_to(repo_root, root)
        paths = sorted([root, *root.rglob("*")], key=lambda p: p.relative_to(root).as_posix())
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for path in paths:
                if path.is_symlink():
                    raise RuntimeError(f"symlink in installed pack: {path}")
                arcname = prefix if path == root else f"{prefix}/{path.relative_to(root).as_posix()}"
                info = _reset(tar.gettarinfo(str(path), arcname))
                if info.isfile():
                    with path.open("rb") as handle:
                        tar.addfile(info, handle)
                else:
                    tar.addfile(info)
    with tar_path.open("wb") as handle, gzip.GzipFile(fileobj=handle, mode="wb", mtime=0, filename="") as gz:
        gz.write(raw.getvalue())
    digest = hashlib.sha256(tar_path.read_bytes()).hexdigest()
    sha_path.write_text(f"{digest}  {tar_path.name}\n", encoding="utf-8")
    return tar_path, sha_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--tag", help="release tag (vX.Y); must match manifest version")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    version = manifest_version(args.repo_root)
    if args.tag is not None and args.tag.removeprefix("v") != version:
        print(f"tag {args.tag} does not match manifest version {version}", file=sys.stderr)
        return 2
    if args.tag is not None:
        problem = notes_problem(args.repo_root, version)
        if problem:
            print(problem, file=sys.stderr)
            return 3
    tar_path, sha_path = build_release(args.repo_root, args.out)
    print(tar_path)
    print(sha_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
