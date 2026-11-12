"""Offline orchestration contracts: no model process may start here."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from writing_eval_cases import load_cases

ROOT = Path(__file__).resolve().parents[1]


def cases():
    return load_cases(ROOT / "qa/matt-writing-inputs.json")


def profile(api):
    return api.EvaluationProfile(executable="pi", provider="test", model="offline-fake", thinking="low", timeout_seconds=2,
        max_case_runs=140, max_provider_calls=1000, max_total_tokens=1000000, max_cost_usd="10", retry_limit=0)


def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    names = {c.owner.split("/")[0] for c in cases()}
    (root / "manifest.json").write_text(json.dumps({"version": "2.33", "skills": sorted(names)}))
    for case in cases():
        p = root / case.owner
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("package owner", encoding="utf-8")
    (root / "qa").mkdir()
    (root / "qa/secret-rubric.json").write_text('{"answer":"must not leak"}')
    return root


def test_null_assistant_content_never_counts_as_a_successful_response() -> None:
    api = importlib.import_module("writing_eval_review")
    message = api.WireMessage.model_validate({"role": "assistant", "stopReason": "stop", "content": None})
    assert message.successful_text() is False


def test_manifest_covers_140_runs_170_stages_and_carries_only_input_hashes() -> None:
    api = importlib.import_module("run_writing_evaluation")
    result = api.build_run_manifest(cases(), profile(api))
    assert len(result.runs) == 140
    assert result.response_stages == 170
    assert len({r.id for r in result.runs}) == 140
    assert [r.condition for r in result.runs[:2]] == ["baseline", "candidate"]
    assert result.runs[0].case_id == "T01"
    assert result.runs[28].condition == "candidate"
    assert all(r.repeat in {1, 2, 3, 4, 5} for r in result.runs)
    assert "criteria" not in result.model_dump_json()
    assert "source/rubric" not in result.model_dump_json()


@pytest.mark.parametrize("field,value", [("provider", ""), ("model", ""), ("max_cost_usd", "0"), ("max_provider_calls", 0), ("max_total_tokens", 0), ("retry_limit", 1)])
def test_profile_rejects_absent_budget_or_implicit_model(field: str, value: str | int) -> None:
    api = importlib.import_module("run_writing_evaluation")
    raw = profile(api).model_dump()
    raw[field] = value
    with pytest.raises(ValidationError):
        api.EvaluationProfile.model_validate(raw)


def test_snapshot_is_payload_only_and_detects_mutation_or_symlink(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    root = source(tmp_path)
    snapshot = api.create_snapshot(root, tmp_path / "snapshot")
    assert not (snapshot.root / "qa").exists()
    assert not (snapshot.root / "scripts").exists()
    assert api.verify_snapshot(snapshot) is True
    p = snapshot.root / "video-production-assets/SKILL.md"
    p.chmod(0o644)
    p.write_text("changed", encoding="utf-8")
    with pytest.raises(api.EvaluationContractError, match="snapshot"):
        api.verify_snapshot(snapshot)
    (root / "video-production-assets/leak.md").symlink_to(root / "qa/secret-rubric.json")
    with pytest.raises(api.EvaluationContractError, match="symlink"):
        api.create_snapshot(root, tmp_path / "bad-snapshot")


def test_manifest_symlink_is_rejected_before_parsing_private_contents(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    root = source(tmp_path)
    (tmp_path / "private.json").write_text('{"credential":"SECRET-SENTINEL"}')
    (root / "manifest.json").unlink()
    (root / "manifest.json").symlink_to(tmp_path / "private.json")
    with pytest.raises(api.EvaluationContractError, match="symlink") as caught:
        api.create_snapshot(root, tmp_path / "snapshot")
    assert "SECRET-SENTINEL" not in str(caught.value)


def test_dry_run_creates_new_manifest_without_starting_subprocess(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    api = importlib.import_module("run_writing_evaluation")
    import subprocess

    def forbidden(*args, **kwargs):
        pytest.fail("dry-run attempted to start a process")

    monkeypatch.setattr(subprocess, "Popen", forbidden)
    root = source(tmp_path)
    output = tmp_path / "dry"
    result = api.prepare_dry_run(root, output, profile(api))
    assert len(result.runs) == 140
    disk = json.loads((output / "run-manifest.json").read_text())
    assert disk["execution_state"] == "PLANNED"
    assert disk["live_authorized"] is False
    assert disk["candidate_snapshot"] is None
    assert not (output / "snapshots/baseline/qa").exists()
    with pytest.raises(FileExistsError):
        api.prepare_dry_run(root, output, profile(api))


def test_live_dispatch_requires_approval_and_preserves_timeout_without_resampling(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    root = source(tmp_path)
    snapshot = api.create_snapshot(root, tmp_path / "snapshot")
    slot = api.build_run_manifest(cases(), profile(api)).runs[0]
    scope = api.RunScope(slot=slot, snapshot=snapshot, output=tmp_path / "attempt", profile=profile(api))
    calls = []

    class Backend:
        def execute(self, case, scope):
            calls.append(case.id)
            raise TimeoutError("timeout")

    with pytest.raises(api.EvaluationContractError, match="approval"):
        api.run_case(cases()[0], scope, Backend())
    assert calls == []
    approved = scope.model_copy(update={"approval_reference": "test-only-authorized-double"})
    result = api.run_case(cases()[0], approved, Backend())
    assert result.status == "INCONCLUSIVE"
    assert calls == ["T01"]
    assert json.loads((scope.output / "execution.json").read_text())["status"] == "INCONCLUSIVE"
    with pytest.raises(FileExistsError):
        api.run_case(cases()[0], approved, Backend())
    assert calls == ["T01"]


def test_fixture_write_permission_is_not_inferred_from_generic_approval(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    root = source(tmp_path)
    snapshot = api.create_snapshot(root, tmp_path / "snapshot")
    case = next(c for c in cases() if c.id == "T09")
    slot = next(s for s in api.build_run_manifest(cases(), profile(api)).runs if s.case_id == "T09")
    scope = api.RunScope(slot=slot, snapshot=snapshot, output=tmp_path / "attempt", profile=profile(api), approval_reference="test")

    class Forbidden:
        def execute(self, case, scope):
            pytest.fail("unapproved fixture backend invoked")

    with pytest.raises(api.EvaluationContractError, match="fixture"):
        api.run_case(case, scope, Forbidden())


def test_unreviewed_or_missing_evidence_cannot_be_aggregated_as_pass(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    manifest = api.build_run_manifest(cases(), profile(api))
    result = api.aggregate_results([], manifest, tmp_path)
    assert result.verdict == "INCONCLUSIVE"
    assert result.missing == 140
    record = api.ReviewedRun(run_id=manifest.runs[0].id, verdict="PASS", reason="looks good",
        evidence_path="missing.json", evidence_sha256="0" * 64)
    result = api.aggregate_results([record], manifest, tmp_path)
    assert result.verdict == "INCONCLUSIVE"
    assert result.invalid_evidence == 1


@pytest.mark.parametrize("tamper", ["sha", "source", "input", "identity", "escape", "unexpected_tool"])
def test_tampered_execution_evidence_is_rejected(tmp_path: Path, tamper: str) -> None:
    api = importlib.import_module("run_writing_evaluation")
    snapshot = api.create_snapshot(source(tmp_path), tmp_path / "snapshot")
    manifest = api.build_run_manifest(cases(), profile(api)).model_copy(update={"baseline_snapshot": snapshot})
    slot = manifest.runs[0]
    data = {"run_id": slot.id, "status": "completed", "input_sha256": slot.input_sha256,
        "source_before": snapshot.sha256, "source_after": snapshot.sha256,
        "trace": [
            {"type": "tool_execution_start", "toolCallId": "read", "toolName": "read", "args": {"path": slot.owner}},
            {"type": "tool_execution_end", "toolCallId": "read", "toolName": "read"},
            {"type": "message_end", "message": {"role": "assistant", "stopReason": "stop", "content": "synthetic"}},
            {"type": "agent_settled"}]}
    if tamper == "source": data["source_after"] = "0" * 64
    if tamper == "input": data["input_sha256"] = "0" * 64
    if tamper == "identity": data["run_id"] = "candidate/T01/r1"
    if tamper == "unexpected_tool": data["trace"].append({"type": "tool_execution_start", "toolName": "bash", "toolCallId": "evil"})
    (tmp_path / "evidence.json").write_text(json.dumps(data))
    pin = hashlib.sha256((tmp_path / "evidence.json").read_bytes()).hexdigest()
    record = api.ReviewedRun(run_id=slot.id, verdict="PASS", reason="synthetic review",
        evidence_path="../evidence.json" if tamper == "escape" else "evidence.json",
        evidence_sha256="0" * 64 if tamper == "sha" else pin)
    result = api.aggregate_results([record], manifest, tmp_path)
    assert result.invalid_evidence == 1
    assert result.verdict == "INCONCLUSIVE"


def test_all_five_passes_are_required_and_one_blocker_overrides_average(tmp_path: Path) -> None:
    api = importlib.import_module("run_writing_evaluation")
    snapshot = api.create_snapshot(source(tmp_path), tmp_path / "snapshot")
    manifest = api.build_run_manifest(cases(), profile(api)).model_copy(update={"baseline_snapshot": snapshot, "candidate_snapshot": snapshot})
    records = []
    for slot in manifest.runs:
        wire = [{"type": "tool_execution_start", "toolCallId": "owner", "toolName": "read", "args": {"path": slot.owner}},
                {"type": "tool_execution_end", "toolCallId": "owner", "toolName": "read", "isError": False},
                {"type": "message_end", "message": {"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "synthetic response for mechanical evidence tests"}]}},
                {"type": "agent_settled", "aborted": False}]
        wire = wire[:2] + wire[2:] * slot.stages
        evidence = {"run_id": slot.id, "status": "completed", "input_sha256": slot.input_sha256,
                    "source_before": snapshot.sha256, "source_after": snapshot.sha256, "trace": wire}
        filename = slot.id.replace("/", "-") + ".json"
        path = tmp_path / filename
        if slot.kind == "fixture":
            from writing_eval_test_support import controlled_fixture_trace
            folder = tmp_path / slot.id
            wire = controlled_fixture_trace(snapshot, folder, slot.owner) + wire[2:]
            evidence["trace"] = wire
            path = folder / "execution.json"
            filename = path.relative_to(tmp_path).as_posix()
        path.write_text(json.dumps(evidence))
        records.append(api.ReviewedRun(run_id=slot.id, verdict="PASS", reason="manual review of synthetic evidence",
            evidence_path=filename, evidence_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    summary = api.aggregate_results(records, manifest, tmp_path)
    assert summary.verdict == "PASS"
    assert summary.improved_cases == ()
    baseline_failure = records.copy()
    baseline_failure[0] = records[0].model_copy(update={"verdict": "FAIL", "reason": "observed baseline defect"})
    fixed = api.aggregate_results(baseline_failure, manifest, tmp_path)
    assert fixed.verdict == "PASS"
    assert fixed.improved_cases == ("T01",)
    multi = next(r for r in records if "/T12/" in r.run_id)
    multi_path = tmp_path / multi.evidence_path
    raw_multi = multi_path.read_bytes()
    partial = json.loads(raw_multi)
    partial["trace"] = partial["trace"][:-2]
    multi_path.write_text(json.dumps(partial))
    partial_records = [r.model_copy(update={"evidence_sha256": hashlib.sha256(multi_path.read_bytes()).hexdigest()}) if r == multi else r for r in records]
    assert api.aggregate_results(partial_records, manifest, tmp_path).verdict == "INCONCLUSIVE"
    multi_path.write_bytes(raw_multi)
    broken = records.copy()
    broken[-1] = records[-1].model_copy(update={"verdict": "FAIL", "blocking": True})
    summary = api.aggregate_results(broken, manifest, tmp_path)
    assert summary.verdict == "FAIL"
    assert summary.blockers == 1
    assert api.aggregate_results(records[:-1], manifest, tmp_path).verdict == "INCONCLUSIVE"
    raw = json.loads((tmp_path / records[0].evidence_path).read_text())
    raw["trace"] = []
    changed = tmp_path / records[0].evidence_path
    changed.write_text(json.dumps(raw))
    records[0] = records[0].model_copy(update={"evidence_sha256": hashlib.sha256(changed.read_bytes()).hexdigest()})
    assert api.aggregate_results(records, manifest, tmp_path).verdict == "INCONCLUSIVE"
