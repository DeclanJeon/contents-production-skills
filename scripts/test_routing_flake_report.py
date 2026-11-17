"""The flake reporter must not overstate what a small sample can prove."""
from __future__ import annotations

import pytest

from routing_flake_report import detection_floor, wilson


def test_wilson_zero_errors_still_has_an_upper_bound() -> None:
    """Zero observed errors is not a zero error rate; the interval must say so."""
    lo, hi = wilson(0, 159)
    assert lo == 0.0
    assert 0.01 < hi < 0.03, f"expected a few-percent upper bound, got {hi}"


def test_wilson_interval_contains_the_point_estimate() -> None:
    for errors, trials in [(0, 10), (1, 10), (5, 10), (10, 10), (3, 159)]:
        lo, hi = wilson(errors, trials)
        assert lo <= errors / trials <= hi


def test_wilson_narrows_as_the_sample_grows() -> None:
    _, wide = wilson(0, 10)
    _, narrow = wilson(0, 400)
    assert narrow < wide


def test_detection_floor_shrinks_with_more_trials() -> None:
    assert detection_floor(3) > detection_floor(8) > detection_floor(159)


def test_detection_floor_matches_the_definition() -> None:
    """r such that a clean run of n trials happens with probability 5%."""
    n = 50
    r = detection_floor(n)
    assert (1 - r) ** n == pytest.approx(0.05, rel=1e-9)


def test_small_samples_are_reported_as_weak() -> None:
    """Three trials per case cannot rule out a large error rate."""
    assert detection_floor(3) > 0.5
    # Only a large aggregate can support a tight bound.
    assert detection_floor(159) < 0.02


def test_infra_failures_are_not_routing_errors() -> None:
    """A crashed dispatch must not count as a wrong route, or as a right one."""
    from routing_flake_report import INFRA

    trials = [
        {"verdict": "correct", "chosen_route": "R08"},
        {"verdict": "dispatch_error", "chosen_route": None},
        {"verdict": "timeout", "chosen_route": None},
    ]
    valid = [t for t in trials if t["verdict"] not in INFRA]
    infra = [t for t in trials if t["verdict"] in INFRA]

    assert len(valid) == 1 and len(infra) == 2
    errors = sum(1 for t in valid if t["verdict"] != "correct")
    assert errors == 0, "infrastructure failures must not become routing errors"


def test_infra_failure_does_not_make_a_case_look_flaky() -> None:
    """Two identical answers plus a crash is not an unstable route."""
    from routing_flake_report import INFRA

    trials = [
        {"verdict": "correct", "chosen_route": "R08"},
        {"verdict": "timeout", "chosen_route": None},
        {"verdict": "correct", "chosen_route": "R08"},
    ]
    seen = sorted({str(t["chosen_route"]) for t in trials
                   if t["verdict"] not in INFRA})
    assert seen == ["R08"], "a crash must not turn one route into two"


def test_retry_helper_does_not_retry_a_wrong_answer() -> None:
    """Retries are for infrastructure, never for re-rolling a routing decision."""
    import routing_eval

    calls: list[int] = []

    def fake_dispatch(*_args, **_kwargs):
        calls.append(1)
        return ("wire", "ROUTE: R11 - wrong on purpose")

    original = routing_eval.dispatch
    routing_eval.dispatch = fake_dispatch  # type: ignore[assignment]
    try:
        wire, text = routing_eval.dispatch_with_retries(
            "prompt", routing_eval.Path("/tmp"), "m", 1, 3, {})
    finally:
        routing_eval.dispatch = original  # type: ignore[assignment]

    assert len(calls) == 1, "a successful dispatch must not be retried"
    assert "R11" in text


def test_retry_helper_retries_an_infrastructure_failure() -> None:
    """A transport fault is re-dispatched; the first two attempts fail."""
    import routing_eval

    calls: list[int] = []

    def flaky_dispatch(*_args, **_kwargs):
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("codex exit 101: transport channel closed")
        return ("wire", "ROUTE: R10 - ok")

    original = routing_eval.dispatch
    routing_eval.dispatch = flaky_dispatch  # type: ignore[assignment]
    try:
        _wire, text = routing_eval.dispatch_with_retries(
            "prompt", routing_eval.Path("/tmp"), "m", 1, 3, {})
    finally:
        routing_eval.dispatch = original  # type: ignore[assignment]

    assert len(calls) == 3, "should have retried twice then succeeded"
    assert "R10" in text


def test_retry_helper_gives_up_after_the_budget() -> None:
    import routing_eval

    calls: list[int] = []

    def always_fails(*_args, **_kwargs):
        calls.append(1)
        raise TimeoutError("codex exec exceeded 300s")

    original = routing_eval.dispatch
    routing_eval.dispatch = always_fails  # type: ignore[assignment]
    try:
        try:
            routing_eval.dispatch_with_retries(
                "prompt", routing_eval.Path("/tmp"), "m", 1, 2, {})
        except TimeoutError:
            pass
        else:
            raise AssertionError("expected the timeout to surface")
    finally:
        routing_eval.dispatch = original  # type: ignore[assignment]

    assert len(calls) == 3, "one attempt plus two retries"
