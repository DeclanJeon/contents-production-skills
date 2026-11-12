"""Drive the actual local MCP stdio boundary without an LLM."""
import json
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).with_name("writing_eval_codex_mcp.py")


def test_stdio_serves_sources_and_refuses_outside_reads(tmp_path: Path) -> None:
    # Given: an isolated source and standard MCP requests.
    root = tmp_path / "source"
    root.mkdir()
    (root / "SKILL.md").write_text("pinned content")
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read", "arguments": {"path": "SKILL.md"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "read", "arguments": {"path": "/etc/passwd"}}},
    ]
    # When: the real stdio server processes them.
    process = subprocess.run([sys.executable, str(SCRIPT), str(root), str(tmp_path / "events.jsonl")],
        input="".join(json.dumps(r) + "\n" for r in requests), capture_output=True, text=True, timeout=10)
    # Then: protocol/results/denial are observable at the wire, with no write capability.
    assert process.returncode == 0, process.stderr
    replies = {r["id"]: r for r in map(json.loads, process.stdout.splitlines())}
    assert replies[1]["result"]["protocolVersion"] == "2025-11-25"
    assert [t["name"] for t in replies[2]["result"]["tools"]] == ["read", "find"]
    assert replies[3]["result"]["content"] == [{"type": "text", "text": "pinned content"}]
    assert replies[4]["result"]["isError"] is True


def test_stdio_fixture_events_preserve_read_completion_order(tmp_path: Path) -> None:
    # Given: three sequential calls: initial read, fresh read, then local edit.
    root = tmp_path / "source"
    root.mkdir()
    calls = [("read", {"path": "fixture/draft.md"}), ("read", {"path": "fixture/draft.md"}),
        ("edit", {"path": "fixture/draft.md", "oldText": "B02: 루마를 봅니다.", "newText": "B02: 옷의 전체 윤곽을 봅니다."})]
    wire = "".join(json.dumps({"jsonrpc": "2.0", "id": n, "method": "tools/call", "params": {"name": name, "arguments": args}}) + "\n"
        for n, (name, args) in enumerate(calls, 1))
    # When: results cross the actual stdio transport.
    process = subprocess.run([sys.executable, str(SCRIPT), str(root), str(tmp_path / "events.jsonl"), str(tmp_path / "fixture")],
        input=wire, capture_output=True, text=True, timeout=10)
    # Then: the old bytes were delivered before insertion and the final bytes are preserved.
    assert process.returncode == 0, process.stderr
    replies = list(map(json.loads, process.stdout.splitlines()))
    assert replies[0]["result"]["content"][0]["text"].startswith("B01: 처음 문장입니다.")
    assert replies[1]["result"]["content"][0]["text"].startswith("B01: 사용자 수정 문장입니다.")
    assert (tmp_path / "fixture/draft.md").read_text() == "B01: 사용자 수정 문장입니다.\nB02: 옷의 전체 윤곽을 봅니다.\nB03: 끝 문장입니다.\n"
    events = [json.loads(s)["type"] for s in (tmp_path / "events.jsonl").read_text().splitlines()]
    assert events.index("tool_execution_end") < events.index("user_edit_inserted") < events.index("fixture_reread") < events.index("fixture_written")
