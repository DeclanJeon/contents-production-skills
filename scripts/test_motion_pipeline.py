"""Checks for the motion pipeline (M1–M6), its matrix, brief template and pointers."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "creative-production" / "references" / "motion-pipeline.md"
SELECTION = ROOT / "creative-production" / "references" / "motion-selection.md"
SKILL = ROOT / "creative-production" / "SKILL.md"
BRIDGE = ROOT / "creative-production" / "references" / "craft-bridge.csv"
BRIEF = ROOT / "video-production-assets" / "assets" / "code-motion-brief-template.md"
CODE = ROOT / "video-production-assets" / "references" / "08b-code-motion-production.md"
VPA_SKILL = ROOT / "video-production-assets" / "SKILL.md"
MODULE_INDEX = ROOT / "video-production-assets" / "references" / "module-index.md"
ANALYSIS_FIELDS = ("audience_task", "message_units", "format_hint", "platform", "duration", "assets",
                   "data_sources", "audio", "brand", "constraints", "delivery")
CRITERIA = ("전달력", "자산 적합성", "구현 가능성", "길이 적합성")
FORMATS = ("showreel", "product_film", "explainer", "character_short", "realtime_3d", "logo_bumper", "edit_assist")
BRIEF_SLOTS = ("입력", "방향", "구조", "빌드", "주의", "시작·납품")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(body: str, anchor: str) -> str:
    start = body.index("{#" + anchor + "}")
    rest = body[start:]
    end = re.search(r"\n## ", rest[1:])
    return rest[: end.start() + 1] if end else rest


def test_pipeline_has_six_stages() -> None:
    body = text(PIPELINE)
    for anchor in ("m1-detect", "m2-analysis", "m3-direction", "m4-design", "m5-route", "m6-review"):
        assert "{#" + anchor + "}" in body, anchor


def test_analysis_table_lists_eleven_fields() -> None:
    m2 = section(text(PIPELINE), "m2-analysis")
    for field in ANALYSIS_FIELDS:
        assert f"`{field}`" in m2, field
    assert "inferred" in m2


def test_direction_compares_candidates_on_four_criteria() -> None:
    m3 = section(text(PIPELINE), "m3-direction")
    for criterion in CRITERIA:
        assert criterion in m3, criterion
    assert "2~3" in m3 and "recipe" in m3 and "reason" in m3


def test_formats_table_covers_corpus_formats() -> None:
    body = text(PIPELINE)
    for fmt in FORMATS:
        assert f"`{fmt}`" in body, fmt


def test_route_section_has_paths_and_downgrade_record() -> None:
    m5 = section(text(PIPELINE), "m5-route")
    for route in ("`local`", "`code`", "`realtime_3d`", "`downgrade`"):
        assert route in m5, route
    assert "downgrade:" in m5
    assert "render_html_motion.mjs" in m5


def test_review_keeps_two_round_limit_and_hash_delivery() -> None:
    m6 = section(text(PIPELINE), "m6-review")
    assert "2회" in m6 and "해시" in m6 and "실제 재생" in m6


def test_brief_template_has_six_required_slots() -> None:
    body = text(BRIEF)
    for slot in BRIEF_SLOTS:
        assert re.search(rf"^## \d\. {re.escape(slot)}", body, re.MULTILINE), slot
    assert "N/A — " in body


def test_selection_redirects_to_pipeline() -> None:
    body = text(SELECTION)
    assert "motion-pipeline.md" in body
    assert len(body.splitlines()) <= 5


def test_entry_skill_points_to_pipeline() -> None:
    body = text(SKILL)
    assert "(references/motion-pipeline.md)" in body
    assert "motion-selection.md" not in body


def test_bridge_and_owner_pointers() -> None:
    with BRIDGE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert any(row["craft_ref"] == "creative-production/references/motion-pipeline.md" for row in rows)
    code_row = next(row for row in rows if row["craft_ref"].endswith("08b-code-motion-production.md"))
    assert "code-motion-brief-template" in code_row["note"]
    for path in (VPA_SKILL, MODULE_INDEX):
        body = text(path)
        assert "code-motion-brief-template.md" in body and "render_html_motion.mjs" in body, path


def test_code_motion_reference_documents_render_path() -> None:
    body = text(CODE)
    assert "{#code-render-path}" in body
    for needle in ("window.__motion", "seek(t)", "render_html_motion.mjs", "--verify-frames", "--contact-sheet"):
        assert needle in body, needle
