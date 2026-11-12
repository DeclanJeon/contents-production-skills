# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3", "typer"]
# ///
# How to run: python3 scripts/run_writing_evaluation.py --help
"""Offline evaluation planning and reviewed-evidence aggregation; no live CLI."""
from __future__ import annotations

from pathlib import Path
import subprocess
from typing import ClassVar, Literal, Protocol

from pydantic import BaseModel, ConfigDict
import typer

from writing_eval_cases import WritingCase, load_cases
from writing_eval_manifest import EvaluationProfile, RunManifest, RunSlot, build_run_manifest, input_digest
from writing_eval_review import ReviewedRun, RunReceipt, WireEvent, aggregate_results
from writing_eval_snapshot import EvaluationContractError, Snapshot, create_snapshot, verify_snapshot

__all__ = ["EvaluationProfile", "EvaluationContractError", "RunScope", "RunOutcome", "ReviewedRun",
           "build_run_manifest", "create_snapshot", "verify_snapshot", "prepare_dry_run", "run_case", "aggregate_results"]
ROOT = Path(__file__).resolve().parents[1]
app = typer.Typer(no_args_is_help=True)


class RunScope(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    slot: RunSlot
    snapshot: Snapshot
    output: Path
    profile: EvaluationProfile
    approval_reference: str | None = None
    fixture_writes_approved: bool = False


class RunOutcome(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    status: Literal["completed", "INCONCLUSIVE"]
    reason: str | None = None
    trace: tuple[WireEvent, ...] = ()


class EvaluationBackend(Protocol):
    """An explicit caller-owned adapter; this module never selects a live provider."""
    def execute(self, case: WritingCase, scope: RunScope) -> RunOutcome: ...


def prepare_dry_run(source: Path, output: Path, profile: EvaluationProfile | None = None) -> RunManifest:
    """Materialize inputs/snapshot/plan only. No CLI, SDK or subprocess invocation."""
    output.mkdir(parents=True, exist_ok=False)
    cases = load_cases(ROOT / "qa/matt-writing-inputs.json")
    snapshot = create_snapshot(source, output / "snapshots/baseline")
    manifest = build_run_manifest(cases, profile).model_copy(update={"baseline_snapshot": snapshot})
    with (output / "run-manifest.json").open("x", encoding="utf-8") as stream:
        _ = stream.write(manifest.model_dump_json(indent=2))
    return manifest


def run_case(case: WritingCase, scope: RunScope, backend: EvaluationBackend) -> RunOutcome:
    """One authorized attempt only; no retries, no automatic craft verdict."""
    if not scope.approval_reference or not scope.approval_reference.strip():
        raise EvaluationContractError("Explicit evaluation approval reference required")
    if scope.slot.case_id != case.id or scope.slot.input_sha256 != input_digest(case) or scope.slot.kind != case.kind:
        raise EvaluationContractError("Case/slot input mismatch")
    if case.kind == "fixture" and not scope.fixture_writes_approved:
        raise EvaluationContractError("Explicit fixture write permission required")
    _ = verify_snapshot(scope.snapshot)
    target = scope.output.resolve()
    if target.is_relative_to(scope.snapshot.root) or scope.snapshot.root.is_relative_to(target):
        raise EvaluationContractError("Evidence must be outside snapshot")
    target.mkdir(parents=True, exist_ok=False)
    with (target / "attempt-input.json").open("x", encoding="utf-8") as stream:
        _ = stream.write(case.model_dump_json(indent=2))
    try:
        result = backend.execute(case, scope)
    except (TimeoutError, OSError, subprocess.TimeoutExpired) as exc:
        result = RunOutcome(status="INCONCLUSIVE", reason=str(exc))
    source_after = scope.snapshot.sha256
    try:
        _ = verify_snapshot(scope.snapshot)
    except (EvaluationContractError, OSError):
        result = RunOutcome(status="INCONCLUSIVE", reason="snapshot mutated during execution")
        source_after = "UNVERIFIED"
    receipt = RunReceipt(run_id=scope.slot.id, status=result.status, input_sha256=scope.slot.input_sha256,
        source_before=scope.snapshot.sha256, source_after=source_after,
        trace=result.trace, reason=result.reason)
    with (target / "execution.json").open("x", encoding="utf-8") as stream:
        _ = stream.write(receipt.model_dump_json(indent=2))
    return result


class ReviewSuite(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    records: tuple[ReviewedRun, ...]


@app.command("prepare")
def prepare_command(output: Path, source: Path = ROOT, profile: Path | None = None) -> None:
    """Create a dry-run plan. Missing model/budget remains unresolved, never guessed."""
    selected = EvaluationProfile.model_validate_json(profile.read_bytes()) if profile else None
    manifest = prepare_dry_run(source, output, selected)
    typer.echo(f"PLANNED: {len(manifest.runs)} cases / {manifest.response_stages} response stages; live_authorized=false")


@app.command("aggregate")
def aggregate_command(reviews: Path, manifest: Path, output: Path) -> None:
    """Verify review cards against pinned evidence under the review file's folder."""
    cards = ReviewSuite.model_validate_json(reviews.read_bytes())
    plan = RunManifest.model_validate_json(manifest.read_bytes())
    result = aggregate_results(list(cards.records), plan, reviews.parent)
    with output.open("x", encoding="utf-8") as stream:
        _ = stream.write(result.model_dump_json(indent=2))
    typer.echo(result.verdict)


if __name__ == "__main__":
    app()
