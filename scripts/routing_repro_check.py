#!/usr/bin/env python3
"""Compare two routing_eval runs case by case, for reproducibility.

Accuracy tells you how often the router agrees with the table. This tells you
whether it agrees *with itself*: run the same cases again in a fresh process
and see if the same routes come back. Those are different questions, and a
package can score 100% twice while disagreeing on which cases it got right.

Usage:
    python3 scripts/routing_repro_check.py qa/run-a qa/run-b
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]

# Crashed dispatches are not opinions about routing, so they are skipped
# rather than reported as disagreement.
INFRA: Final = frozenset({"dispatch_error", "timeout"})


def routes_by_case(summary: dict) -> dict[str, list[str]]:
    """Return the distinct non-empty routes each case produced, per run."""
    seen: dict[str, list[str]] = {}
    for entry in summary.get("results", []):
        routes = {
            str(trial.get("chosen_route"))
            for trial in entry["trials"]
            if trial.get("verdict") not in INFRA and trial.get("chosen_route")
        }
        seen[str(entry["case_id"])] = sorted(routes)
    return seen


def compare(first: dict, second: dict) -> dict[str, object]:
    a = routes_by_case(first)
    b = routes_by_case(second)
    shared = sorted(set(a) & set(b))
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))

    agree: list[str] = []
    disagree: list[tuple[str, list[str], list[str]]] = []
    for case_id in shared:
        # A run can leave a case unanswered; that is a gap, not agreement.
        if a[case_id] and a[case_id] == b[case_id]:
            agree.append(case_id)
        else:
            disagree.append((case_id, a[case_id], b[case_id]))

    return {
        "shared": shared,
        "only_a": only_a,
        "only_b": only_b,
        "agree": agree,
        "disagree": disagree,
        "agreement": len(agree) / len(shared) if shared else 0.0,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    first_dir, second_dir = Path(argv[1]), Path(argv[2])
    first = json.loads((first_dir / "summary.json").read_text(encoding="utf-8"))
    second = json.loads((second_dir / "summary.json").read_text(encoding="utf-8"))
    result = compare(first, second)

    print(f"A {first_dir}  model={first.get('model')} repeat={first.get('repeat')}")
    print(f"B {second_dir}  model={second.get('model')} repeat={second.get('repeat')}")
    print()
    print(f"shared cases     {len(result['shared'])}")
    print(f"same route       {len(result['agree'])}")
    print(f"route differed   {len(result['disagree'])}")
    print(f"agreement        {result['agreement']:.1%}")
    if result["only_a"]:
        print(f"only in A        {len(result['only_a'])}: {', '.join(result['only_a'][:8])}")
    if result["only_b"]:
        print(f"only in B        {len(result['only_b'])}: {', '.join(result['only_b'][:8])}")

    if result["disagree"]:
        print()
        print(f"{'case':6} {'A routes':16} {'B routes':16} expected")
        for case_id, a_routes, b_routes in result["disagree"]:
            expected = next(
                (str(e.get("expected_route")) for e in first["results"]
                 if str(e["case_id"]) == case_id), "?")
            print(f"{case_id:6} {','.join(a_routes) or '-':16} "
                  f"{','.join(b_routes) or '-':16} {expected}")

    print()
    print("Note: agreement is not correctness. Two runs can agree on a wrong")
    print("route, and a case that is wrong in both runs still counts as a")
    print("reproduced answer here. Read this next to each run's accuracy.")
    return 0 if not result["disagree"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
