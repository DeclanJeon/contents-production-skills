"""Exercise real RPC pipes with a local fake peer, never a provider."""
from __future__ import annotations

import importlib
import json
import os
from pathlib import Path

import pytest

from writing_eval_cases import load_cases

ROOT = Path(__file__).resolve().parents[1]


def peer(tmp_path: Path, mode: str = "normal") -> Path:
    executable = tmp_path / "fake-pi"
    executable.write_text("#!/usr/bin/env python3\n" + '''
import json, os, sys, time
from pathlib import Path
Path(__file__).with_suffix('.pid').write_text(str(os.getpid()))
history = []
mode = MODE
for line in sys.stdin.buffer:
    command = json.loads(line)
    name = command['type']
    data = {'disposition': 'handled' if mode == 'handled' else 'started'} if name == 'prompt' else {}
    print(json.dumps({'type':'response','command':name,'id':command['id'],'success':True,'data':data}), flush=True)
    if name != 'prompt': continue
    history.append(command['message'])
    print(json.dumps({'type':'tool_execution_start','toolCallId':'owner','toolName':'read','args':{'path':'orchestrating-video-preproduction/references/video-direction.md'}}), flush=True)
    print(json.dumps({'type':'tool_execution_end','toolCallId':'owner','toolName':'read','isError':False}), flush=True)
    print(json.dumps({'type':'message_end','message':{'role':'assistant','stopReason':'stop','content':[{'type':'text','text':42 if mode == 'bad_message' else json.dumps({'pid':os.getpid(),'history':history,'marker':'a\u2028b\u2029c'},ensure_ascii=False)}]}},ensure_ascii=False), flush=True)
    print(json.dumps({'type':'agent_end','willRetry':False}), flush=True)
    if mode == 'ack_only': time.sleep(10)
    if mode == 'handled': continue
    if mode == 'delay':
        import select
        if select.select([sys.stdin], [], [], 0.15)[0]:
            print('next prompt arrived before settled', file=sys.stderr, flush=True)
            sys.exit(9)
    print(json.dumps({'type':'agent_settled','aborted':mode == 'aborted'}), flush=True)
'''.replace("MODE", repr(mode)), encoding="utf-8")
    executable.chmod(0o700)
    return executable


def execute(tmp_path: Path, executable: Path, output_name: str = "run"):
    api = importlib.import_module("writing_eval_rpc")
    case = next(c for c in load_cases(ROOT / "qa/matt-writing-inputs.json") if c.id == "T11")
    source = tmp_path / "source"
    owner = source / case.owner
    owner.parent.mkdir(parents=True, exist_ok=True)
    owner.write_text("owner", encoding="utf-8")
    (source / "manifest.json").write_text(json.dumps({"skills": ["orchestrating-video-preproduction"]}), encoding="utf-8")
    profile = api.RpcProfile(executable=str(executable), provider="test", model="offline-fake", thinking="low", timeout_seconds=1)
    return api.run_conversation(case, api.RpcWorkspace(root=source, output=tmp_path / output_name), profile)


def test_same_child_keeps_history_and_never_prompts_before_settled(tmp_path: Path) -> None:
    result = execute(tmp_path, peer(tmp_path, "delay"))
    assert result["status"] == "completed"
    assert result["verdict"] == "UNREVIEWED"
    records = [json.loads((tmp_path / "run" / f"turn-{n}.attempt.json").read_text()) for n in (1, 2)]
    responses = [json.loads(r["trace"]["final_text"]) for r in records]
    assert responses[0]["pid"] == responses[1]["pid"]
    assert len(responses[0]["history"]) == 1
    assert len(responses[1]["history"]) == 2
    assert responses[1]["history"][1] == "초보 대상입니다. 이제 이 자료로 원고를 완성해 주세요. CTA는 없습니다."
    assert records[0]["prompt"] == responses[0]["history"][0]
    assert records[0]["trace"]["settled"] is True
    assert responses[1]["marker"] == "a\u2028b\u2029c"
    assert records[1]["trace"]["protocol_errors"] == []


def test_separate_repeats_have_new_process_and_empty_history(tmp_path: Path) -> None:
    executable = peer(tmp_path)
    execute(tmp_path, executable, "one")
    execute(tmp_path, executable, "two")
    responses = [json.loads(json.loads((tmp_path / name / "turn-1.attempt.json").read_text())["trace"]["final_text"]) for name in ("one", "two")]
    assert responses[0]["pid"] != responses[1]["pid"]
    assert all(len(r["history"]) == 1 for r in responses)


@pytest.mark.parametrize("mode", ["ack_only", "handled", "aborted", "bad_message"])
def test_incomplete_protocol_stops_later_turns_and_preserves_output(tmp_path: Path, mode: str) -> None:
    result = execute(tmp_path, peer(tmp_path, mode))
    assert result["status"] == "INCONCLUSIVE"
    assert (tmp_path / "run/turn-1.stdout.jsonl").is_file()
    assert not (tmp_path / "run/turn-2.attempt.json").exists()
    pid = int((tmp_path / "fake-pi.pid").read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


def test_unicode_line_separator_and_output_collision(tmp_path: Path) -> None:
    executable = peer(tmp_path)
    result = execute(tmp_path, executable)
    assert result["status"] == "completed"
    with pytest.raises(FileExistsError):
        execute(tmp_path, executable)
    api = importlib.import_module("writing_eval_rpc")
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="provider"):
        api.RpcProfile(executable=str(executable), provider="", model="offline", thinking="low", timeout_seconds=1)
