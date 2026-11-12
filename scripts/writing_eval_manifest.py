# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_evaluation.py
"""Immutable evaluation plans; plan creation is never live authorization."""
from __future__ import annotations

from decimal import Decimal
import json
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from writing_eval_cases import CaseKind, OWNERS, WritingCase
from writing_eval_snapshot import EvaluationContractError, Snapshot, digest
from writing_eval_transport import RpcProfile

Condition = Literal["baseline", "candidate"]


class EvaluationProfile(RpcProfile):
    max_case_runs: int = Field(gt=0)
    max_provider_calls: int | None = Field(gt=0)
    max_total_tokens: int | None = Field(gt=0)
    max_cost_usd: Decimal | None = Field(gt=0, allow_inf_nan=False)
    retry_limit: Literal[0] = 0


class RunSlot(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    id: str
    case_id: str
    condition: Condition
    repeat: int = Field(ge=1, le=5)
    kind: CaseKind
    owner: str
    stages: int = Field(gt=0)
    input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class RunManifest(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    version: Literal["0.2"] = "0.2"
    execution_state: Literal["PLANNED"] = "PLANNED"
    live_authorized: Literal[False] = False
    profile: EvaluationProfile | None
    response_stages: int
    runs: tuple[RunSlot, ...]
    baseline_snapshot: Snapshot | None = None
    candidate_snapshot: Snapshot | None = None


def input_digest(case: WritingCase) -> str:
    data = {"id": case.id, "kind": case.kind, "owner": case.owner,
            "messages": [case.message(n) for n in range(len(case.turns))]}
    return digest(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def build_run_manifest(cases: list[WritingCase], profile: EvaluationProfile | None) -> RunManifest:
    if len(cases) != 14 or {c.id for c in cases} != set(OWNERS):
        raise EvaluationContractError("Evaluation requires the full 14-case roster without duplicates")
    slots: list[RunSlot] = []
    for repeat in range(1, 6):
        conditions: tuple[Condition, Condition] = ("baseline", "candidate") if repeat % 2 else ("candidate", "baseline")
        for case in cases:
            for condition in conditions:
                slots.append(RunSlot(id=f"{condition}/{case.id}/r{repeat}", case_id=case.id,
                    condition=condition, repeat=repeat, kind=case.kind, owner=case.owner,
                    stages=len(case.turns), input_sha256=input_digest(case)))
    return RunManifest(profile=profile, runs=tuple(slots), response_stages=sum(s.stages for s in slots))
