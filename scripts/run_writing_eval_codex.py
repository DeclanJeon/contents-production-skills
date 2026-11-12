# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3", "typer"]
# ///
# How to run: python3 scripts/run_writing_eval_codex.py --help
"""Explicitly authorized, pinned native Codex batches; never auto-grade or retry."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
from typing import ClassVar, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, ValidationError

from run_writing_evaluation import EvaluationBackend, RunScope, run_case
from writing_eval_cases import load_cases
from writing_eval_codex import CodexBackend
from writing_eval_manifest import Condition, RunManifest, build_run_manifest
from writing_eval_review import RunReceipt, verify_fixture_files, verify_trace
from writing_eval_snapshot import EvaluationContractError, Snapshot, digest, verify_snapshot

ROOT = Path(__file__).resolve().parents[1]
HARNESS = (
    "run_writing_eval_codex.py", "writing_eval_codex.py", "writing_eval_codex_tools.py", "writing_eval_codex_mcp.py",
    "run_writing_evaluation.py", "writing_eval_cases.py", "writing_eval_manifest.py", "writing_eval_review.py",
    "writing_eval_snapshot.py", "writing_eval_source_paths.py", "writing_eval_references.py", "writing_eval_wire.py", "writing_eval_transport.py", "run_guide_behavior.py", "guide_eval_routes.py",
)


class BatchRequest(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    manifest: Path
    condition: Literal["baseline", "candidate", "paired"]
    approval_reference: str
    fixture_writes_approved: bool = False
    continue_unstarted: bool = False


class BatchResult(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    status: Literal["FINISHED", "STOPPED"]
    completed: int
    reused: int
    inconclusive: int
    remaining: int
    invocation_id: str


class HarnessPin(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    files: dict[str, str]
    executable: str
    cli_version: str
    profile_sha256: str


def harness_files() -> dict[str, str]:
    paths = [ROOT / "scripts" / name for name in HARNESS]
    paths += [ROOT / "qa/matt-writing-inputs.json", ROOT / "qa/matt-writing-rubric.json"]
    return {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in paths}


def dispatch_batch(request: BatchRequest, backend: EvaluationBackend | None = None) -> BatchResult:
    if not request.approval_reference.strip():
        raise EvaluationContractError("Explicit evaluation approval required")
    plan = RunManifest.model_validate_json(request.manifest.read_bytes())
    profile = plan.profile
    conditions: tuple[Condition, ...] = ("baseline", "candidate") if request.condition == "paired" else (request.condition,)
    snapshots: dict[Condition, Snapshot] = {}
    for condition in conditions:
        snapshot = plan.baseline_snapshot if condition == "baseline" else plan.candidate_snapshot
        if snapshot is None:
            raise EvaluationContractError("Missing pinned source snapshot")
        _ = verify_snapshot(snapshot)
        snapshots[condition] = snapshot
    if profile is None or profile.provider != "openai" or profile.model != "gpt-6-luna":
        raise EvaluationContractError("Explicit approved Codex gpt-6-luna profile required")
    if any(v is not None for v in (profile.max_cost_usd, profile.max_total_tokens, profile.max_provider_calls)):
        raise EvaluationContractError("CLI cannot enforce finite provider/token/cost ceilings")
    cases = load_cases(ROOT / "qa/matt-writing-inputs.json")
    canonical = build_run_manifest(cases, profile)
    if plan.runs != canonical.runs or plan.response_stages != canonical.response_stages:
        raise EvaluationContractError("Run roster/input mismatch")
    if len(plan.runs) > profile.max_case_runs:
        raise EvaluationContractError("Case-run ceiling smaller than fixed 140-run evaluation")
    slots = [slot for slot in plan.runs if slot.condition in conditions]
    if any(slot.kind == "fixture" for slot in slots) and not request.fixture_writes_approved:
        raise EvaluationContractError("Explicit isolated fixture write permission required")
    root = request.manifest.resolve().parent
    reusable: set[str] = set()
    for slot in slots:
        snapshot = snapshots[slot.condition]
        target = root / "runs" / slot.id
        if not target.exists():
            continue
        if not request.continue_unstarted or not (target / "execution.json").is_file():
            raise EvaluationContractError(f"Existing attempt cannot be overwritten/resampled: {slot.id}")
        receipt = RunReceipt.model_validate_json((target / "execution.json").read_bytes())
        if (receipt.status != "completed" or receipt.run_id != slot.id or receipt.input_sha256 != slot.input_sha256
                or receipt.source_before != snapshot.sha256 or receipt.source_after != snapshot.sha256
                or not verify_trace(receipt, slot, snapshot)):
            raise EvaluationContractError(f"Existing attempt is not reusable: {slot.id}")
        if slot.kind == "fixture":
            try:
                if not verify_fixture_files(target, receipt.trace):
                    raise EvaluationContractError(f"Invalid prior fixture evidence: {slot.id}")
            except (OSError, UnicodeError, ValidationError) as exc:
                raise EvaluationContractError(f"Missing/invalid prior fixture evidence: {slot.id}") from exc
        reusable.add(slot.id)
    if any(not (snapshots[slot.condition].root / slot.owner).is_file() for slot in slots):
        raise EvaluationContractError("Owner missing from pinned snapshot")
    current_files = harness_files()
    version = subprocess.check_output([profile.executable, "--version"], text=True, timeout=15).strip()
    if not version.startswith("codex-cli "):
        raise EvaluationContractError("Selected executable is not Codex CLI")
    pin = HarnessPin(files=current_files, executable=profile.executable, cli_version=version,
        profile_sha256=digest(profile.model_dump_json().encode()))
    pin_path = root / "adapter-pin.json"
    if pin_path.exists():
        if HarnessPin.model_validate_json(pin_path.read_bytes()) != pin:
            raise EvaluationContractError("Harness/profile changed; start a new evaluation epoch")
    else:
        if reusable:
            raise EvaluationContractError("Cannot reuse attempts without prior adapter pin")
        with pin_path.open("x", encoding="utf-8") as stream:
            _ = stream.write(pin.model_dump_json(indent=2))
    invocation = uuid4().hex
    metadata = root / f"dispatch-{request.condition}-{invocation}.json"
    with metadata.open("x", encoding="utf-8") as stream:
        _ = stream.write(request.model_dump_json(indent=2))
    selected_backend = backend if backend is not None else CodexBackend()
    by_id = {case.id: case for case in cases}
    completed, reused, inconclusive = 0, 0, 0
    for slot in slots:
        if harness_files() != current_files:
            raise EvaluationContractError("Harness changed during execution; evidence epoch incomplete")
        if slot.id in reusable:
            completed += 1
            reused += 1
            print(f"{slot.id}: completed (retained, NOT resampled)", flush=True)
            continue
        scope = RunScope(slot=slot, snapshot=snapshots[slot.condition], output=root / "runs" / slot.id, profile=profile,
            approval_reference=request.approval_reference, fixture_writes_approved=request.fixture_writes_approved)
        result = run_case(by_id[slot.case_id], scope, selected_backend)
        print(f"{slot.id}: {result.status} / UNREVIEWED" + (f" / {result.reason}" if result.reason else ""), flush=True)
        if result.status == "INCONCLUSIVE":
            inconclusive += 1
            break  # Preserve failure; do not spend on a possibly broken adapter or resample.
        completed += 1
    if harness_files() != current_files:
        raise EvaluationContractError("Harness changed during execution; evidence epoch incomplete")
    summary = BatchResult(status="FINISHED" if completed == len(slots) else "STOPPED", completed=completed,
        reused=reused, inconclusive=inconclusive, remaining=len(slots) - completed - inconclusive, invocation_id=invocation)
    with metadata.with_suffix(".summary.json").open("x", encoding="utf-8") as stream:
        _ = stream.write(summary.model_dump_json(indent=2))
    return summary


class Options(argparse.Namespace):
    # Mutable CLI parse state. Required flags still have to be explicitly supplied.
    manifest: Path = Path(".")
    condition: Literal["baseline", "candidate", "paired"] = "baseline"
    approval_reference: str = ""
    fixture_writes_approved: bool = False
    continue_unstarted: bool = False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    _ = parser.add_argument("--manifest", type=Path, required=True)
    _ = parser.add_argument("--condition", choices=("baseline", "candidate", "paired"), required=True)
    _ = parser.add_argument("--approval-reference", required=True)
    _ = parser.add_argument("--fixture-writes-approved", action="store_true")
    _ = parser.add_argument("--continue-unstarted", action="store_true")
    args = parser.parse_args(namespace=Options())
    request = BatchRequest(manifest=args.manifest, condition=args.condition, approval_reference=args.approval_reference,
        fixture_writes_approved=args.fixture_writes_approved, continue_unstarted=args.continue_unstarted)
    result = dispatch_batch(request)
    print(result.model_dump_json(), flush=True)
    return 0 if result.status == "FINISHED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
