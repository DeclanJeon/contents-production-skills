"""Checks for creative-production/references/craft-bridge.csv and its Step 1 read and Step 4 pointer."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "creative-production" / "references" / "craft-bridge.csv"
SKILL = ROOT / "creative-production" / "SKILL.md"
ROW_CAP = 40
STAGE_TOKEN = re.compile(r"S(0\d|1[0-2])")
HEADING_ANCHOR = re.compile(r"#{1,6}\s.*\{#[^}]+\}\s*$")
STILLS_REFS = ("19a-product-promo-formulas", "still-motion-recipes")
REQUIRED_REFS = (
    "08a-motion-craft",
    "09a-short-form-edit-recipes",
    "11a-ai-video-prompting",
    "19a-product-promo-formulas",
    "23a-captions-layout",
    "29a-template-recreation",
    "33-motion-style-library",
    "still-motion-recipes",
    "30-marketing-story-craft.md#od-openmotion-ad-script",
)


def read_rows(path: Path = BRIDGE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ref(craft_ref: str) -> tuple[str, str]:
    path, _, anchor = craft_ref.partition("#")
    return path, anchor


def stages_valid(stage: str) -> bool:
    return all(STAGE_TOKEN.fullmatch(token) for token in stage.split("·"))


def unresolved_refs(rows: list[dict[str, str]]) -> list[str]:
    problems = []
    for row in rows:
        path, anchor = split_ref(row["craft_ref"])
        target = ROOT / path
        if not target.is_file():
            problems.append(f"missing file: {row['craft_ref']}")
        elif "#" in row["craft_ref"] and not anchor:
            problems.append(f"empty anchor: {row['craft_ref']}")
        elif anchor and not any(
            HEADING_ANCHOR.match(line) and line.rstrip().endswith("{#" + anchor + "}")
            for line in target.read_text(encoding="utf-8").splitlines()
        ):
            problems.append(f"missing anchor: {row['craft_ref']}")
    return problems


def test_bridge_columns() -> None:
    with BRIDGE.open(encoding="utf-8", newline="") as handle:
        assert next(csv.reader(handle)) == ["stage", "when", "craft_ref", "note"]


def test_bridge_rows_are_complete() -> None:
    rows = read_rows()
    assert rows
    for row in rows:
        assert all(row[column].strip() for column in ("stage", "when", "craft_ref")), row
        assert None not in row, row


def test_bridge_stage_vocab() -> None:
    bad = [row["stage"] for row in read_rows() if not stages_valid(row["stage"])]
    assert not bad, bad
    assert stages_valid("S04·S07")
    assert not stages_valid("S13") and not stages_valid("G1") and not stages_valid("S04,S07")


def test_bridge_refs_resolve() -> None:
    assert unresolved_refs(read_rows()) == []


def test_bridge_detects_broken_refs() -> None:
    row = {"stage": "S04", "when": "x", "craft_ref": "", "note": ""}
    assert unresolved_refs([{**row, "craft_ref": "creative-production/references/no-such-file.md"}])
    anchor_ref = "video-production-assets/references/30-marketing-story-craft.md#od-no-such-anchor"
    assert unresolved_refs([{**row, "craft_ref": anchor_ref}])
    empty_anchor = "video-production-assets/references/30-marketing-story-craft.md#"
    assert unresolved_refs([{**row, "craft_ref": empty_anchor}])


def test_bridge_covers_absorbed_refs() -> None:
    refs = [row["craft_ref"] for row in read_rows()]
    missing = [needle for needle in REQUIRED_REFS if not any(needle in ref for ref in refs)]
    assert not missing, missing


def test_bridge_stills_route_reaches_still_refs() -> None:
    rows = read_rows()
    stills_rows = [row for row in rows if row["when"].startswith("스틸")]
    for needle in STILLS_REFS:
        assert any(needle in row["craft_ref"] for row in stills_rows), needle
    allowed = STILLS_REFS + ("23a-captions-layout",)
    stray = [row["craft_ref"] for row in stills_rows if not any(n in row["craft_ref"] for n in allowed)]
    assert not stray, stray
    # Stills-only videos reach captions through the general caption row, whatever the owner.
    caption_path = "video-production-assets/references/23a-captions-layout.md"
    assert any(row["craft_ref"] == caption_path and row["stage"] == "S09" for row in rows)


def test_bridge_row_cap() -> None:
    assert len(read_rows()) <= ROW_CAP


def test_step1_reads_bridge_right_after_route_selection() -> None:
    text = SKILL.read_text(encoding="utf-8")
    step1 = text.split("## Step 1", 1)[1].split("\n## ", 1)[0]
    assert "references/craft-bridge.csv" in step1
    assert "whether you hand off or do it yourself" in step1
    assert "Owner rules and gates still win" in step1
    slots = step1.index("**authority_axis**")
    bridge = step1.index("references/craft-bridge.csv")
    assert slots < bridge < step1.index("open the selected `owner`")


def test_step4_keeps_craft_refs_pointer() -> None:
    text = SKILL.read_text(encoding="utf-8")
    step4 = text.split("## Step 4", 1)[1].split("\n## ", 1)[0]
    assert "`craft_refs`" in step4
    assert "references/craft-bridge.csv" not in step4


def test_skill_map_links_bridge() -> None:
    text = (ROOT / "creative-production" / "references" / "skill-map.md").read_text(encoding="utf-8")
    route = text.split("## 1.", 1)[1].split("\n## 2.", 1)[0]
    assert "craft-bridge.csv" in route


def test_contract_core_names_craft_refs() -> None:
    text = (ROOT / "video-production-assets" / "references" / "contract-core.md").read_text(encoding="utf-8")
    handoff = text.split("## Worker handoff and single writer", 1)[1].split("\n## ", 1)[0]
    assert "craft_refs" in handoff
    assert "참조는 권한·범위를 넓히지 않는다" in handoff
