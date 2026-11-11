# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Parse source-anchored editing scope into immutable values."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Final, Literal, NoReturn, TypeAlias

JsonValue: TypeAlias = "None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]"
Kind: TypeAlias = Literal["dialogue", "narration", "direction"]
SCHEMA: Final = "korean-script-postediting/1"


class PacketError(ValueError):
    """A malformed scope cannot be judged."""
    def __init__(self, reason: str) -> None:
        self.reason: str = reason
        super().__init__(reason)


@dataclass(frozen=True, slots=True)
class ProtectedSpan:
    start: int
    end: int
    after_start: int
    after_end: int
    text: str


@dataclass(frozen=True, slots=True)
class Unit:
    locator: str
    kind: Kind
    speaker: str | None
    start: int
    end: int
    before: str
    after: str
    editable: bool
    reason: str
    protected_spans: tuple[ProtectedSpan, ...]


@dataclass(frozen=True, slots=True)
class Packet:
    schema: str
    source_sha256: str
    units: tuple[Unit, ...]


def mapping(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise PacketError("expected JSON object")
    return value


def sequence(value: JsonValue) -> list[JsonValue]:
    if not isinstance(value, list):
        raise PacketError("expected JSON array")
    return value


def text(data: dict[str, JsonValue], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise PacketError(f"{key}: expected string")
    _ = value.encode("utf-8")
    return value


def integer(data: dict[str, JsonValue], key: str) -> int:
    value = data.get(key)
    if type(value) is not int:
        raise PacketError(f"{key}: expected integer, not bool")
    return value


def spans(data: JsonValue, pair: tuple[str, str]) -> tuple[ProtectedSpan, ...]:
    result: list[ProtectedSpan] = []
    last_before = last_after = 0
    for raw in sequence(data):
        item = mapping(raw)
        span = ProtectedSpan(integer(item, "start"), integer(item, "end"),
                             integer(item, "after_start"), integer(item, "after_end"),
                             text(item, "text"))
        if not (last_before <= span.start < span.end <= len(pair[0])
                and last_after <= span.after_start < span.after_end <= len(pair[1])):
            raise PacketError("protected span range/order/overlap")
        if pair[0][span.start:span.end] != span.text:
            raise PacketError("protected span does not match source")
        if span.after_end - span.after_start != len(span.text):
            raise PacketError("protected candidate span length")
        result.append(span)
        last_before, last_after = span.end, span.after_end
    return tuple(result)


def parse_unit(raw: JsonValue) -> Unit:
    data = mapping(raw)
    editable = data.get("editable")
    if type(editable) is not bool:
        raise PacketError("editable: expected bool")
    if "speaker" not in data or "protected_spans" not in data:
        raise PacketError("speaker and protected_spans are required")
    speaker = data["speaker"]
    if speaker is not None and not isinstance(speaker, str):
        raise PacketError("speaker: expected string or null")
    kind = text(data, "kind")
    if kind not in ("dialogue", "narration", "direction"):
        raise PacketError("unsupported kind")
    before, after = text(data, "before"), text(data, "after")
    unit = Unit(text(data, "locator"), kind, speaker,
                integer(data, "start"), integer(data, "end"), before, after,
                editable, text(data, "reason"), spans(data["protected_spans"], (before, after)))
    if not unit.locator.strip():
        raise PacketError("empty locator")
    if before != after and not unit.reason.strip():
        raise PacketError("changed unit requires reason")
    return unit


def parse_packet(data: JsonValue, source: str) -> Packet:
    """Parse explicit ranges; never infer roles or quote provenance."""
    raw = mapping(data)
    if text(raw, "schema") != SCHEMA:
        raise PacketError("unsupported schema")
    digest = text(raw, "source_sha256")
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise PacketError("invalid source_sha256")
    units = tuple(parse_unit(item) for item in sequence(raw.get("units")))
    previous_end = 0
    seen: set[str] = set()
    for unit in units:
        if unit.locator in seen:
            raise PacketError("duplicate locator")
        if not previous_end <= unit.start < unit.end <= len(source):
            raise PacketError("unit range/order/overlap")
        if source[unit.start:unit.end] != unit.before:
            raise PacketError("before does not match source range")
        seen.add(unit.locator)
        previous_end = unit.end
    return Packet(SCHEMA, digest, units)


def unique_object(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    """Reject duplicate keys rather than silently choosing the last permission."""
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise PacketError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> NoReturn:
    raise PacketError(f"nonfinite JSON constant: {value}")


def load_packet(raw: bytes) -> JsonValue:
    """Decode strict UTF-8 JSON without duplicate-key or NaN ambiguity."""
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)
