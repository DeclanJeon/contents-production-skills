"""Codex isolation/evidence boundaries, with no implicit live requests."""
from pathlib import Path
import subprocess
import sys

import pytest

from writing_eval_codex import CodexBackend, CodexCapture, parse_capture, sandbox_command, native_command
from run_writing_evaluation import run_case
from run_writing_evaluation import RunScope
from writing_eval_cases import WritingCase, resolve_owner
from writing_eval_manifest import RunSlot, input_digest
from writing_eval_snapshot import FilePin, Snapshot
import tomllib
from writing_eval_manifest import EvaluationProfile
from writing_eval_snapshot import EvaluationContractError


def test_explicit_unlimited_budget_can_be_pinned() -> None:
    # Given: the user removed monetary/provider/token ceilings, not the case limit.
    # When: that explicit profile is parsed.
    profile = EvaluationProfile(executable="codex", provider="openai", model="gpt-6-luna", thinking="low",
        timeout_seconds=240, max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    # Then: unlimited remains explicit JSON null, not an invented dollar amount.
    assert '"max_cost_usd":null' in profile.model_dump_json()


def test_captures_native_completion_without_treating_progress_as_final() -> None:
    # Given: real Codex JSONL envelope shapes and one terminal turn.
    raw = b'\n'.join([
        b'{"type":"thread.started","thread_id":"session-a"}',
        b'{"type":"turn.started"}',
        b'{"type":"item.completed","item":{"type":"agent_message","text":"progress"}}',
        b'{"type":"item.completed","item":{"type":"agent_message","text":"final answer"}}',
        b'{"type":"turn.completed","usage":{"input_tokens":20,"output_tokens":4}}',
    ])
    # When: the raw response is interpreted.
    capture = parse_capture(raw)
    # Then: the final native message and continuation identity are retained.
    assert capture == CodexCapture(thread_id="session-a", final="final answer", input_tokens=20, output_tokens=4)


@pytest.mark.parametrize("raw", [
    b'{"type":"turn.started"}\n',
    b'{"type":"thread.started","thread_id":"a"}\n{"type":"turn.completed"}',
    b'{"type":"turn.failed","error":{"message":"provider unavailable"}}',
    b'{"type":"item.completed","item":{"type":"command_execution","command":"curl remote"}}',
    b'{"type":"item.completed","item":{"type":"mcp_tool_call","server":"unknown","tool":"read"}}',
    b'{"type":"item.completed","item":{"type":"mcp_tool_call","server":"evaluation","tool":"read","result":{"isError":true}}}',
    b'{"type":"item.completed","item":{"type":"mcp_tool_call","server":"evaluation","tool":"read","status":"failed","result":{"content":[]},"error":null}}',
])
def test_incomplete_or_unapproved_native_execution_cannot_be_completed(raw: bytes) -> None:
    # Given: missing terminal evidence, errors, or an unapproved tool.
    # When/Then: no successful receipt is manufactured.
    if b'"item"' in raw or b'"turn.failed"' in raw:
        raw = (b'{"type":"thread.started","thread_id":"a"}\n' + raw
            + b'\n{"type":"item.completed","item":{"type":"agent_message","text":"cannot erase failure"}}'
            + b'\n{"type":"turn.completed","usage":{"input_tokens":20,"output_tokens":4}}')
    with pytest.raises(EvaluationContractError):
        parse_capture(raw)


@pytest.mark.parametrize("case_id, kind, expected_tools", [("T13", "single", {"read", "find"}), ("T09", "fixture", {"read", "edit", "write"})])
def test_explicit_approvals_are_scoped_to_controlled_tools(tmp_path: Path, case_id, kind, expected_tools) -> None:
    # Given: an approved source-only or one-file-fixture capability.
    case = WritingCase(id=case_id, kind=kind, owner=resolve_owner(case_id), turns=("probe",))
    profile = EvaluationProfile(executable="codex", provider="openai", model="gpt-6-luna", thinking="low", timeout_seconds=240,
        max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    slot = RunSlot(id="probe", case_id=case_id, condition="baseline", repeat=1, kind=kind, owner=case.owner, stages=1, input_sha256=input_digest(case))
    snapshot = Snapshot(root=tmp_path / "source", sha256="0" * 64, files=(FilePin(path=case.owner, sha256="0" * 64),))
    scope = RunScope(slot=slot, snapshot=snapshot, output=tmp_path / "run", profile=profile, approval_reference="test", fixture_writes_approved=kind == "fixture")
    # When: the actual TOML overrides for the native CLI are built.
    command = native_command(case, scope, None)
    config = tomllib.loads("\n".join(command[n + 1] for n, arg in enumerate(command) if arg == "-c"))
    # Then: only explicitly controlled tools are preapproved; no global bypass.
    server = config["mcp_servers"]["evaluation"]
    assert set(server["tools"]) == expected_tools
    assert all(v["approval_mode"] == "approve" for v in server["tools"].values())
    assert "approval_policy" not in config


def test_native_timeout_retains_partial_wire_without_resampling(tmp_path: Path) -> None:
    # Given: a local CLI double that emits partial wire and then blocks (no provider).
    import sys
    source = tmp_path / "source"
    owner = resolve_owner("T13")
    p = source / owner
    p.parent.mkdir(parents=True)
    p.write_text("local transport fixture")
    (source / "manifest.json").write_text('{"skills":["video-production-assets"]}')
    from writing_eval_snapshot import create_snapshot
    snapshot = create_snapshot(source, tmp_path / "snapshot")
    executable = tmp_path / "blocked-cli"
    executable.write_text(f"#!{sys.executable}\nimport signal,sys\nsys.stdin.read()\nprint('{{\"type\":\"thread.started\",\"thread_id\":\"partial\"}}', flush=True)\nsignal.pause()\n")
    executable.chmod(0o755)
    case = WritingCase(id="T13", kind="single", owner=owner, turns=("transport probe",))
    profile = EvaluationProfile(executable=str(executable), provider="openai", model="gpt-6-luna", thinking="low", timeout_seconds=0.5,
        max_case_runs=140, max_provider_calls=None, max_total_tokens=None, max_cost_usd=None)
    slot = RunSlot(id="offline-timeout", case_id="T13", condition="baseline", repeat=1, kind="single", owner=owner, stages=1, input_sha256=input_digest(case))
    scope = RunScope(slot=slot, snapshot=snapshot, output=tmp_path / "run", profile=profile, approval_reference="offline transport test")
    # When: the real OS subprocess/deadline path runs once.
    result = run_case(case, scope, CodexBackend())
    # Then: incomplete wire and an inconclusive receipt survive, with no retry directory.
    assert result.status == "INCONCLUSIVE" and "deadline" in (result.reason or "")
    assert (scope.output / "turn-1.stdout.jsonl").read_bytes() == b'{"type":"thread.started","thread_id":"partial"}\n'
    assert (scope.output / "execution.json").is_file()
    assert not (scope.output / "turn-2.stdout.jsonl").exists()


def test_os_sandbox_denies_external_writes_but_allows_runtime_state(tmp_path: Path) -> None:
    # Given: a writable runtime and an external sentinel, with no model involved.
    run = tmp_path / "run"
    run.mkdir()
    source = tmp_path / "source"
    source.mkdir()
    sentinel = tmp_path / "sentinel"
    sentinel.write_text("unchanged")
    program = "from pathlib import Path; import sys; Path(sys.argv[1]).write_text('allowed'); Path(sys.argv[2]).write_text('forbidden')"
    # When: the actual sandbox executes a process with both target paths.
    command = sandbox_command(run, source, [sys.executable, "-B", "-c", program, str(run / "proof"), str(sentinel)])
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    # Then: only isolated runtime state is writable.
    assert result.returncode != 0 and "Read-only file system" in result.stderr
    assert (run / "proof").read_text() == "allowed"
    assert sentinel.read_text() == "unchanged"
