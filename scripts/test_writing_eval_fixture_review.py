"""T09 acceptance must require real ordered race evidence and actual final bytes."""
from pathlib import Path
import json

import pytest

from writing_eval_cases import load_cases
from writing_eval_manifest import build_run_manifest
from writing_eval_review import ReviewedRun, RunReceipt, WireEvent, aggregate_results, verify_trace
from writing_eval_snapshot import create_snapshot, digest
from writing_eval_test_support import controlled_fixture_trace


@pytest.fixture
def fixture_run(tmp_path: Path):
    source = tmp_path / "source"
    owner = "video-production-assets/references/03-screenplay.md"
    p = source / owner
    p.parent.mkdir(parents=True)
    p.write_text("local owner")
    (source / "manifest.json").write_text('{"skills":["video-production-assets"]}')
    snapshot = create_snapshot(source, tmp_path / "snapshot")
    cases = load_cases(Path(__file__).resolve().parents[1] / "qa/matt-writing-inputs.json")
    manifest = build_run_manifest(cases, None).model_copy(update={"baseline_snapshot": snapshot})
    slot = next(s for s in manifest.runs if s.condition == "baseline" and s.case_id == "T09")
    folder = tmp_path / "evidence"
    trace = controlled_fixture_trace(snapshot, folder, owner)
    trace += [{"type":"message_end", "message":{"role":"assistant", "stopReason":"stop", "content":"mechanical fixture result"}}, {"type":"agent_settled"}]
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256,
        source_before=snapshot.sha256, source_after=snapshot.sha256, trace=tuple(WireEvent.model_validate(e) for e in trace))
    path = folder / "execution.json"
    path.write_text(receipt.model_dump_json())
    record = ReviewedRun(run_id=slot.id, verdict="PASS", reason="mechanical fixture evidence", evidence_path="evidence/execution.json", evidence_sha256=digest(path.read_bytes()))
    return tmp_path, manifest, slot, receipt, record


def test_fixture_trace_requires_insertion_and_post_insertion_read(fixture_run) -> None:
    # Given: owner/final/settled evidence without the required concurrent-edit sequence.
    _, manifest, slot, receipt, _ = fixture_run
    trace = tuple(e for e in receipt.trace if e.type not in {"user_edit_inserted", "fixture_reread"})
    invalid = receipt.model_copy(update={"trace": trace})
    # When/Then: generic completion is not sufficient for T09.
    assert not verify_trace(invalid, slot, manifest.baseline_snapshot)


@pytest.mark.parametrize("tamper", ["bytes", "missing_file", "symlink", "raw_order", "raw_hash"])
def test_fixture_aggregator_rejects_missing_or_tampered_physical_evidence(fixture_run, tamper: str) -> None:
    # Given: valid mechanical evidence changed independently of its receipt.
    root, manifest, _, _, record = fixture_run
    folder = root / "evidence"
    draft = folder / "fixture/draft.md"
    if tamper == "bytes":
        draft.write_text("B01: lost user edit\nB02: wrong\nB03: changed\n")
    elif tamper == "missing_file":
        draft.unlink()
    elif tamper == "symlink":
        other = root / "outside.md"
        other.write_bytes(draft.read_bytes())
        draft.unlink()
        draft.symlink_to(other)
    else:
        path = folder / "tools.jsonl"
        events = [json.loads(s) for s in path.read_text().splitlines()]
        if tamper == "raw_order":
            events = [e for e in events if e["type"] != "user_edit_inserted"]
        else:
            next(e for e in events if e["type"] == "fixture_written")["sha256"] = "0" * 64
        path.write_text("".join(json.dumps(e) + "\n" for e in events))
    # When: unchanged claimed-PASS review is aggregated.
    result = aggregate_results([record], manifest, root)
    # Then: the physical/ordered evidence, not the assertion, controls validity.
    assert result.invalid_evidence == 1


def test_fixture_aggregator_accepts_complete_mechanical_evidence(fixture_run) -> None:
    # Given: actual controlled read/insertion/re-read/edit and final bytes.
    root, manifest, _, _, record = fixture_run
    # When: the mechanical record is checked.
    result = aggregate_results([record], manifest, root)
    # Then: this one record is valid; missing other cases still prevent suite PASS.
    assert result.invalid_evidence == 0 and result.verdict == "INCONCLUSIVE"


def test_legacy_fixture_projection_keeps_physical_byte_and_order_checks(fixture_run) -> None:
    from writing_eval_review import verify_fixture_files
    root, _, _, receipt, _ = fixture_run
    # Historical normalizers did not retain page annotations in the receipt.
    legacy = tuple(e.model_copy(update={"offset":None, "returned_lines":None, "content_sha256":None}) for e in receipt.trace)
    assert verify_fixture_files(root / "evidence", legacy)
    (root / "evidence/fixture/draft.md").write_text("lost user edit")
    assert not verify_fixture_files(root / "evidence", legacy)
