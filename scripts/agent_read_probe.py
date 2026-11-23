#!/usr/bin/env python3
"""Real-agent read probe for the creative-production entry and craft bridge.

Installs the package into a temp dir, runs each case in
``creative-production/evals/agent-read-probes.json`` through
``pi --print --mode json`` with read-only tools, and records which installed
files the agent opened. Opened paths are install-relative. Raw JSONL stays in
the temp dir and is not written to ``--out``.

Verdicts: positive passes when any ``expect_any_read`` file was opened, no
``expect_none_read`` file was opened, and every ``expect_text`` group (a list of
alternatives) has one alternative in the final answer;
negative passes when ``creative-production/SKILL.md`` was not opened. Every
non-negative case also fails when the answer ends with an optional offer
(``closing_check.find_optional_offer``). Nonstop (s1) passes only when the entry
skill was opened, there is no optional offer, the last line is a contract closing
line (``다음: … — 자동 진행`` or ``대기: … — 필요: …``), the answer contains
storyboard/shot-list content, it makes no completion claim, nothing follows the
closing line, and a ``대기:`` reason is on the allowed list
(``closing_check.wait_reason_allowed``). The closing line must match exactly one of
the two patterns (no hedges, no mixed forms), and a paid-execution ``대기:`` without
storyboard/shot-list content fails.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import closing_check

DEFAULT_CASES = ROOT / "creative-production" / "evals" / "agent-read-probes.json"
KINDS = ("positive", "negative", "nonstop")
ENTRY_SKILL = "creative-production/SKILL.md"
OPENING_TOOLS = ("read", "grep")
TIMEOUT_SECONDS = 900
DEFAULT_MODEL = "anthropic/claude-sonnet-5-5"
NONSTOP_KEYWORDS = {
    "기획": ("기획",),
    "대본": ("대본", "스크립트"),
    "콘티": ("콘티", "스토리보드"),
    "실행 승인 요청": ("승인", "진행할까", "진행해도"),
}
STORYBOARD_KEYWORDS = ("스토리보드", "샷 리스트", "샷 명세", "샷 목록", "shot list", "콘티")
COMPLETION_CLAIMS = ("생성했습니다", "생성 완료", "렌더 완료", "렌더링 완료", "제작 완료", "만들었습니다")


@dataclass
class ParsedRun:
    calls: list[tuple[str, str]] = field(default_factory=list)
    opened: list[str] = field(default_factory=list)
    final: str = ""


def load_cases(path: Path = DEFAULT_CASES) -> list[dict]:
    cases = json.loads(Path(path).read_text(encoding="utf-8"))["cases"]
    seen: set[str] = set()
    for case in cases:
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
        if case["kind"] not in KINDS:
            raise ValueError(f"{case['id']}: unknown kind {case['kind']}")
    return cases


def _relative(raw: str, install_root: Path) -> str:
    path = Path(raw)
    if path.is_absolute():
        for root in (install_root, install_root.resolve()):
            try:
                return path.relative_to(root).as_posix()
            except ValueError:
                continue
    return path.as_posix().removeprefix("./")


def parse_events(lines, install_root: Path) -> ParsedRun:
    """Extract tool calls and the last assistant text from ``pi --mode json`` lines."""
    run = ParsedRun()
    for line in lines:
        if not line.strip().startswith("{"):
            continue
        event = json.loads(line)
        if event.get("type") == "tool_execution_start":
            args = event.get("args", {})
            tool = event["toolName"]
            target = args.get("path") or args.get("pattern") or ""
            target = _relative(target, install_root) if args.get("path") else str(target)
            run.calls.append((tool, target))
            if tool in OPENING_TOOLS and args.get("path"):
                run.opened.append(target)
        elif event.get("type") == "message_end":
            message = event.get("message", {})
            if message.get("role") == "assistant":
                text = "".join(
                    part.get("text", "")
                    for part in message.get("content", [])
                    if part.get("type") == "text"
                )
                if text:
                    run.final = text
    return run


def render_reads(run: ParsedRun) -> str:
    return "".join(f"  {tool}: {target}\n" for tool, target in run.calls)


def nonstop_hints(final: str) -> str:
    found = [name for name, words in NONSTOP_KEYWORDS.items() if any(w in final for w in words)]
    missing = [name for name in NONSTOP_KEYWORDS if name not in found]
    claims = [w for w in COMPLETION_CLAIMS if w in final]
    return (
        f"키워드 확인 {found}, 누락 {missing}, 생성 완료 주장 표현 {claims or '없음'}"
    )


def judge(case: dict, opened: list[str], final: str) -> tuple[bool | None, str]:
    opened_set = set(opened)
    kind = case["kind"]
    if kind == "negative":
        if ENTRY_SKILL in opened_set:
            return False, f"{ENTRY_SKILL} opened"
        return True, f"{ENTRY_SKILL} not opened"
    offer = closing_check.find_optional_offer(final)
    if kind == "positive":
        hits = [p for p in case["expect_any_read"] if p in opened_set]
        if not hits:
            return False, f"none of {case['expect_any_read']} opened"
        forbidden = [p for p in case.get("expect_none_read", []) if p in opened_set]
        if forbidden:
            return False, f"must not open {forbidden}"
        missing = [group for group in case.get("expect_text", []) if not any(word in final for word in group)]
        if missing:
            return False, f"answer lacks {missing}"
        if offer:
            return False, f"optional offer ending: {offer!r}"
        defect = closing_check.closing_defect(final)
        if defect:
            return False, defect
        return True, f"opened {hits}"
    if ENTRY_SKILL not in opened_set:
        return False, f"{ENTRY_SKILL} not opened"
    problems = []
    if offer:
        problems.append(f"optional offer ending: {offer!r}")
    form = closing_check.closing_form(final)
    if form is None:
        problems.append("last line is not a 다음:/대기: closing line")
        defect = closing_check.closing_defect(final)
        if defect:
            problems.append(defect)
    trailing = closing_check.text_after_closing(final)
    if trailing:
        problems.append(f"text after closing line: {trailing!r}")
    bad_wait = closing_check.disallowed_wait_reason(final)
    if bad_wait:
        problems.append(f"disallowed 대기 reason: {bad_wait!r}")
    if not any(word in final for word in STORYBOARD_KEYWORDS):
        if closing_check.is_paid_execution_wait(final):
            problems.append("paid-execution 대기 without storyboard/shot-list content")
        else:
            problems.append("no storyboard/shot-list content")
    claims = [w for w in COMPLETION_CLAIMS if w in final]
    if claims:
        problems.append(f"completion claim {claims}")
    if problems:
        return False, f"{'; '.join(problems)} — {nonstop_hints(final)}"
    note = closing_check.blocking_on_placeholderable_fact(final)
    suffix = f" (주의: 자리표시자로 둘 수 있는 사실에서 대기 {note!r})" if note else ""
    return True, f"closing={form}, storyboard content, no offer, no completion claim{suffix} — {nonstop_hints(final)}"


def run_case(case: dict, suffix: str, install: Path, sandbox: Path, raw_dir: Path, model: str) -> dict:
    prompt = f"{case['prompt']} {suffix}"
    command = [
        "pi", "--print", "--mode", "json", "--no-skills", "--skill", str(install),
        "--tools", "read,ls,find,grep", "--model", model, prompt,
    ]
    raw = raw_dir / f"{case['id']}.jsonl"
    try:
        with raw.open("w", encoding="utf-8") as handle:
            subprocess.run(
                command, cwd=sandbox, stdout=handle, stderr=subprocess.STDOUT,
                timeout=TIMEOUT_SECONDS, check=False,
            )
    except subprocess.TimeoutExpired:
        return {"id": case["id"], "kind": case["kind"], "opened": [], "pass": False,
                "reason": f"timeout after {TIMEOUT_SECONDS}s", "run": ParsedRun()}
    run = parse_events(raw.read_text(encoding="utf-8").splitlines(), install)
    if not run.final:
        return {"id": case["id"], "kind": case["kind"], "opened": run.opened, "pass": False,
                "reason": "no final answer in pi output", "run": run}
    verdict, reason = judge(case, run.opened, run.final)
    return {"id": case["id"], "kind": case["kind"], "opened": run.opened,
            "pass": verdict, "reason": reason, "run": run}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--only", default="", help="comma-separated case ids")
    parser.add_argument("--jobs", type=int, default=5)
    args = parser.parse_args(argv)

    spec = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = load_cases(args.cases)
    if args.only:
        wanted = [item for item in args.only.split(",") if item]
        unknown = set(wanted) - {case["id"] for case in cases}
        if unknown:
            parser.error(f"unknown case ids: {sorted(unknown)}")
        cases = [case for case in cases if case["id"] in wanted]
    args.out.mkdir(parents=True, exist_ok=True)

    import install_package

    with tempfile.TemporaryDirectory(prefix="agent-probe-") as tmp:
        tmp_path = Path(tmp)
        install = tmp_path / "skills"
        install_package.install(install, repo_root=ROOT, exclude_derived_support=True)
        sandbox = tmp_path / "sandbox"
        raw_dir = tmp_path / "raw"
        sandbox.mkdir()
        raw_dir.mkdir()
        with ThreadPoolExecutor(max_workers=max(1, min(args.jobs, 5))) as pool:
            results = list(pool.map(
                lambda case: run_case(case, spec["suffix"], install, sandbox, raw_dir, args.model),
                cases,
            ))

    summary = []
    for result in results:
        run = result.pop("run")
        (args.out / f"{result['id']}.reads.txt").write_text(render_reads(run), encoding="utf-8")
        (args.out / f"{result['id']}.final.md").write_text(run.final, encoding="utf-8")
        summary.append(result)
    (args.out / "summary.json").write_text(
        json.dumps({"model": args.model, "results": summary}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for item in summary:
        print(f"{item['id']:3} {item['kind']:8} pass={item['pass']} {item['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
