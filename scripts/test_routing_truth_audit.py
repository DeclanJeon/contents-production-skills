"""The ground-truth audit must fail when the ground truth is wrong.

Every check is exercised twice: once on the real data (it must pass) and once
on a deliberately corrupted copy (it must fail). A check that can only pass is
decoration.
"""
from __future__ import annotations

import copy

import routing_truth_audit as audit


def _data():
    return audit.load()


def test_real_data_passes_every_check() -> None:
    routes, cases = _data()
    for name, check in audit.CHECKS:
        problems, _notes = check(routes, cases)
        assert not problems, f"{name} failed on the real data: {problems[:3]}"


def test_coverage_fails_when_a_route_loses_its_case() -> None:
    routes, cases = _data()
    trimmed = [c for c in cases if c["route_id"] != "R02"]
    problems, _ = audit.check_coverage(routes, trimmed)
    assert any("R02" in p for p in problems)


def test_exclusion_fails_when_a_withheld_request_becomes_execution() -> None:
    routes, cases = _data()

    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "B04":      # "...이미지는 아직 만들지 말고"
                case["route_id"] = "R24"      # executed_media
        return out

    problems, _ = audit.check_exclusions(routes, corrupt(cases))
    assert any("B04" in p for p in problems), problems


def test_warrant_fails_when_execution_is_expected_without_authority() -> None:
    routes, cases = _data()

    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "B03":
                # Strip every execution signal, keep the executed-media route.
                case["prompt"] = "이 장면을 어떻게 만들지 정리해줘"
        return out

    problems, _ = audit.check_warrant(routes, corrupt(cases))
    assert any("B03" in p for p in problems), problems


def test_contrast_fails_when_both_sides_share_a_route() -> None:
    routes, cases = _data()

    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "B04":      # pairs with B03 on media_axis
                case["route_id"] = "R24"
        return out

    problems, _ = audit.check_contrast_pairs(routes, corrupt(cases))
    assert any("B03" in p and "B04" in p for p in problems), problems


def test_contrast_fails_when_the_dimension_does_not_actually_flip() -> None:
    routes, cases = _data()
    # B10/B11 are declared to flip authority_axis. Point both at text-only
    # routes whose authority axis is empty and the declaration becomes false.
    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "B11":
                case["route_id"] = "R10"
        return out

    problems, _ = audit.check_contrast_pairs(routes, corrupt(cases))
    assert any("authority_axis" in p for p in problems), problems


def test_skew_is_reported_not_failed() -> None:
    """Dominance is a statement about coverage, not a defect to fix."""
    routes, cases = _data()
    problems, notes = audit.check_skew(routes, cases)
    assert problems == []
    assert any("dominated" in n for n in notes), notes


def test_owner_check_fails_when_the_owner_is_wrong() -> None:
    """Regression: a new case declared R24's owner as the wrong skill."""
    routes, cases = _data()

    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "D02":
                case["expected_owner"] = "video-production-assets"
        return out

    problems, _ = audit.check_owner(routes, corrupt(cases))
    assert any("D02" in p for p in problems), problems


def test_same_route_check_fails_when_a_non_distinction_gets_split() -> None:
    """If someone 'fixes' E02 back to R24, this must fail immediately.

    E02 was first written expecting R24. The model answered R12 every time, and
    the skill's own prose confirmed R12 -- new stills are in scope for
    storytelling-with-still-images. The pair is now declared a non-distinction.
    """
    routes, cases = _data()

    def corrupt(case_list):
        out = copy.deepcopy(case_list)
        for case in out:
            if case["case_id"] == "E02":
                case["route_id"] = "R24"
                case["expected_owner"] = "creative-production"
        return out

    problems, _ = audit.check_same_route(routes, corrupt(cases))
    assert any("E01" in p and "E02" in p for p in problems), problems


def test_real_data_same_route_pairs_hold() -> None:
    routes, cases = _data()
    problems, notes = audit.check_same_route(routes, cases)
    assert problems == [], problems
    assert any("both R12" in note for note in notes), notes
