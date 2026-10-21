"""Typed failures shared by page-spec, rendering, and output boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PageSpecError(Exception):
    path: Path
    detail: str

    def __str__(self) -> str:
        return f"{self.path}: {self.detail}"


@dataclass(frozen=True, slots=True)
class RenderError(Exception):
    detail: str
    path: Path | None = None

    def __str__(self) -> str:
        return f"{self.path}: {self.detail}" if self.path is not None else self.detail
