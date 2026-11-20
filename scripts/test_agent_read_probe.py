"""Offline checks for scripts/agent_read_probe.py. These tests never call pi."""
from __future__ import annotations

from pathlib import Path

import pytest

import agent_read_probe as probe

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "scripts" / "fixtures" / "agent_probe_sample.jsonl"
INSTALL = Path("/tmp/probe-install")
SKILL = "creative-production/SKILL.md"


def test_probe_cases_valid() -> None:
    cases = probe.load_cases(probe.DEFAULT_CASES)
    ids = [case["id"] for case in cases]
    assert ids == ["p1", "p2", "p3", "p4", "p5", "n1", "n2", "n3", "s1"]
    assert len(set(ids)) == len(ids)
    for case in cases:
        assert case["kind"] in probe.KINDS
        assert case["prompt"].strip()
        for rel in case.get("expect_any_read", []):
            assert (ROOT / rel).is_file(), f"{case['id']}: {rel} not in repo"
        if case["kind"] in ("positive", "nonstop"):
            assert case.get("expect_any_read"), case["id"]
    p3 = next(case for case in cases if case["id"] == "p3")
    assert "skill" not in p3["prompt"].lower() and "스킬" not in p3["prompt"]


def test_load_cases_rejects_duplicate_ids(tmp_path: Path) -> None:
    path = tmp_path / "cases.json"
    path.write_text(
        '{"cases": [{"id": "a", "kind": "negative", "prompt": "x"},'
        ' {"id": "a", "kind": "negative", "prompt": "y"}]}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate"):
        probe.load_cases(path)


def test_parse_reads() -> None:
    parsed = probe.parse_events(FIXTURE.read_text(encoding="utf-8").splitlines(), INSTALL)
    assert parsed.calls == [
        ("read", SKILL),
        ("grep", "video-production-assets/references/30-marketing-story-craft.md"),
        ("find", "video-production-assets/references"),
        ("read", "video-production-assets/references/23a-captions-layout.md"),
    ]
    assert parsed.opened == [
        SKILL,
        "video-production-assets/references/30-marketing-story-craft.md",
        "video-production-assets/references/23a-captions-layout.md",
    ]
    assert parsed.final.startswith("기획안과 대본, 콘티")
    assert str(INSTALL) not in probe.render_reads(parsed)


def test_judge() -> None:
    positive = {"id": "p5", "kind": "positive", "expect_any_read": ["a.md", "b.md"]}
    negative = {"id": "n1", "kind": "negative"}
    assert probe.judge(positive, ["x.md", "b.md"], "")[0] is True
    assert probe.judge(positive, ["x.md"], "")[0] is False
    assert probe.judge(negative, ["x.md"], "")[0] is True
    assert probe.judge(negative, ["x.md", SKILL], "")[0] is False


NONSTOP_CASE = {"id": "s1", "kind": "nonstop", "expect_any_read": [SKILL]}
GOOD_S1 = (
    "## 스토리보드\n| 1 | 0–3s | 클로즈업 |\n\n"
    "다음: 컷별 프롬프트·에셋 계획 — 자동 진행"
)


def test_judge_nonstop_passes_with_contract_closing() -> None:
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], GOOD_S1)
    assert verdict is True, reason
    wait = "샷 리스트를 정리했습니다.\n\n대기: G2 실행 승인 — 필요: 이미지 생성 모델·비용 승인"
    assert probe.judge(NONSTOP_CASE, [SKILL], wait)[0] is True
    verdict, reason = probe.judge(NONSTOP_CASE, [], GOOD_S1)
    assert verdict is False
    assert "SKILL.md" in reason


def test_judge_nonstop_fails_on_optional_offer_missing_closing_or_content() -> None:
    offer = "스토리보드 7컷.\n\n원하시면 캐릭터 시트를 이어서 만들 수 있습니다."
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], offer)
    assert verdict is False and "optional offer" in reason and "closing line" in reason
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], "스토리보드 7컷을 정리했습니다.")
    assert verdict is False and "closing line" in reason
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], "기획 요약.\n\n다음: 대본 — 자동 진행")
    assert verdict is False and "storyboard" in reason
    claimed = GOOD_S1.replace("0–3s", "0–3s 영상을 생성했습니다")
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], claimed)
    assert verdict is False and "completion claim" in reason


def test_judge_nonstop_fails_on_real_sonnet_s1_endings() -> None:
    for name in ("sonnet-final-r1.txt", "sonnet-final-r2.txt", "sonnet-final-r3.txt"):
        text = (ROOT / "scripts" / "fixtures" / "closing_endings" / name).read_text(encoding="utf-8")
        assert probe.judge(NONSTOP_CASE, [SKILL], text)[0] is False, name


def test_judge_positive_fails_on_optional_offer() -> None:
    positive = {"id": "p5", "kind": "positive", "expect_any_read": ["a.md"]}
    assert probe.judge(positive, ["a.md"], "자막 규칙입니다.\n\nIf you'd like, I can add more.")[0] is False
    assert probe.judge(positive, ["a.md"], "자막 규칙입니다.")[0] is True
    assert probe.judge({"id": "n1", "kind": "negative"}, ["x.md"], "원하시면 더 드립니다.")[0] is True


def test_judge_nonstop_fails_on_disallowed_wait_and_text_after_closing() -> None:
    folder = ROOT / "scripts" / "fixtures" / "closing_endings"
    for name, expected in (
        ("f1r2-eco-r1.txt", "disallowed 대기 reason"),
        ("f1r2-eco-r2.txt", "disallowed 대기 reason"),
        ("f1r2-sonnet-r1.txt", "disallowed 대기 reason"),
        ("f1r2-sonnet-r2.txt", "text after closing line"),
    ):
        verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], (folder / name).read_text(encoding="utf-8"))
        assert verdict is False and expected in reason, name
    text = "## 스토리보드\n" + (folder / "f1r2-sonnet-r3.txt").read_text(encoding="utf-8")
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], text)
    assert verdict is True, reason


def test_judge_nonstop_fails_on_hedged_or_parenthesized_closing_line() -> None:
    folder = ROOT / "scripts" / "fixtures" / "closing_endings"
    for name, expected in (
        ("f1r3-sonnet-r2-s1.txt", "hedge"),
        ("f1r2-eco-r3.txt", "not an exact pattern"),
    ):
        text = "## 스토리보드\n" + (folder / name).read_text(encoding="utf-8")
        verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], text)
        assert verdict is False and expected in reason, (name, reason)


def test_judge_positive_fails_on_mixed_closing_line() -> None:
    positive = {"id": "p5", "kind": "positive", "expect_any_read": ["a.md"]}
    mixed = (ROOT / "scripts" / "fixtures" / "closing_endings" / "f1r3-sonnet-r2-p5.txt").read_text(encoding="utf-8")
    verdict, reason = probe.judge(positive, ["a.md"], mixed)
    assert verdict is False
    verdict, reason = probe.judge(positive, ["a.md"], mixed.replace("답을 주시면", "답을 받아"))
    assert verdict is False and "mixed" in reason


def test_judge_nonstop_fails_on_paid_wait_without_storyboard_content() -> None:
    folder = ROOT / "scripts" / "fixtures" / "closing_endings"
    tail = (folder / "f1r3-eco-r2-s1.txt").read_text(encoding="utf-8")
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], tail)
    assert verdict is False and "paid-execution 대기 without storyboard/shot-list content" in reason
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], "## 5. 샷 명세표 (8샷)\n" + tail)
    assert verdict is True, reason
    verdict, reason = probe.judge(NONSTOP_CASE, [SKILL], "## 스토리보드\n" + tail)
    assert verdict is True, reason
