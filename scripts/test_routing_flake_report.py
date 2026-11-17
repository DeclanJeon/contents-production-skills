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
