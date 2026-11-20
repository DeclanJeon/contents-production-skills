"""Offline checks for scripts/closing_check.py and the closing-contract wording."""
from __future__ import annotations

from pathlib import Path

import pytest

import closing_check as cc
import routing_regression

ROOT = Path(__file__).resolve().parents[1]
ENDINGS = ROOT / "scripts" / "fixtures" / "closing_endings"
SKILL = ROOT / "creative-production" / "SKILL.md"
POLICY = ROOT / "creative-production" / "references" / "policy.md"
SKILL_MAP = ROOT / "creative-production" / "references" / "skill-map.md"
FRONTIER_WORD_CAP = 2900

# Real Sonnet s1 endings from the 2.63 probes (3x-final, 3x-nonstop-fix, 3x-triggers).
SONNET_OFFER_ENDINGS = [
    "sonnet-final-r1.txt",
    "sonnet-final-r2.txt",
    "sonnet-final-r3.txt",
    "sonnet-nonstop-r1.txt",
    "sonnet-nonstop-r2.txt",
    "sonnet-nonstop-r3.txt",
    "sonnet-triggers-r1.txt",
    "sonnet-triggers-r2.txt",
]


def ending(name: str) -> str:
    return (ENDINGS / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", SONNET_OFFER_ENDINGS)
def test_real_sonnet_endings_are_flagged(name: str) -> None:
    text = ending(name)
    assert cc.find_optional_offer(text) is not None
    assert cc.closing_form(text) is None


@pytest.mark.parametrize(
    "line",
    [
        "원하시면 컷별 프롬프트로 이어서 작성하겠습니다.",
        "필요하시면 캐릭터 시트도 만들어 드립니다.",
        "원하면 편집 플랜까지 확장할 수 있습니다.",
        "스토리보드를 더 다듬을까요?",
        "캐릭터 시트를 만들어 드릴까요",
        "정보를 주시면 이어서 작성하겠습니다.",
        "If you'd like, I can continue with the character sheet.",
        "Want me to write the shot prompts next?",
        "Let me know and I will continue.",
    ],
)
def test_offer_patterns_hit(line: str) -> None:
    assert cc.find_optional_offer(f"## 스토리보드\n본문\n\n{line}\n") == line


def test_contract_closing_lines_have_no_offer() -> None:
    next_text = "스토리보드 7컷을 정리했습니다.\n\n다음: 컷별 프롬프트·에셋 계획 — 자동 진행"
    wait_text = "프롬프트까지 작성했습니다.\n\n대기: G2 실행·비용 승인 — 필요: 이미지 생성 모델과 비용 승인"
    assert cc.find_optional_offer(next_text) is None
    assert cc.find_optional_offer(wait_text) is None
    assert cc.closing_form(next_text) == "next"
    assert cc.closing_form(wait_text) == "wait"


def test_closing_form_tolerates_markdown_and_rejects_partial_forms() -> None:
    assert cc.closing_form("본문\n\n**다음: 스토리보드 — 자동 진행**") == "next"
    assert cc.closing_form("본문\n\n> `대기: G2 승인 — 필요: 비용 승인`") == "wait"
    assert cc.closing_form("본문\n\n다음: 스토리보드") is None
    assert cc.closing_form("본문\n\n대기: G2 승인") is None
    assert cc.closing_form("다음: 스토리보드 — 자동 진행\n\n본문 한 줄 더") is None
    assert cc.closing_form("") is None


def test_only_the_tail_is_scanned() -> None:
    body = "원하시면 이라는 말이 본문 앞쪽에 있습니다.\n" + "\n".join(f"줄 {i}" for i in range(8))
    assert cc.find_optional_offer(body) is None


def test_requirement_list_without_offer_is_not_flagged() -> None:
    # Deepseek-eco style ending: a list of needed facts, no optional offer.
    text = (
        "스토리보드 7컷을 정리했습니다.\n\n"
        "다음에 필요한 것: ① 브랜드명·로고 ② 바리스타 외형 ③ 제작 방식(실촬영 또는 AI 생성)"
    )
    assert cc.find_optional_offer(text) is None
    assert cc.closing_form(text) is None


def test_placeholderable_wait_is_flagged_but_real_gate_is_not() -> None:
    blocked = "대기: 브랜드 정보 — 필요: 브랜드명과 로고 유무"
    gate = "대기: G2 실행 승인 — 필요: 이미지 생성 모델·비용 승인"
    assert cc.blocking_on_placeholderable_fact(blocked) == "브랜드명과 로고 유무"
    assert cc.blocking_on_placeholderable_fact(gate) is None
    assert cc.blocking_on_placeholderable_fact("다음: 프롬프트 — 자동 진행") is None


def flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


@pytest.mark.parametrize("path", [SKILL, POLICY, SKILL_MAP])
def test_closing_contract_wording_present(path: Path) -> None:
    text = flat(path)
    assert "다음: <" in text and "자동 진행" in text, path.name
    assert "대기: <" in text and "필요: <" in text, path.name
    for phrase in ("원하시면", "필요하시면", "할까요?", "드릴까요", "if you'd like", "want me to", "let me know"):
        assert phrase in text, f"{path.name}: {phrase}"
    assert "[브랜드명]" in text, path.name


def test_skill_closing_contract_sits_in_step_0() -> None:
    step0 = SKILL.read_text(encoding="utf-8").split("## Step 0", 1)[1].split("\n## ", 1)[0]
    assert "**Closing contract.**" in step0


def test_frontier_words_stay_under_freed_cap() -> None:
    assert routing_regression.measure(routing_regression.FRONTIER)["words"] <= FRONTIER_WORD_CAP
