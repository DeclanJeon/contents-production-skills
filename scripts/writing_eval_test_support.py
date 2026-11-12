"""Mechanical test evidence only; never simulates a model quality verdict."""
from pathlib import Path
import json
from pydantic import JsonValue

from writing_eval_codex_tools import SourceTools
from writing_eval_snapshot import Snapshot


def controlled_fixture_trace(snapshot: Snapshot, folder: Path, owner: str) -> list[dict[str, JsonValue]]:
    folder.mkdir(parents=True, exist_ok=True)
    tools = SourceTools(snapshot.root, folder / "tools.jsonl", folder / "fixture")
    _ = tools.call("read", {"path": owner})
    tools.delivered()
    _ = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    _ = tools.call("read", {"path": "fixture/draft.md"})
    tools.delivered()
    _ = tools.call("edit", {"path": "fixture/draft.md", "oldText": "B02: 루마를 봅니다.", "newText": "B02: 옷의 전체 윤곽을 봅니다."})
    tools.delivered()
    return [json.loads(line) for line in (folder / "tools.jsonl").read_text().splitlines()]
