# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_rpc.py
"""One persistent Pi conversation per isolated writing-evaluation repeat."""
from __future__ import annotations

from pathlib import Path
import json
import subprocess
from typing import ClassVar, Literal, TypedDict

from pydantic import BaseModel, ConfigDict, ValidationError

from run_guide_behavior import case_system, digest, fingerprint, parse_events, save_new
from writing_eval_cases import CaseContractError, WritingCase
from writing_eval_transport import (
    RpcCommand, RpcPipe, RpcProfile, RpcProtocolError, RpcWorkspace, shutdown,
)


class ReadEvidence(BaseModel):
    path: str
    local_path: str | None
    success: bool
    offset: int | None = None
    limit: int | None = None


class ExecutionTrace(BaseModel):
    """Validate the legacy parser boundary before consuming its fields."""
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="allow")
    final_text: str
    final_stop_reason: str | None
    settled: bool
    aborted: bool
    protocol_errors: tuple[str, ...]
    tool_errors: tuple[ReadFailure, ...]
    tools_called: tuple[str, ...]
    reads: tuple[ReadEvidence, ...]


class ReadFailure(BaseModel):
    tool: str | None
    call_id: str | None


class RpcResult(TypedDict):
    id: str
    status: Literal["completed", "INCONCLUSIVE"]
    verdict: Literal["UNREVIEWED"]
    reason: str | None
    completed_turns: int


def run_conversation(case: WritingCase, workspace: RpcWorkspace, profile: RpcProfile) -> RpcResult:
    """Run authorized messages, never turn a successful execution into PASS."""
    if case.kind != "conversation":
        raise CaseContractError(f"Expected conversation adapter: {case.id}")
    root = workspace.root.resolve()
    output = workspace.output.resolve()
    if output.is_relative_to(root):
        raise CaseContractError("RPC evidence must be outside model-readable snapshot")
    if not (root / case.owner).is_file():
        raise CaseContractError(f"Missing owner: {case.owner}")
    output.mkdir(parents=True, exist_ok=False)
    before = fingerprint(root)["sha256"]
    system = case_system(case.owner)
    command = [profile.executable, "--mode", "rpc", "--provider", profile.provider,
               "--model", profile.model, "--thinking", profile.thinking,
               "--tools", "read,grep,find,ls", "--no-extensions", "--no-mcp", "--no-skills",
               "--no-prompt-templates", "--no-context-files", "--no-session",
               "--no-approve", "--offline", "--append-system-prompt", system]
    save_new(output / "metadata.json", {
        "id": case.id, "profile": profile.model_dump(), "command": command,
        "owner": case.owner, "source_before": before,
        "system_prompt": system, "system_sha256": digest(system.encode()),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "transport_sha256": digest(Path(__file__).with_name("writing_eval_transport.py").read_bytes()),
        "limits": "Execution only; no automatic PASS. Read-only tools are not an OS sandbox.",
    })
    result: RpcResult = {"id": case.id, "status": "completed", "verdict": "UNREVIEWED",
                         "reason": None, "completed_turns": 0}
    with (output / "stderr.txt").open("xb") as stderr, (output / "stdin.jsonl").open("xb") as sent:
        try:
            with subprocess.Popen(command, cwd=root, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=stderr,
                                  start_new_session=True) as process:
                try:
                    pipe = RpcPipe(process, profile.timeout_seconds)
                    with (output / "setup.stdout.jsonl").open("xb") as setup:
                        for setting in ("set_auto_retry", "set_auto_compaction"):
                            item = RpcCommand(id=setting, type=setting, enabled=False)
                            _ = sent.write(item.model_dump_json(exclude_none=True).encode() + b"\n")
                            sent.flush()
                            _ = pipe.exchange(item, setup)
                    for index in range(len(case.turns)):
                        prefix = output / f"turn-{index + 1}"
                        item = RpcCommand(id=f"turn-{index + 1}", type="prompt", message=case.message(index))
                        _ = sent.write(item.model_dump_json(exclude_none=True).encode() + b"\n")
                        sent.flush()
                        reason = None
                        with prefix.with_suffix(".stdout.jsonl").open("xb") as wire:
                            try:
                                _ = pipe.exchange(item, wire)
                            except (RpcProtocolError, ValidationError, BrokenPipeError, OSError) as exc:
                                reason = str(exc)
                        try:
                            trace = ExecutionTrace.model_validate(parse_events(prefix.with_suffix(".stdout.jsonl").read_text(encoding="utf-8"), root))
                        except (TypeError, KeyError, AttributeError, ValidationError) as exc:
                            # This legacy parser assumes well-shaped payloads; retain raw wire on invalid input.
                            reason = f"Malformed RPC evidence: {exc}"
                            trace = ExecutionTrace(final_text="", final_stop_reason=None, settled=False,
                                aborted=False, protocol_errors=(reason,), tool_errors=(), tools_called=(), reads=())
                        if (trace.protocol_errors or trace.tool_errors or not trace.settled
                                or trace.aborted or trace.final_stop_reason != "stop"
                                or not trace.final_text):
                            reason = reason or "Missing successful final assistant message/settled evidence"
                        if any(t not in {"read", "grep", "find", "ls"} for t in trace.tools_called):
                            reason = "Unexpected tool in read-only run"
                        if index == 0 and not any(r.success and r.local_path == case.owner for r in trace.reads):
                            reason = reason or "Owner not read"
                        after = fingerprint(root)["sha256"]
                        if after != before:
                            reason = "Source changed during evaluation"
                        _ = prefix.with_suffix(".response.md").write_text(trace.final_text, encoding="utf-8")
                        save_new(prefix.with_suffix(".attempt.json"), {
                            "id": item.id, "prompt": item.message,
                            "prompt_sha256": digest(case.message(index).encode()),
                            "trace": trace.model_dump(mode="json"), "source_before": before, "source_after": after,
                            "verdict": "UNREVIEWED", "reason": reason,
                            "status": "INCONCLUSIVE" if reason else "completed",
                        })
                        if reason:
                            raise RpcProtocolError(reason)
                        result["completed_turns"] += 1
                finally:
                    shutdown(process)
                if process.returncode != 0:
                    raise RpcProtocolError(f"RPC peer exited with {process.returncode}")
        except (OSError, ValidationError, RpcProtocolError, subprocess.TimeoutExpired) as exc:
            result.update(status="INCONCLUSIVE", reason=str(exc))
    with (output / "execution-summary.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        _ = stream.write("\n")
    return result
