"""Live dispatch must reject incomplete permissions before any backend call."""
from pathlib import Path
import json
import sys
from typing import Literal, assert_never

import pytest

from run_writing_eval_codex import BatchRequest, dispatch_batch
from run_writing_evaluation import prepare_dry_run, RunOutcome, RunScope
from writing_eval_cases import WritingCase, load_cases
from writing_eval_review import WireEvent, WireMessage
from writing_eval_snapshot import create_snapshot
from writing_eval_manifest import EvaluationProfile
from writing_eval_snapshot import EvaluationContractError


@pytest.fixture
def planned(tmp_path: Path) -> Path:
    # A minimal real runtime package is sufficient for dispatch preflight.
    source = tmp_path / "source"
    (source / "video-production-assets").mkdir(parents=True)
    (source / "manifest.json").write_text('{"skills":["video-production-assets"]}')
    (source / "video-production-assets/SKILL.md").write_text("offline fixture")
    profile = EvaluationProfile(executable="codex", provider="openai", model="gpt-6-luna", thinking="low", timeout_seconds=240,
        max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    output = tmp_path / "evaluation"
    _ = prepare_dry_run(source, output, profile)
    return output


class ForbiddenBackend:
    def execute(self, _case: WritingCase, _scope: RunScope) -> RunOutcome:
        raise AssertionError("Preflight must not invoke backend")


def test_fixture_permission_is_checked_before_first_case(planned: Path) -> None:
    # Given: all 70 baseline slots, but no fixture write permission.
    request = BatchRequest(manifest=planned / "run-manifest.json", condition="baseline", approval_reference="approved")
    # When/Then: the entire dispatch is denied before the first ordinary case too.
    with pytest.raises(EvaluationContractError, match="fixture"):
        dispatch_batch(request, ForbiddenBackend())
    assert not (planned / "runs").exists()


def test_missing_approval_cannot_dispatch(planned: Path) -> None:
    # Given: explicit fixture permission but a blank evaluation approval.
    request = BatchRequest(manifest=planned / "run-manifest.json", condition="baseline", approval_reference=" ", fixture_writes_approved=True)
    # When/Then: no backend can be called.
    with pytest.raises(EvaluationContractError, match="approval"):
        dispatch_batch(request, ForbiddenBackend())


def test_paired_mode_requires_both_snapshots_before_any_dispatch(planned: Path) -> None:
    # Given: a requested balanced comparison but no candidate yet.
    request = BatchRequest(manifest=planned / "run-manifest.json", condition="paired", approval_reference="approved", fixture_writes_approved=True)
    # When/Then: no source substitution or partial baseline-only execution occurs.
    with pytest.raises(EvaluationContractError, match="snapshot"):
        dispatch_batch(request, ForbiddenBackend())


def test_missing_candidate_cannot_dispatch(planned: Path) -> None:
    # Given: a baseline-only manifest.
    request = BatchRequest(manifest=planned / "run-manifest.json", condition="candidate", approval_reference="approved", fixture_writes_approved=True)
    # When/Then: no implicit candidate snapshot or source substitution occurs.
    with pytest.raises(EvaluationContractError, match="snapshot"):
        dispatch_batch(request, ForbiddenBackend())


class RoutingBackend:
    """Local source-reader double; no model/fixture-quality certification."""
    def execute(self, case: WritingCase, scope: RunScope) -> RunOutcome:
        text = (scope.snapshot.root / case.owner).read_text()
        trace = [WireEvent(type="controlled_read", path=str(scope.snapshot.root / case.owner))]
        for _ in case.turns:
            trace.extend([WireEvent(type="message_end", message=WireMessage(role="assistant", stopReason="stop", content=text)),
                WireEvent(type="agent_settled", aborted=False)])
        return RunOutcome(status="completed", trace=tuple(trace))


def test_paired_dispatch_uses_each_slots_snapshot_and_balanced_order(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # Given: distinct baseline/candidate bytes, a fake local version-only CLI, and the real controller/API.
    root = Path(__file__).resolve().parents[1]
    cases = load_cases(root / "qa/matt-writing-inputs.json")
    source = tmp_path / "source"
    source.mkdir()
    names = sorted({c.owner.split("/")[0] for c in cases})
    (source / "manifest.json").write_text(json.dumps({"skills": names}))
    for case in cases:
        p = source / case.owner
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("BASELINE")
    executable = tmp_path / "codex-offline"
    executable.write_text(f"#!{sys.executable}\nprint('codex-cli offline-test')\n")
    executable.chmod(0o755)
    profile = EvaluationProfile(executable=str(executable), provider="openai", model="gpt-6-luna", thinking="low", timeout_seconds=240,
        max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    output = tmp_path / "evaluation"
    manifest = prepare_dry_run(source, output, profile)
    for case in cases:
        (source / case.owner).write_text("CANDIDATE")
    candidate = create_snapshot(source, output / "snapshots/candidate")
    manifest = manifest.model_copy(update={"candidate_snapshot": candidate})
    selected = output / "comparison-manifest.json"
    selected.write_text(manifest.model_dump_json())
    request = BatchRequest(manifest=selected, condition="paired", approval_reference="offline test only", fixture_writes_approved=True)
    # When: the controller dispatches the fixed 140-slot matrix to a local routing double.
    result = dispatch_batch(request, RoutingBackend())
    # Then: order alternates as planned and every receipt reflects the right physical source bytes.
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("baseline/T01/r1:") and lines[1].startswith("candidate/T01/r1:")
    assert lines[28].startswith("candidate/T01/r2:") and lines[29].startswith("baseline/T01/r2:")
    assert result.completed == 140 and result.status == "FINISHED"
    for slot in manifest.runs:
        receipt = json.loads((output / "runs" / slot.id / "execution.json").read_bytes())
        expected = "BASELINE" if slot.condition == "baseline" else "CANDIDATE"
        final = next(e["message"]["content"] for e in receipt["trace"] if e["type"] == "message_end")
        assert final == expected


def test_existing_attempt_is_never_overwritten_or_resampled(planned: Path) -> None:
    # Given: an interrupted attempt with already-captured wire bytes.
    attempt = planned / "runs/baseline/T01/r1"
    attempt.mkdir(parents=True)
    capture = attempt / "turn-1.stdout.jsonl"
    capture.write_text("preserve interrupted evidence")
    request = BatchRequest(manifest=planned / "run-manifest.json", condition="baseline", approval_reference="approved", fixture_writes_approved=True)
    # When/Then: dispatch does not make new calls before finding the collision.
    with pytest.raises(EvaluationContractError, match="(?i)existing"):
        dispatch_batch(request, ForbiddenBackend())
    assert capture.read_text() == "preserve interrupted evidence"


@pytest.mark.parametrize("tamper", ["bytes", "missing_log", "event_hash"])
def test_resume_rejects_corrupt_physical_fixture_before_any_new_call(tmp_path: Path, tamper: Literal["bytes", "missing_log", "event_hash"]) -> None:
    from run_writing_eval_codex import HarnessPin, harness_files
    from writing_eval_review import RunReceipt
    from writing_eval_snapshot import digest
    from writing_eval_test_support import controlled_fixture_trace

    # Given: a completed, ordered T09 receipt with real controlled fixture files.
    cases = load_cases(Path(__file__).resolve().parents[1] / "qa/matt-writing-inputs.json")
    source = tmp_path / "source"
    source.mkdir()
    names = sorted({c.owner.split("/")[0] for c in cases})
    (source / "manifest.json").write_text(json.dumps({"skills": names}))
    for case in cases:
        owner = source / case.owner
        owner.parent.mkdir(parents=True, exist_ok=True)
        owner.write_text("mechanical source")
    executable = tmp_path / "codex-offline"
    executable.write_text(f"#!{sys.executable}\nprint('codex-cli offline-test')\n")
    executable.chmod(0o755)
    profile = EvaluationProfile(executable=str(executable), provider="openai", model="gpt-6-luna", thinking="low", timeout_seconds=240,
        max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    output = tmp_path / "evaluation"
    manifest = prepare_dry_run(source, output, profile)
    snapshot = manifest.baseline_snapshot
    assert snapshot is not None
    slot = next(s for s in manifest.runs if s.condition == "baseline" and s.case_id == "T09")
    folder = output / "runs" / slot.id
    events = controlled_fixture_trace(snapshot, folder, slot.owner)
    trace = tuple(WireEvent.model_validate(e) for e in events) + (
        WireEvent(type="message_end", message=WireMessage(role="assistant", stopReason="stop", content="mechanical fixture")),
        WireEvent(type="agent_settled", aborted=False),)
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256,
        source_before=snapshot.sha256, source_after=snapshot.sha256, trace=trace)
    (folder / "execution.json").write_text(receipt.model_dump_json())
    pin = HarnessPin(files=harness_files(), executable=str(executable), cli_version="codex-cli offline-test",
        profile_sha256=digest(profile.model_dump_json().encode()))
    (output / "adapter-pin.json").write_text(pin.model_dump_json())
    match tamper:
        case "bytes":
            (folder / "fixture/draft.md").write_text("lost user edit")
        case "missing_log":
            (folder / "tools.jsonl").unlink()
        case "event_hash":
            raw = [json.loads(line) for line in (folder / "tools.jsonl").read_text().splitlines()]
            next(e for e in raw if e["type"] == "fixture_written")["sha256"] = "0" * 64
            (folder / "tools.jsonl").write_text("".join(json.dumps(e) + "\n" for e in raw))
        case unreachable:
            assert_never(unreachable)
    request = BatchRequest(manifest=output / "run-manifest.json", condition="baseline", approval_reference="offline resume regression",
        fixture_writes_approved=True, continue_unstarted=True)
    # When/Then: reject invalid prior evidence before dispatching even the first unstarted slot.
    with pytest.raises(EvaluationContractError, match="(?i)fixture"):
        dispatch_batch(request, ForbiddenBackend())
    assert not (output / "runs/baseline/T01/r1").exists()
