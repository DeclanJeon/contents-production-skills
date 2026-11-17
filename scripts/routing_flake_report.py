#!/usr/bin/env python3
"""Summarise a repeated routing_eval run: per-case flake rate and intervals.

A single "159/159" says little about stability, because three trials per case
cannot distinguish "never flaky" from "flaky 10% of the time". This reporter
gives the honest version of the number:

  * per-case flake count and Wilson score interval on the per-trial error rate
  * an aggregate interval for the boundary set as a whole
  * the smallest per-trial error rate the sample could still have missed

Usage:
    python3 scripts/routing_flake_report.py qa/routing-flake-2026-11-17
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]

# Infrastructure failures are not routing opinions. Counting them as wrong
# answers would make the table look worse for reasons that have nothing to do
# with routing, and counting them as right answers would be worse still.
INFRA: Final = frozenset({"dispatch_error", "timeout"})


def wilson(errors: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion. Better than normal approx at 0."""
    if trials == 0:
        return (0.0, 1.0)
    p = errors / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    margin = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denom
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def detection_floor(trials: int) -> float:
    """Highest per-trial error rate that P(seeing zero errors) would still hide.

    With n clean trials, an error rate of r survives with probability
    (1-r)^n. This returns the largest r for which that is still >= 5%, i.e. the
    error rate this sample could plausibly have missed.
    """
    return 1 - 0.05 ** (1 / trials) if trials else 1.0


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else None
    if target is None:
        print(__doc__.strip())
        return 2
    summary_path = target / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    results = summary["results"]
    repeat = summary.get("repeat", 1)
    lines: list[str] = []
    total_errors = 0
    total_trials = 0
    total_infra = 0
    flaky: list[str] = []

    print(f"model={summary['model']}  repeat={repeat}  cases={len(results)}  "
          f"package={summary['package_version']}")
    print()
    print(f"{'case':6} {'exp':4} {'ok':>3}/{'n':<3} {'skip':>4} {'seen':14} verdict")
    for entry in results:
        trials = entry["trials"]
        n = len(trials)
        infra = sum(1 for t in trials if t.get("verdict") in INFRA)
        valid = [t for t in trials if t.get("verdict") not in INFRA]
        errors = sum(1 for t in valid if t.get("verdict") != "correct")
        total_errors += errors
        total_trials += len(valid)
        total_infra += infra
        seen = sorted({str(t.get("chosen_route")) for t in valid})
        note = ""
        if len(seen) > 1:
            flaky.append(str(entry["case_id"]))
            note = "route changed between trials"
        elif errors:
            note = "consistently wrong"
        verdict = "flaky" if len(seen) > 1 else ("wrong" if errors else "ok")
        print(f"{entry['case_id']:6} {entry['expected_route']:4} "
              f"{len(valid) - errors:3}/{len(valid):<3} {infra:4} "
              f"{','.join(seen) or '-':14} {verdict}"
              + (f"  <- {note}" if note else ""))

    lo, hi = wilson(total_errors, total_trials)
    floor = detection_floor(repeat)
    print()
    print(f"scored trials    {total_trials}")
    print(f"routing errors   {total_errors}")
    print(f"infra failures   {total_infra} (excluded)")
    print(f"per-trial error   {total_errors / total_trials:.2%} "
          f"(95% Wilson {lo:.2%}..{hi:.2%})")
    print(f"flaky cases      {len(flaky)}" + (f": {', '.join(flaky)}" if flaky else ""))
    print()
    agg_floor = detection_floor(total_trials)
    print("Power, stated plainly:")
    print(f"  per case ({repeat} trials)  zero errors rules out only > {floor:.1%}")
    print(f"  aggregate ({total_trials} trials)  zero errors rules out > {agg_floor:.2%}")
    print("Per-case rates are underpowered at this sample size; quote the aggregate")
    print("bound, not 'never flaky'. Ruling out a 1% per-trial rate needs ~298")
    print("trials per case.")
    lines.append(f"flaky={len(flaky)} routing_errors={total_errors}/{total_trials} "
                 f"infra_excluded={total_infra}")

    (target / "flake-report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
