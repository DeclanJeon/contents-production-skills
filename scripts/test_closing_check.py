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
    "sonnet-triggers-r1.txt",
    "sonnet-nonstop-r3.txt",
    "sonnet-triggers-r2.txt",
]

def ending(name: str) -> str:
    return (ENDINGS / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", SONNET_OFFER_ENDINGS)
def test_real_sonnet_endings_are_flagged(name: str) -> None:
    text = ending(name)
    assert cc.find_optional_offer(text) is not None
    assert cc.closing_form(text) is None


def test_storyboard_table_dialogue_is_not_an_offer() -> None:
    table_end = (
        "| 컷 | 대사 |\n|---|---|\n| 3 | 바리스타: \"오늘 커피 한 잔 할까요?\" |\n"
        "| 4 | 손님: \"좋아요, 같이 마실까요?\" |\n\n다음: 컷별 프롬프트 — 자동 진행"
    )
    assert cc.find_optional_offer(table_end) is None
    assert cc.closing_form(table_end) == "next"
    assert cc.find_optional_offer("본문\n| 3 | 바리스타: \"한 잔 할까요?\" |") is None
    adjacent = "본문\n원하시면 캐릭터 시트도 만들어 드릴게요.\n다음: 컷별 프롬프트 — 자동 진행"
    assert cc.find_optional_offer(adjacent) is not None
    assert cc.find_optional_offer("다음: 프롬프트 — 자동 진행\n원하시면 시트도 만들어 드립니다.") is not None


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
    assert cc.closing_form("본문\n\n자동 진행") is None
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
    phrases = ("원하시면", "할까요?") if path == SKILL else (
        "원하시면", "필요하시면", "할까요?", "드릴까요", "if you'd like", "want me to", "let me know"
    )
    for phrase in phrases:
        assert phrase in text, f"{path.name}: {phrase}"
    assert "[브랜드명]" in text, path.name


def test_skill_closing_contract_sits_in_step_0() -> None:
    step0 = SKILL.read_text(encoding="utf-8").split("## Step 0", 1)[1].split("\n## ", 1)[0]
    assert "**Closing contract.**" in step0


def test_frontier_words_stay_under_freed_cap() -> None:
    assert routing_regression.measure(routing_regression.FRONTIER)["words"] <= FRONTIER_WORD_CAP


# Real s1 endings after F1 round 1 (2 models x 3 runs), last 6 lines each.
F1R2_DISALLOWED_WAIT = ["f1r2-eco-r1.txt", "f1r2-eco-r2.txt", "f1r2-sonnet-r1.txt"]


@pytest.mark.parametrize("name", F1R2_DISALLOWED_WAIT)
def test_real_wait_endings_on_g1_or_placeholders_are_disallowed(name: str) -> None:
    text = ending(name)
    assert cc.closing_form(text) == "wait"
    assert cc.disallowed_wait_reason(text) is not None


def test_real_next_ending_is_clean() -> None:
    text = ending("f1r2-sonnet-r3.txt")
    assert cc.closing_form(text) == "next"
    assert cc.disallowed_wait_reason(text) is None
    assert cc.text_after_closing(text) is None
    assert cc.find_optional_offer(text) is None
    assert cc.closing_defect(text) is None


def test_real_next_line_with_parentheses_is_not_exact() -> None:
    text = ending("f1r2-eco-r3.txt")
    assert "(" in text.splitlines()[-1]
    assert cc.closing_form(text) is None
    assert cc.closing_defect(text) is not None


def test_real_hedged_next_line_is_not_a_closing_form() -> None:
    text = ending("f1r3-sonnet-r2-s1.txt")
    assert cc.closing_form(text) is None
    assert cc.closing_hedge(text.splitlines()[-1]) is not None
    assert "hedge" in cc.closing_defect(text)


def test_real_mixed_form_line_is_not_a_closing_form() -> None:
    text = ending("f1r3-sonnet-r2-p5.txt")
    assert cc.closing_form(text) is None
    assert cc.mixed_closing(text.splitlines()[-1])
    assert cc.closing_defect(text) is not None


def test_real_paid_wait_is_exact_and_allowed() -> None:
    text = ending("f1r3-eco-r2-s1.txt")
    assert cc.closing_form(text) == "wait"
    assert cc.disallowed_wait_reason(text) is None
    assert cc.is_paid_execution_wait(text)
    assert not cc.is_paid_execution_wait("본문\n\n다음: 프롬프트 — 자동 진행")


@pytest.mark.parametrize(
    "line",
    [
        "다음: 컷별 프롬프트 — 자동 진행",
        "**다음: 컷별 프롬프트·에셋 계획 — 자동 진행**",
        "대기: 유료 생성 실행·비용 승인 — 필요: 모델·비용 승인",
    ],
)
def test_exact_patterns_accepted(line: str) -> None:
    assert cc.closing_form(f"본문\n\n{line}") in {"next", "wait"}
    assert cc.closing_defect(f"본문\n\n{line}") is None


@pytest.mark.parametrize(
    "line",
    [
        "다음: 스토리보드 — 자동 진행 가능 (원하시면 요청해 주세요)",
        "다음: 스토리보드 — 자동 진행 가능",
        "다음: 스토리보드 (S06) — 자동 진행",
        "다음: 스토리보드 — 자동 진행 — 대기: 실행·비용 승인 — 필요: 비용 승인",
        "대기: 실행·비용 승인 — 필요: 비용 승인 — 다음: 프롬프트 — 자동 진행",
        "대기: 실행·비용 승인 — 필요: 답을 주시면 확정",
        "다음: 스토리보드 — 자동 진행, 요청해 주세요",
    ],
)
def test_hedged_or_mixed_closing_lines_are_not_closing_forms(line: str) -> None:
    assert cc.closing_form(f"본문\n\n{line}") is None
    assert cc.closing_defect(f"본문\n\n{line}") is not None


def test_real_text_after_closing_line_is_detected() -> None:
    text = ending("f1r2-sonnet-r2.txt")
    assert cc.closing_form(text) is None
    assert cc.text_after_closing(text) is not None
    assert cc.text_after_closing(text).startswith("(단,")


def test_text_after_closing_detects_offer_after_wait_line() -> None:
    text = "본문\n\n대기: 유료 생성 실행 승인 — 필요: 비용 승인\n원하시면 시트도 만들 수 있습니다."
    assert cc.text_after_closing(text) == "원하시면 시트도 만들 수 있습니다."
    assert cc.text_after_closing("본문\n\n다음: 대본 — 자동 진행") is None
    assert cc.text_after_closing("본문 한 줄\n둘째 줄") is None


@pytest.mark.parametrize(
    "line",
    [
        "대기: G2 실행·비용 승인 — 필요: 이미지 생성 모델·비용 승인",
        "대기: 배우 초상 사용 — 필요: 출연자 초상·음성 동의",
        "대기: 게시 승인 — 필요: 업로드 승인",
        "대기: 사용자 지정 중단 — 필요: 컷 검토 후 재개 지시",
        "대기: 주제 없음 — 필요: 영상의 주제와 목적",
    ],
)
def test_allowed_wait_reasons(line: str) -> None:
    assert cc.wait_reason_allowed(line)


@pytest.mark.parametrize(
    "line",
    [
        "대기: G1 기획 확인 — 필요: 이 기획안 승인",
        "대기: 보드 승인 — 필요: 보드 수용 여부",
        "대기: 브랜드 정보 — 필요: 브랜드명과 로고",
        "대기: 카피 확정 — 필요: 컵홀더 카피",
        "대기: 실행·비용 승인과 G1 확정 — 필요: G1 수락과 비용 승인",
        "대기: 확인 — 필요: 다음 진행 여부",
        "대기: 보드 승인 — 필요: 비용 없음 확인",
        "대기: 스토리보드 승인 — 필요: 승인 후 유료 생성 진행",
    ],
)
def test_disallowed_wait_reasons(line: str) -> None:
    assert not cc.wait_reason_allowed(line)


@pytest.mark.parametrize(
    "line",
    [
        "대기: 기획안 기반 유료 영상 실행·비용 승인 — 필요: 모델 선택과 비용 승인",
        "대기: 유료 영상 생성 실행·비용 승인 — 필요: G2 보드 수락과 모델·비용 승인",
        "대기: G2 보드 수락과 실행·비용 승인 — 필요: 보드 승인과 비용 승인",
        "대기: 보드 수락과 유료 생성 실행·비용 승인 — 필요: 모델·비용 승인",
    ],
)
def test_paid_wait_may_also_ask_board_acceptance(line: str) -> None:
    assert cc.wait_reason_allowed(line)
    assert cc.is_paid_execution_wait(line)


@pytest.mark.parametrize("line", ["대기: 기획안 승인 — 필요: 기획안 수락 여부", "대기: 기획 수락 — 필요: 비용 없음 확인"])
def test_plan_acceptance_wait_stays_disallowed(line: str) -> None:
    assert not cc.wait_reason_allowed(line)


def test_en_dash_closing_line_is_named_in_defect() -> None:
    text = "본문\n\n다음: 컷별 프롬프트 – 자동 진행"
    assert cc.closing_form(text) is None
    assert "–" in cc.closing_defect(text) and "dash" in cc.closing_defect(text)


def test_skill_ends_with_before_you_reply_checklist() -> None:
    text = SKILL.read_text(encoding="utf-8")
    last = text.rstrip().rsplit("\n## ", 1)[1]
    assert last.startswith("Before you reply")
    flat_last = " ".join(last.split())
    for phrase in ("다음: ", "대기: ", "nothing after it", "S04–S07", "S08", "S06", "G1", "가능", "요청해 주세요", "주시면"):
        assert phrase in flat_last, phrase
    assert len([line for line in last.splitlines() if line.startswith("- ")]) <= 4


@pytest.mark.parametrize("path", [SKILL, POLICY, SKILL_MAP])
def test_closed_wait_list_and_g1_rule_stated(path: Path) -> None:
    text = flat(path)
    assert "G1" in text and ("plan acceptance" in text or "기획 수락" in text), path.name
    assert "S06" in text, path.name


def test_policy_states_never_wait_rule_and_examples() -> None:
    text = flat(POLICY)
    assert "G1 and plan acceptance are never a 대기 reason; placeholders are never a 대기 reason" in text
    assert "`다음: 컷별 프롬프트·에셋 계획 — 자동 진행`" in text
    assert "`대기: 유료 영상 생성 실행·비용 승인 — 필요: 모델 선택과 비용 승인`" in text
    assert "nothing follows it" in text
    assert "`^다음: [^—(]+ — 자동 진행$`" in text and "`^대기: [^—]+ — 필요: .+$`" in text
    assert "valid only after the storyboard/shot list exists" in text


def test_closing_contract_is_scoped_to_finished_video_goal() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert "End every finished-video-goal reply" in text
    last = text.rstrip().rsplit("\n## ", 1)[1]
    assert "Finished-video goal:" in last
    assert "single-artifact" in POLICY.read_text(encoding="utf-8")


def test_g2_without_pre_delegation_folds_into_s08_wait() -> None:
    assert "with G2 board acceptance" in flat(SKILL)
    assert "G2 without pre-delegation is not a separate stop" in flat(POLICY)
    sm = flat(SKILL_MAP)
    assert "G2는 별도 정지가 아니라 S08" in sm
    assert "미리 위임 없으면 S08 실행·비용 대기에 합침" in sm
