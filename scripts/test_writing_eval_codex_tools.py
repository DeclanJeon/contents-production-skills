"""Controlled source/fixture tools: no provider or model dependencies."""
from pathlib import Path
import json

import pytest

from writing_eval_codex_tools import SourceTools, INITIAL, INJECTED, EXPECTED
from writing_eval_snapshot import EvaluationContractError


@pytest.fixture
def tools(tmp_path: Path) -> SourceTools:
    root = tmp_path / "source"
    (root / "owner").mkdir(parents=True)
    (root / "owner/SKILL.md").write_text("local owner\nsecond line\n")
    return SourceTools(root, tmp_path / "events.jsonl", tmp_path / "fixture")


def test_reads_local_source_with_explicit_range(tools: SourceTools) -> None:
    # Given: a local owner with two lines.
    # When: the model requests the second line.
    result = tools.call("read", {"path": "owner/SKILL.md", "offset": 2, "limit": 1})
    # Then: only the selected source content is returned.
    assert result == "second line"


@pytest.mark.parametrize("path", ["../outside.md", "/etc/passwd", "qa/rubric.md", "owner/.hidden.md", "owner/script.py"])
def test_rejects_reads_outside_runtime_markdown(tools: SourceTools, path: str) -> None:
    # Given: a request outside the readable runtime contract.
    # When/Then: it cannot be satisfied.
    with pytest.raises((EvaluationContractError, FileNotFoundError)):
        tools.call("read", {"path": path})


def test_rejects_symlink_even_when_it_targets_runtime_source(tools: SourceTools) -> None:
    # Given: an alias that could hide an escaping file later.
    (tools.root / "alias.md").symlink_to(tools.root / "owner/SKILL.md")
    # When/Then: alias traversal is refused.
    with pytest.raises(EvaluationContractError):
        tools.call("read", {"path": "alias.md"})


def test_inserts_edit_only_after_full_successful_fixture_read(tools: SourceTools) -> None:
    # Given: the literal initial draft and a controlled initial read.
    assert tools.draft is not None
    assert tools.draft.read_text() == INITIAL
    # When: the complete read has been delivered to the caller.
    before = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    # Then: the caller saw old bytes, while the fixture now has the user edit.
    assert before == INITIAL
    assert tools.draft.read_text() == INJECTED


def test_complete_ranged_fixture_read_retains_terminal_newline(tools: SourceTools) -> None:
    # Given: a range that includes every line, including the final newline.
    # When: it is successfully delivered.
    text = tools.call("read", {"path": "fixture/draft.md", "offset": 1, "limit": 2000})
    tools.delivered()
    # Then: the full initial bytes were delivered and insertion follows.
    assert text == "B01: 처음 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n"
    assert tools.draft is not None and tools.draft.read_text().startswith("B01: 사용자 수정 문장입니다.")


def test_resolves_contained_parent_relative_markdown_links(tools: SourceTools) -> None:
    # Given: a normal relative link inside the pinned source tree.
    # When: a caller follows that path without removing its parent segment.
    text = tools.call("read", {"path": "owner/../owner/SKILL.md"})
    # Then: canonical local bytes, not a needless tool error, are returned.
    assert text == "local owner\nsecond line\n"


def test_partial_read_does_not_satisfy_fixture_insertion(tools: SourceTools) -> None:
    # Given: only the first line was requested.
    _ = tools.call("read", {"path": "fixture/draft.md", "limit": 1})
    # When: that partial result is delivered.
    tools.delivered()
    # Then: no full-read event is fabricated.
    assert tools.draft is not None and tools.draft.read_text() == INITIAL


def test_fixture_requires_reread_before_any_write(tools: SourceTools) -> None:
    # Given: an injected edit that the model has not re-read.
    _ = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    # When/Then: stale write is refused.
    with pytest.raises(EvaluationContractError):
        tools.call("edit", {"path": "fixture/draft.md", "oldText": "B02: 루마를 봅니다.", "newText": "B02: 옷의 전체 윤곽을 봅니다."})


def test_local_edit_preserves_injected_and_locked_bytes(tools: SourceTools) -> None:
    # Given: successful initial read, insertion, and delivered re-read.
    _ = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    _ = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    # When: exactly one approved line is replaced.
    _ = tools.call("edit", {"path": "fixture/draft.md", "oldText": "B02: 루마를 봅니다.", "newText": "B02: 옷의 전체 윤곽을 봅니다."})
    # Then: all bytes match the independently specified final draft.
    assert tools.draft is not None and tools.draft.read_text() == EXPECTED


def test_single_adapter_has_no_fixture_permission(tmp_path: Path) -> None:
    # Given: a source-only tool capability.
    root = tmp_path / "source"
    root.mkdir()
    tools = SourceTools(root, tmp_path / "events.jsonl", None)
    # When/Then: it cannot create or write a fixture.
    with pytest.raises(EvaluationContractError):
        tools.call("write", {"path": "fixture/draft.md", "content": "bad"})


def test_rejects_runtime_writes_even_with_fixture_permission(tools: SourceTools) -> None:
    # Given: fixture permission, not package write permission.
    # When/Then: writing an owner is refused.
    with pytest.raises(EvaluationContractError):
        tools.call("write", {"path": "owner/SKILL.md", "content": "bad"})


def test_zero_start_and_large_line_request_read_the_same_local_bytes(tools: SourceTools) -> None:
    # Given: native clients commonly request the whole document from offset zero.
    # When: that compatible range is supplied.
    text = tools.call("read", {"path": "owner/SKILL.md", "offset": 0, "limit": 10000})
    # Then: it denotes the first line, without relaxing path or byte boundaries.
    assert text == "local owner\nsecond line\n"


def test_large_read_returns_bounded_page_and_explicit_next_line(tools: SourceTools) -> None:
    # Given: a legitimate runtime document larger than a single tool payload.
    lines = [f"LINE-{n:04}:" + "x" * 100 for n in range(1000)]
    original = "\n".join(lines) + "\n"
    (tools.root / "owner/large.md").write_text(original)
    # When: the client requests all lines.
    result = tools.call("read", {"path": "owner/large.md", "limit": 10000})
    # Then: a bounded, non-error page points to exactly the next source line.
    page = json.loads(result)
    assert len(result.encode()) <= 50000
    assert page["type"] == "partial_read" and 1 < page["next_offset"] < 1000
    assert page["text"] == "\n".join(lines[:page["next_offset"] - 1])
    assert page["text"].startswith("LINE-0000:")


def test_source_find_lists_only_readable_runtime_markdown(tmp_path: Path) -> None:
    # Given: public runtime and prohibited QA/hidden files with matching names.
    root = tmp_path / "source"
    for name in ["owner/SKILL.md", "qa/owner.md", ".private/owner.md"]:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("source")
    (root / "owner-directory.md").mkdir()
    tools = SourceTools(root, tmp_path / "events.jsonl", None)
    # When: an uncertain path is looked up before reading.
    result = tools.call("find", {"path": "owner"})
    # Then: lookup cannot disclose excluded QA or hidden documents.
    assert result == "owner/SKILL.md"


def test_fixture_cannot_acquire_source_find_capability(tools: SourceTools) -> None:
    # Given: the narrower T09 capability set.
    # When/Then: an undisclosed extra tool cannot be used.
    with pytest.raises(EvaluationContractError):
        tools.call("find", {"path": "owner"})


def test_parent_escape_cannot_read_an_existing_file(tools: SourceTools) -> None:
    # Given: a real outside file, not merely a nonexistent path.
    (tools.root.parent / "outside.md").write_text("private bytes")
    # When/Then: canonical containment prevents reading it.
    with pytest.raises(EvaluationContractError):
        tools.call("read", {"path": "../outside.md"})


def test_find_accepts_explicit_query_and_root_relative_scope(tmp_path: Path) -> None:
    root = tmp_path / "source"
    for name in ["one/A01.md", "two/A01.md", "one/other.md"]:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("runtime")
    lookup = SourceTools(root, tmp_path / "events.jsonl", None)
    assert lookup.call("find", {"query":"A01", "path":"one"}) == "one/A01.md"
    assert lookup.call("find", {"query":"A01"}) == "one/A01.md\ntwo/A01.md"
    assert lookup.call("find", {"path":"A01"}) == "one/A01.md\ntwo/A01.md"


@pytest.mark.parametrize("scope", ["../outside", "/etc", "qa", "node_modules", ".hidden"])
def test_find_query_does_not_widen_source_scope(tmp_path: Path, scope: str) -> None:
    root = tmp_path / "source"
    root.mkdir()
    lookup = SourceTools(root, tmp_path / "events.jsonl", None)
    with pytest.raises(EvaluationContractError):
        lookup.call("find", {"query":"A01", "path":scope})


def test_tool_budget_stops_repeated_requests(tools: SourceTools) -> None:
    # Given: a deliberately small tool-call budget.
    tools.max_calls = 1
    _ = tools.call("read", {"path": "owner/SKILL.md"})
    # When/Then: a second read cannot extend the run indefinitely.
    with pytest.raises(EvaluationContractError):
        tools.call("read", {"path": "owner/SKILL.md"})
