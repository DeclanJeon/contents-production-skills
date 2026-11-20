"""Checks for creative-production/references/craft-bridge.csv and its Step 4 link."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "creative-production" / "references" / "craft-bridge.csv"
SKILL = ROOT / "creative-production" / "SKILL.md"
ROW_CAP = 40
STAGE_TOKEN = re.compile(r"S(0\d|1[0-2])")
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
        elif anchor and "{#" + anchor + "}" not in target.read_text(encoding="utf-8"):
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


def test_bridge_covers_absorbed_refs() -> None:
    refs = [row["craft_ref"] for row in read_rows()]
    missing = [needle for needle in REQUIRED_REFS if not any(needle in ref for ref in refs)]
    assert not missing, missing


def test_bridge_stills_route_reaches_still_refs() -> None:
    rows = read_rows()
    for needle in ("19a-product-promo-formulas", "23a-captions-layout", "still-motion-recipes"):
        assert any(needle in row["craft_ref"] and "스틸" in row["when"] for row in rows), needle


def test_bridge_row_cap() -> None:
    assert len(read_rows()) <= ROW_CAP


def test_step4_links_bridge() -> None:
    text = SKILL.read_text(encoding="utf-8")
    step4 = text.split("## Step 4", 1)[1].split("\n## ", 1)[0]
    assert "references/craft-bridge.csv" in step4
    assert "craft_refs" in step4


def test_skill_map_links_bridge() -> None:
    text = (ROOT / "creative-production" / "references" / "skill-map.md").read_text(encoding="utf-8")
    assert "craft-bridge.csv" in text


def test_contract_core_names_craft_refs() -> None:
    text = (ROOT / "video-production-assets" / "references" / "contract-core.md").read_text(encoding="utf-8")
    assert "craft_refs" in text
