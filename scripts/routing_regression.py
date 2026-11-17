# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Deterministic routing regression for the contents-production-skills package.

This is a structural bench, not an LLM judge. It answers two questions:

1. Frontier cost: how many words/bytes must be read before the first
   current-stage owner is selected?
2. Route agreement: given a frozen case list, does `routing.csv` still point
   at the same owner, and does the frozen owner's SKILL.md still exist?

Run: python3 scripts/routing_regression.py
     python3 scripts/routing_regression.py --json > before.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
ROUTING_CSV: Final = ROOT / "creative-production/references/routing.csv"
CASES: Final = ROOT / "creative-production/evals/routing-cases.json"

# Files an agent must read before it can name a current-stage owner.
FRONTIER: Final = (
    "creative-production/SKILL.md",
    "creative-production/references/routing.csv",
)
# Legacy frontier, measured for comparison until the layered split lands.
LEGACY_FRONTIER: Final = (
    "creative-production/SKILL.md",
    "creative-production/references/production-routing.md",
)


def _word_bytes(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    return len(text.split()), len(text.encode("utf-8"))


def measure(paths: tuple[str, ...]) -> dict[str, object]:
    total_words = 0
    total_bytes = 0
    per_file: dict[str, dict[str, int]] = {}
    for rel in paths:
        path = ROOT / rel
        if not path.exists():
            continue
        words, nbytes = _word_bytes(path)
        per_file[rel] = {"words": words, "bytes": nbytes}
        total_words += words
        total_bytes += nbytes
    return {
        "files": len(per_file),
        "words": total_words,
        "bytes": total_bytes,
        "missing": [rel for rel in paths if not (ROOT / rel).exists()],
        "per_file": per_file,
    }


def load_routes() -> dict[str, dict[str, str]]:
    if not ROUTING_CSV.exists():
        return {}
    with ROUTING_CSV.open(encoding="utf-8", newline="") as handle:
        return {row["route_id"]: row for row in csv.DictReader(handle)}


def load_cases() -> list[dict[str, str]]:
    if not CASES.exists():
        return []
    return json.loads(CASES.read_text(encoding="utf-8"))["cases"]


def check_cases() -> tuple[list[dict[str, object]], int]:
    routes = load_routes()
    results: list[dict[str, object]] = []
    failures = 0
    for case in load_cases():
        route = routes.get(case["route_id"])
        problems: list[str] = []
        if route is None:
            problems.append(f"route_id {case['route_id']!r} missing from routing.csv")
            owner = None
        else:
            owner = route["owner"]
            if owner != case["expected_owner"]:
                problems.append(
                    f"owner drift: csv={owner!r} expected={case['expected_owner']!r}"
                )
        if owner and not (ROOT / owner).exists() and owner != "UNASSIGNED":
            # Owners are skill names; resolve to <skill>/SKILL.md.
            if not (ROOT / owner / "SKILL.md").exists():
                problems.append(f"owner skill directory missing: {owner!r}")
        if problems:
            failures += 1
        results.append(
            {"case_id": case["case_id"], "ok": not problems, "problems": problems}
        )
    return results, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    layered = measure(FRONTIER)
    legacy = measure(LEGACY_FRONTIER)
    results, failures = check_cases()

    report = {
        "frontier_layered": layered,
        "frontier_legacy": legacy,
        "route_cases": len(results),
        "route_failures": failures,
        "routes_in_csv": len(load_routes()),
        "results": results,
    }

    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1 if failures else 0

    print("== frontier cost (read before first owner selection) ==")
    for label, data in (("layered", layered), ("legacy", legacy)):
        print(f"  {label:8} files={data['files']} words={data['words']} bytes={data['bytes']}")
        if data["missing"]:
            print(f"           missing: {', '.join(data['missing'])}")
    if legacy["words"] and layered["words"]:
        saved = 100 * (1 - layered["words"] / legacy["words"])
        print(f"  delta    words {saved:+.0f}% vs legacy")
    print(f"\n== routes in csv: {len(load_routes())} ==")
    print(f"== route regression: {len(results)} cases, {failures} failing ==")
    for item in results:
        if not item["ok"]:
            print(f"  FAIL {item['case_id']}")
            for problem in item["problems"]:
                print(f"       - {problem}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
