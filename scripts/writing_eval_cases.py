# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_cases.py
"""Validated writing-evaluation inputs, independent of evaluator-only rubrics."""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, model_validator

CaseKind = Literal["single", "conversation", "fixture"]
PREFIX: Final = "이번 작업은 영상 기획/원고 텍스트만입니다. 채팅으로 답하고 생성·업로드·게시·외부 변경은 하지 마세요. 제공 자료는 평가용 가정이며 실제 자산을 검사했다고 말하지 마세요."
OWNERS: Final = {
    "T01": "video-production-assets/references/01-brief.md",
    "T02": "developing-video-synopses/references/synopsis-craft.md",
    "T03": "developing-video-synopses/references/synopsis-craft.md",
    "T04": "developing-video-synopses/references/synopsis-craft.md",
    "T05": "video-production-assets/references/03-screenplay.md",
    "T06": "video-production-assets/references/03-screenplay.md",
    "T07": "video-production-assets/references/03-screenplay.md",
    "T08": "video-production-assets/SKILL.md",
    "T09": "video-production-assets/references/03-screenplay.md",
    "T10a": "developing-video-synopses/SKILL.md",
    "T10b": "developing-video-synopses/SKILL.md",
    "T11": "orchestrating-video-preproduction/references/video-direction.md",
    "T12": "video-production-assets/references/03-screenplay.md",
    "T13": "video-production-assets/references/03-screenplay.md",
}


class CaseContractError(ValueError):
    """An input violates the approved case/adapter boundary."""

    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def resolve_owner(case_id: str) -> str:
    if case_id not in OWNERS:
        raise CaseContractError(f"Unknown writing case: {case_id}")
    return OWNERS[case_id]


class WritingCase(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    id: str
    kind: CaseKind
    owner: str
    turns: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def check_contract(self) -> WritingCase:
        if self.owner != resolve_owner(self.id):
            raise CaseContractError(f"Owner mismatch: {self.id}")
        expected_count = {"T11": 2, "T12": 3}.get(self.id, 1)
        expected_kind = {"T09": "fixture", "T11": "conversation", "T12": "conversation"}.get(self.id, "single")
        if len(self.turns) != expected_count or any(not t.strip() for t in self.turns):
            raise CaseContractError(f"Invalid turns: {self.id}")
        if self.kind != expected_kind:
            raise CaseContractError(f"Adapter mismatch: {self.id}")
        return self

    def message(self, turn: int) -> str:
        """Only the first user message carries the common scope prefix."""
        if turn:
            return self.turns[turn]
        prefix = PREFIX
        if self.id == "T09":
            prefix = prefix.replace("채팅으로 답하고", "허용된 임시 fixture의 원고만 수정하고")
        return prefix + "\n\n" + self.turns[0]


class WritingSuite(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    version: Literal["0.2"]
    cases: tuple[WritingCase, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_ids(self) -> WritingSuite:
        identifiers = [case.id for case in self.cases]
        if len(set(identifiers)) != len(identifiers):
            raise CaseContractError("Duplicate writing case ID")
        return self


class SingleCase(TypedDict):
    id: str
    prompt: str


def load_cases(path: Path) -> list[WritingCase]:
    """Parse a data-only suite; unknown fields (including rubric) are errors."""
    return list(WritingSuite.model_validate_json(path.read_bytes()).cases)


def single_turn_case(case: WritingCase) -> SingleCase:
    if case.kind != "single":
        raise CaseContractError(f"Expected single adapter, got {case.kind}: {case.id}")
    return {"id": case.id, "prompt": case.message(0)}
