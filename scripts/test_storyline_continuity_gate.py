"""Storyline gate discoverability/structural contracts, not semantic vision QA.

These user-authorized document checks guard the coordinator's canonical route
and required evidence bindings in the existing edit cells. They do not judge
continuity, agent compliance, or playback; fresh-context review owns those.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
REFERENCE: Final = ROOT / "video-production-assets/references/26-state-causality-continuity.md"
TEMPLATE: Final = ROOT / "video-production-assets/assets/09-edit-template.md"
ANCHOR: Final = "storyline-continuity-gate"


@pytest.mark.parametrize("relative", [
    "creative-production/SKILL.md",
    "video-production-assets/SKILL.md",
    "higgsfield-generate/SKILL.md",
    "higgsfield-video-replicate/SKILL.md",
    "higgsfield-video-explainer/SKILL.md",
    "video-production-assets/assets/09-edit-template.md",
])
def test_required_storyline_route_resolves_to_canonical_gate(relative: str) -> None:
    # Given: either the coordinator or its existing edit evidence surface.
    source = ROOT / relative
    # When: the explicitly required canonical route is followed.
    paragraphs = source.read_text(encoding="utf-8").split("\n\n")
    routes = [p for p in paragraphs if f"26-state-causality-continuity.md#{ANCHOR}" in p]
    # Then: omission of the required route or its target is a structural failure.
    assert len(routes) == 1, f"{relative}: missing unique required storyline route"
    assert re.search(r"REQUIRED|필수", routes[0])
    href = re.search(r"\]\(([^)]+)\)", routes[0])
    assert href is not None
    destination, _, fragment = href[1].partition("#")
    assert (source.parent / destination).resolve() == REFERENCE.resolve()
    assert fragment == ANCHOR
    assert f'<a id="{fragment}"></a>' in REFERENCE.read_text(encoding="utf-8")


@pytest.mark.parametrize("required_slots", [
    ("scene/shot", "최초", "offscreen", "cross-cut", "flashback"),
    ("planned", "not produced", "UNVERIFIED"),
    ("accepted", "source_in_s", "source_out_s", "FPS/PTS", "raw tail"),
    ("out/in", "인접 모션", "needs_revision"),
    ("delivery_checks", "정속", "오디오", "unverified"),
])
def test_canonical_gate_exposes_order_plan_take_boundary_and_acceptance_slots(
    required_slots: tuple[str, ...],
) -> None:
    # Given: the canonical target, not a duplicate procedure in the coordinator.
    text = REFERENCE.read_text(encoding="utf-8")
    # When: the required gate section is opened.
    marker = f'<a id="{ANCHOR}"></a>'
    assert marker in text, "canonical whole-storyline procedure is not discoverable"
    section = text.split(marker, 1)[1].split("\n## ", 2)[1]
    # Then: its structural evidence roles cover each stage of the handoff.
    for slot in required_slots:
        assert slot in section, f"canonical gate lost required evidence role: {slot}"


@pytest.mark.parametrize("relative", [
    "higgsfield-generate/SKILL.md",
    "higgsfield-video-replicate/SKILL.md",
    "higgsfield-video-explainer/SKILL.md",
])
def test_standalone_execution_exposes_fail_closed_request_handoff(relative: str) -> None:
    # Removing this route lets direct execution bypass native reference validation.
    source = ROOT / relative
    paragraphs = source.read_text(encoding="utf-8").split("\n\n")
    routes = [p for p in paragraphs if "sequence-execution.md" in p]
    assert len(routes) == 1, f"{relative}: missing unique dependent-generation route"
    route = routes[0]
    assert re.search(r"REQUIRED|필수", route)
    for role in ("accepted", "history", "selected", "block", "standalone"):
        assert role in route, f"{relative}: missing handoff role {role}"
    destinations = re.findall(r"\]\(([^)]+)\)", route)
    assert any((source.parent / href.split("#")[0]).resolve().is_file()
               for href in destinations)


def test_optional_state_details_do_not_disable_basic_continuity_gate() -> None:
    text = (ROOT / "video-production-assets/SKILL.md").read_text(encoding="utf-8")
    section = text.split("## 선택적 상태·인과 인계", 1)[1].split("\n## ", 1)[0]
    assert "상세 슬롯" in section
    assert "기본 연속성 게이트는 필수" in section
    assert "인계할 때만" not in section


def test_edit_template_binds_required_evidence_to_existing_cells() -> None:
    # Given: the existing cut table, whose headings and field names must survive.
    text = TEMPLATE.read_text(encoding="utf-8")
    headers = next(line for line in text.splitlines() if line.startswith("| cut_id |"))
    assert headers.split(" | ") == [
        "| cut_id", "shot_id/asset_id", "source_in_s", "source_out_s",
        "playback_rate", "final_start_s", "final_end_s",
        "행동·카메라 변화 / 컷아웃→컷인 phase·state + cue time / 컷 이유",
        "transition/duration_s", "sound_id·sync anchor",
        "reaction/settle hold final start–end s·연속성/검수 상태 |",
    ]
    # When: the required continuity instructions for those cells are inspected.
    binding = next((p for p in text.split("\n\n") if f"#{ANCHOR}" in p), "")
    # Then: predecessor/outpoint/next-input/evidence/verdict are not optional notes.
    for slot in (
        "cut_id", "선행", "ID·버전", "planned", "accepted", "source_in_s",
        "source_out_s", "FPS/PTS", "다음 입력", "out/in", "인접 모션",
        "검수 상태", "unverified", "delivery_checks",
    ):
        assert slot in binding, f"edit cells lost required evidence binding: {slot}"
