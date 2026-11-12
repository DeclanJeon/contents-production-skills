# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_evaluation.py
"""Pinned runtime-only snapshots; never copy repository QA into model context."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import ClassVar, Final

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EvaluationContractError(RuntimeError):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class FilePin(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class Snapshot(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    root: Path
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    files: tuple[FilePin, ...] = Field(min_length=1)


class PackageManifest(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="ignore")
    skills: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def safe_skill_names(self) -> PackageManifest:
        if len(set(self.skills)) != len(self.skills) or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s) for s in self.skills):
            raise EvaluationContractError("Unsafe/duplicate snapshot skill name")
        return self


EXCLUDED: Final = frozenset({"support", "qa", "tests", "__pycache__", "node_modules"})


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def files_digest(files: tuple[FilePin, ...]) -> str:
    return digest(json.dumps([f.model_dump() for f in files], sort_keys=True, separators=(",", ":")).encode())


def payload_files(root: Path) -> tuple[Path, ...]:
    if (root / "manifest.json").is_symlink():
        raise EvaluationContractError("Snapshot manifest symlink refused")
    manifest = PackageManifest.model_validate_json((root / "manifest.json").read_bytes())
    paths = [root / "manifest.json"]
    for skill in manifest.skills:
        folder = root / skill
        if not folder.is_dir() or folder.is_symlink():
            raise EvaluationContractError(f"Missing/linked snapshot skill: {skill}")
        for p in sorted(folder.rglob("*")):
            parts = p.relative_to(folder).parts
            if any(part.startswith(".") or part in EXCLUDED for part in parts) or p.name.startswith("test_"):
                continue
            if p.is_symlink():
                raise EvaluationContractError(f"Snapshot symlink refused: {p}")
            if p.is_file():
                paths.append(p)
    return tuple(sorted(paths))


def create_snapshot(source: Path, destination: Path) -> Snapshot:
    """Copy current bytes, not HEAD; preserve incomplete destinations on failure."""
    root = source.resolve()
    target = destination.resolve()
    if target.exists():
        raise FileExistsError(target)
    files = payload_files(root)
    for source_file in files:
        if source_file.is_symlink():
            raise EvaluationContractError(f"Snapshot symlink refused: {source_file}")
        skill_root = root / source_file.relative_to(root).parts[0]
        if target.is_relative_to(skill_root) or root.is_relative_to(target):
            raise EvaluationContractError("Snapshot destination overlaps source payload")
    pins = tuple(FilePin(path=p.relative_to(root).as_posix(), sha256=digest(p.read_bytes())) for p in files)
    target.mkdir(parents=True, exist_ok=False)
    for pin in pins:
        data = (root / pin.path).read_bytes()
        if digest(data) != pin.sha256:
            raise EvaluationContractError("Source changed while copying snapshot")
        p = target / pin.path
        p.parent.mkdir(parents=True, exist_ok=True)
        _ = p.write_bytes(data)
        p.chmod(0o444)
    after = tuple(FilePin(path=p.relative_to(root).as_posix(), sha256=digest(p.read_bytes())) for p in payload_files(root))
    if pins != after:
        raise EvaluationContractError("Source changed while copying snapshot")
    return Snapshot(root=target, sha256=files_digest(pins), files=pins)


def safe_evidence_path(root: Path, relative: str) -> Path:
    """Require a real contained receipt file without any symlink component."""
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise EvaluationContractError("Evidence path must be contained and relative")
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise EvaluationContractError("Missing/escaping evidence file")
    if any((root / Path(*candidate.parts[:n])).is_symlink() for n in range(1, len(candidate.parts) + 1)):
        raise EvaluationContractError("Evidence symlink refused")
    return resolved


def verify_snapshot(snapshot: Snapshot) -> bool:
    paths = sorted(snapshot.root.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise EvaluationContractError("snapshot contains a symlink")
    actual = tuple(FilePin(path=p.relative_to(snapshot.root).as_posix(), sha256=digest(p.read_bytes())) for p in paths if p.is_file())
    if actual != snapshot.files or files_digest(actual) != snapshot.sha256:
        raise EvaluationContractError("snapshot payload mutated")
    return True
