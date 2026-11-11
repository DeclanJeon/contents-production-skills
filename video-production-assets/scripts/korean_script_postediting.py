# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
# ─── How to run ───
# python3 korean_script_postediting.py --source original.md --candidate candidate.md --packet packet.json
"""Read-only Korean speech editing gates, not a semantic quality certificate."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Final, NoReturn, TypedDict

from korean_script_packet import JsonValue, PacketError, Unit, load_packet, parse_packet

LIMITATIONS: Final = (
    "의미·인물성·권한 진위·실제 청취·사용자 승인 미검증. "
    "명시된 범위만 검사하며 미등록 고유명사·한국어 수사·인용 출처는 자동 인증하지 않는다."
)
NUMBER: Final = re.compile(
    r"[$₩€]?[+-]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)(?:[ \t]*(?:억원|만원|kg|mg|km|cm|mm|ml|°C|"
    r"원|년|월|일|시|분|초|명|개|회|배|g|m|L|℃|%))?"
)
RISK: Final = re.compile(r"(?<![가-힣])(?:안|못)(?=\s)|않|없|수\s*있|수도|것\s*같|보인다|해야|필요하")
QUOTE: Final = re.compile(r'["“”‘’]')


class Issue(TypedDict):
    code: str
    locator: str
    reason: str


class UnitReport(TypedDict):
    locator: str
    change_rate: float
    full_change_rate: float
    weight: int
    changed: bool


class Report(TypedDict):
    schema: str
    source_sha256: str
    exit_code: int
    scope: list[str]
    change_rate: float
    changed_units: int
    review_required: bool
    blockers: list[Issue]
    warnings: list[Issue]
    units: list[UnitReport]
    limitations: str


def change_rate(before: str, after: str) -> float:
    """Compare NFC copies without deleting punctuation or whitespace."""
    left, right = (unicodedata.normalize("NFC", s) for s in (before, after))
    return 1.0 - difflib.SequenceMatcher(None, left, right, autojunk=False).ratio()


def rate_band(rate: float) -> int:
    """Return a gate without rounding away exact threshold boundaries."""
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise PacketError("rate outside finite [0,1]")
    if rate >= 0.50:
        return 2
    if rate >= 0.30:
        return 1
    return 0


def report_shell(source: bytes) -> Report:
    return Report(schema="korean-script-postediting-report/1",
                  source_sha256=hashlib.sha256(source).hexdigest(), exit_code=0,
                  scope=[], change_rate=0, changed_units=0, review_required=False,
                  blockers=[], warnings=[], units=[], limitations=LIMITATIONS)


def issue(code: str, locator: str, reason: str) -> Issue:
    return Issue(code=code, locator=locator, reason=reason)


def editable_text(unit: Unit) -> tuple[str, str]:
    """Remove explicit locked spans on comparison copies only."""
    left, right = unit.before, unit.after
    for span in reversed(unit.protected_spans):
        left = left[:span.start] + left[span.end:]
        right = right[:span.after_start] + right[span.after_end:]
    return left, right


def inspect_unit(unit: Unit, result: Report) -> UnitReport:
    changed = unit.before != unit.after
    if changed and not unit.editable:
        result["blockers"].append(issue("locked_unit", unit.locator, "비편집 발화 변경"))
    for span in unit.protected_spans:
        if unit.after[span.after_start:span.after_end] != span.text:
            result["blockers"].append(issue("protected_span", unit.locator, "잠금 구간 변경"))
    if NUMBER.findall(unit.before) != NUMBER.findall(unit.after):
        result["blockers"].append(issue("numbers", unit.locator, "수치·단위·날짜 토큰 변경"))
    left, right = editable_text(unit)
    rate = change_rate(left, right) if unit.editable else 0.0
    weight = max(len(unicodedata.normalize("NFC", s)) for s in (left, right)) if unit.editable else 0
    if changed:
        if len(unit.before) < 100:
            result["warnings"].append(issue("short_unit", unit.locator, "100자 미만 수정: 정밀 원문 대조"))
        if [(m.group(), m.start()) for m in RISK.finditer(unit.before)] != [
                (m.group(), m.start()) for m in RISK.finditer(unit.after)]:
            result["warnings"].append(issue("meaning_risk", unit.locator, "부정·서법 변화: 양방향 의미 대조"))
        if QUOTE.search(unit.before) or QUOTE.search(unit.after):
            result["warnings"].append(issue("quote_context", unit.locator, "실제 인용/창작 대사 구분 확인"))
    return UnitReport(locator=unit.locator, change_rate=rate,
                      full_change_rate=change_rate(unit.before, unit.after),
                      weight=weight, changed=changed)


def analyze(source: bytes, candidate: bytes, packet_data: JsonValue) -> Report:
    """Judge a candidate against the initial source and explicit editing scope."""
    result = report_shell(source)
    try:
        original = source.decode("utf-8")
        _ = candidate.decode("utf-8")
        packet = parse_packet(packet_data, original)
        if packet.source_sha256 != result["source_sha256"]:
            raise PacketError("source_sha256 does not match initial source")
        result["scope"] = [unit.locator for unit in packet.units]
        cursor = 0
        parts: list[str] = []
        for unit in packet.units:
            parts.extend((original[cursor:unit.start], unit.after))
            cursor = unit.end
            result["units"].append(inspect_unit(unit, result))
        parts.append(original[cursor:])
        if "".join(parts).encode("utf-8") != candidate:
            result["blockers"].append(issue("candidate_scope", "document", "후보와 범위 패킷 불일치/범위 밖 변경"))
    except (PacketError, UnicodeError) as exc:
        result["exit_code"] = 3
        result["blockers"].append(issue("indeterminate", "packet", str(exc)))
        result["review_required"] = True
        return result
    weight = sum(unit["weight"] for unit in result["units"])
    rate = sum(unit["change_rate"] * unit["weight"] for unit in result["units"]) / weight if weight else 0
    result["change_rate"] = rate
    result["changed_units"] = sum(unit["changed"] for unit in result["units"])
    if rate_band(rate) > 0:
        result["warnings"].append(issue("change_rate", "scope", "30% 이상: 경고, 50% 이상: 채택 중단"))
    result["exit_code"] = 2 if result["blockers"] or rate_band(rate) == 2 else int(bool(result["warnings"]))
    result["review_required"] = bool(result["exit_code"])
    return result


class GateParser(argparse.ArgumentParser):
    """Keep CLI usage errors in the same JSON/exit-3 contract."""
    def error(self, message: str) -> NoReturn:
        raise PacketError(message)


class InputPaths(argparse.Namespace):
    source: Path
    candidate: Path
    packet: Path


def main(argv: list[str] | None = None) -> int:
    parser = GateParser(description=__doc__, allow_abbrev=False)
    for name in ("source", "candidate", "packet"):
        _ = parser.add_argument(f"--{name}", required=True, type=Path)
    try:
        args = parser.parse_args(argv, namespace=InputPaths())
        source = args.source.read_bytes()
        candidate = args.candidate.read_bytes()
        data = load_packet(args.packet.read_bytes())
        result = analyze(source, candidate, data)
    except (OSError, UnicodeError, json.JSONDecodeError, PacketError) as exc:
        result = report_shell(b"")
        result["exit_code"] = 3
        result["review_required"] = True
        result["blockers"].append(issue("indeterminate", "input", str(exc)))
    print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
