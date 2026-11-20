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
    "approval/rights asks": r"rights.*execution.*spend.*publication|권리·실행·비용·게시",
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
        for name, pattern in {**COMMON, "reason": REASON[path]}.items():
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
