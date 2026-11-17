"""The reproduction checker must not report agreement where there is none."""
from __future__ import annotations

from routing_repro_check import compare


def _run(results: list[tuple[str, list[tuple[str, str | None]]]]) -> dict:
    """Build a summary-shaped dict: (case_id, [(verdict, route), ...])"""
    return {
        "results": [
            {
                "case_id": case_id,
                "trials": [{"verdict": v, "chosen_route": r} for v, r in trials],
            }
            for case_id, trials in results
        ]
    }


def test_identical_runs_agree() -> None:
    a = _run([("C10", [("correct", "R10")]), ("C11", [("correct", "R11")])])
    result = compare(a, a)
    assert result["agreement"] == 1.0
    assert result["disagree"] == []


def test_changed_route_is_a_disagreement() -> None:
    a = _run([("C10", [("correct", "R10")])])
    b = _run([("C10", [("near_miss", "R11")])])
    result = compare(a, b)
    assert result["agreement"] == 0.0
    assert result["disagree"] == [("C10", ["R10"], ["R11"])]


def test_infrastructure_failures_are_not_compared() -> None:
    a = _run([("C10", [("correct", "R10"), ("timeout", None)])])
    b = _run([("C10", [("correct", "R10")])])
    assert compare(a, b)["agreement"] == 1.0


def test_a_case_unanswered_in_one_run_is_not_agreement() -> None:
    a = _run([("C10", [("correct", "R10")])])
    b = _run([("C10", [("unanswered", None)])])
    result = compare(a, b)
    assert result["agree"] == []
    assert result["disagree"] == [("C10", ["R10"], [])]


def test_only_shared_cases_are_counted() -> None:
    a = _run([("C10", [("correct", "R10")]), ("C11", [("correct", "R11")])])
    b = _run([("C10", [("correct", "R10")]), ("C99", [("correct", "R99")])])
    result = compare(a, b)
    assert result["shared"] == ["C10"]
    assert result["only_a"] == ["C11"]
    assert result["only_b"] == ["C99"]
    assert result["agreement"] == 1.0


def test_agreeing_on_a_wrong_route_still_counts_as_reproduced() -> None:
    """Agreement is stability, not correctness -- the tool must not conflate them."""
    a = _run([("C10", [("near_miss", "R11")])])
    b = _run([("C10", [("near_miss", "R11")])])
    assert compare(a, b)["agreement"] == 1.0
