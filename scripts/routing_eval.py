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

    "creative-production/references/routing-disambiguation.csv",
)

INSTRUCTION: Final = """\
You are routing one user request for a video-production skill package.

Read `creative-production/SKILL.md` and do exactly what its routing step says,
including every file that step tells you to read. The skill decides what to
read; this instruction deliberately names no other file, because naming them
here would let the router skip its own reading list and still score well.

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


def build_sandbox(dest: Path, owner_skills: set[str],
                  full_package: bool = False) -> None:
    """Copy the router frontier and owner skills.

    With `full_package`, every skill's SKILL.md and references/ come along, so a
    handoff run can open whichever owner it chose -- including a wrong one. If
    only the expected owner were present, "did it read the owner skill" would be
    unmeasurable for exactly the cases where it matters.
    """
    for rel in FRONTIER_FILES:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    if full_package:
        for skill_dir in sorted(ROOT.iterdir()):
            if not (skill_dir / "SKILL.md").is_file():
                continue
            (dest / skill_dir.name).mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_dir / "SKILL.md", dest / skill_dir.name / "SKILL.md")
            refs = skill_dir / "references"
            if refs.is_dir():
                shutil.copytree(refs, dest / skill_dir.name / "references",
                                dirs_exist_ok=True)
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
    disambiguation = ROOT / "creative-production/references/routing-disambiguation.csv"
    if disambiguation.exists():
        shutil.copy2(disambiguation, skill_root / "references" / disambiguation.name)

    # Sealed CODEX_HOME: auth only, so ~/.codex/skills is invisible.
    home = dest / ".codex-home"
    home.mkdir(parents=True, exist_ok=True)
    (home / "skills").mkdir(exist_ok=True)
    auth = Path.home() / ".codex/auth.json"
    if auth.is_file():
        target = home / "auth.json"
        shutil.copy2(auth, target)
        target.chmod(0o600)

    # The allowlist is derived from FRONTIER_FILES, never typed out by hand.
    # A hardcoded list silently omitted the disambiguation table, and some runs
    # then refused to route at all ("required ... is outside the permitted
    # reading list") while others ignored the restriction, making the failure
    # intermittent and the score meaningless.
    allowed = list(FRONTIER_FILES)
    extra = ""
    if full_package:
        extra = ("\nEvery skill in this fixture is a real copy. When the router\n"
                 "names an owner SKILL.md or a required_read path, read that path\n"
                 "here, under this directory.\n")
    (dest / "AGENTS.md").write_text(
        "# Routing fixture\n\n"
        "This directory is a self-contained, read-only routing fixture.\n\n"
        "Read ONLY paths inside this directory, and never any path outside it.\n"
        "Start from:\n"
        + "".join(f"- `{rel}`\n" for rel in allowed)
        + "".join(f"- `skills/{rel}` (same content)\n" for rel in allowed)
        + extra
        + "\nDo NOT read `~/.codex/skills`, `~/.agents`, or any installed copy.\n"
        "Answer only in the requested format. Do not write files.\n",
        encoding="utf-8",
    )


HANDOFF_INSTRUCTION: Final = """\
You are the video-production coordinator handling one user request.

Read `creative-production/SKILL.md` and do exactly what its routing step says,
including every file that step tells you to read. That step also tells you which
owner skill to read once a route is chosen; follow it. The skill decides what to
read; this instruction deliberately names no file, because naming them here lets
the coordinator skip its own reading list and still look correct.

Then answer in exactly this form and nothing else:
ROUTE: <route_id>
SLOTS: <deliverable_kind> | <media_axis> | <authority_axis>
ARTIFACT: <the one artifact you will produce, under 20 words>

User request:
"""


def parse_handoff(text: str) -> dict[str, str]:
    """Pull the three declared slots and the promised artifact out of an answer."""
    fields = {"route": "", "slots": "", "artifact": ""}
    for line in text.splitlines():
        stripped = line.strip().strip("*` ")
        upper = stripped.upper()
        for key, prefix in (("route", "ROUTE:"), ("slots", "SLOTS:"),
                            ("artifact", "ARTIFACT:")):
            if upper.startswith(prefix):
                fields[key] = stripped.split(":", 1)[1].strip().strip("*` ").strip()
    return fields


EMPTY_AUTHORITY: Final = frozenset({"none", "n/a", "na", "-", "empty", "no"})
CONCRETE_MEDIA: Final = frozenset({"text_only", "none_or_stills", "executed_media"})


def handoff_checks(chosen: str | None, expected: str, routes: dict[str, dict[str, str]],
                   parsed: dict[str, str], reads: list[str]) -> dict[str, object]:
    """Did the route actually reach the right skill and the right requirement?

    Route accuracy only says the label was right. These checks say whether the
    coordinator opened the owner skill it just selected, opened the references
    that row lists, and named the deliverable that row promises.
    """
    read_set = {path.strip().lstrip("./") for path in reads}
    owner = routes.get(chosen, {}).get("owner", "") if chosen else ""
    owner_skill = f"{owner}/SKILL.md"
    required = [
        part.strip()
        for part in (routes.get(chosen, {}).get("required_read") or "").split(";")
        if part.strip()
    ]
    missing = [part for part in required if part.lstrip("./") not in read_set]
    declared = [part.strip() for part in parsed.get("slots", "").split("|")]
    want = routes.get(expected, {})
    slots_match = False
    if len(declared) == 3:
        # "none", "n/a", "-" all mean "no approvals supplied"; treating the word
        # as a truthy approval made four correct answers look wrong.
        authority = declared[2].lower()
        declared_authority = "" if authority in EMPTY_AUTHORITY else authority
        # A row whose media_axis is `varies` spans axes on purpose, so any single
        # concrete axis the coordinator commits to is a reading of the row, not a
        # contradiction of it.
        declared_media = declared[1].lower()
        media_ok = declared[1] == want.get("media_axis", "") or (
            want.get("media_axis") == "varies"
            and declared_media in CONCRETE_MEDIA
        )
        slots_match = (
            declared[0] == want.get("deliverable_kind", "")
            and media_ok
            and bool(declared_authority) == bool(want.get("authority_axis", ""))
        )
    return {
        "owner_loaded": bool(owner) and owner_skill in read_set,
        "required_read_missing": missing,
        "slots_match": slots_match,
        "slots_declared": parsed.get("slots", ""),
        "artifact": parsed.get("artifact", ""),
    }


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
    # Scratch goes to real disk, not a possibly-full tmpfs: capture can be large.
    with tempfile.TemporaryDirectory(prefix="run-", dir=scratch_root()) as scratch:
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


INFRA_VERDICTS: Final = frozenset({"dispatch_error", "timeout"})


def dispatch_with_retries(
    prompt: str,
    sandbox: Path,
    model: str,
    timeout: int,
    retries: int,
    trial: dict[str, object],
) -> tuple[str, str]:
    """Retry a dispatch that failed for infrastructure reasons.

    A long sweep meets transient backend failures: `codex exit 101` with MCP
    transport errors, or a run that simply overruns. Those are not routing
    opinions and must not be scored as wrong answers, so they are retried.
    A wrong *route* is never retried -- that would be re-rolling the dice until
    the table looks good.
    """
    attempts: list[str] = []
    for attempt in range(retries + 1):
        try:
            return dispatch(prompt, sandbox, model, timeout)
        except Exception as error:  # noqa: BLE001 - classified by the caller
            attempts.append(("timeout: " if isinstance(error, TimeoutError) else "") +
                            str(error)[:200])
            # A TimeoutError is infrastructure; any other exception is retried
            # once more only because codex exits nonzero on transport faults.
            if attempt >= retries:
                raise
            print(f"      retry {attempt + 1}/{retries} after: {attempts[-1][:90]}",
                  flush=True)
    raise RuntimeError("unreachable")  # pragma: no cover


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="output directory for prompts and raw wire")
    parser.add_argument("--limit", type=int, help="run only the first N cases")
    parser.add_argument("--case", action="append", help="run only these case_ids")
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument(
        "--stage", choices=("route", "handoff"), default="route",
        help="route: stop at the route_id. handoff: also demand the three slots, "
             "the assigned artifact, and the owner skill that route names.")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--retries", type=int, default=2,
        help="re-dispatch infrastructure failures (exit 101, timeout) up to N times",
    )
    parser.add_argument(
        "--repeat", type=int, default=1,
        help="run each case N times to measure answer stability (default 1)",
    )
    args = parser.parse_args(argv)
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
        build_sandbox(sandbox, owners, full_package=args.stage == "handoff")

        # Round-robin the repeats so any drift over wall-clock time is spread
        # across cases instead of landing on the last case of each repetition.
        total = len(cases) * args.repeat
        done = 0
        for repeat_index in range(args.repeat):
            for case in cases:
                done += 1
                instruction = (HANDOFF_INSTRUCTION if args.stage == "handoff"
                               else INSTRUCTION)
                prompt = instruction + case["prompt"].strip() + "\n"
                trial: dict[str, object] = {"trial": repeat_index + 1}
                try:
                    wire, text = dispatch_with_retries(
                        prompt, sandbox, args.model, args.timeout, args.retries, trial)
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
                    if args.stage == "handoff":
                        parsed = parse_handoff(text)
                        checks = handoff_checks(chosen, case["route_id"], routes,
                                                parsed, reads)
                        trial.update(handoff=checks)
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
        # Crashes and timeouts are not opinions about routing. Judging a case
        # on them produced a "stably WRONG" list made entirely of exit-101
        # failures, which is exactly backwards: nothing was answered at all.
        valid = [t for t in trials if str(t["verdict"]) not in INFRA_VERDICTS]
        choices = [str(t.get("chosen_route")) for t in valid if t.get("chosen_route")]
        verdicts = [str(t["verdict"]) for t in valid]
        distinct = sorted(set(choices))
        correct_votes = verdicts.count("correct")
        # A case is stable only if every answered trial chose the same route.
        stable = len(distinct) == 1
        if not valid:
            judgement = "no_data"
        elif not choices:
            judgement = "unanswered"
        elif not stable:
            judgement = "flaky"
            flaky.append(str(entry["case_id"]))
        elif correct_votes == len(valid):
            judgement = "stable_correct"
        else:
            judgement = "stable_wrong"
        if len(set(verdicts)) > 1:
            unstable_verdict.append(str(entry["case_id"]))
        entry["distinct_routes"] = distinct
        entry["correct_votes"] = correct_votes
        entry["trials_run"] = len(trials)
        entry["scored_trials"] = len(valid)
        entry["stable"] = stable
        entry["judgement"] = judgement
        # `choices` can be empty when nothing was answered at all.
        entry["chosen_route"] = distinct[0] if stable and distinct else (
            choices[0] if choices else None)
        entry["verdict"] = (
            verdicts[0] if stable and verdicts else ("flaky" if choices else "no_data"))
        results.append(entry)

    attempts = sum(v for v in tally.values())
    infra = sum(v for k, v in tally.items() if k in INFRA_VERDICTS)
    scored = attempts - infra
    correct = tally.get("correct", 0)
    stable_correct = [r["case_id"] for r in results if r["judgement"] == "stable_correct"]
    decided = [r for r in results
               if r["judgement"] in {"stable_correct", "stable_wrong"}]
    no_data = [r["case_id"] for r in results
               if r["judgement"] in {"no_data", "unanswered"}]
    stable_wrong = [r["case_id"] for r in results if r["judgement"] == "stable_wrong"]
    dangerous_cases = sorted({
        str(entry["case_id"])
        for entry in results
        for trial in entry["trials"]  # type: ignore[union-attr]
        if trial.get("verdict") == "dangerous"
    })

    handoff: dict[str, object] = {}
    if args.stage == "handoff":
        answered = [
            trial
            for entry in results
            for trial in entry["trials"]
            if isinstance(trial.get("handoff"), dict)
        ]
        owner_loaded = [t for t in answered if t["handoff"]["owner_loaded"]]
        slots_ok = [t for t in answered if t["handoff"]["slots_match"]]
        read_gaps = [
            (entry["case_id"], t["handoff"]["required_read_missing"])
            for entry in results
            for t in entry["trials"]
            if isinstance(t.get("handoff"), dict) and t["handoff"]["required_read_missing"]
        ]
        artifact_missing = [
            entry["case_id"]
            for entry in results
            for t in entry["trials"]
            if isinstance(t.get("handoff"), dict) and not t["handoff"]["artifact"].strip()
        ]
        handoff = {
            "trials": len(answered),
            "owner_loaded": len(owner_loaded),
            "slots_match": len(slots_ok),
            "required_read_gaps": read_gaps,
            "artifact_missing": sorted(set(artifact_missing)),
        }

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stage": args.stage,
        "model": args.model,
        "package_version": json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["version"],
        "repeat": args.repeat,
        "cases": len(results),
        "attempts": attempts,
        "correct": correct,
        "scored": scored,
        "infrastructure_failures": infra,
        "accuracy": round(correct / scored, 3) if scored else 0.0,
        "stable_cases": len(stable_correct) + len(stable_wrong),
        "stable_correct": len(stable_correct),
        "decided_cases": len(decided),
        "no_data": no_data,
        "stable_accuracy": (
            round(len(stable_correct) / len(decided), 3) if decided else 0.0),
        "stable_wrong": stable_wrong,
        "flaky": flaky,
        "unstable_verdict": unstable_verdict,
        "tally": tally,
        "dangerous": dangerous_cases,
        "note": "LLM output is measurement only, never package truth.",
        "handoff": handoff,
        "results": results,
    }
    if outdir:
        (outdir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"accuracy        {correct}/{scored} scored attempts = {summary['accuracy']:.1%}  "
          f"model={args.model}  repeat={args.repeat}")
    if infra:
        print(f"infrastructure  {infra}/{attempts} attempts failed after retries "
              f"and are excluded from accuracy")
    print(f"stable accuracy {summary['stable_correct']}/{len(decided)} decided cases = "
          f"{summary['stable_accuracy']:.1%}")
    if no_data:
        print(f"no usable answer {len(no_data)}/{len(results)} cases: "
              f"{', '.join(map(str, no_data[:10]))}")
    print(f"tally           {dict(sorted(tally.items()))}")
    if handoff:
        print()
        print("== handoff: did the route reach the skill and the requirement? ==")
        print(f"  owner SKILL.md opened   {handoff['owner_loaded']}/{handoff['trials']} trials")
        print(f"  three slots matched     {handoff['slots_match']}/{handoff['trials']} trials")
        if handoff["required_read_gaps"]:
            shown = handoff["required_read_gaps"][:5]
            print(f"  required_read not opened: {len(handoff['required_read_gaps'])} "
                  f"trials, e.g. {shown}")
        else:
            print("  required_read           every listed reference was opened")
        if handoff["artifact_missing"]:
            print(f"  no artifact named:      {', '.join(handoff['artifact_missing'][:8])}")
        print("  route accuracy alone cannot show any of this: a right label that")
        print("  never opens its owner skill still produces the wrong work.")
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
