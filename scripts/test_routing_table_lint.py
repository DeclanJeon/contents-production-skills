"""Stabilization guard: the route table stays internally consistent.

These checks catch the failure modes that a duplicated table used to hide:
a duplicate deliverable kind that makes a slot ambiguous, a `required_read`
path that no longer exists, a route with no stop boundary, and a route that
silently permits media without naming who authorized it.
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
CSV_PATH: Final = ROOT / "creative-production/references/routing.csv"

MEDIA_AXES: Final = {"text_only", "none_or_stills", "executed_media", "varies"}


def _rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_deliverable_kinds_are_unique_and_present() -> None:
    # Given/When: each route must own exactly one deliverable kind
    rows = _rows()
    counts = Counter(row["deliverable_kind"] for row in rows)

    # Then: no ambiguity from a duplicated kind, and no empty value
    duplicates = {kind: n for kind, n in counts.items() if n > 1}
    assert not duplicates, f"duplicate deliverable_kind: {duplicates}"
    assert all(kind.strip() for kind in counts), "empty deliverable_kind"


def test_media_axis_is_from_the_closed_vocabulary() -> None:
    # Given/When: media_axis drives the dangerous/near-miss classification
    rows = _rows()

    # Then: only known values appear, so the classifier stays meaningful
    unknown = {row["route_id"]: row["media_axis"] for row in rows
               if row["media_axis"] not in MEDIA_AXES}
    assert not unknown, f"unknown media_axis: {unknown}"


def test_every_route_has_a_stop_boundary() -> None:
    # Given/When: a route without a stop boundary invites scope creep
    rows = _rows()

    # Then: all of them state where to stop
    missing = [row["route_id"] for row in rows if not row["stop_boundary"].strip()]
    assert not missing, f"routes without stop_boundary: {missing}"


def test_executed_media_routes_outside_the_coordinator_declare_authority() -> None:
    # Given/When: a non-coordinator route may only run media with supplied authority
    rows = _rows()
    offenders = [
        row["route_id"]
        for row in rows
        if row["media_axis"] == "executed_media"
        and row["owner"] != "creative-production"
        and not row["authority_axis"].strip()
    ]

    # Then: the delegation surface names the gate it depends on
    assert not offenders, (
        f"executed_media routes must declare authority_axis: {offenders}"
    )


def test_required_read_paths_resolve() -> None:
    """`required_read` is prose; this checks every path-like token in it."""
    rows = _rows()
    broken: list[str] = []
    for row in rows:
        for token in row["required_read"].replace(",", " ").split():
            token = token.strip("()[]`;")
            if not (token.endswith(".md") or token.endswith(".csv")):
                continue
            if "/" not in token:
                continue
            candidates = [
                ROOT / token,
                ROOT / "creative-production/references" / token,
                ROOT / "video-production-assets/references" / token,
                ROOT / "video-production-assets" / token,
            ]
            if not any(path.exists() for path in candidates):
                broken.append(f"{row['route_id']}: {token}")
    assert not broken, f"required_read paths do not resolve: {broken}"


def test_installer_ships_the_layered_canon_and_no_archive(tmp_path: Path) -> None:
    """The installed copy must carry the router, the CSV and the policy layer."""
    import install_package

    target = tmp_path / "installed"
    install_package.install(
        target, repo_root=ROOT, exclude_derived_support=True,
    )

    for rel in (
        "creative-production/SKILL.md",
        "creative-production/references/routing.csv",
        "creative-production/references/policy.md",
        "creative-production/references/routing-disambiguation.csv",
    ):
        assert (target / rel).is_file(), f"installer omitted {rel}"

    shipped_archives = [
        path.relative_to(target).as_posix()
        for path in (target / "creative-production").rglob("archive")
    ]
    assert not shipped_archives, f"dev-only archive shipped: {shipped_archives}"


def test_policy_layer_names_every_cross_cutting_rule_once() -> None:
    """policy.md owns the shared rules; it must actually contain them."""
    policy = (ROOT / "creative-production/references/policy.md").read_text(
        encoding="utf-8",
    )
    required_sections = (
        "Authority hierarchy",
        "Scope boundary",
        "Read-only and no-generation probes",
        "Single writer",
        "Evidence and provenance",
        "Execution gate",
        "History lifecycle",
        "Honesty about the runtime",
    )
    missing = [section for section in required_sections if section not in policy]
    assert not missing, f"policy.md lost sections: {missing}"


def _disambiguation_rows() -> list[dict[str, str]]:
    import csv

    path = ROOT / "creative-production/references/routing-disambiguation.csv"
    assert path.is_file(), "routing-disambiguation.csv is missing"
    return list(csv.DictReader(path.open(encoding="utf-8")))


def test_disambiguation_pairs_are_well_formed() -> None:
    """Each row names two real, different routes and says something."""
    routes = {
        row["route_id"]: row
        for row in _rows()
    }
    rows = _disambiguation_rows()
    assert rows, "the pair table is empty"

    problems: list[str] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        a, b = row["route_a"], row["route_b"]
        if a not in routes or b not in routes:
            problems.append(f"unknown route in pair {a}/{b}")
            continue
        if a == b:
            problems.append(f"pair {a}/{b} compares a route with itself")
        if (a, b) in seen:
            problems.append(f"duplicate pair {a}/{b}")
        seen.add((a, b))
        if [a, b] != sorted([a, b]):
            problems.append(f"pair {a}/{b} is not in canonical order")
        words = row["discriminator"].split()
        if len(words) < 6:
            problems.append(f"pair {a}/{b} discriminator says too little: "
                            f"{row['discriminator']!r}")
        if len(words) > 30:
            problems.append(f"pair {a}/{b} discriminator is a paragraph "
                            f"({len(words)} words); this file sits in the frontier")
    assert not problems, problems


def test_disambiguation_never_restates_a_stop_boundary() -> None:
    """The pair file explains a choice; it must not become a second rulebook."""
    routes = {row["route_id"]: row for row in _rows()}
    problems: list[str] = []
    for row in _disambiguation_rows():
        for side in ("route_a", "route_b"):
            boundary = routes[row[side]]["stop_boundary"]
            # Long verbatim overlap would duplicate the canon and drift from it.
            fragment = boundary[:60]
            if fragment and fragment in row["discriminator"]:
                problems.append(
                    f"pair {row['route_a']}/{row['route_b']} copies the "
                    f"stop_boundary of {row[side]}")
    assert not problems, problems


def test_router_requires_the_pair_table_unconditionally() -> None:
    """A conditional rule was measured never to fire, so it must be required.

    With "read it only when two routes remain plausible", eleven confusable
    cases were run and the file was read zero times: one route always looks
    plausible immediately. A file nobody reads is worse than no file.
    """
    text = (ROOT / "creative-production/SKILL.md").read_text(encoding="utf-8")
    assert "routing-disambiguation.csv" in text, (
        "the router never mentions the pair table")
    lowered = text.lower()
    assert "required" in lowered, "the router does not require the pair table"
    for phrase in ("only on a tie", "only when two routes", "if two routes remain"):
        assert phrase not in lowered, (
            f"the router still gates the pair table ({phrase!r}), which measured "
            "as never firing")
