"""Offline input/dispatch contracts; never submit model requests."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
from typing import Literal, assert_never

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "qa/matt-writing-inputs.json"
PREFIX = "이번 작업은 영상 기획/원고 텍스트만입니다. 채팅으로 답하고 생성·업로드·게시·외부 변경은 하지 마세요. 제공 자료는 평가용 가정이며 실제 자산을 검사했다고 말하지 마세요."
T05 = "중간 질문 없이 한 번에 두 블록의 영상 발화 원고를 써 주세요. 초보 대상이며 중심 질문은 ‘두 옷의 차이를 어떻게 볼까?’입니다. 자료 A: 한 옷은 어깨가 넓고 허리가 좁아 보인다. 자료 B: 다른 옷은 위아래 폭이 비슷해 보인다. 결말은 ‘이제 전체 윤곽을 나란히 봅니다.’로 고정합니다. CTA는 넣지 마세요."


def test_roster_dispatch_preserves_exact_single_prompt() -> None:
    api = importlib.import_module("writing_eval_cases")
    cases = api.load_cases(INPUTS)
    assert [c.id for c in cases] == [
        "T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09",
        "T10a", "T10b", "T11", "T12", "T13",
    ]
    selected = next(c for c in cases if c.id == "T05")
    assert api.single_turn_case(selected) == {"id": "T05", "prompt": PREFIX + "\n\n" + T05}
    assert len(next(c for c in cases if c.id == "T11").turns) == 2
    assert len(next(c for c in cases if c.id == "T12").turns) == 3
    assert api.resolve_owner("T10a") == "developing-video-synopses/SKILL.md"
    assert api.resolve_owner("T13") == "video-production-assets/references/03-screenplay.md"


@pytest.mark.parametrize("identifier", ["T09", "T11", "T12"])
def test_single_execution_rejects_other_adapter_kinds(identifier: str) -> None:
    api = importlib.import_module("writing_eval_cases")
    case = next(c for c in api.load_cases(INPUTS) if c.id == identifier)
    with pytest.raises(api.CaseContractError, match="single"):
        api.single_turn_case(case)


@pytest.mark.parametrize("mutation", ["duplicate", "unknown", "empty", "rubric", "owner", "turn_count"])
def test_untrusted_suite_rejects_invalid_contract(tmp_path: Path, mutation: Literal["duplicate", "unknown", "empty", "rubric", "owner", "turn_count"]) -> None:
    api = importlib.import_module("writing_eval_cases")
    raw = json.loads(INPUTS.read_text(encoding="utf-8"))
    match mutation:
        case "duplicate": raw["cases"].append(raw["cases"][0].copy())
        case "unknown": raw["cases"][0]["id"] = "T99"
        case "empty": raw["cases"][0]["turns"] = [""]
        case "rubric": raw["cases"][0]["expected"] = "secret verdict"
        case "owner": raw["cases"][0]["owner"] = "../secret.txt"
        case "turn_count": raw["cases"][0]["turns"].append("unexpected second message")
        case unreachable: assert_never(unreachable)
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    with pytest.raises((ValidationError, api.CaseContractError)):
        api.load_cases(path)


@pytest.mark.parametrize("identifier", ["T09", "T11", "T12"])
def test_direct_single_executor_rejects_multi_or_writing_case(tmp_path: Path, identifier: str) -> None:
    api = importlib.import_module("writing_eval_cases")
    runner = importlib.import_module("run_guide_behavior")
    with pytest.raises(api.CaseContractError, match="single"):
        runner.execute({"id": identifier, "prompt": "must not submit"}, tmp_path, tmp_path, {}, "baseline")


def test_existing_executor_consumes_t_prompt_without_changing_legacy_permissions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    api = importlib.import_module("writing_eval_cases")
    runner = importlib.import_module("run_guide_behavior")
    case = next(c for c in api.load_cases(INPUTS) if c.id == "T05")
    wire = "\n".join(json.dumps(e) for e in [
        {"type": "tool_execution_start", "toolCallId": "read", "toolName": "read", "args": {"path": case.owner}},
        {"type": "tool_execution_end", "toolCallId": "read", "toolName": "read", "isError": False},
        {"type": "message_end", "message": {"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "원고"}]}},
        {"type": "agent_settled", "aborted": False},
    ]).encode()

    class FakeProcess:
        returncode = 0

        def communicate(self, timeout: float) -> tuple[bytes, bytes]:
            return wire, b""

    monkeypatch.setattr(runner.subprocess, "Popen", lambda *args, **kwargs: FakeProcess())
    monkeypatch.setattr(runner, "fingerprint", lambda root: {"sha256": "baseline"})
    result = runner.execute(api.single_turn_case(case), tmp_path, tmp_path,
        {"executable": "pi", "provider": "test", "model": "test", "timeout_seconds": 3}, "baseline")
    record = json.loads((tmp_path / "T05.attempt.json").read_text(encoding="utf-8"))
    assert result["status"] == "completed"
    assert record["verdict"] == "UNREVIEWED"
    assert record["command"][-1] == PREFIX + "\n\n" + T05
    assert "read,grep,find,ls" in record["command"]
    assert "--no-session" in record["command"]
    assert record["prompt_sha256"] == hashlib.sha256((PREFIX + "\n\n" + T05).encode()).hexdigest()
