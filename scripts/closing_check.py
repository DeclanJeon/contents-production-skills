#!/usr/bin/env python3
"""Offline checks for the creative-production closing contract.

A reply ends with exactly one closing line:

* ``다음: <next stage> — 자동 진행``  (more stages remain; the next turn starts
  that stage automatically), or
* ``대기: <specific gate or blocking fact> — 필요: <exact approval or fact>``.

An optional offer ("원하시면 … 이어서", "if you'd like", "want me to") is never a
closing line because it makes the user's reply a precondition for work that
needs none. See ``creative-production/references/policy.md`` (Closing line).
"""
from __future__ import annotations

import re

TAIL_LINES = 6

OPTIONAL_OFFER_PATTERNS = (
    r"원하시면",
    r"원하면",
    r"필요하시면",
    r"할까요",
    r"까요\s*[?？]",
    r"드릴까요",
    r"주실래요",
    r"(말씀|이야기)\s*(해\s*)?(주시면|하시면)",
    r"주시면[^\n]{0,80}(이어서|이어|진행|작성|구체화|확정|확장|하겠습니다|드리겠습니다)",
    r"(이어서|확장)[^\n]{0,40}(수\s*있습니다|가능합니다|수\s*있어요)",
    r"(만들|작성할|쓸|변환할|확장할)\s*수\s*(있습니다|있어요)",
    r"if\s+you(?:'|’)d\s+like",
    r"if\s+you\s+(?:want|wish|prefer)",
    r"would\s+you\s+like",
    r"want\s+me\s+to",
    r"shall\s+i\b",
    r"let\s+me\s+know",
    r"feel\s+free\s+to",
)
_OPTIONAL_OFFER = re.compile("|".join(f"(?:{p})" for p in OPTIONAL_OFFER_PATTERNS), re.IGNORECASE)

_MARKUP = " \t*_`>#-"
_NEXT_LINE = re.compile(r"^다음\s*:\s*\S.*자동\s*진행")
_WAIT_LINE = re.compile(r"^대기\s*:\s*\S.*필요\s*:\s*(?P<need>\S.*)$")

# Facts the next stage can carry as a labelled placeholder (`[브랜드명]`), so they
# are not a reason to stop. Approval words mean a real gate and are never flagged.
PLACEHOLDERABLE_FACTS = ("브랜드명", "브랜드 이름", "카페 이름", "카페명", "로고", "슬로건", "카피", "외형", "연령", "태그라인")
APPROVAL_WORDS = ("승인", "동의", "권한", "허가", "비용", "예산", "결제", "권리", "게시", "실행")


def _tail(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-TAIL_LINES:]


def find_optional_offer(text: str) -> str | None:
    """Return the first tail line (last ~6 non-empty lines) that is an optional offer."""
    for line in _tail(text):
        if _OPTIONAL_OFFER.search(line):
            return line
    return None


def _last_line(text: str) -> str:
    tail = _tail(text)
    return tail[-1].strip(_MARKUP) if tail else ""


def closing_form(text: str) -> str | None:
    """Return 'next' or 'wait' when the last non-empty line is a contract closing line."""
    line = _last_line(text)
    if _NEXT_LINE.match(line):
        return "next"
    if _WAIT_LINE.match(line):
        return "wait"
    return None


def blocking_on_placeholderable_fact(text: str) -> str | None:
    """Return the ``필요:`` part when a wait line asks only for facts a placeholder can carry."""
    match = _WAIT_LINE.match(_last_line(text))
    if not match:
        return None
    need = match.group("need")
    if any(word in need for word in PLACEHOLDERABLE_FACTS) and not any(word in need for word in APPROVAL_WORDS):
        return need
    return None
