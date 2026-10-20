#!/usr/bin/env python3
"""Run isolated, read-only Pi cases; completion is NEVER an automatic PASS.

Requires an already installed/authenticated Pi CLI. No install, credentials export,
media tools, or model defaults. Stores exact prompts, wire output, actual file-read
traces and source fingerprints. Review verdicts belong in a separate report.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

REPO = Path(__file__).resolve().parents[1]
OWNER = {
    "G01": "video-production-assets/references/11-ai-handoff.md",
    "G02": "designing-video-character-sheets/references/character-craft.md",
    "G03": "video-production-assets/references/11-ai-handoff.md",
    "G04": "video-production-assets/references/11-ai-handoff.md",
    "G05": "video-production-assets/references/09-edit.md",
    "G06": "video-production-assets/references/22-dialogue-lipsync.md",
    "G07": "video-production-assets/references/21-generated-video-qa-retry.md",
    "G08": "video-production-assets/references/14-production-ops.md",
    "G09": "video-production-assets/references/20-visual-mode-ssot.md",
    "G10": "video-production-assets/references/15-delivery.md",
    "G11": "camera-spatial-design/references/motion-timing-lens.md",
    "G12": "creative-production/SKILL.md",
    "F01": "video-production-assets/references/21-generated-video-qa-retry.md",
    "F02": "video-production-assets/references/20-visual-mode-ssot.md",
    "F03": "video-production-assets/references/11-ai-handoff.md",
    "F04": "video-production-assets/references/11-ai-handoff.md",
    "F05": "designing-video-character-sheets/references/character-craft.md",
    "F06": "video-production-assets/references/06-shots.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_new(path: Path, value):
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")


def package_manifest(root: Path) -> Path:
    """Installer keeps the manifest inside the host skill, not at skill root."""
    source = root / "manifest.json"
    return source if source.is_file() else root / "video-production-assets/support/manifest.json"


def fingerprint(root: Path):
    manifest_path = package_manifest(root)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = []
    for name in manifest["skills"]:
        for directory, dirs, files in os.walk(root / name, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in {"support", "__pycache__", ".pytest_cache", "node_modules"})
            for name in sorted(files):
                p = Path(directory) / name
                if p.suffix in {".pyc", ".pyo"} or name.endswith(".from-backup"):
                    continue
                records.append([p.relative_to(root).as_posix(), digest(p.read_bytes())])
    records.append(["manifest.json", digest(manifest_path.read_bytes())])
    return {"sha256": digest(json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode()),
            "files": records, "excludes": ["derived support", "caches", "*.from-backup", "repository QA/docs"]}


def parse_events(wire: str, root: Path):
    """Parse LF-delimited Pi JSON, authoritative messages and settled state."""
    final = ""
    final_stop_reason = None
    tool_calls = []
    settled = False
    aborted = False
    errors = []
    tool_errors = []
    reads = []
    pending = {}
    tools = []
    usage = []
    model_ids = set()
    for number, line in enumerate(wire.split("\n"), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"invalid JSONL record {number}")
            continue
        if event.get("type") == "tool_execution_start":
            name = event.get("toolName")
            tools.append(name)
            tool_calls.append({"name": name, "args": event.get("args", {})})
            pending[event.get("toolCallId")] = event
        elif event.get("type") == "tool_execution_end":
            start = pending.get(event.get("toolCallId"), {})
            name = event.get("toolName", start.get("toolName"))
            if event.get("isError"):
                tool_errors.append({"tool": name, "call_id": event.get("toolCallId")})
            if name == "read":
                raw = start.get("args", {}).get("path", "")
                path = Path(raw) if raw else None
                if path is not None and not path.is_absolute():
                    path = root / path
                resolved = path.resolve() if path else None
                reads.append({"path": raw,
                              "local_path": resolved.relative_to(root).as_posix() if resolved and resolved.is_relative_to(root) else None,
                              "success": not event.get("isError", False),
                              "offset": start.get("args", {}).get("offset"),
                              "limit": start.get("args", {}).get("limit")})
        elif event.get("type") == "message_end":
            msg = event.get("message", {})
            if msg.get("role") == "assistant":
                if msg.get("model"):
                    model_ids.add(str(msg["model"]))
                if msg.get("usage"):
                    usage.append(msg["usage"])
                reason = msg.get("stopReason")
                final_stop_reason = reason
                if reason in {"error", "aborted", "length"}:
                    errors.append(f"assistant stopReason={reason}")
                text = "\n".join(c.get("text", "") for c in msg.get("content", []) if c.get("type") == "text")
                if reason != "toolUse" and text:
                    final = text
        elif event.get("type") == "agent_settled":
            settled = True
            aborted = bool(event.get("aborted"))
    return {"final_text": final, "final_stop_reason": final_stop_reason,
            "tool_calls": tool_calls, "settled": settled, "aborted": aborted,
            "protocol_errors": errors, "tool_errors": tool_errors, "reads": reads,
            "tools_called": tools, "usage_per_assistant_message": usage,
            "observed_models": sorted(model_ids)}


def case_system(owner):
    return (
        "You are executing one isolated package QA case. The user prompt below is replayed verbatim. "
        "This run is text-only and read-only: no file writes, shell execution, generation, cloning, upload, spend or publication. "
        "Only read package instruction/reference/template files under the current working directory. "
        "Do not inspect qa/, tests, support/, *.from-backup, evaluation expectations, extraction audits or coverage/scan ledgers. "
        f"Begin by reading the current checkout owner {owner}; follow only relevant craft/contract/template links needed for the request. "
        "Use local checkout sources, not global similarly named skills. Treat named production assets in a case as supplied hypothetical facts "
        "unless an actual file is provided; do not invent paths or claim inspection of unavailable assets. "
        "Return the requested usable answer in Korean with concise package file/section citations, not a test score. "
        "Do not recite the entire pipeline for a narrow question. Existing scope, approval and unverified-evidence boundaries still apply."
    )


def execute(case, root, out, profile, before):
    identifier = case["id"]
    owner = OWNER[identifier.split("-", 1)[0]]
    system = case_system(owner)
    command = [profile["executable"], "--mode", "json", "--provider", profile["provider"],
               "--model", profile["model"], "--thinking", "low", "--tools", "read,grep,find,ls",
               "--no-extensions", "--no-mcp", "--no-skills", "--no-prompt-templates",
               "--no-context-files", "--no-session", "--no-approve", "--offline",
               "--append-system-prompt", system, "--print", "--", case["prompt"]]
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    timed_out = False
    process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=(os.name != "nt"))
    try:
        stdout, stderr = process.communicate(timeout=profile["timeout_seconds"])
    except subprocess.TimeoutExpired:
        timed_out = True
        if os.name != "nt":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        stdout, stderr = process.communicate()
    stem = out / identifier
    with stem.with_suffix(".stdout.jsonl").open("xb") as f:
        f.write(stdout)
    with stem.with_suffix(".stderr.txt").open("xb") as f:
        f.write(stderr)
    trace = parse_events(stdout.decode("utf-8", errors="replace"), root)
    with stem.with_suffix(".response.md").open("x", encoding="utf-8") as f:
        f.write(trace["final_text"])
    after = fingerprint(root)["sha256"]
    read_paths = {r["local_path"] for r in trace["reads"] if r["success"]}
    status = "completed"
    if timed_out:
        status = "timeout"
    elif (process.returncode != 0 or trace["protocol_errors"] or not trace["settled"]
          or trace["aborted"] or not trace["final_text"] or trace["final_stop_reason"] != "stop"):
        status = "execution_error"
    elif owner not in read_paths:
        status = "owner_not_read"
    elif any(t not in {"read", "grep", "find", "ls"} for t in trace["tools_called"]):
        status = "unexpected_tool"
    elif after != before:
        status = "source_mutated"
    record = {"id": identifier, "status": status, "verdict": "UNREVIEWED",
              "prompt": case["prompt"], "prompt_sha256": digest(case["prompt"].encode()),
              "owner": owner, "system_prompt": system, "system_sha256": digest(system.encode()),
              "command": command, "started_at": started, "duration_seconds": time.monotonic() - start,
              "exit_code": process.returncode, "timed_out": timed_out,
              "source_before": before, "source_after": after, "trace": trace,
              "wire_stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr)}
    save_new(stem.with_suffix(".attempt.json"), record)
    return {"id": identifier, "status": status, "verdict": "UNREVIEWED", "record": stem.with_suffix(".attempt.json").name}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skill-root", type=Path, default=REPO)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--suite", type=Path, action="append")
    p.add_argument("--case", action="append")
    p.add_argument("--provider", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--executable", default="pi")
    p.add_argument("--timeout", type=int, default=240)
    p.add_argument("--concurrency", type=int, default=1)
    args = p.parse_args(argv)
    if not 1 <= args.concurrency <= 4 or args.timeout <= 0:
        p.error("concurrency must be 1..4; timeout must be positive")
    executable = shutil.which(args.executable)
    if not executable:
        p.error("Pi executable not available")
    suites = args.suite or [REPO / "qa/guide-integration-scenarios.json", REPO / "qa/guide-followup-scenarios.json"]
    cases = [c for path in suites for c in json.loads(path.read_text(encoding="utf-8"))["cases"]]
    if args.case:
        cases = [c for c in cases if c["id"] in args.case]
        if {c["id"] for c in cases} != set(args.case):
            p.error("unknown case ID")
    if not cases or len({c["id"] for c in cases}) != len(cases):
        p.error("cases must be nonempty and unique")
    root = args.skill_root.resolve()
    source = fingerprint(root)
    for c in cases:
        if not (root / OWNER[c["id"].split("-", 1)[0]]).is_file():
            p.error("case owner missing from selected checkout")
    version = subprocess.check_output([executable, "--version"], text=True).strip()
    profile = {"executable": executable, "version": version, "provider": args.provider,
               "model": args.model, "thinking": "low", "timeout_seconds": args.timeout,
               "concurrency": args.concurrency, "tools": ["read", "grep", "find", "ls"]}
    args.output.mkdir(parents=True, exist_ok=False)
    save_new(args.output / "metadata.json", {"profile": profile, "skill_root": str(root),
             "manifest_path": str(package_manifest(root)),
             "source": source, "runner_sha256": digest(Path(__file__).read_bytes()),
             "cases": [{"id": c["id"], "prompt_sha256": digest(c["prompt"].encode())} for c in cases],
             "limits": "Single model/sample per case; successful execution is not a reviewed PASS; no media actions."})
    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        pending = {pool.submit(execute, c, root, args.output, profile, source["sha256"]): c["id"] for c in cases}
        for f in as_completed(pending):
            result = f.result()
            results.append(result)
            print(f"{result['id']}: {result['status']} / UNREVIEWED", flush=True)
    results.sort(key=lambda x: x["id"])
    save_new(args.output / "execution-summary.json", {"cases": results, "review_status": "UNREVIEWED"})
    return 0 if all(r["status"] == "completed" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
