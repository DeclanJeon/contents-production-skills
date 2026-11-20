#!/usr/bin/env python3
"""Offline checks for the creative-production closing contract.

A reply ends with exactly one closing line:

* ``다음: <next stage> — 자동 진행``  (more stages remain; the next turn starts
  that stage automatically), or
* ``대기: <specific gate or blocking fact> — 필요: <exact approval or fact>``,
  allowed only for execution/spend approval (which also asks board/G2 acceptance), rights/likeness/voice consent,
  publication approval, a stop the user named, or no subject/purpose at all.

The closing line is the final line: nothing (notes, offers, summaries) follows it.
It matches exactly ``^다음: [^—(]+ — 자동 진행$`` or ``^대기: [^—]+ — 필요: .+$``:
no parentheses or hedges ("가능", "요청해 주세요", "주시면") and no mixed forms.
G1, plan acceptance, brand names and copy are never a 대기 reason.

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
# The closing line is exactly one of these two patterns and nothing else.
_NEXT_LINE = re.compile(r"다음: [^—(]+ — 자동 진행")
_WAIT_LINE = re.compile(r"대기: [^—]+ — 필요: (?P<need>.+)")
# Hedges inside a closing line, e.g. "자동 진행 가능 (원하시면 요청해 주세요)".
_CLOSING_HEDGE = re.compile(r"가능\s*[(（]|요청해\s*주세요|주시면")

# Facts the next stage can carry as a labelled placeholder (`[브랜드명]`), so they
# are not a reason to stop. Approval words mean a real gate and are never flagged.
PLACEHOLDERABLE_FACTS = ("브랜드명", "브랜드 이름", "카페 이름", "카페명", "로고", "슬로건", "카피", "외형", "연령", "태그라인")
APPROVAL_WORDS = ("승인", "동의", "권한", "허가", "비용", "예산", "결제", "권리", "게시", "실행")


def _tail(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-TAIL_LINES:]


def _is_closing_start(line: str) -> bool:
    return line.strip(_MARKUP).startswith(("다음:", "대기:"))


def _is_prose(line: str) -> bool:
    return not line.startswith(("|", "#"))


def _closing_region(text: str) -> list[str]:
    """Lines where an optional offer can sit.

    With a closing line: up to two prose lines immediately above the last
    다음:/대기: line, that line, and everything after it. Without one: the last
    three prose lines. Prose excludes table rows (``|``) and headings (``#``), so
    storyboard dialogue in table cells is never read as an offer.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    starts = [i for i, line in enumerate(lines) if _is_closing_start(line)]
    if starts:
        above = [line for line in lines[:starts[-1]] if _is_prose(line)][-2:]
        return above + lines[starts[-1]:]
    return [line for line in lines if _is_prose(line)][-3:]


def find_optional_offer(text: str) -> str | None:
    """Return the first line of the closing region that is an optional offer."""
    for line in _closing_region(text):
        if _OPTIONAL_OFFER.search(line):
            return line
    return None


def _last_line(text: str) -> str:
    tail = _tail(text)
    return tail[-1].strip(_MARKUP) if tail else ""


def closing_hedge(line: str) -> str | None:
    """Return the hedge found inside a closing-looking line ("가능 (", "요청해 주세요", "주시면")."""
    found = _CLOSING_HEDGE.search(line)
    return found.group(0) if found else None


def mixed_closing(line: str) -> bool:
    """True when one line holds both a ``다음:`` and a ``대기:`` closing form."""
    return "다음:" in line and "대기:" in line


def _exact_form(line: str) -> str | None:
    """'next' or 'wait' when the line is exactly one contract pattern, hedge-free and unmixed."""
    if closing_hedge(line) or mixed_closing(line):
        return None
    if _NEXT_LINE.fullmatch(line):
        return "next"
    if _WAIT_LINE.fullmatch(line):
        return "wait"
    return None


def closing_form(text: str) -> str | None:
    """Return 'next' or 'wait' when the last non-empty line is exactly a contract closing line.

    Exact patterns: ``^다음: [^—(]+ — 자동 진행$`` and ``^대기: [^—]+ — 필요: .+$``.
    A hedge ("자동 진행 가능 (…)", "요청해 주세요", "주시면"), parentheses in a 다음
    line, or both forms in one line make it None.
    """
    return _exact_form(_last_line(text))


def closing_defect(text: str) -> str | None:
    """Explain why a 다음:/대기:-looking last line is not an exact closing line, else None."""
    line = _last_line(text)
    if not (line.startswith("다음") or line.startswith("대기")) or _exact_form(line):
        return None
    if "–" in line and "—" not in line:
        return f"wrong dash '–' (use em dash '—') in closing line: {line!r}"
    hedge = closing_hedge(line)
    if hedge:
        return f"hedge {hedge!r} in closing line: {line!r}"
    if mixed_closing(line):
        return f"mixed 다음:/대기: forms in one line: {line!r}"
    return f"closing line is not an exact pattern: {line!r}"


def blocking_on_placeholderable_fact(text: str) -> str | None:
    """Return the ``필요:`` part when a wait line asks only for facts a placeholder can carry."""
    line = _last_line(text)
    match = _WAIT_LINE.fullmatch(line) if _exact_form(line) == "wait" else None
    if not match:
        return None
    need = match.group("need")
    if any(word in need for word in PLACEHOLDERABLE_FACTS) and not any(word in need for word in APPROVAL_WORDS):
        return need
    return None


# 대기 is a closed list: execution/spend approval, rights/likeness/voice consent,
# publication approval, a stop the user named, or no subject/purpose at all.
ALLOWED_WAIT_KEYWORDS = (
    "실행", "비용", "유료", "결제", "예산", "권리", "동의", "초상", "목소리", "게시",
    "중단", "정지", "주제", "목적",
)
# G1, plan/board acceptance, placeholderable facts and preferences never justify 대기.
_DISALLOWED_WAIT = re.compile(
    r"G1(?!\d)|기획(?:안)?\s*(?:승인|수락)|보드\s*(?:승인|수용|확인)|스토리보드\s*(?:승인|수용|확인)|수락|채택"
    r"|브랜드\s*(?:명|이름)|카피|로고|슬로건|취향|선호|외형|연령|태그라인",
    re.IGNORECASE,
)


# A paid/external-execution 대기 may also ask for board (G2) acceptance: without
# pre-delegation G2 folds into that single stop.
_BOARD_ACCEPTANCE = re.compile(r"(?:G2\s*)?(?:스토리보드|보드)\s*(?:승인|수용|확인|수락)|G2\s*(?:검수\s*)?(?:승인|수락)")
_PAID_WORDS = ("실행", "비용", "유료", "결제")
# Board acceptance is stripped only beside a paid-execution word followed by 승인 in the same clause.
_PAID_APPROVAL = re.compile(r"(?:실행|비용|유료|결제)[^—]*승인")


def wait_reason_allowed(line: str) -> bool:
    """True when a ``대기:`` line names only a reason from the closed allowed list.

    Heuristic: false when the line mentions G1, plan acceptance, a brand name,
    copy or similar placeholderable facts, or when it names no allowed reason keyword.
    Board/G2 acceptance is disallowed alone but allowed alongside a paid-execution 승인 clause.
    """
    text = line.strip(_MARKUP)
    if _PAID_APPROVAL.search(text):
        text = _BOARD_ACCEPTANCE.sub("", text)
    if _DISALLOWED_WAIT.search(text):
        return False
    return any(word in text for word in ALLOWED_WAIT_KEYWORDS)


def disallowed_wait_reason(text: str) -> str | None:
    """Return the closing 대기 line when its reason is not on the allowed list."""
    line = _last_line(text)
    if _exact_form(line) == "wait" and not wait_reason_allowed(line):
        return line
    return None


def is_paid_execution_wait(text: str) -> bool:
    """True when the closing line is a 대기 for paid/external execution or its cost."""
    line = _last_line(text)
    return _exact_form(line) == "wait" and any(word in line for word in _PAID_WORDS)


def text_after_closing(text: str) -> str | None:
    """Return the first non-empty line after a closing line, or None.

    Only the last ~6 lines are scanned. A parenthetical that merely mentions
    ``대기:`` does not count as a closing line, since a closing line starts with its form.
    """
    tail = _tail(text)
    for index, raw in enumerate(tail):
        line = raw.strip(_MARKUP)
        if _exact_form(line) and index < len(tail) - 1:
            return tail[index + 1]
    return None
