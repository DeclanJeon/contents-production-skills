"""Crosswalk navigation contract for the directing-vocabulary index.

The crosswalk says where an external document's term is owned; if a target file
or heading disappears, the pointer silently sends an agent to a dead owner. These
tests resolve every relative link + anchor against the real tree, and prove the
checker can fail by running it on corrupted copies.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
CROSSWALK: Final = ROOT / "video-production-assets/references/directing-vocabulary-crosswalk.md"
LINK_RE: Final = re.compile(r"\]\(([^)\s]+)\)")
HEADING_RE: Final = re.compile(r"^#{1,6} (.+)$", re.MULTILINE)
CATEGORY_ROW_RE: Final = re.compile(r"^\| \d{2} ", re.MULTILINE)


def slug(heading: str) -> str:
    """Return the GitHub-style fragment for a heading (Korean preserved)."""
    lowered = heading.strip().lower()
    stripped = re.sub(r"[^\w\s-]", "", lowered, flags=re.UNICODE)
    return re.sub(r"\s+", "-", stripped)


def headings(path: Path) -> set[str]:
    return {slug(match) for match in HEADING_RE.findall(path.read_text(encoding="utf-8"))}


def link_problems(text: str, base: Path) -> list[str]:
    """Return every relative link whose file or fragment does not resolve."""
    problems: list[str] = []
    for raw in LINK_RE.findall(text):
        if raw.startswith(("http://", "https://", "mailto:")):
            continue
        target, _, fragment = raw.partition("#")
        path = (base / target).resolve() if target else base
        if not path.is_file():
            problems.append(f"missing target: {raw}")
            continue
        if fragment and slug(fragment) not in headings(path):
            problems.append(f"missing fragment: {raw}")
    return problems


def test_crosswalk_links_resolve() -> None:
    problems = link_problems(CROSSWALK.read_text(encoding="utf-8"), CROSSWALK.parent)
    assert problems == [], problems


def test_crosswalk_covers_every_document_category() -> None:
    text = CROSSWALK.read_text(encoding="utf-8")
    assert len(CATEGORY_ROW_RE.findall(text)) == 30


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ("](08-animation.md#실행-절차)", "](08-animation.md#없는-조항)"),
        ("](08-animation.md#실행-절차)", "](missing-owner.md#실행-절차)"),
    ],
)
def test_checker_detects_corruption(tmp_path: Path, mutation: str, expected: str) -> None:
    text = CROSSWALK.read_text(encoding="utf-8")
    assert mutation in text
    corrupted = tmp_path / CROSSWALK.name
    corrupted.write_text(text.replace(mutation, expected), encoding="utf-8")

    problems = link_problems(corrupted.read_text(encoding="utf-8"), CROSSWALK.parent)

    assert problems, "corrupted crosswalk should not pass"
