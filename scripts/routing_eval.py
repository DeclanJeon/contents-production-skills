# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Measured routing accuracy for the layered router.

Unlike `routing_regression.py` (a structural bench proving the CSV and the
frozen case list agree), this dispatches each case prompt to a real agent in an
isolated read-only sandbox that contains ONLY the router frontier
(`creative-production/SKILL.md` + `references/routing.csv`) plus the owner
SKILL.md files the router may name. The agent must answer with one route_id.

What this measures, honestly:

- `accuracy`: chosen route_id == expected route_id.
- `near_miss`: wrong route, but the two rows share `media_axis` and a
  same-owner or same-deliverable-family relationship.
- `dangerous`: wrong route that crosses the media/authority axis (e.g. a
  text-only request routed to an executed-media route). These are the
  expensive errors; they are reported separately and never averaged away.

The harness never writes into the repo, never installs anything, and never
claims LLM output as package truth. It stores exact prompts and raw wire.

Requires an authenticated Codex CLI.

Run:
    python3 scripts/routing_eval.py --limit 3          # smoke
    python3 scripts/routing_eval.py --out qa/routing-eval-<date>
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
ROUTING_CSV: Final = ROOT / "creative-production/references/routing.csv"
CASES: Final = ROOT / "creative-production/evals/routing-cases.json"
ROUTER_SKILL: Final = ROOT / "creative-production/SKILL.md"

# Frontier the agent is allowed to read: the router itself plus every owner's
# SKILL.md, which is what a real coordinator would open next. Nothing else.
FRONTIER_FILES: Final = (
    "creative-production/SKILL.md",
    "creative-production/references/routing.csv",
)

INSTRUCTION: Final = """\
You are routing one user request for a video-production skill package.

Read `creative-production/references/routing.csv` and
`creative-production/SKILL.md`. Then decide which single `route_id` applies.

Rules:
- Judge by the three slots in the CSV: deliverable_kind, media_axis
  (text_only / none_or_stills / executed_media / varies), authority_axis.
- Default to `text_only` unless the request actually permits generated media or
  an actual edit.
- Do not pick a route because keywords are similar. Pick the narrowest route
  whose deliverable matches what was asked for.
- Use `UNASSIGNED` only if no route fits.

Answer with ONE line in exactly this form and nothing else:
ROUTE: <route_id>
WHY: <under 15 words>

User request:
"""


def scratch_root() -> Path:
    """Prefer real disk over a possibly full tmpfs."""
    override = os.environ.get("ROUTING_EVAL_TMP")
    if override:
        Path(override).mkdir(parents=True, exist_ok=True)
        return Path(override)
    for candidate in (Path("/var/tmp"), ROOT / ".routing-eval-tmp"):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".probe"
            probe.write_text("x", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError:
            continue
    return Path(tempfile.gettempdir())


def load_routes() -> dict[str, dict[str, str]]:
    with ROUTING_CSV.open(encoding="utf-8", newline="") as handle:
        return {row["route_id"]: row for row in csv.DictReader(handle)}


def load_cases() -> list[dict[str, str]]:
    return json.loads(CASES.read_text(encoding="utf-8"))["cases"]


def build_sandbox(dest: Path, owner_skills: set[str]) -> None:
    """Copy only the router frontier and the named owner SKILL.md files."""
    for rel in FRONTIER_FILES:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    for owner in owner_skills:
        src = ROOT / owner / "SKILL.md"
        if src.exists():
            target = dest / owner / "SKILL.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
    # Copy the frontier into <sandbox>/skills/creative-production as well, so a
    # skill-style lookup finds the fixture instead of the real installation.
    skill_root = dest / "skills" / "creative-production"
    (skill_root / "references").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROUTER_SKILL, skill_root / "SKILL.md")
    shutil.copy2(ROUTING_CSV, skill_root / "references" / "routing.csv")

    # Sealed CODEX_HOME: auth only, so ~/.codex/skills is invisible.
    home = dest / ".codex-home"
    home.mkdir(parents=True, exist_ok=True)
    (home / "skills").mkdir(exist_ok=True)
    auth = Path.home() / ".codex/auth.json"
    if auth.is_file():
        target = home / "auth.json"
        shutil.copy2(auth, target)
        target.chmod(0o600)

    (dest / "AGENTS.md").write_text(
        "# Routing fixture\n\n"
        "This directory is a self-contained, read-only routing fixture.\n\n"
        "Read ONLY these paths, and never any path outside this directory:\n"
        "- `creative-production/SKILL.md`\n"
        "- `creative-production/references/routing.csv`\n"
        "- `skills/creative-production/SKILL.md` (same content)\n"
        "- `skills/creative-production/references/routing.csv` (same content)\n\n"
        "Do NOT read `~/.codex/skills`, `~/.agents`, or any installed copy.\n"
        "Answer only with the ROUTE/WHY lines requested. Do not write files.\n",
        encoding="utf-8",
    )


def normalise_route(raw: str) -> str | None:
    """Accept `R13`, `R13 - one_production_asset`, `r13.` or `**R13**`."""
    match = ROUTE_TOKEN.search(raw.upper())
    if match:
        return match.group(1)
    if raw.strip().upper().startswith("UNASSIGNED"):
        return "UNASSIGNED"
    return None


def kill_group(process: "subprocess.Popen[str]") -> None:
    """Kill the child and everything it spawned."""
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):  # already gone
        process.kill()


def run_bounded(
    command: list[str], stdin_text: str, timeout: int, env: dict[str, str]
) -> tuple[str, str, int]:
    """Run a command with a hard deadline, capturing output through files.

    Two failure modes are being defended against, both observed in practice:

    1. A sweep stalled indefinitely at case B06 even though ``--timeout`` was
       set. Anything that waits for the stdout pipe to reach EOF can stall
       forever when a descendant keeps the inherited descriptor open, and
       ``subprocess.run(timeout=...)`` re-enters ``communicate()`` after it
       kills the direct child, so it can stall there too.
    2. Killing only the direct child leaves codex's own children running.

    So: capture through temporary files (no EOF to wait for), put the child in
    its own session, and kill the whole group on overrun. Raises TimeoutError so
    the caller records ``timeout`` rather than confusing it with a crash.
    """
    with tempfile.TemporaryDirectory(prefix="run-") as scratch:
        out_path = Path(scratch) / "stdout"
        err_path = Path(scratch) / "stderr"
        stdin_path = Path(scratch) / "stdin"
        stdin_path.write_text(stdin_text, encoding="utf-8")
        with out_path.open("wb") as out_file, err_path.open("wb") as err_file, \
                stdin_path.open("rb") as stdin_file:
            process = subprocess.Popen(
                command,
                stdin=stdin_file,
                stdout=out_file,
                stderr=err_file,
                env=env,
                start_new_session=True,
            )
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                kill_group(process)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:  # pragma: no cover - killpg failed
                    pass
                raise TimeoutError(f"codex exec exceeded {timeout}s") from None
        # Files are closed, so this cannot block on a surviving descendant.
        out = out_path.read_bytes().decode("utf-8", "replace")
        err = err_path.read_bytes().decode("utf-8", "replace")
    return out, err, process.returncode


def dispatch(prompt: str, sandbox: Path, model: str, timeout: int) -> tuple[str, str]:
    """Return (raw_wire, agent_text). Raises on dispatch failure."""
    command = [
        "codex", "exec",
        "--skip-git-repo-check",
        "--ignore-user-config",
        "--json",
        "-s", "read-only",
        "-C", str(sandbox),
        "-m", model,
        # Isolate from the real install so the measurement only sees the fixture.
        # Shell stays enabled because the fixture must be readable; containment
        # comes from -C <sandbox>, -s read-only and leaked_outside() auditing.
        "-c", f'skills.search_dirs=["{sandbox / "skills"}"]',
        "-c", "mcp_servers={}",
        "-",  # read the prompt from stdin
    ]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    # Point CODEX_HOME at the fixture so the installed skill tree is not even
    # discoverable. Only auth.json is carried over, which is what the CLI needs;
    # no user config, no installed skills, no MCP state.
    sealed_home = sandbox / ".codex-home"
    if sealed_home.is_dir():
        env["CODEX_HOME"] = str(sealed_home)
    stdout, stderr, returncode = run_bounded(command, prompt, timeout, env)
    wire = stdout + stderr
    texts: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        if item.get("type") == "agent_message" and item.get("text"):
            texts.append(item["text"])
    if returncode != 0 and not texts:
        raise RuntimeError(f"codex exit {returncode}: {wire[-800:]}")
    return wire, "\n".join(texts)


def parse_route(text: str) -> tuple[str | None, str]:
    route = None
    why = ""
    for line in text.splitlines():
        stripped = line.strip().strip("*` ")
        upper = stripped.upper()
        if upper.startswith("ROUTE:"):
            route = stripped.split(":", 1)[1].strip().strip("*` ").strip()
        elif upper.startswith("WHY:"):
            why = stripped.split(":", 1)[1].strip()
    if route:
        return normalise_route(route), why
    # Fallback: agents sometimes answer bare, e.g.
    # "R13 - one_production_asset - text_only ...".
    match = ROUTE_TOKEN.search(text.upper())
    if match:
        return match.group(1), ""
    return None, why


def resolve_owner_answer(text: str, routes: dict[str, dict[str, str]]) -> list[str]:
    """Route ids matching an owner-name answer, so the sweep can report it."""
    lowered = text.lower()
    by_owner: dict[str, list[str]] = {}
    for route_id, row in routes.items():
        by_owner.setdefault(row["owner"], []).append(route_id)
    return sorted(
        f"{owner}={ids}"
        for owner, ids in by_owner.items()
        if owner.lower() in lowered
    )


ROUTE_TOKEN: Final = re.compile(r"\b(R\d{2})\b")


READER: Final = re.compile(r"\b(?:cat|head|tail|less|bat|sed|awk|grep|wc)\b")


def read_paths(wire: str) -> list[str]:
    """File paths the agent actually asked a reader tool to open.

    Shell wrappers (`/usr/bin/bash -lc '...'`) are unwrapped first so that the
    program name is not mistaken for a file path.
    """
    found: list[str] = []
    for line in wire.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") or {}
        command = item.get("command") or ""
        if not command:
            continue
        inner = re.search(r"-lc\s+'([^']*)'", command)
        script = inner.group(1) if inner else command
        for chunk in re.split(r"[;|&]+", script):
            parts = chunk.split()
            if not parts or not READER.search(parts[0]):
                if not any(READER.fullmatch(part) for part in parts):
                    continue
            for token in parts:
                token = token.strip("'\"")
                if token.endswith((".md", ".csv")):
                    found.append(token)
    return sorted(set(found))


def leaked_outside(files: list[str], sandbox: Path) -> list[str]:
    """Paths read outside the fixture, which invalidate the measurement."""
    sandbox = sandbox.resolve()
    leaks = []
    for path in files:
        if not (path.endswith(".md") or path.endswith(".csv")):
            continue
        # Relative paths are already sandbox-relative (the agent runs with -C).
        if not Path(path).is_absolute():
            continue
        try:
            resolved = Path(path).resolve()
        except OSError:
            continue
        if not resolved.is_relative_to(sandbox):
            leaks.append(path)
    return leaks


def classify(chosen: str | None, expected: str, routes: dict[str, dict[str, str]]) -> str:
    if chosen == expected:
        return "correct"
    if chosen is None or chosen == "UNASSIGNED":
        return "unanswered"
    if chosen not in routes or expected not in routes:
        return "invalid"
    got, want = routes[chosen], routes[expected]
    media_cross = got["media_axis"] != want["media_axis"]
    authority_cross = bool(got["authority_axis"]) != bool(want["authority_axis"])
    if media_cross or authority_cross:
        return "dangerous"
    return "near_miss"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="output directory for prompts and raw wire")
    parser.add_argument("--limit", type=int, help="run only the first N cases")
    parser.add_argument("--case", action="append", help="run only these case_ids")
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--repeat", type=int, default=1,
        help="run each case N times to measure answer stability (default 1)",
    )
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be >= 1")

    if shutil.which("codex") is None:
        print("BLOCKED: codex CLI not installed; routing accuracy not measured.", file=sys.stderr)
        return 2

    routes = load_routes()
    cases = load_cases()
    if args.case:
        wanted = set(args.case)
        cases = [c for c in cases if c["case_id"] in wanted]
    if args.limit:
        cases = cases[: args.limit]
    if not cases:
        print("no cases selected", file=sys.stderr)
        return 2

    outdir = Path(args.out) if args.out else None
    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    owners = {row["owner"] for row in routes.values() if row["owner"] != "UNASSIGNED"}
    per_case: dict[str, dict[str, object]] = {}
    tally: dict[str, int] = {}
    trial_log: list[tuple[str, dict[str, object]]] = []

    def record_trial(case: dict[str, str], trial: dict[str, object]) -> None:
        entry = per_case.setdefault(case["case_id"], {
            "case_id": case["case_id"],
            "prompt": case["prompt"],
            "expected": case["expected_owner"],
            "expected_route": case["route_id"],
            "trials": [],
        })
        entry["trials"].append(trial)  # type: ignore[union-attr]
        verdict = str(trial["verdict"])
        tally[verdict] = tally.get(verdict, 0) + 1
        trial_log.append((case["case_id"], trial))

    with tempfile.TemporaryDirectory(prefix="routing-eval-", dir=scratch_root()) as tmp:
        sandbox = Path(tmp) / "fixture"
        sandbox.mkdir()
        build_sandbox(sandbox, owners)

        # Round-robin the repeats so any drift over wall-clock time is spread
        # across cases instead of landing on the last case of each repetition.
        total = len(cases) * args.repeat
        done = 0
        for repeat_index in range(args.repeat):
            for case in cases:
                done += 1
                prompt = INSTRUCTION + case["prompt"].strip() + "\n"
                trial: dict[str, object] = {"trial": repeat_index + 1}
                try:
                    wire, text = dispatch(prompt, sandbox, args.model, args.timeout)
                    chosen, why = parse_route(text)
                    verdict = classify(chosen, case["route_id"], routes)
                    reads = read_paths(wire)
                    leaks = leaked_outside(reads, sandbox)
                    if leaks:
                        # A leaked read means the fixture was bypassed; not a valid vote.
                        verdict = "isolation_leak"
                    if chosen is None:
                        trial["owner_answers"] = resolve_owner_answer(text, routes)
                    trial.update(chosen_route=chosen, why=why, verdict=verdict,
                                 agent_text=text, reads=reads, leaks=leaks)
                    if outdir:
                        suffix = "" if args.repeat == 1 else f".t{repeat_index + 1}"
                        (outdir / f"{case['case_id']}{suffix}.wire.jsonl").write_text(
                            wire, encoding="utf-8")
                    mark = "OK  " if verdict == "correct" else "MISS"
                    print(f"[{done}/{total}] {mark} {case['case_id']} "
                          f"t{repeat_index + 1} expected={case['route_id']} "
                          f"got={chosen} ({verdict})", flush=True)
                except Exception as error:  # noqa: BLE001 - record, do not crash the sweep
                    timed_out = isinstance(error, TimeoutError)
                    trial.update(chosen_route=None,
                                 verdict="timeout" if timed_out else "dispatch_error",
                                 error=str(error)[:400])
                    label = "TIME" if timed_out else "ERR "
                    print(f"[{done}/{total}] {label} {case['case_id']} "
                          f"t{repeat_index + 1}: {error}"[:300], flush=True)
                record_trial(case, trial)

    # --- per-case stability -------------------------------------------------
    results: list[dict[str, object]] = []
    flaky: list[str] = []
    unstable_verdict: list[str] = []
    for entry in per_case.values():
        trials = entry["trials"]  # type: ignore[index]
        choices = [str(t.get("chosen_route")) for t in trials]
        verdicts = [str(t["verdict"]) for t in trials]
        distinct = sorted(set(choices))
        correct_votes = verdicts.count("correct")
        # A case is stable only if every trial chose the same route.
        stable = len(distinct) == 1
        if not stable:
            flaky.append(str(entry["case_id"]))
        if len(set(verdicts)) > 1:
            unstable_verdict.append(str(entry["case_id"]))
        entry["distinct_routes"] = distinct
        entry["correct_votes"] = correct_votes
        entry["trials_run"] = len(trials)
        entry["stable"] = stable
        entry["judgement"] = (
            "stable_correct" if stable and correct_votes == len(trials)
            else "stable_wrong" if stable
            else "flaky"
        )
        entry["chosen_route"] = distinct[0] if stable else choices[0]
        entry["verdict"] = verdicts[0] if stable else "flaky"
        results.append(entry)

    attempts = sum(v for v in tally.values())
    correct = tally.get("correct", 0)
    stable_correct = [r["case_id"] for r in results if r["judgement"] == "stable_correct"]
    stable_wrong = [r["case_id"] for r in results if r["judgement"] == "stable_wrong"]
    dangerous_cases = sorted({
        str(entry["case_id"])
        for entry in results
        for trial in entry["trials"]  # type: ignore[union-attr]
        if trial.get("verdict") == "dangerous"
    })

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": args.model,
        "package_version": json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["version"],
        "repeat": args.repeat,
        "cases": len(results),
        "attempts": attempts,
        "correct": correct,
        "accuracy": round(correct / attempts, 3) if attempts else 0.0,
        "stable_cases": len(stable_correct) + len(stable_wrong),
        "stable_correct": len(stable_correct),
        "stable_accuracy": round(len(stable_correct) / len(results), 3) if results else 0.0,
        "stable_wrong": stable_wrong,
        "flaky": flaky,
        "unstable_verdict": unstable_verdict,
        "tally": tally,
        "dangerous": dangerous_cases,
        "note": "LLM output is measurement only, never package truth.",
        "results": results,
    }
    if outdir:
        (outdir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"accuracy        {correct}/{attempts} attempts = {summary['accuracy']:.1%}  "
          f"model={args.model}  repeat={args.repeat}")
    print(f"stable accuracy {summary['stable_correct']}/{len(results)} cases = "
          f"{summary['stable_accuracy']:.1%}")
    print(f"tally           {dict(sorted(tally.items()))}")
    if summary["dangerous"]:
        print(f"DANGEROUS cases: {', '.join(map(str, summary['dangerous']))}")
    if stable_wrong:
        print(f"stably WRONG:    {', '.join(map(str, stable_wrong))}")
    if flaky:
        print(f"FLAKY (route changed between trials): {', '.join(flaky)}")
        for entry in results:
            if entry["case_id"] in flaky:
                print(f"   {entry['case_id']}: {entry['distinct_routes']} "
                      f"expected={entry['expected_route']}")
    if outdir:
        print(f"wrote {outdir}/summary.json")
    return 0 if not dangerous_cases else 1


if __name__ == "__main__":
    raise SystemExit(main())
