# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# Imported by run_korean_postediting_eval.py collect; no live execution.
"""Validate frozen plans and collect supplied Pi JSONL as unreviewed evidence."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from korean_postediting_eval import (
    COMMON, Batch, EvalError, JsonValue, Profile, build_batch, json_text,
    load_cases, mapping, parse_json, render_batch, sequence, text,
)
from run_guide_behavior import digest, parse_events


@dataclass(frozen=True, slots=True)
class CaptureInput:
    job_id: str
    wire: bytes
    stderr: bytes
    exit_code: int


def check_path(path: Path) -> None:
    """Reject symlink traversal before resolving a caller-selected path."""
    absolute = path.absolute()
    if any(part.is_symlink() for part in (absolute, *absolute.parents)):
        raise EvalError("symlink traversal is not allowed")


def relative_name(name: str) -> Path:
    path = Path(name)
    if path.is_absolute() or any(p in (".", "..") for p in path.parts):
        raise EvalError("unsafe artifact path")
    if re.fullmatch(r"[A-Za-z0-9_./-]+", name) is None or not path.parts:
        raise EvalError("unsafe artifact name")
    return path


def frozen_job(run_dir: Path, job_id: str) -> tuple[dict[str, JsonValue], dict[str, JsonValue]]:
    check_path(run_dir)
    check_path(run_dir / "plan.json")
    plan = mapping(parse_json((run_dir / "plan.json").read_bytes()))
    if plan.get("schema") != "korean-postediting-eval-batch/1":
        raise EvalError("unsupported batch schema")
    artifacts = mapping(plan.get("artifacts"))
    for name, expected in artifacts.items():
        path = run_dir / relative_name(name)
        check_path(path)
        if digest(path.read_bytes()) != text(expected):
            raise EvalError(f"snapshot modified: {name}")
    cases = load_cases((run_dir / "suite.json").read_bytes())
    settings = mapping(plan.get("profile"))
    profile = Profile(text(settings["provider"]) if settings.get("provider") is not None else None,
                      text(settings["model"]) if settings.get("model") is not None else None,
                      text(settings.get("thinking")))
    baseline = (run_dir / "system-baseline.txt").read_bytes().decode("utf-8")
    treatment = (run_dir / "system-postediting.txt").read_bytes().decode("utf-8")
    if baseline != COMMON or not treatment.startswith(COMMON + "\n\n선택된 후편집 지침:\n"):
        raise EvalError("condition/system mismatch")
    canonical = build_batch(cases, ("placeholder", "placeholder"), profile)
    expected = render_batch(Batch(cases, profile, canonical.jobs, baseline, treatment))
    if plan != mapping(parse_json(expected["plan.json"].encode())):
        raise EvalError("inconsistent frozen plan: pairs/profile/inputs/commands")
    jobs = [mapping(j) for j in sequence(plan.get("jobs"))]
    selected = [j for j in jobs if j.get("id") == job_id]
    if len(selected) != 1:
        raise EvalError("unknown or duplicate job")
    job = selected[0]
    for field in ("prompt", "system"):
        name = text(job.get(f"{field}_path"))
        if artifacts.get(name) != job.get(f"{field}_sha256"):
            raise EvalError("job input hash does not match artifact manifest")
    return plan, job


def inspect_wire(raw: bytes, root: Path) -> tuple[dict[str, JsonValue], list[str], list[str], list[str]]:
    """Guard legacy decoder's shape assumptions before reusing its JSONL parser."""
    users: list[str] = []
    providers: list[str] = []
    problems: list[str] = []
    wire = raw.decode("utf-8")
    records = [mapping(parse_json(line.encode())) for line in wire.split("\n") if line.strip()]
    if not records or records[-1].get("type") != "agent_settled":
        problems.append("missing terminal agent_settled")
    for event in records:
        kind = text(event.get("type"))
        if kind == "agent_settled" and event.get("aborted") is not False:
            problems.append("settled event missing explicit aborted=false")
        if kind == "agent_end" and event.get("willRetry") is not False:
            problems.append("agent end may retry")
        if kind.startswith(("tool_", "auto_retry", "compaction", "summarization_retry")):
            problems.append(f"unexpected event: {kind}")
        if kind == "message_end":
            msg = mapping(event.get("message"))
            role = text(msg.get("role"))
            if role not in ("user", "assistant"):
                problems.append("unexpected message role/context")
            if role == "user":
                content = msg.get("content")
                if isinstance(content, str):
                    users.append(content)
                else:
                    blocks = [mapping(c) for c in sequence(content)]
                    if any(c.get("type") != "text" for c in blocks):
                        problems.append("unexpected non-text user context")
                    users.append("\n".join(text(c.get("text")) for c in blocks if c.get("type") == "text"))
            if role == "assistant":
                providers.append(text(msg.get("provider")))
                _ = text(msg.get("model"))
                for block in sequence(msg.get("content")):
                    item = mapping(block)
                    if item.get("type") == "toolCall":
                        problems.append("assistant toolCall")
                    if item.get("type") == "text":
                        _ = text(item.get("text"))
    trace: dict[str, JsonValue] = parse_events(wire, root)
    return trace, users, providers, problems


def collect_capture(run_dir: Path, capture: CaptureInput) -> dict[str, str | bytes]:
    """Record supplied output; neither execute commands nor certify model quality."""
    plan, job = frozen_job(run_dir, capture.job_id)
    if type(capture.exit_code) is not int:
        raise EvalError("exit_code must be supplied as integer")
    profile = mapping(plan.get("profile"))
    problems: list[str] = []
    trace: dict[str, JsonValue] = {}
    try:
        trace, users, providers, problems = inspect_wire(capture.wire, run_dir)
        expected_prompt = (run_dir / relative_name(text(job.get("prompt_path")))).read_bytes().decode("utf-8")
        if users != [expected_prompt]:
            problems.append("user prompt/source mismatch")
        provider = text(profile["provider"]) if profile.get("provider") is not None else None
        model = text(profile["model"]) if profile.get("model") is not None else None
        if provider is None or model is None:
            problems.append("provider/model selection unresolved")
        if not providers or set(providers) != {provider} or trace.get("observed_models") != [model]:
            problems.append("actual provider/model mismatch")
        if (not trace.get("settled") or trace.get("aborted") or trace.get("protocol_errors")
                or trace.get("tool_errors") or trace.get("tools_called")
                or trace.get("final_stop_reason") != "stop" or not trace.get("final_text")):
            problems.append("incomplete/failed/unsafe trace")
    except (EvalError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        problems.append(f"invalid JSONL trace: {exc}")
    if capture.exit_code != 0:
        problems.append("supplied process exit code is nonzero")
    status = "execution_error" if problems else "completed"
    problem_values: list[JsonValue] = list(problems)
    attempt: dict[str, JsonValue] = {
        "schema": "korean-postediting-eval-capture/1", "job_id": capture.job_id,
        "case_id": job.get("case_id"), "condition": job.get("condition"), "status": status,
        "verdict": "UNREVIEWED", "default_application": "held", "profile": profile,
        "supplied_exit_code": capture.exit_code, "problems": problem_values, "trace": trace,
        "plan_sha256": digest((run_dir / "plan.json").read_bytes()),
        "prompt_sha256": job.get("prompt_sha256"), "system_sha256": job.get("system_sha256"),
        "stdout_sha256": digest(capture.wire), "stderr_sha256": digest(capture.stderr),
        "limitations": "Supplied capture/exit code, not execution attestation or proof the system prompt was consumed. "
                      "No quality approval, spend control, tool/runtime verification or automatic promotion."
    }
    response = trace.get("final_text", "")
    return {"stdout.jsonl": capture.wire, "stderr.txt": capture.stderr,
            "response.md": response if isinstance(response, str) else "",
            "attempt.json": json_text(attempt)}
