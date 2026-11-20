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


def test_judge_nonstop_is_never_auto_passed() -> None:
    case = {"id": "s1", "kind": "nonstop", "expect_any_read": [SKILL]}
    final = "기획안, 대본, 콘티를 정리했습니다. 실행 승인을 해주세요."
    verdict, reason = probe.judge(case, [SKILL], final)
    assert verdict is None
    assert "후보" in reason
    verdict, reason = probe.judge(case, [], final)
    assert verdict is False
    assert "SKILL.md" in reason
