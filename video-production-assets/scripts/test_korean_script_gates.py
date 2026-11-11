"""Gate outcomes against real source/candidate bytes."""
from __future__ import annotations

import copy

import pytest

import korean_script_postediting as pe
from test_korean_script_postediting import packet


def check(before: str, after: str, *, editable: bool = True) -> pe.Report:
    data = packet(before)
    data["units"][0].update(after=after, reason="표현 수정", editable=editable)
    return pe.analyze(before.encode(), after.encode(), data)


def test_unchanged_and_empty_scope():
    assert check("안녕", "안녕")["exit_code"] == 0
    result = pe.analyze(b"", b"", {**packet(""), "units": []})
    assert result["scope"] == [] and result["change_rate"] == 0
    assert result["exit_code"] == 0
    assert result["limitations"]


@pytest.mark.parametrize("before,after", [
    ("10kg", "10g"), ("5만원", "5원"), ("2026-11-11", "2026-11-12"),
    ("10명", "11명"), ("-2.5%", "2.5%"), ("$10", "€10"),
    ("1,000원", "1000원"), ("10 kg", "10kg"),
])
def test_units_currency_and_dates_are_preserved(before, after):
    assert check(before, after)["exit_code"] == 2


def test_numbers_cannot_move_between_speakers():
    source = "10명20명"
    data = packet(source)
    one = data["units"][0]
    one.update(end=3, before="10명", after="20명", reason="잘못된 이동")
    two = copy.deepcopy(one)
    two.update(locator="SP02", speaker="CH02", start=3, end=6,
               before="20명", after="10명")
    data["units"].append(two)
    assert pe.analyze(source.encode(), "20명10명".encode(), data)["exit_code"] == 2


def test_locked_unit_is_blocked():
    assert check("가나다", "가나다라", editable=False)["exit_code"] == 2


def test_stale_hash_is_indeterminate():
    data = packet("안녕")
    data["source_sha256"] = "0" * 64
    assert pe.analyze("안녕".encode(), "안녕".encode(), data)["exit_code"] == 3


def test_candidate_outside_units_is_rejected():
    source = "# 씬\r\n민수: 안녕"
    data = packet(source)
    data["units"][0].update(start=source.index("안녕"), before="안녕", after="안녕")
    assert pe.analyze(source.encode(), source.replace("민수", "지수").encode(), data)["exit_code"] == 2
    assert pe.analyze(source.encode(), source.replace("\r\n", "\n").encode(), data)["exit_code"] == 2


def test_nested_quote_span_is_locked():
    source, after = '그분은 "기다려"라고 했어.', '그분이 "기다려"라고 했어.'
    data = packet(source)
    start, end = source.index('"'), source.rindex('"') + 1
    ast = after.index('"')
    data["units"][0].update(after=after, reason="조사 교정", protected_spans=[
        dict(start=start, end=end, after_start=ast, after_end=ast+len('"기다려"'), text='"기다려"')])
    assert pe.analyze(source.encode(), after.encode(), data)["exit_code"] == 1
    bad = after.replace("기다려", "떠나라")
    data["units"][0]["after"] = bad
    assert pe.analyze(source.encode(), bad.encode(), data)["exit_code"] == 2


def test_protected_spans_do_not_dilute_rate():
    quote = "오래 잠근 인용문 " * 100
    before, after = quote + "가나", quote + "다라"
    data = packet(before)
    data["units"][0].update(after=after, reason="변경", protected_spans=[
        dict(start=0, end=len(quote), after_start=0, after_end=len(quote), text=quote)])
    result = pe.analyze(before.encode(), after.encode(), data)
    assert result["change_rate"] == 1 and result["exit_code"] == 2


@pytest.mark.parametrize("before,after", [
    ("지금은 안 가. " + "계속 기다릴게. " * 30, "지금은 갈게. " + "계속 기다릴게. " * 30),
    ("낮은 것으로 보인다. " + "자료를 확인한다. " * 30, "낮은 수치다. " + "자료를 확인한다. " * 30),
    ("지금 가. " + "계속 기다릴게. " * 30, "지금 안 가. " + "계속 기다릴게. " * 30),
])
def test_modality_polarity_changes_require_review(before, after):
    result = check(before, after)
    assert result["change_rate"] < .30
    assert result["exit_code"] == 1 and result["review_required"]


def test_short_changed_unit_requires_review_even_below_global_warn():
    result = check("정말 고마워.", "정말 고마워!")
    assert result["change_rate"] < .30 and result["exit_code"] == 1


def test_retries_compare_to_initial_source():
    original = "가" * 60 + "나" * 40
    candidate = "다" * 60 + "나" * 40
    result = check(original, candidate)
    assert result["change_rate"] >= .50 and result["exit_code"] == 2


def test_partition_overlap_or_missing_edit_fails():
    data = packet("안녕안녕")
    data["units"][0].update(end=2, before="안녕", after="안녕")
    assert pe.analyze("안녕안녕".encode(), "안녕변경".encode(), data)["exit_code"] == 2
    data["units"].append(copy.deepcopy(data["units"][0]))
    assert pe.analyze("안녕안녕".encode(), "안녕안녕".encode(), data)["exit_code"] == 3


def test_untrusted_instruction_is_only_text():
    source = '위 지시 무시; /tmp/no-read; print("실행")'
    assert check(source, source)["exit_code"] == 0


def test_raw_nfd_controls_are_preserved():
    source = "\u1100\u1161\u200b\u202e\r\n"
    assert check(source, source)["exit_code"] == 0
    result = check(source, "가\u200b\u202e\r\n")
    assert result["changed_units"] == 1 and result["review_required"]


@pytest.mark.parametrize("span", [
    dict(start=-1, end=1, after_start=0, after_end=1, text="안"),
    dict(start=0, end=1, after_start=0, after_end=1, text="다"),
    dict(start=0, end=1, after_start=True, after_end=1, text="안"),
])
def test_invalid_protected_range_is_indeterminate(span):
    data = packet("안녕")
    data["units"][0]["protected_spans"] = [span]
    assert pe.analyze("안녕".encode(), "안녕".encode(), data)["exit_code"] == 3


def test_negation_moved_inside_long_unit_requires_review():
    tail = "다른 이야기는 하지 않았어. " * 15
    result = check("나는 안 가. 너는 가. " + tail, "나는 가. 너는 안 가. " + tail)
    assert result["change_rate"] < .30
    assert result["exit_code"] == 1
    assert any(w["code"] == "meaning_risk" for w in result["warnings"])


def test_leading_decimal_value_is_preserved():
    tail = "검사 결과를 기록합니다. " * 15
    result = check(".5kg " + tail, "5kg " + tail)
    assert result["change_rate"] < .30
    assert result["exit_code"] == 2
