"""Reachability contract for craft-selection documents.

A craft table that sits behind another conditional pointer is never read: this
package already measured that failure mode for conditional reading rules. These
tests keep every craft selector at the owner's own skill/table level and keep the
vocabulary crosswalk reachable from the coordinator.

Each check runs on a corrupted copy too, so a checker that can only pass is
treated as a defect.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
CROSSWALK: Final = "video-production-assets/references/directing-vocabulary-crosswalk.md"

# (owner file, target as written in that file, phrase the trigger block must name)
CRAFT_SELECTORS: Final[tuple[tuple[str, str, str], ...]] = (
    ("creative-production/SKILL.md",
     "../" + CROSSWALK,
     "names a technique"),
    ("creative-production/SKILL.md",
     "../" + CROSSWALK,
     "crosswalk"),
    ("video-production-assets/SKILL.md",
     "references/edit-sound-language-catalog.md",
     "속도·타격"),
    ("video-production-assets/SKILL.md",
     "references/08-animation.md",
     "타격·모션 속도"),
    ("video-production-assets/references/production-reference-index.md",
     "directing-vocabulary-crosswalk.md",
     "연출 용어 크로스워크"),
)

HEADING_RE: Final = re.compile(r"^#{1,6} (.+)$", re.MULTILINE)
LINK_RE: Final = re.compile(r"\]\(([^)\s]+)\)")


def slug(heading: str) -> str:
    lowered = heading.strip().lower()
    stripped = re.sub(r"[^\w\s-]", "", lowered, flags=re.UNICODE)
    return re.sub(r"\s+", "-", stripped)


def paragraphs(text: str) -> list[str]:
    """Blank-line separated blocks; a markdown table row is its own block."""
    return [block for block in re.split(r"\n\s*\n", text) if block.strip()]


def blocks_linking(text: str, target: str) -> list[str]:
    return [block for block in paragraphs(text)
            if any(link.partition("#")[0] == target for link in LINK_RE.findall(block))]


def reachability_problems(root: Path) -> list[str]:
    problems: list[str] = []
    for owner, target, phrase in CRAFT_SELECTORS:
        owner_path = root / owner
        if not owner_path.is_file():
            problems.append(f"missing owner: {owner}")
            continue
        blocks = blocks_linking(owner_path.read_text(encoding="utf-8"), target)
        if not blocks:
            problems.append(f"{owner}: no link to {target}")
            continue
        if not any(phrase in block for block in blocks):
            problems.append(f"{owner}: link to {target} lacks trigger phrase {phrase!r}")
        destination = (owner_path.parent / target).resolve()
        if not destination.is_file():
            problems.append(f"{owner}: link target missing on disk: {target}")
    return problems


def test_every_craft_selector_is_reachable_from_its_owner() -> None:
    assert reachability_problems(ROOT) == []


def test_crosswalk_fragments_resolve() -> None:
    problems: list[str] = []
    for owner, target, _phrase in CRAFT_SELECTORS:
        owner_path = ROOT / owner
        for block in blocks_linking(owner_path.read_text(encoding="utf-8"), target):
            for link in LINK_RE.findall(block):
                raw_target, _, fragment = link.partition("#")
                if raw_target != target or not fragment:
                    continue
                path = (owner_path.parent / raw_target).resolve()
                heads = {slug(h) for h in HEADING_RE.findall(path.read_text(encoding="utf-8"))}
                if slug(fragment) not in heads:
                    problems.append(f"{owner}: dead fragment #{fragment}")
    assert problems == []


@pytest.mark.parametrize("phrase", ["속도·타격", "타격·모션 속도"])
def test_checker_detects_a_dropped_trigger_phrase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, phrase: str,
) -> None:
    owner = ROOT / "video-production-assets/SKILL.md"
    text = owner.read_text(encoding="utf-8")
    assert phrase in text
    copy_root = tmp_path / "repo"
    (copy_root / "video-production-assets").mkdir(parents=True)
    (copy_root / "creative-production").mkdir(parents=True)
    (copy_root / "video-production-assets/SKILL.md").write_text(
        text.replace(phrase, "무관한 문구"), encoding="utf-8")
    (copy_root / "video-production-assets/references").mkdir()
    (copy_root / "video-production-assets/references/production-reference-index.md").write_text(
        (ROOT / "video-production-assets/references/production-reference-index.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    (copy_root / "video-production-assets/references/directing-vocabulary-crosswalk.md").write_text(
        (ROOT / CROSSWALK).read_text(encoding="utf-8"), encoding="utf-8")
    for name in ("edit-sound-language-catalog.md", "08-animation.md"):
        (copy_root / "video-production-assets/references" / name).write_text("x", encoding="utf-8")
    (copy_root / "creative-production/SKILL.md").write_text(
        (ROOT / "creative-production/SKILL.md").read_text(encoding="utf-8"), encoding="utf-8")

    problems = reachability_problems(copy_root)

    assert any("lacks trigger phrase" in problem and phrase in problem for problem in problems)


def test_checker_detects_a_dropped_link(tmp_path: Path) -> None:
    copy_root = tmp_path / "repo"
    for relative in ("creative-production", "video-production-assets/references"):
        (copy_root / relative).mkdir(parents=True)
    (copy_root / "creative-production/SKILL.md").write_text("no links here", encoding="utf-8")
    (copy_root / "video-production-assets/SKILL.md").write_text(
        (ROOT / "video-production-assets/SKILL.md").read_text(encoding="utf-8")
        .replace("references/edit-sound-language-catalog.md", "references/없는파일.md"),
        encoding="utf-8")
    (copy_root / "video-production-assets/references/production-reference-index.md").write_text(
        (ROOT / "video-production-assets/references/production-reference-index.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    (copy_root / "video-production-assets/references/directing-vocabulary-crosswalk.md").write_text(
        (ROOT / CROSSWALK).read_text(encoding="utf-8"), encoding="utf-8")

    problems = reachability_problems(copy_root)

    assert any("edit-sound-language-catalog.md" in problem for problem in problems)
