"""Explicit document-relative reads preserve the root boundary and real tool evidence."""
from pathlib import Path
import json
import subprocess
import sys
from typing import Literal, assert_never

import pytest

from writing_eval_codex_tools import SourceTools
from writing_eval_snapshot import EvaluationContractError, FilePin, Snapshot
from writing_eval_review import RunReceipt, WireEvent, verify_trace
from writing_eval_manifest import RunSlot

BASE = "first/references/owner.md"
TARGET = "second/references/대상 문서.md"
HREF = "../../second/references/대상%20문서.md#scope"
BODY = "정의입니다.\n두 번째 줄입니다.\n"


@pytest.fixture
def source_tools(tmp_path: Path) -> SourceTools:
    root = tmp_path / "source"
    for name, text in [(BASE, f"[definition]({HREF})\n"), (TARGET, BODY)]:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    return SourceTools(root, tmp_path / "events.jsonl", None)


def test_literal_href_uses_explicit_source_document_not_root_or_skill_folder(source_tools: SourceTools) -> None:
    # The former root join escaped the snapshot. The same href has a safe document base.
    result = source_tools.call("read", {"path": HREF, "relative_to": BASE})
    source_tools.delivered()
    assert result == "정의입니다.\n두 번째 줄입니다.\n"
    events = [json.loads(s) for s in source_tools.events.read_text().splitlines()]
    resolved = next(e for e in events if e["type"] == "reference_resolved")
    assert resolved["path"] == str(source_tools.root / TARGET)
    assert resolved["args"] == {"path": HREF, "relative_to": BASE}
    assert next(e for e in events if e["type"] == "controlled_read")["path"] == str(source_tools.root / TARGET)


def test_relative_range_keeps_same_line_and_unicode_semantics(source_tools: SourceTools) -> None:
    result = source_tools.call("read", {"path": HREF, "relative_to": BASE, "offset": 2, "limit": 1})
    assert result == "두 번째 줄입니다."


def test_fragment_only_reference_reads_the_containing_document(source_tools: SourceTools) -> None:
    result = source_tools.call("read", {"path": "#scope", "relative_to": BASE})
    assert result == f"[definition]({HREF})\n"


def test_root_read_contract_is_not_implicitly_rebased(source_tools: SourceTools) -> None:
    # The resolver must not turn a malformed old root path into a guessed successful read.
    with pytest.raises((EvaluationContractError, FileNotFoundError)):
        source_tools.call("read", {"path": "first/../../second/references/대상 문서.md"})
    assert not any(json.loads(s)["type"] == "controlled_read" for s in source_tools.events.read_text().splitlines())


@pytest.mark.parametrize("href", [
    "../../../outside.md", "%2e%2e/%2e%2e/%2e%2e/outside.md", "/etc/passwd",
    "https://example.org/runtime.md", "file:///etc/passwd", "//server/runtime.md", "C:/secret.md",
    "../../second/references/대상%20문서.md?download=1", "../../qa/rubric.md", "../../tests/test.md",
    "../../support/private.md", "../../.hidden/secret.md", "../../second/script.py",
    "../../second/references/bad%00.md", "..\\..\\outside.md",
])
def test_context_never_authorizes_escape_external_uri_or_excluded_source(source_tools: SourceTools, href: str) -> None:
    (source_tools.root.parent / "outside.md").write_text("private bytes")
    for name in ["qa/rubric.md", "tests/test.md", "support/private.md", ".hidden/secret.md", "second/script.py"]:
        p = source_tools.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("must remain unread")
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": href, "relative_to": BASE})
    assert not any(json.loads(s)["type"] == "controlled_read" for s in source_tools.events.read_text().splitlines())


@pytest.mark.parametrize("base", ["../outside.md", "/etc/passwd", "qa/base.md", "first/.hidden.md"])
def test_source_document_itself_must_obey_the_same_guard(source_tools: SourceTools, base: str) -> None:
    (source_tools.root.parent / "outside.md").write_text("outside base")
    for name in ["qa/base.md", "first/.hidden.md"]:
        p = source_tools.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("excluded base")
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": HREF, "relative_to": base})


def test_context_cannot_traverse_symlink_even_before_parent_segment(source_tools: SourceTools) -> None:
    (source_tools.root / "alias").symlink_to(source_tools.root / "second", target_is_directory=True)
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": "../../alias/../second/references/대상%20문서.md", "relative_to": BASE})
    (source_tools.root / "base-alias.md").symlink_to(source_tools.root / BASE)
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": TARGET, "relative_to": "base-alias.md"})


@pytest.mark.parametrize("tool", ["find", "edit", "write"])
def test_context_field_is_read_only_not_ignored_by_other_operations(source_tools: SourceTools, tool: str) -> None:
    with pytest.raises(EvaluationContractError):
        source_tools.call(tool, {"path": TARGET, "relative_to": BASE, "content": "overwrite"})
    assert (source_tools.root / TARGET).read_text() == BODY


def test_fixture_virtual_path_cannot_be_document_qualified(source_tools: SourceTools) -> None:
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": "fixture/draft.md", "relative_to": BASE})


def test_real_stdio_schema_read_and_denial_include_context(tmp_path: Path, source_tools: SourceTools) -> None:
    script = Path(__file__).with_name("writing_eval_codex_mcp.py")
    requests = [
        {"jsonrpc":"2.0", "id":1, "method":"tools/list"},
        {"jsonrpc":"2.0", "id":2, "method":"tools/call", "params":{"name":"read", "arguments":{"path":HREF, "relative_to":BASE}}},
        {"jsonrpc":"2.0", "id":3, "method":"tools/call", "params":{"name":"read", "arguments":{"path":"../../../outside.md", "relative_to":BASE}}},
    ]
    process = subprocess.run([sys.executable, str(script), str(source_tools.root), str(tmp_path / "wire-events.jsonl")],
        input="".join(json.dumps(r) + "\n" for r in requests), capture_output=True, text=True, timeout=10)
    assert process.returncode == 0, process.stderr
    replies = {r["id"]:r for r in map(json.loads, process.stdout.splitlines())}
    schema = next(t for t in replies[1]["result"]["tools"] if t["name"]=="read")["inputSchema"]
    assert "relative_to" in schema["properties"]
    assert replies[2]["result"]["content"] == [{"type":"text", "text":BODY}]
    assert replies[2]["result"]["isError"] is False and replies[3]["result"]["isError"] is True


def test_receipt_verifier_uses_same_document_relative_address(source_tools: SourceTools) -> None:
    # Construct actual read events and retain the real relative-to argument at the boundary.
    _ = source_tools.call("read", {"path": HREF, "relative_to": BASE})
    source_tools.delivered()
    events = [WireEvent.model_validate_json(s) for s in source_tools.events.read_text().splitlines()]
    events += [WireEvent.model_validate({"type":"message_end", "message":{"role":"assistant", "stopReason":"stop", "content":"actual answer"}}), WireEvent(type="agent_settled")]
    snapshot = Snapshot(root=source_tools.root, sha256="0"*64, files=(FilePin(path=TARGET,sha256="0"*64),))
    slot = RunSlot(id="baseline/T04/r1", case_id="T04", condition="baseline", repeat=1, kind="single", owner=TARGET, stages=1, input_sha256="0"*64)
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256,
        source_before=snapshot.sha256, source_after=snapshot.sha256, trace=tuple(events))
    assert verify_trace(receipt, slot, snapshot)
    serialized = json.loads(receipt.model_dump_json())
    assert serialized["trace"][0]["args"]["relative_to"] == BASE


@pytest.mark.parametrize("corruption", ["missing_physical", "wrong_call", "missing_completion"])
def test_qualified_read_requires_correlated_physical_read_and_completion(source_tools: SourceTools,
    corruption: Literal["missing_physical", "wrong_call", "missing_completion"]) -> None:
    _ = source_tools.call("read", {"path": HREF, "relative_to": BASE})
    source_tools.delivered()
    raw = [json.loads(s) for s in source_tools.events.read_text().splitlines()]
    match corruption:
        case "missing_physical":
            raw = [e for e in raw if e["type"] != "controlled_read"]
        case "wrong_call":
            next(e for e in raw if e["type"] == "controlled_read")["toolCallId"] = "other-call"
        case "missing_completion":
            raw = [e for e in raw if e["type"] != "tool_execution_end"]
        case unreachable:
            assert_never(unreachable)
    events = [WireEvent.model_validate(e) for e in raw]
    events += [WireEvent.model_validate({"type":"message_end", "message":{"role":"assistant", "stopReason":"stop", "content":"claimed answer"}}), WireEvent(type="agent_settled")]
    snapshot = Snapshot(root=source_tools.root, sha256="0"*64, files=(FilePin(path=TARGET,sha256="0"*64),))
    slot = RunSlot(id="baseline/T04/r1", case_id="T04", condition="baseline", repeat=1, kind="single", owner=TARGET, stages=1, input_sha256="0"*64)
    receipt = RunReceipt(run_id=slot.id, status="completed", input_sha256=slot.input_sha256,
        source_before=snapshot.sha256, source_after=snapshot.sha256, trace=tuple(events))
    assert not verify_trace(receipt, slot, snapshot)


@pytest.mark.parametrize("name", ["bad%ZZ.md", "bad%2.md", "bad%.md"])
def test_malformed_percent_escapes_do_not_become_literal_local_filenames(source_tools: SourceTools, name: str) -> None:
    (source_tools.root / "second" / name).write_text("not a valid URI escape")
    with pytest.raises(EvaluationContractError):
        source_tools.call("read", {"path": "../../second/" + name, "relative_to": BASE})


def test_valid_encoded_literal_percent_is_decoded_only_once(source_tools: SourceTools) -> None:
    (source_tools.root / "second/bad%ZZ.md").write_text("literal percent filename")
    result = source_tools.call("read", {"path": "../../second/bad%25ZZ.md", "relative_to": BASE})
    assert result == "literal percent filename"
