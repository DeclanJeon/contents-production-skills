# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3", "typer"]
# ///
# How to run: imported by the explicitly authorized evaluation batch runner.
"""Native Codex CLI lifecycle/evidence; no automatic retries or craft grading."""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Literal

from pydantic import BaseModel, JsonValue, ValidationError

from run_guide_behavior import case_system
from run_writing_evaluation import RunOutcome, RunScope
from writing_eval_cases import WritingCase
from writing_eval_review import WireEvent, WireMessage
from writing_eval_snapshot import EvaluationContractError, digest


@dataclass(frozen=True, slots=True)
class CodexCapture:
    thread_id: str
    final: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class NativeItem(BaseModel):
    type: str
    text: str = ""
    server: str | None = None
    tool: str | None = None
    status: str | None = None
    result: JsonValue = None
    error: JsonValue = None


class NativeEvent(BaseModel):
    type: str
    thread_id: str | None = None
    item: NativeItem | None = None
    usage: dict[str, int] | None = None
    error: JsonValue = None


def parse_capture(raw: bytes) -> CodexCapture:
    thread = ""
    final = ""
    completed = 0
    usage: dict[str, int] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        event = NativeEvent.model_validate_json(line)
        if event.type in {"turn.failed", "error"} or event.error is not None:
            raise EvaluationContractError("Native Codex execution failed; inspect raw wire")
        if event.thread_id:
            if thread and thread != event.thread_id:
                raise EvaluationContractError("Native thread changed during turn")
            thread = event.thread_id
        if event.type == "turn.completed":
            completed += 1
            usage = event.usage or {}
        item = event.item
        if item is None:
            continue
        if item.type not in {"agent_message", "reasoning", "mcp_tool_call"}:
            raise EvaluationContractError(f"Unapproved native item: {item.type}")
        if item.type == "mcp_tool_call":
            if (item.server != "evaluation" or item.tool not in {"read", "find", "edit", "write"}
                    or item.error is not None or item.status in {"failed", "cancelled"}):
                raise EvaluationContractError("Unapproved/failed MCP call")
            if isinstance(item.result, dict) and (item.result.get("isError") is True or item.result.get("is_error") is True):
                raise EvaluationContractError("Failed MCP tool result")
        if event.type == "item.completed" and item.type == "agent_message":
            final = item.text
    if not thread or not final.strip() or completed != 1:
        raise EvaluationContractError("Missing thread/final/native turn completion")
    return CodexCapture(thread, final, usage.get("input_tokens"), usage.get("output_tokens"))


def sandbox_command(run: Path, source: Path, command: list[str]) -> list[str]:
    """Only isolated runtime/evidence is writable; auth is mounted, never copied."""
    run = run.resolve()
    source = source.resolve()
    if run.is_relative_to(source) or source.is_relative_to(run):
        raise EvaluationContractError("Sandbox source/runtime overlap")
    home = run / "codex-home"
    home.mkdir(exist_ok=True, mode=0o700)
    temporary = run / "tmp"
    temporary.mkdir(exist_ok=True, mode=0o700)
    result = ["bwrap", "--die-with-parent", "--unshare-pid", "--new-session", "--ro-bind", "/", "/", "--bind", str(run), str(run)]
    auth = Path.home() / ".codex/auth.json"
    if auth.is_file():
        target = home / "auth.json"
        target.touch(exist_ok=True)
        result += ["--ro-bind", str(auth), str(target)]
    for hidden in (Path.home() / ".agents", Path.home() / ".codex/skills"):
        if hidden.is_dir():
            result += ["--tmpfs", str(hidden)]
    result += ["--proc", "/proc", "--dev", "/dev", "--chdir", str(source),
        "--setenv", "CODEX_HOME", str(home), "--setenv", "TMPDIR", str(temporary), "--setenv", "PYTHONDONTWRITEBYTECODE", "1"]
    for key in ("OPENAI_API_KEY", "CODEX_API_KEY", "OPENAI_BASE_URL", "OPENAI_ORG_ID", "OPENAI_ORGANIZATION", "OPENAI_PROJECT_ID"):
        result += ["--unsetenv", key]
    return result + ["--", *command]


def case_instructions(case: WritingCase) -> str:
    if case.kind != "fixture":
        return case_system(case.owner)
    return "".join((
        "You are executing one controlled package fixture case. Replay the user request faithfully. ",
        "Authorized actions: read local package Markdown, read fixture/draft.md, and edit/write ONLY that supplied temporary fixture through the provided MCP tools. ",
        "Package sources and all other files remain read-only. Native shell/filesystem command execution remains read-only and unavailable; that does not revoke the separately authorized MCP fixture edits. ",
        "No other writes, shell execution, media generation, cloning, upload, external spend or publication are authorized. ",
        "Use local checkout sources, not global similarly named skills. Read only relevant package references and the controlled fixture; never inspect qa/, tests, support/, evaluation expectations or audit ledgers. ",
        "The controlled fixture is an actual supplied file. Other named production assets are hypothetical unless an actual file is supplied; never claim unavailable asset inspection. ",
        "Return the requested usable answer in Korean within its requested scope, not a test score. Existing production approval and unverified-evidence boundaries still apply. ",
    ))


def native_command(case: WritingCase, scope: RunScope, thread: str | None) -> list[str]:
    server = Path(__file__).with_name("writing_eval_codex_mcp.py")
    args = [str(server), str(scope.snapshot.root), str(scope.output / "tools.jsonl")]
    if case.kind == "fixture":
        args.append(str(scope.output / "fixture"))
    tool_protocol = (
        "The fixture has the sole virtual path fixture/draft.md, with NO skill-name prefix. "
        if case.kind == "fixture" else "Use find to locate uncertain package paths before reading. "
    )
    instructions = "".join((
        case_instructions(case),
        (f"\nThe first MCP read path is exactly {case.owner!r}. " if thread is None
            else f"\nContinue the same case/thread. Previously offered reference addresses remain valid across this turn's tool restart; reuse them without re-reading their source unless needed. The owner document is {case.owner!r}. "),
        "Paths are relative to the snapshot ROOT, ",
        "not a skill directory: retain the full top-level skill-name prefix on direct package paths. ",
        "There is ONE read tool for both initial files and offered source references. First use read(path=the owner filename above). Afterwards follow links or inline source references using the SAME read tool with the exact read_arguments object from companion metadata (path is then an offered ref_... address). Copy that object; no tool switch, path math or base classification. For unlisted files use root-qualified read or find where available. Legacy relative_to addressing is explicit only; guessing or retries never erase an error. ",
        tool_protocol,
        "Use only the supplied evaluation MCP tools. Other tools/external services are forbidden. ",
        "Keep final output in the user's requested form; omit citations when only a sentence or changed text was requested.",
    ))
    settings = {
        "model_provider": '"openai"', "project_doc_max_bytes": "0", "web_search": '"disabled"',
        "model_reasoning_effort": json.dumps(scope.profile.thinking),
        "developer_instructions": json.dumps(instructions, ensure_ascii=False),
        "features.shell_tool": "false", "features.unified_exec": "false",
        "features.apply_patch_freeform": "false", "features.multi_agent": "false",
        "skills.config": '[{name="skill-creator",enabled=false},{name="skill-installer",enabled=false}]',
        "mcp_servers.evaluation.command": json.dumps(sys.executable),
        "mcp_servers.evaluation.args": json.dumps(args),
        "mcp_servers.evaluation.tools.read.output_token_limit": "30000",
    }
    command = [scope.profile.executable, "exec", "--ignore-user-config", "--ignore-rules", "--json",
        "--skip-git-repo-check", "-s", "read-only", "-C", str(scope.snapshot.root), "-m", scope.profile.model]
    for tool in (["read", "edit", "write"] if case.kind == "fixture" else ["read", "find"]):
        settings[f"mcp_servers.evaluation.tools.{tool}.approval_mode"] = '"approve"'
    for name, value in settings.items():
        command += ["-c", f"{name}={value}"]
    if thread is not None:
        command += ["resume", "--json", "-m", scope.profile.model, thread]
    return command + ["-"]


class CodexBackend:
    """One fresh isolated runtime per case; explicit native resume per later turn."""

    def execute(self, case: WritingCase, scope: RunScope) -> RunOutcome:
        profile = scope.profile
        if profile.provider != "openai" or profile.model != "gpt-6-luna":
            raise EvaluationContractError("This approved backend is pinned to OpenAI gpt-6-luna")
        if any(value is not None for value in (profile.max_cost_usd, profile.max_total_tokens, profile.max_provider_calls)):
            raise EvaluationContractError("Native CLI cannot enforce finite provider/token/dollar ceilings; no request submitted")
        trace: list[WireEvent] = []
        thread: str | None = None
        deadline = time.monotonic() + profile.timeout_seconds
        consumed = 0
        status: Literal["completed", "INCONCLUSIVE"] = "completed"
        reason: str | None = None
        stages: list[dict[str, JsonValue]] = []
        try:
            for n in range(len(case.turns)):
                prefix = scope.output / f"turn-{n + 1}"
                message = case.message(n)
                with prefix.with_suffix(".input.txt").open("x", encoding="utf-8") as stream:
                    _ = stream.write(message)
                command = sandbox_command(scope.output, scope.snapshot.root, native_command(case, scope, thread))
                with prefix.with_suffix(".command.json").open("x", encoding="utf-8") as stream:
                    _ = stream.write(json.dumps(command, ensure_ascii=False, indent=2))
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Case deadline exceeded")
                with prefix.with_suffix(".stdout.jsonl").open("xb") as out, prefix.with_suffix(".stderr.txt").open("xb") as err:
                    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err, start_new_session=True)
                    try:
                        _ = process.communicate(message.encode(), timeout=remaining)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        _ = process.communicate()
                        raise TimeoutError("Native CLI case deadline exceeded") from None
                raw = prefix.with_suffix(".stdout.jsonl").read_bytes()
                if process.returncode != 0:
                    raise EvaluationContractError(f"Native CLI exit {process.returncode}; raw stdout/stderr retained")
                capture = parse_capture(raw)
                if thread is not None and capture.thread_id != thread:
                    raise EvaluationContractError("Conversation did not resume the same native thread")
                thread = capture.thread_id
                with prefix.with_suffix(".response.md").open("x", encoding="utf-8") as stream:
                    _ = stream.write(capture.final)
                tools_path = scope.output / "tools.jsonl"
                tool_lines = tools_path.read_bytes().splitlines() if tools_path.exists() else []
                trace.extend(WireEvent.model_validate_json(line) for line in tool_lines[consumed:])
                consumed = len(tool_lines)
                trace += [WireEvent(type="message_end", message=WireMessage(role="assistant", stopReason="stop", content=capture.final)),
                    WireEvent(type="agent_settled", aborted=False)]
                stages.append({"turn": n + 1, "thread_id": thread, "input_tokens": capture.input_tokens,
                    "output_tokens": capture.output_tokens, "stdout_sha256": digest(raw), "input_sha256": digest(message.encode())})
            if not any(e.type == "controlled_read" and e.path == str(scope.snapshot.root / case.owner) for e in trace):
                raise EvaluationContractError("Missing actual owner read")
            if any(e.isError for e in trace):
                raise EvaluationContractError("Controlled tool error in trace")
            if case.kind == "fixture" and not {"user_edit_inserted", "fixture_reread"}.issubset(e.type for e in trace):
                raise EvaluationContractError("Missing controlled insertion/re-read evidence")
        except (EvaluationContractError, OSError, TimeoutError, ValidationError) as exc:
            status, reason = "INCONCLUSIVE", str(exc)
            tools_path = scope.output / "tools.jsonl"
            if tools_path.exists():
                trace.extend(WireEvent.model_validate_json(line) for line in tools_path.read_bytes().splitlines()[consumed:])
        with (scope.output / "native-observation.json").open("x", encoding="utf-8") as stream:
            _ = stream.write(json.dumps({"stages": stages, "status": status, "reason": reason,
                "normalization": "message_end/agent_settled normalize Codex final agent_message + turn.completed, not native Pi events",
                "provider_requests": "NOT_EXPOSED", "actual_cost_usd": "NOT_EXPOSED", "provider_stop_reason": "NOT_EXPOSED",
                "seed": "UNSUPPORTED", "application_retries": 0, "transport_retries": "native defaults; reserved provider cannot be overridden"}, ensure_ascii=False, indent=2))
        return RunOutcome(status=status, reason=reason, trace=tuple(trace))
