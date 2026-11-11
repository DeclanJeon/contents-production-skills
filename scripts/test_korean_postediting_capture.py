"""Synthetic trace ingestion is not a live model evaluation."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import korean_postediting_capture as cap
import korean_postediting_eval as ev
from test_korean_postediting_eval import batch


def frozen_run(tmp_path):
    run = tmp_path / "frozen"
    run.mkdir()
    files = ev.render_batch(batch(ev.Profile("test-provider", "test-model", "low")))
    for name, content in files.items():
        path = run / name
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_bytes(content.encode())
    return run, json.loads(files["plan.json"])["jobs"][0]


def events(job):
    return [{"type": "message_end", "message": {"role": "user", "content": job["prompt"]}},
            {"type": "message_end", "message": {"role": "assistant", "model": "test-model",
             "provider": "test-provider", "stopReason": "stop",
             "content": [{"type": "text", "text": "합성 응답\u2028둘째 줄"}], "usage": {"input": 10}}},
            {"type": "agent_settled", "aborted": False}]


def input_for(job, stream, exit_code=0):
    wire = b"\n".join(json.dumps(e, ensure_ascii=False).encode() for e in stream) + b"\n"
    return cap.CaptureInput(job["id"], wire, b"synthetic stderr\r\n", exit_code)


def job_with_prompt(run, job):
    return {**job, "prompt": (run / job["prompt_path"]).read_text(encoding="utf-8")}


def test_collect_complete_keeps_unreviewed(tmp_path):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    captured = cap.collect_capture(run, input_for(job, events(job)))
    attempt = json.loads(captured["attempt.json"])
    assert attempt["status"] == "completed"
    assert attempt["verdict"] == "UNREVIEWED" and attempt["default_application"] == "held"
    assert attempt["job_id"] == job["id"]
    assert attempt["trace"]["usage_per_assistant_message"] == [{"input": 10}]


@pytest.mark.parametrize("mutation", ["model", "provider", "prompt"])
def test_rejects_wrong_model_provider_or_prompt(tmp_path, mutation):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    stream = events(job)
    if mutation == "prompt":
        stream[0]["message"]["content"] = "not the requested source"
    else:
        stream[1]["message"][mutation] = "different"
    result = json.loads(cap.collect_capture(run, input_for(job, stream))["attempt.json"])
    assert result["status"] == "execution_error" and result["verdict"] == "UNREVIEWED"


@pytest.mark.parametrize("mutation", ["tool", "tool_block", "retry", "length", "error", "unsettled", "exit"])
def test_tool_retry_error_and_unsettled_are_not_complete(tmp_path, mutation):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    stream = events(job)
    if mutation == "tool":
        stream.insert(0, {"type": "tool_execution_start", "toolName": "bash", "toolCallId": "x", "args": {}})
    if mutation == "tool_block":
        stream[1]["message"]["content"].append({"type": "toolCall", "name": "read", "arguments": {}})
    if mutation == "retry":
        stream.insert(0, {"type": "auto_retry_start", "attempt": 1})
    if mutation in ("length", "error"):
        stream[1]["message"]["stopReason"] = mutation
    if mutation == "unsettled":
        stream.pop()
    result = json.loads(cap.collect_capture(run, input_for(job, stream, int(mutation == "exit")))["attempt.json"])
    assert result["status"] == "execution_error"


@pytest.mark.parametrize("raw", [b"not-json\n", b"[]\n", b"null\n", b'{"type":"message_end","message":null}\n',
                                  b'{"type":"message_end","message":{"role":"assistant","content":[null]}}\n'])
def test_malformed_json_shapes_fail_closed(tmp_path, raw):
    run, job = frozen_run(tmp_path)
    result = cap.collect_capture(run, cap.CaptureInput(job["id"], raw, b"", 0))
    assert json.loads(result["attempt.json"])["status"] == "execution_error"
    assert result["stdout.jsonl"] == raw


def test_snapshot_tamper_is_rejected(tmp_path):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    (run / job["prompt_path"]).write_text("changed", encoding="utf-8")
    with pytest.raises(ev.EvalError):
        cap.collect_capture(run, input_for(job, events(job)))


def test_unicode_lf_framing_and_raw_bytes_survive(tmp_path):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    sample = input_for(job, events(job))
    files = cap.collect_capture(run, sample)
    assert files["stdout.jsonl"] == sample.wire
    assert files["stderr.txt"] == sample.stderr
    assert files["response.md"] == "합성 응답\u2028둘째 줄"


def test_unknown_job_or_unselected_profile_cannot_complete(tmp_path):
    run, job = frozen_run(tmp_path)
    sample = input_for(job_with_prompt(run, job), events(job_with_prompt(run, job)))
    with pytest.raises(ev.EvalError):
        cap.collect_capture(run, cap.CaptureInput("../../escape", sample.wire, b"", 0))


def test_collect_cli_records_synthetic_trace_without_model_calls(tmp_path, monkeypatch):
    import run_korean_postediting_eval as cli
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    sample = input_for(job, events(job))
    wire = tmp_path / "synthetic.jsonl"
    wire.write_bytes(sample.wire)
    output = tmp_path / "captured"
    def forbidden_process(*args, **kwargs):
        pytest.fail("collect must never invoke a subprocess/model")
    monkeypatch.setattr(subprocess, "Popen", forbidden_process)
    result = cli.main(["collect", "--run-dir", str(run), "--job", job["id"],
                       "--wire", str(wire), "--exit-code", "0", "--output", str(output)])
    assert result == 0
    assert (output / "stdout.jsonl").read_bytes() == sample.wire
    record = json.loads((output / "attempt.json").read_bytes())
    assert record["verdict"] == "UNREVIEWED" and record["default_application"] == "held"


@pytest.mark.parametrize("mutation", ["missing_aborted", "string_aborted", "will_retry", "tool_result", "image"])
def test_incomplete_or_extra_context_trace_is_rejected(tmp_path, mutation):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    stream = events(job)
    if mutation == "missing_aborted":
        del stream[-1]["aborted"]
    if mutation == "string_aborted":
        stream[-1]["aborted"] = ""
    if mutation == "will_retry":
        stream.insert(-1, {"type": "agent_end", "willRetry": True})
    if mutation == "tool_result":
        stream.insert(-1, {"type": "message_end", "message": {"role": "toolResult", "content": "extra"}})
    if mutation == "image":
        stream[0]["message"]["content"] = [{"type": "text", "text": job["prompt"]},
                                            {"type": "image", "data": "extra image"}]
    result = cap.collect_capture(run, input_for(job, stream))
    assert json.loads(result["attempt.json"])["status"] == "execution_error"


@pytest.mark.parametrize("mutation", ["missing_hash", "missing_pair", "wrong_system", "wrong_command"])
def test_inconsistent_frozen_plan_is_rejected(tmp_path, mutation):
    run, job = frozen_run(tmp_path)
    job = job_with_prompt(run, job)
    plan = json.loads((run / "plan.json").read_bytes())
    if mutation == "missing_hash":
        del plan["artifacts"][job["prompt_path"]]
        del plan["jobs"][0]["prompt_sha256"]
    if mutation == "missing_pair":
        plan["jobs"].pop()
    if mutation == "wrong_system":
        plan["jobs"][0]["system_path"] = "system-postediting.txt"
        plan["jobs"][0]["system_sha256"] = plan["artifacts"]["system-postediting.txt"]
    if mutation == "wrong_command":
        plan["jobs"][0]["command"].remove("--no-tools")
    (run / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    with pytest.raises(ev.EvalError):
        cap.collect_capture(run, input_for(job, events(job)))
