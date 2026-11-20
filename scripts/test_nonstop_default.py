"""The infer-and-propose nonstop default must read the same in the three files that state it."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COORDINATOR = ROOT / "creative-production" / "SKILL.md"
INTAKE = ROOT / "concept-intake-design" / "SKILL.md"
SKILL_MAP = ROOT / "creative-production" / "references" / "skill-map.md"

# Each file must state: the reversible axes inferred, the recording, the ask conditions.
COMMON = {
    "reversible axes": r"platform.*tone.*length.*structure.*style|플랫폼.*톤.*길이.*구조.*스타일",
    "recorded inferred": r"`inferred`",
    "no core axis": r"subject or purpose|주제·목적",
    "explicit choose/discuss": r"골라볼래.*같이 정하자",
}
# Approvals are asked at their own gates, never at S01 and never inferred.
OWN_GATES = {
    COORDINATOR: r"Rights, execution, spend and publication approvals are asked at their own gates, never at S01 and never inferred",
    INTAKE: r"Rights, execution, spend and publication approvals are asked at their own gates \(G2, S08, S09, publication\), never here and never inferred",
    SKILL_MAP: r"권리·실행·비용·게시 승인은 각자의 게이트.*S01에서 묻거나 추론하지 않는다",
}
REASON = {
    COORDINATOR: r"one-line reason",
    INTAKE: r"one-line reason",
    SKILL_MAP: r"한 줄 이유",
}


def flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def step0() -> str:
    text = COORDINATOR.read_text(encoding="utf-8")
    return " ".join(text.split("## Step 0", 1)[1].split("\n## ", 1)[0].split())


def intake_step3() -> str:
    text = INTAKE.read_text(encoding="utf-8")
    return " ".join(text.split("3. **", 1)[1].split("4. **", 1)[0].split())


def skill_map_rules() -> str:
    text = SKILL_MAP.read_text(encoding="utf-8")
    return " ".join(text.split("## 3.", 1)[1].split("\n## ", 1)[0].split())


def sections() -> dict[Path, str]:
    return {COORDINATOR: step0(), INTAKE: intake_step3(), SKILL_MAP: skill_map_rules()}


def test_three_files_state_infer_and_propose_default() -> None:
    for path, section in sections().items():
        for name, pattern in {**COMMON, "reason": REASON[path], "own gates": OWN_GATES[path]}.items():
            assert re.search(pattern, section), f"{path.name}: missing {name}"


def test_old_always_ask_wording_is_gone() -> None:
    assert "asks the open axes in one batched turn" not in step0()
    assert not intake_step3().startswith("Ask once, batched.**")
    assert "사용자 선택은 S01에서 한 번만 받는다" not in skill_map_rules()


def test_intake_still_asks_one_batch_with_options_when_it_must() -> None:
    step3 = intake_step3()
    assert "Ask once, batched" in step3
    assert "numbered options, a default, an AI recommendation" in step3


def test_execution_and_spend_gates_are_unchanged_by_the_default() -> None:
    assert "Pre-accepted review gates never open spend" in step0()
    assert "위임은 실행·비용 권한을 열지 않는다" in skill_map_rules()


def test_approvals_are_not_an_s01_ask_condition() -> None:
    assert "or for rights, execution, spend or publication approval" not in step0()
    assert "or for rights, execution, spend or publication approval" not in intake_step3()
    assert "권리·실행·비용·게시 승인이 필요할 때만 S01" not in skill_map_rules()


def test_policy_allows_inferred_reversible_direction_but_not_acceptance() -> None:
    policy = flat(ROOT / "creative-production" / "references" / "policy.md")
    assert "reversible open axes" in policy and "`inferred` proposals" in policy
    assert "a proposal is never acceptance" in policy
    assert "at their own gates, never at intake and never inferred" in policy


def test_concept_packet_is_an_input_and_the_coordinator_continues() -> None:
    coordinator = step0()
    for needle in (
        "input, not a stopping point",
        "continue in the same turn",
        "synopsis/script, storyboard, prompts/asset plan",
        "first real gate or explicit stop",
        "which approval is needed next",
        "never end at the packet with an optional offer",
    ):
        assert needle in coordinator, needle
    intake = flat(INTAKE)
    assert "input, not a stopping point" in intake
    assert "continues in the same turn" in intake
    assert "optional \"next steps\" offer is not a finished turn" in intake
    assert "멈춤 지점이 아니다" in skill_map_rules()
    assert "같은 턴" in skill_map_rules()
