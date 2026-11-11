"""Packet boundaries and conservative change metrics."""
from __future__ import annotations

import copy
import hashlib
from typing import Literal, assert_never

import pytest

import korean_script_postediting as pe


def packet(source: str) -> dict[str, pe.JsonValue]:
    return {"schema": "korean-script-postediting/1",
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(), "units": [
                {"locator": "S01/SP01", "kind": "dialogue", "speaker": "CH01",
                 "start": 0, "end": len(source), "before": source, "after": source,
                 "editable": True, "reason": "", "protected_spans": []}]}


def test_rate_boundaries_and_empty():
    assert pe.change_rate("", "") == 0
    assert pe.change_rate("가", "") == 1
    assert pe.change_rate("가", "가") == 0
    assert [pe.rate_band(x) for x in (0.299999, 0.30, 0.499999, 0.50)] == [0, 1, 1, 2]


def test_nfc_only_for_comparison():
    assert pe.change_rate("가", "\u1100\u1161") == 0


@pytest.mark.parametrize("rate", [float("nan"), float("inf"), -float("inf"), -0.1, 1.1])
def test_rate_rejects_invalid_values(rate):
    with pytest.raises(ValueError):
        pe.rate_band(rate)


@pytest.mark.parametrize("field,value", [
    ("start", True), ("start", -1), ("end", 100), ("end", 0),
    ("editable", "true"), ("before", "다른 원문"), ("kind", "prompt"),
    ("speaker", 12), ("locator", ""), ("protected_spans", "bad"),
])
def test_packet_rejects_invalid_shape(field, value):
    data = packet("안녕")
    data["units"][0][field] = value
    with pytest.raises(pe.PacketError):
        pe.parse_packet(data, "안녕")


def test_packet_rejects_schema_and_missing_key():
    for mutation in ("schema", "missing"):
        data = packet("안녕")
        if mutation == "schema":
            data["schema"] = "other/1"
        else:
            del data["units"][0]["before"]
        with pytest.raises(pe.PacketError):
            pe.parse_packet(data, "안녕")


def test_repeated_dialogue_has_distinct_offsets():
    data = packet("안녕안녕")
    one = data["units"][0]
    one.update(end=2, before="안녕", after="안녕")
    two = copy.deepcopy(one)
    two.update(locator="S01/SP02", start=2, end=4)
    data["units"].append(two)
    parsed = pe.parse_packet(data, "안녕안녕")
    assert [u.start for u in parsed.units] == [0, 2]


@pytest.mark.parametrize("mutation", ["duplicate", "overlap", "reverse"])
def test_packet_rejects_duplicate_overlap_and_reverse(mutation: Literal["duplicate", "overlap", "reverse"]):
    data = packet("안녕안녕")
    one = data["units"][0]
    one.update(end=2, before="안녕", after="안녕")
    two = copy.deepcopy(one)
    two.update(locator="S02", start=2, end=4)
    match mutation:
        case "duplicate":
            two["locator"] = one["locator"]
        case "overlap":
            two.update(start=1, end=3, before="녕안", after="녕안")
        case "reverse":
            one, two = two, one
        case invalid:
            assert_never(invalid)
    data["units"] = [one, two]
    with pytest.raises(pe.PacketError):
        pe.parse_packet(data, "안녕안녕")
