"""Reachability contract for craft-selection documents.

A craft table behind another conditional pointer is never read: this package
already measured that failure mode for conditional reading rules. These tests keep
every craft selector on its owner's dispatch surface (the owner SKILL.md or the
module index the owner moved its on-demand table into) and keep the vocabulary
crosswalk reachable from the coordinator.

Each check also runs on corrupted copies, so a checker that can only pass is
treated as a defect.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
CROSSWALK: Final = "video-production-assets/references/directing-vocabulary-crosswalk.md"
OWNER_DISPATCH: Final = (
    "video-production-assets/SKILL.md",
    "video-production-assets/references/module-index.md",
)

# (owner dispatch files — the row may live in any one of them, target document, trigger phrase)
CRAFT_SELECTORS: Final[tuple[tuple[tuple[str, ...], str, str], ...]] = (
    (("creative-production/SKILL.md",), CROSSWALK, "names a technique"),
    (OWNER_DISPATCH,
     "video-production-assets/references/edit-sound-language-catalog.md",
     "속도·타격"),
    (OWNER_DISPATCH,
     "video-production-assets/references/08-animation.md",
     "타격·모션 속도"),
    (("video-production-assets/references/production-reference-index.md",),
     CROSSWALK,
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


def links_to(block: str, base: Path, wanted: Path) -> list[str]:
    found: list[str] = []
    for raw in LINK_RE.findall(block):
        target = raw.partition("#")[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if (base / target).resolve() == wanted:
            found.append(raw)
    return found


def trigger_blocks(owner: Path, wanted: Path) -> list[str]:
    return [block for block in paragraphs(owner.read_text(encoding="utf-8"))
            if links_to(block, owner.parent, wanted)]


def reachability_problems(root: Path) -> list[str]:
    problems: list[str] = []
    for owners, target, phrase in CRAFT_SELECTORS:
        wanted = (root / target).resolve()
        linked: list[str] = []
        triggered: list[str] = []
        for owner in owners:
            owner_path = root / owner
            if not owner_path.is_file():
                continue
            blocks = trigger_blocks(owner_path, wanted)
            if not blocks:
                continue
            linked.append(owner)
            if any(phrase in block for block in blocks):
                triggered.append(owner)
        if not linked:
            problems.append(f"no owner links {target}: {', '.join(owners)}")
        elif not triggered:
            problems.append(
                f"{target}: linked from {', '.join(linked)} without trigger phrase {phrase!r}")
    return problems


def fragment_problems(root: Path) -> list[str]:
    crosswalk = (root / CROSSWALK).resolve()
    heads = {slug(h) for h in HEADING_RE.findall(crosswalk.read_text(encoding="utf-8"))}
    problems: list[str] = []
    for owners, target, _phrase in CRAFT_SELECTORS:
        wanted = (root / target).resolve()
        for owner in owners:
            owner_path = root / owner
            if not owner_path.is_file():
                continue
            for block in trigger_blocks(owner_path, wanted):
                for raw in links_to(block, owner_path.parent, wanted):
                    _, _, fragment = raw.partition("#")
                    if fragment and slug(fragment) not in heads:
                        problems.append(f"{owner}: dead fragment #{fragment}")
    return problems


def _stage_tree(root: Path, drop: tuple[str, ...] = ()) -> Path:
    """Copy the dispatch surface into a throwaway root so a copy can be corrupted."""
    for directory in ("creative-production", "video-production-assets/references"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    copies = {
        "creative-production/SKILL.md": ROOT / "creative-production/SKILL.md",
        "video-production-assets/SKILL.md": ROOT / "video-production-assets/SKILL.md",
        "video-production-assets/references/production-reference-index.md":
            ROOT / "video-production-assets/references/production-reference-index.md",
        CROSSWALK: ROOT / CROSSWALK,
    }
    for relative, source in copies.items():
        if relative in drop:
            continue
        text = source.read_text(encoding="utf-8")
        for marker in drop:
            text = text.replace(marker, "제거된-문구")
        (root / relative).write_text(text, encoding="utf-8")
    for relative in ("video-production-assets/references/edit-sound-language-catalog.md",
                     "video-production-assets/references/08-animation.md"):
        (root / relative).write_text("# stub\n", encoding="utf-8")
    return root


def test_every_craft_selector_is_reachable_from_its_owner() -> None:
    assert reachability_problems(ROOT) == []


def test_crosswalk_fragments_resolve() -> None:
    assert fragment_problems(ROOT) == []


def test_checker_detects_a_dropped_trigger_phrase(tmp_path: Path) -> None:
    root = _stage_tree(tmp_path / "repo", drop=("속도·타격",))

    problems = reachability_problems(root)

    assert any("without trigger phrase" in problem and "속도·타격" in problem
               for problem in problems), problems


def test_checker_detects_a_dropped_link(tmp_path: Path) -> None:
    root = _stage_tree(tmp_path / "repo", drop=("edit-sound-language-catalog.md",))

    problems = reachability_problems(root)

    assert any("edit-sound-language-catalog.md" in problem for problem in problems), problems


@pytest.mark.parametrize("module_index", [False, True])
def test_selector_is_reachable_from_either_dispatch_file(
    tmp_path: Path, module_index: bool,
) -> None:
    """The owner may move its on-demand table into the module index (staged loading)."""
    stage = _stage_tree(tmp_path / "repo")
    owners = ("video-production-assets/SKILL.md",
              "video-production-assets/references/module-index.md")
    row = next(line for owner in owners
               for line in (ROOT / owner).read_text(encoding="utf-8").splitlines()
               if "속도·타격" in line and "edit-sound-language-catalog.md" in line)
    for owner in owners:
        copy = stage / owner
        if copy.is_file():
            copy.write_text(copy.read_text(encoding="utf-8").replace(row + "\n", ""),
                            encoding="utf-8")
    destination = stage / ("video-production-assets/references/module-index.md"
                           if module_index else "video-production-assets/SKILL.md")
    link = "edit-sound-language-catalog.md" if module_index else "references/edit-sound-language-catalog.md"
    row_here = re.sub(r"\]\([^)]*edit-sound-language-catalog\.md\)", f"]({link})", row)
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = destination.read_text(encoding="utf-8") if destination.is_file() else ""
    destination.write_text(existing + "\n" + row_here + "\n", encoding="utf-8")

    assert reachability_problems(stage) == []
