"""Routing regression guard: routing.csv stays canonical and in sync."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Final

import routing_regression

ROOT: Final = Path(__file__).resolve().parents[1]
CSV_PATH: Final = ROOT / "creative-production/references/routing.csv"
REQUIRED_COLUMNS: Final = (
    "route_id",
    "deliverable_kind",
    "media_axis",
    "authority_axis",
    "owner",
    "required_read",
    "stop_boundary",
)


def _rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_routing_csv_has_required_columns_and_unique_ids() -> None:
    # Given: the canonical route table
    rows = _rows()

    # Then: it is machine-readable and stable
    assert rows, "routing.csv has no data rows"
    assert tuple(rows[0].keys()) == REQUIRED_COLUMNS
    ids = [row["route_id"] for row in rows]
    assert len(ids) == len(set(ids)), "duplicate route_id"


def test_routing_csv_owners_resolve_to_installed_skills() -> None:
    # Given/When: every route owner must be a real sibling skill
    for row in _rows():
        owner = row["owner"]
        if owner == "UNASSIGNED":
            continue
        assert (ROOT / owner / "SKILL.md").exists(), f"{row['route_id']}: {owner}"


def test_routing_cases_agree_with_csv() -> None:
    # Given/When: the frozen prompt cases must not drift from the table
    _results, failures = routing_regression.check_cases()

    # Then: zero drift
    assert failures == 0


def test_layered_frontier_is_smaller_than_legacy() -> None:
    # Given: the pre-split frontier is archived for comparison
    layered = routing_regression.measure(routing_regression.FRONTIER)
    legacy = routing_regression.measure(routing_regression.LEGACY_FRONTIER)

    # Then: routing never regresses past the split baseline
    assert layered["missing"] == []
    assert layered["words"] < legacy["words"]


def test_boundary_cases_cover_every_confusable_cluster() -> None:
    """Adversarial probes must exist next to the routes they can be mistaken for."""
    cases = routing_regression.load_cases()
    boundary = [c for c in cases if c["case_id"].startswith("B")]
    assert boundary, "no adversarial boundary cases registered"

    # Every note must explain why the case is adversarial, or it is just coverage.
    missing_reason = [c["case_id"] for c in boundary if not c.get("boundary_note")]
    assert not missing_reason, f"boundary cases without a reason: {missing_reason}"

    # The clusters that actually collide in practice must each be represented.
    clusters = {
        "storyboard depth": {"R10", "R11", "R24"},
        "silent family": {"R07", "R08", "R09"},
        "text-plan vs image package": {"R05", "R24"},
        "camera family": {"R16", "R17", "R19", "R21"},
        "assets module depth": {"R06", "R13", "R15"},
        "reference and audit": {"R25", "R26", "R27"},
        "persona vs sheet": {"R03", "R04"},
    }
    covered = {c["route_id"] for c in boundary}
    uncovered = {
        name: sorted(cluster - covered) for name, cluster in clusters.items()
        if cluster - covered
    }
    assert not uncovered, f"boundary clusters missing probes: {uncovered}"


def test_boundary_cases_do_not_leak_their_own_answer() -> None:
    """A probe that contains the giveaway keyword measures nothing."""
    cases = routing_regression.load_cases()
    # Route ids must never be spelled out in a probe prompt.
    leaking = [
        c["case_id"]
        for c in cases
        if c["case_id"].startswith("B") and c["route_id"].lower() in c["prompt"].lower()
    ]
    assert not leaking, f"boundary prompts leak their route id: {leaking}"
