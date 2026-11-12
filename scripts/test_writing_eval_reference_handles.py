"""References are selected from validated source metadata, never reconstructed by the model."""
from pathlib import Path
import json
import subprocess
import sys

import pytest

from writing_eval_codex_tools import SourceTools
from writing_eval_snapshot import EvaluationContractError, Snapshot, FilePin
from writing_eval_review import WireEvent, RunReceipt, verify_trace
from writing_eval_manifest import RunSlot

BASE = "one/references/owner.md"
TARGET = "two/references/link guide.md"
INLINE = "one/assets/inline.md"


@pytest.fixture
def reader(tmp_path: Path) -> SourceTools:
    root = tmp_path / "source"
    content = "[linked](../../two/references/link%20guide.md#scope)\nUse `assets/inline.md`.\n"
    for name, text in [(BASE, content), (TARGET, "linked bytes\nsecond line\n"), (INLINE, "inline bytes\n")]:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return SourceTools(root, tmp_path / "events.jsonl", None)


def test_reference_menu_distinguishes_actual_href_and_skill_relative_inline(reader: SourceTools) -> None:
    raw = reader.call("read", {"path": BASE})
    reader.delivered()
    assert raw == "[linked](../../two/references/link%20guide.md#scope)\nUse `assets/inline.md`.\n"
    assert {r.target for r in reader.last_references} == {TARGET, INLINE}
    for ref in tuple(reader.last_references):
        text = reader.call("read_reference", {"reference_id": ref.reference_id})
        reader.delivered()
        assert text == ("linked bytes\nsecond line\n" if ref.target == TARGET else "inline bytes\n")


def test_one_read_tool_accepts_root_file_then_offered_handle(reader: SourceTools) -> None:
    # The initial owner filename and later offered handle share one callable tool.
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    ref = next(r for r in reader.last_references if r.target == TARGET)
    assert reader.call("read", {"path": ref.reference_id}) == "linked bytes\nsecond line\n"


def test_reference_survives_mcp_restart_within_same_case(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    ref = next(r for r in reader.last_references if r.target == TARGET)
    resumed = SourceTools(reader.root, reader.events, None)
    assert resumed.call("read", {"path":ref.reference_id}) == "linked bytes\nsecond line\n"


def test_restart_does_not_restore_an_undelivered_page(reader: SourceTools) -> None:
    _ = reader.call("read", {"path":BASE})
    ref = reader.last_references[0]
    resumed = SourceTools(reader.root, reader.events, None)
    with pytest.raises(EvaluationContractError):
        resumed.call("read", {"path":ref.reference_id})


def test_restart_rejects_changed_source_page(reader: SourceTools) -> None:
    _ = reader.call("read", {"path":BASE})
    reader.delivered()
    (reader.root / BASE).write_text("source changed after its delivered read")
    with pytest.raises(EvaluationContractError):
        SourceTools(reader.root, reader.events, None)


def test_reference_log_from_other_snapshot_does_not_grant_handles(tmp_path: Path, reader: SourceTools) -> None:
    _ = reader.call("read", {"path":BASE})
    reader.delivered()
    ref = reader.last_references[0]
    other = tmp_path / "other-root"
    other.mkdir()
    resumed = SourceTools(other, reader.events, None)
    with pytest.raises(EvaluationContractError):
        resumed.call("read", {"path":ref.reference_id})


def test_reference_range_is_the_existing_exact_read_range(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    ref = next(r for r in reader.last_references if r.target == TARGET)
    text = reader.call("read_reference", {"reference_id": ref.reference_id, "offset": 2, "limit": 1})
    assert text == "second line"


def test_reference_catalogue_does_not_read_or_offer_external_excluded_or_escaping_targets(reader: SourceTools) -> None:
    for name in ["qa/private.md", ".hidden/private.md"]:
        p = reader.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("private")
    (reader.root.parent / "outside.md").write_text("private outside")
    (reader.root / BASE).write_text("[outside](../../../outside.md) [qa](../../qa/private.md) [web](https://example.com/private.md) [hidden](../../.hidden/private.md) [missing](missing.md)")
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    assert reader.last_references == ()
    events = [json.loads(s) for s in reader.events.read_text().splitlines()]
    assert [e["path"] for e in events if e["type"] == "controlled_read"] == [str(reader.root / BASE)]


def test_unknown_or_unoffered_reference_id_is_an_error(reader: SourceTools) -> None:
    with pytest.raises(EvaluationContractError):
        reader.call("read_reference", {"reference_id": "invented"})


def test_reference_target_revalidates_symlink_guard_at_use(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    ref = next(r for r in reader.last_references if r.target == TARGET)
    p = reader.root / TARGET
    p.unlink()
    outside = reader.root.parent / "outside.md"
    outside.write_text("outside")
    p.symlink_to(outside)
    with pytest.raises(EvaluationContractError):
        reader.call("read_reference", {"reference_id": ref.reference_id})


def test_unreturned_page_does_not_offer_its_links(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE, "offset": 2, "limit": 1})
    reader.delivered()
    assert {r.target for r in reader.last_references} == {INLINE}


def test_stdio_keeps_source_as_first_content_and_offers_executable_reference_metadata(tmp_path: Path, reader: SourceTools) -> None:
    script = Path(__file__).with_name("writing_eval_codex_mcp.py")
    with subprocess.Popen([sys.executable, str(script), str(reader.root), str(tmp_path / "wire.jsonl")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        assert process.stdin is not None and process.stdout is not None
        process.stdin.write(json.dumps({"jsonrpc":"2.0", "id":1, "method":"tools/call", "params":{"name":"read", "arguments":{"path":BASE}}}) + "\n")
        process.stdin.flush()
        first = json.loads(process.stdout.readline())["result"]
        assert first["content"][0]["text"] == (reader.root / BASE).read_text()
        menu = json.loads(first["content"][1]["text"])["references"]
        ref = next(r for r in menu if r["target"] == TARGET)
        rest, error = process.communicate(json.dumps({"jsonrpc":"2.0", "id":2, "method":"tools/call", "params":{"name":"read", "arguments":{"path":ref["reference_id"]}}}) + "\n", timeout=10)
    assert process.returncode == 0, error
    assert json.loads(rest)["result"]["content"][0]["text"] == "linked bytes\nsecond line\n"


def test_reference_receipt_requires_selection_physical_read_and_completion(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    ref = next(r for r in reader.last_references if r.target == TARGET)
    _ = reader.call("read", {"path": ref.reference_id})
    reader.delivered()
    events = tuple(WireEvent.model_validate_json(s) for s in reader.events.read_text().splitlines())
    finish = (WireEvent.model_validate({"type":"message_end", "message":{"role":"assistant", "stopReason":"stop", "content":"actual"}}), WireEvent(type="agent_settled"))
    snapshot = Snapshot(root=reader.root, sha256="0"*64, files=(FilePin(path=TARGET, sha256="0"*64),))
    slot = RunSlot(id="baseline/T04/r1", case_id="T04", condition="baseline", repeat=1, kind="single", owner=TARGET, stages=1, input_sha256="0"*64)
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256, source_before=snapshot.sha256, source_after=snapshot.sha256, trace=events + finish)
    assert verify_trace(receipt, slot, snapshot)
    bad = receipt.model_copy(update={"trace":tuple(e for e in receipt.trace if e.type != "reference_selected")})
    assert not verify_trace(bad, slot, snapshot)
    # A physical read before selecting its handle is not the promised ordered proof.
    physical_first = list(receipt.trace)
    selection = next(i for i,e in enumerate(physical_first) if e.type == "reference_selected")
    physical = next(i for i,e in enumerate(physical_first) if e.type == "controlled_read" and e.path == str(reader.root / TARGET))
    physical_first[selection], physical_first[physical] = physical_first[physical], physical_first[selection]
    assert not verify_trace(receipt.model_copy(update={"trace":tuple(physical_first)}), slot, snapshot)
    # References from an undelivered source cannot be selected early either.
    late_completion = list(receipt.trace)
    root_end = next(i for i,e in enumerate(late_completion) if e.type == "tool_execution_end" and e.toolName == "read")
    completed = late_completion.pop(root_end)
    late_completion.insert(len(late_completion) - 2, completed)
    assert not verify_trace(receipt.model_copy(update={"trace":tuple(late_completion)}), slot, snapshot)
    # An orphan controlled_read is not an actual successful tool call.
    orphan = (WireEvent(type="controlled_read", path=str(reader.root / TARGET)),) + finish
    assert not verify_trace(receipt.model_copy(update={"trace":orphan}), slot, snapshot)


def test_reference_registry_requires_successful_source_delivery(reader: SourceTools) -> None:
    _ = reader.call("read", {"path": BASE})
    ref = reader.last_references[0]
    with pytest.raises(EvaluationContractError):
        reader.call("read_reference", {"reference_id": ref.reference_id})


@pytest.mark.parametrize("name", ["__pycache__/private.md", "node_modules/private.md", "one/references/test_private.md"])
def test_snapshot_excluded_files_cannot_be_read_or_offered(reader: SourceTools, name: str) -> None:
    path = reader.root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("snapshot excluded")
    with pytest.raises(EvaluationContractError):
        reader.call("read", {"path": name})
    (reader.root / BASE).write_text("[excluded](../../" + name + ")")
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    assert reader.last_references == ()


def test_find_skips_all_snapshot_exclusions_instead_of_failing_the_lookup(reader: SourceTools) -> None:
    for name in ["__pycache__/private.md", "node_modules/private.md", "one/test_private.md"]:
        path = reader.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("excluded")
    assert reader.call("find", {"path": "private"}) == "No matching runtime Markdown paths"


@pytest.mark.parametrize("destination", [
    '../../two/references/link%20guide.md "optional title"',
    '<../../two/references/link%20guide.md>',
    '../../two/references/guide(v1).md',
])
def test_common_markdown_destinations_offer_handles(reader: SourceTools, destination: str) -> None:
    (reader.root / "two/references/guide(v1).md").write_text("parenthesis target")
    (reader.root / BASE).write_text("[guide](" + destination + ")")
    _ = reader.call("read", {"path": BASE})
    reader.delivered()
    assert len(reader.last_references) == 1
    selected = reader.call("read_reference", {"reference_id": reader.last_references[0].reference_id})
    assert selected in {"linked bytes\nsecond line\n", "parenthesis target"}


@pytest.mark.parametrize("target", ["two/references/unlinked.md", INLINE])
def test_receipt_offer_must_come_from_actual_returned_page(reader: SourceTools, target: str) -> None:
    # Root read only returns the first line; INLINE is on the unreturned second line.
    (reader.root / "two/references/unlinked.md").write_text("not referenced anywhere")
    _ = reader.call("read", {"path": BASE, "limit": 1})
    reader.delivered()
    _ = reader.call("read", {"path": target})
    reader.delivered()
    raw = [json.loads(s) for s in reader.events.read_text().splitlines()]
    first = next(e["toolCallId"] for e in raw if e["type"] == "tool_execution_start")
    second = next(e["toolCallId"] for e in raw if e["type"] == "tool_execution_start" and e["toolCallId"] != first)
    forged = "ref_" + "f"*24
    start = next(i for i,e in enumerate(raw) if e["type"] == "tool_execution_start" and e["toolCallId"] == second)
    raw[start]["toolName"] = "read_reference"
    raw[start]["args"] = {"reference_id":forged}
    raw.insert(start + 1, {"type":"reference_selected", "toolCallId":second, "path":str(reader.root / target), "args":{"path":target, "reference_id":forged}})
    next(e for e in raw if e["type"] == "tool_execution_end" and e["toolCallId"] == second)["toolName"] = "read_reference"
    insertion = next(i for i,e in enumerate(raw) if e["type"] == "tool_execution_end" and e["toolCallId"] == first)
    raw.insert(insertion, {"type":"reference_offered", "toolCallId":first, "path":str(reader.root / target), "args":{"path":target,"relative_to":BASE,"reference_id":forged}})
    events = tuple(WireEvent.model_validate(e) for e in raw) + (WireEvent.model_validate({"type":"message_end", "message":{"role":"assistant", "stopReason":"stop", "content":"claimed"}}), WireEvent(type="agent_settled"))
    snapshot = Snapshot(root=reader.root, sha256="0"*64, files=(FilePin(path=target, sha256="0"*64),))
    slot = RunSlot(id="baseline/T04/r1", case_id="T04", condition="baseline", repeat=1, kind="single", owner=target, stages=1, input_sha256="0"*64)
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256, source_before=snapshot.sha256, source_after=snapshot.sha256, trace=events)
    assert not verify_trace(receipt, slot, snapshot)
