#!/usr/bin/env python3
"""Audit the ground truth of the routing eval, not the router.

Every measurement so far answers "does the router agree with the expected
route". If an expected route is wrong, that measurement is worthless. So the
cases themselves get checked here, model-free, against `routing.csv`.

What this can and cannot do: it cannot prove a prompt "means" a route, which
is a judgement. It can prove the cases are internally consistent with the table
and that the contrast pairs really do flip the dimension they claim to flip.

Checks:
  1. coverage        every route has at least one case
  2. exclusion       a request that withholds a deliverable is never mapped to
                     a route that performs it
  3. warrant         an executed-media or approval-bearing route is only
                     expected where the request actually authorises it
  3b. owner          each case's expected owner matches routing.csv
  4. contrast pairs  declared pairs must differ on the declared dimension
  4b. same-route     declared non-distinctions must really not distinguish
  5. skew            report how much of the set is text_only, because accuracy
                     is dominated by whatever the majority axis is

Usage:
    python3 scripts/routing_truth_audit.py [--json]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
ROUTES: Final = ROOT / "creative-production/references/routing.csv"
CASES: Final = ROOT / "creative-production/evals/routing-cases.json"

# Requests that explicitly withhold something. If one of these is mapped to a
# route whose media_axis is executed_media, the expected answer contradicts the
# request, and the eval would be training over-execution.
WITHHOLDS: Final = (
    "이미지 없이", "이미지는 아직", "아직 만들지", "검증은 아직", "시트는 아직",
    "텍스트로만", "다른 모듈은 필요 없어",
)

# Requests that authorise spending or execution. An executed-media route is only
# defensible when at least one of these appears.
# "3D" is deliberately broad: the alternative ("3D로") missed a request phrased
# as "3D 공간 오클루전 검증해줘". Requests that *withhold* 3D work are caught by
# the exclusion check instead, which runs on the opposite class of routes, so the
# two checks cannot cancel each other out.
WARRANTS: Final = (
    "실제", "뽑아서", "뽑아", "만들어서", "촬영", "재생해서", "3D", "이미지까지",
    "스틸까지",
)

EXECUTING_AUTHORITY: Final = frozenset(
    {"approved_execution", "requested_spatial_verification", "supplied_media_only"})

# (a, b, dimension the pair is supposed to flip)
CONTRAST_PAIRS: Final = (
    ("B03", "B04", "media_axis"),       # images included vs images withheld
    ("B08", "B09", "media_axis"),       # text only vs real stills
    ("B10", "B11", "authority_axis"),   # 3D deferred vs 3D requested
    ("B23", "B24", "media_axis"),       # stills assembled vs full production
    ("B01", "B02", "deliverable_kind"),  # production board vs rough ideation
    ("B01", "B01b", "deliverable_kind"),
    ("B21", "B22", "deliverable_kind"),  # persona only vs character sheet
    ("B05", "B07", "deliverable_kind"),  # silent drama vs silent satire
    # D-pairs: same request, only the authorising clause differs. These target
    # the axis where a mistake costs money.
    ("D01", "D02", "media_axis"),        # images deferred vs images now
    ("D03", "D04", "authority_axis"),    # 3D deferred vs 3D requested
    ("D05", "D06", "authority_axis"),    # plan-only vs supplied footage
    # E-pairs: the hardest three-way split -- a board on paper, stills that
    # already exist, and stills that must be generated.
    ("E03", "E04", "media_axis"),        # board on paper vs existing stills
    ("E05", "E06", "media_axis"),        # short edit vs full short lifecycle
)

# Pairs that must NOT change the route. These encode a distinction the table
# deliberately does not make, so a future "fix" that splits them will fail here
# instead of quietly inventing a boundary that is not in the skills.
SAME_ROUTE_PAIRS: Final = (
    # storytelling-with-still-images/SKILL.md says "Use for new or existing
    # still-image cuts ... If new stills are requested, use codex-imagen".
    # Generating the stills is in scope, so existing vs new stills is not a
    # routing distinction. E02 was first written expecting R24; the model
    # answered R12 every time and was right.
    ("E01", "E02", "new vs existing stills stays in one route"),
)

METADATA_FIELDS: Final = ("media_axis", "authority_axis", "owner", "deliverable_kind")


def load() -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    routes = {r["route_id"]: r for r in csv.DictReader(ROUTES.open(encoding="utf-8"))}
    raw = json.loads(CASES.read_text(encoding="utf-8"))
    cases = raw["cases"] if isinstance(raw, dict) else raw
    return routes, cases


def check_coverage(routes, cases) -> tuple[list[str], list[str]]:
    covered = {c["route_id"] for c in cases}
    missing = sorted(set(routes) - covered)
    unknown = sorted(covered - set(routes))
    problems = [f"route {r} has no case" for r in missing]
    problems += [f"case expects unknown route {r}" for r in unknown]
    return problems, [f"routes covered {len(set(routes) & covered)}/{len(routes)}"]


def check_exclusions(routes, cases) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []
    for case in cases:
        hits = [phrase for phrase in WITHHOLDS if phrase in case["prompt"]]
        if not hits:
            continue
        route = routes[case["route_id"]]
        if route["media_axis"] == "executed_media":
            problems.append(
                f"{case['case_id']} withholds ({', '.join(hits)}) but expects "
                f"{case['route_id']} which is executed_media")
        notes.append(f"{case['case_id']} withholds -> {case['route_id']} "
                     f"({route['media_axis']})")
    return problems, notes


def check_warrant(routes, cases) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    notes: list[str] = []
    for case in cases:
        route = routes[case["route_id"]]
        needs = (route["media_axis"] == "executed_media"
                 or route["authority_axis"] in EXECUTING_AUTHORITY)
        if not needs:
            continue
        if not any(token in case["prompt"] for token in WARRANTS):
            problems.append(
                f"{case['case_id']} expects {case['route_id']} "
                f"(media={route['media_axis']}, authority={route['authority_axis'] or '-'}) "
                "but the request never authorises execution")
        notes.append(f"{case['case_id']} -> {case['route_id']} warranted")
    return problems, notes


def check_owner(routes, cases) -> tuple[list[str], list[str]]:
    """Each case's expected owner must be the owner the table assigns."""
    problems: list[str] = []
    for case in cases:
        route = routes.get(case["route_id"])
        if route is None:
            continue
        if case.get("expected_owner") != route["owner"]:
            problems.append(
                f"{case['case_id']} expects owner {case.get('expected_owner')!r} "
                f"but {case['route_id']} is owned by {route['owner']!r}")
    return problems, []


def check_contrast_pairs(routes, cases) -> tuple[list[str], list[str]]:
    by_id = {c["case_id"]: c for c in cases}
    problems: list[str] = []
    notes: list[str] = []
    for first, second, dimension in CONTRAST_PAIRS:
        for case_id in (first, second):
            if case_id not in by_id:
                problems.append(f"contrast pair references missing case {case_id}")
        if first not in by_id or second not in by_id:
            continue
        route_a = routes[by_id[first]["route_id"]]
        route_b = routes[by_id[second]["route_id"]]
        if by_id[first]["route_id"] == by_id[second]["route_id"]:
            problems.append(f"{first} and {second} share route "
                            f"{by_id[first]['route_id']}, so the pair proves nothing")
            continue
        if route_a[dimension] == route_b[dimension]:
            problems.append(
                f"{first} vs {second} should flip {dimension} but both are "
                f"{route_a[dimension]!r}")
        # A pair that differs only in deliverable_kind has no axis to lean on,
        # so the router has to read the prose. Worth knowing how many exist.
        only_kind = [f for f in METADATA_FIELDS if route_a[f] != route_b[f]] == [
            "deliverable_kind"]
        notes.append(f"{first} vs {second} flips {dimension}"
                     + (" (no axis help)" if only_kind else ""))
    return problems, notes


def check_same_route(routes, cases) -> tuple[list[str], list[str]]:
    """Declared non-distinctions must really be non-distinctions."""
    by_id = {c["case_id"]: c for c in cases}
    problems: list[str] = []
    notes: list[str] = []
    for first, second, reason in SAME_ROUTE_PAIRS:
        if first not in by_id or second not in by_id:
            problems.append(f"same-route pair references a missing case: "
                            f"{first}/{second}")
            continue
        route_a, route_b = by_id[first]["route_id"], by_id[second]["route_id"]
        if route_a != route_b:
            problems.append(
                f"{first} ({route_a}) and {second} ({route_b}) must share a route: "
                f"{reason}")
        notes.append(f"{first}/{second} both {route_a} -- {reason}")
    return problems, notes


def check_skew(routes, cases) -> tuple[list[str], list[str]]:
    counts: dict[str, int] = {}
    for case in cases:
        axis = routes[case["route_id"]]["media_axis"]
        counts[axis] = counts.get(axis, 0) + 1
    notes = [f"{axis}: {count} cases ({count / len(cases):.0%})"
             for axis, count in sorted(counts.items(), key=lambda kv: -kv[1])]
    # Not a failure: it is a statement about what the accuracy number covers.
    dominant, count = max(counts.items(), key=lambda kv: kv[1])
    if count / len(cases) > 0.6:
        notes.append(f"NOTE accuracy is dominated by {dominant} "
                     f"({count / len(cases):.0%} of cases)")
    return [], notes


CHECKS: Final = (
    ("coverage", check_coverage),
    ("exclusion", check_exclusions),
    ("warrant", check_warrant),
    ("owner", check_owner),
    ("contrast", check_contrast_pairs),
    ("same-route", check_same_route),
    ("skew", check_skew),
)


def main(argv: list[str]) -> int:
    routes, cases = load()
    all_problems: list[str] = []
    report: dict[str, object] = {}

    for name, check in CHECKS:
        problems, notes = check(routes, cases)
        all_problems += problems
        report[name] = {"problems": problems, "notes": notes}
        status = "FAIL" if problems else "ok  "
        print(f"[{status}] {name}")
        for note in notes:
            print(f"         {note}")
        for problem in problems:
            print(f"    !!   {problem}")

    print()
    if all_problems:
        print(f"{len(all_problems)} problem(s). The expected routes must be fixed "
              "before any accuracy number from this set means anything.")
    else:
        print("Ground truth is internally consistent with routing.csv.")
        print("This does NOT prove each prompt means its route; that is a judgement.")
        print("What it proves: no case contradicts the table's own axes, and every")
        print("declared contrast pair actually flips the dimension it claims.")

    if "--json" in argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if all_problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
