r"""Validation suite for voice-mix-finishing specification.

Implements acceptance criteria from wo-02-acceptance-criteria.md and team lead
review fixes from wo-04:
- Clean standalone helper functions for text and boundary validation
- Robust flag matching for ffmpeg -n ((?<!\S)-n(?!\S)) and new output file requirements
- Scope verification: approved/adopted take applicability
- Ambiguous request disambiguation requiring take-repair inspection or stage check
  in the same or immediately following sentence
- Elimination of boost contradiction (air boost coexisting with 150-300 Hz body boost)
- Prevention of prescriptive terms on empirical audio numbers (Korean & English)
- Level-matched A/B, listening verification, delivery policy citations, bypass path, mute respect
- CI-safe: No external version control or process execution dependencies inside pytest suite
  (invariants and registration checks are handled by verify_ticket21_invariants.py)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
FINISHING: Final = (
    ROOT / "creative-production/references/voice-mix-finishing.md"
)

POINTER_SOURCES: Final = (
    "creative-production/references/audio-production-routing.md",
    "creative-production/SKILL.md",
    "video-production-assets/references/take-repair.md",
    "storytelling-with-still-images/SKILL.md",
    "community-shorts-stills-pipeline/references/pipeline-stages.md",
)

EMPIRICAL_NUMBER_PATTERNS: Final = (
    re.compile(r"\b100\s*Hz\b", re.IGNORECASE),
    re.compile(r"\b80\s*Hz\b", re.IGNORECASE),
    re.compile(r"\b300\s*[-–~]\s*500\s*Hz\b", re.IGNORECASE),
    re.compile(r"\b800\s*Hz\s*[-–~]\s*1\.5\s*kHz\b", re.IGNORECASE),
    re.compile(r"\b150\s*[-–~]\s*300\s*Hz\b", re.IGNORECASE),
    re.compile(r"\b5\s*[-–~]\s*8\s*kHz\b", re.IGNORECASE),
    re.compile(r"\b8\s*kHz\b", re.IGNORECASE),
    re.compile(r"\b250\s*Hz\b", re.IGNORECASE),
    re.compile(r"\b2\s*kHz\b", re.IGNORECASE),
    re.compile(r"\b4\s*:\s*1\b"),
    re.compile(r"\b2\s*[-–~]\s*3\s*dB\b", re.IGNORECASE),
    re.compile(r"\b3\s*[-–~]\s*5\s*dB\b", re.IGNORECASE),
    re.compile(r"\b10\s*[-–~]\s*20\s*%", re.IGNORECASE),
    re.compile(r"\b20\s*ms\b", re.IGNORECASE),
    re.compile(r"\b1/4\b"),
    re.compile(r"\b1/8\b"),
)

FORBIDDEN_PRESCRIPTIVE_PATTERNS: Final = (
    # Korean prescriptive terms
    re.compile(r"엄격"),
    re.compile(r"표준값"),
    re.compile(r"최대"),
    re.compile(r"반드시"),
    re.compile(r"필수\s*규격"),
    re.compile(r"한정"),
    # English prescriptive terms
    re.compile(r"\bmust\b", re.IGNORECASE),
    re.compile(r"\bmandatory\b", re.IGNORECASE),
    re.compile(r"\bstrict\b", re.IGNORECASE),
    re.compile(r"\bstandard\s+value\b", re.IGNORECASE),
    re.compile(r"\bmaximum\b", re.IGNORECASE),
    re.compile(r"\bat\s+most\b", re.IGNORECASE),
    re.compile(r"\bonly\b", re.IGNORECASE),
    re.compile(r"\bnever\s+exceed\b", re.IGNORECASE),
)


def extract_sentences(text: str) -> list[str]:
    """Split markdown text into logical sentences for rule auditing."""
    sentences = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = re.split(r"(?<=[.!?。])\s+", line)
        for part in parts:
            p = part.strip()
            if p:
                sentences.append(p)
    return sentences


def check_prescriptive_words(text: str) -> list[str]:
    """Check that image-derived empirical baseline numbers do not have prescriptive terms attached."""
    sentences = extract_sentences(text)
    violations: list[str] = []
    for s in sentences:
        has_num = any(pat.search(s) for pat in EMPIRICAL_NUMBER_PATTERNS)
        if not has_num:
            continue
        for forbid in FORBIDDEN_PRESCRIPTIVE_PATTERNS:
            match = forbid.search(s)
            if match:
                violations.append(
                    f"Forbidden word '{match.group(0)}' in empirical sentence: {s!r}"
                )
    return violations


def check_boost_contradiction(text: str) -> list[str]:
    """Check that air boost is not claimed as exclusive/only, and 150-300 Hz body boost is documented."""
    sentences = extract_sentences(text)
    problems: list[str] = []

    for s in sentences:
        has_air = bool(re.search(r"(?:air|공기감|8\s*kHz)", s, re.IGNORECASE))
        has_boost = bool(re.search(r"(?:boost|부스트)", s, re.IGNORECASE))
        if has_air and has_boost:
            # Check restrictive phrasing in English or Korean
            if re.search(r"\b(?:only|limited to|exclusively|reserved for|restrict)\b|한정|에만|만\s", s, re.IGNORECASE):
                problems.append(f"Restrictive air boost phrasing: {s!r}")

    # 150-300 Hz body boost must be present as a creator example
    body_boost_pat = re.compile(
        r"(?:150\s*[-–~]\s*300\s*Hz.*(?:body|바디).*(?:boost|보강|업|lift|reinforce)|"
        r"(?:boost|보강|업|lift|reinforce).*(?:body|바디).*150\s*[-–~]\s*300\s*Hz|"
        r"150\s*[-–~]\s*300\s*Hz.*(?:boost|보강|업|lift|reinforce).*(?:body|바디)|"
        r"(?:boost|보강|업|lift|reinforce).*150\s*[-–~]\s*300\s*Hz)",
        re.IGNORECASE,
    )
    if not body_boost_pat.search(text):
        problems.append("missing 150-300 Hz body boost guideline")

    return problems


def check_mandatory_inclusions(text: str) -> list[str]:
    """Check for level matching, listening check, delivery policy, non-destructive output, bypass, and mute."""
    problems: list[str] = []

    # (a) Level-matched A/B comparison
    if not re.search(r"(level-matched|volume-matched|matched-level|level\s*matching|볼륨\s*맞추|레벨\s*매칭)", text, re.IGNORECASE):
        problems.append("missing level-matched A/B comparison rule")

    # (b) Subjective listening verification separated from metrics
    if "audio_listening_verified" not in text:
        problems.append("missing audio_listening_verified check")

    # (c) No independent delivery loudness target; citations required
    if not re.search(r"(no\s+(independent|custom|own)\s+loudness\s+target|자체\s*라우드니스\s*목표\s*(를\s*두지\s*않|없))", text, re.IGNORECASE):
        problems.append("missing declaration of no independent loudness target")

    sentences = extract_sentences(text)
    for s in sentences:
        if re.search(r"-\d+\s*LUFS", s):
            if not ("assembly.md" in s or "pipeline-stages.md" in s):
                problems.append(f"Sentence citing LUFS must cite owning pipeline reference (assembly.md or pipeline-stages.md): {s!r}")

    # (d) Non-destructive output with ffmpeg -n AND new output file requirement
    if not re.search(r"(?<!\S)-n(?!\S)", text):
        problems.append("missing non-destructive ffmpeg -n flag")
    if not re.search(r"(new output file|new file|새 파일|새로운 파일|separate output)", text, re.IGNORECASE):
        problems.append("missing requirement to output to a new/separate file")

    # (e) Bypass / no-processing pass
    if not re.search(r"\b(bypass|no-processing|no processing|무처리)\b", text, re.IGNORECASE):
        problems.append("missing bypass / no-processing path")

    # (f) Respect no_audio / mute
    if not re.search(r"\bno_audio\b|무음", text):
        problems.append("missing no_audio / mute respect rule")

    return problems


def check_boundary_rules(text: str, take_repair_text: str | None = None) -> list[str]:
    """Check ownership boundaries between take-repair and voice-mix-finishing."""
    problems: list[str] = []

    # (a) Applies to adopted/approved takes
    if not re.search(
        r"(applies to|scope|intended for|for\s+(?:approved|adopted)|적용|대상).*(?:(?:adopted|approved)\s+take|승인\s*된\s*(?:테이크|음성|대사))",
        text,
        re.IGNORECASE | re.DOTALL,
    ):
        problems.append("missing approved/adopted take scope statement")

    # (b) Defect repair links to take-repair.md
    if "take-repair.md" not in text:
        problems.append("missing link to take-repair.md for defect repair")

    # (c) Ambiguous requests do not jump straight to finishing; require checking take-repair or confirming stage
    sentences = extract_sentences(text)
    ambiguous_handled = False
    for i, s in enumerate(sentences):
        if re.search(r"\b(ambiguous|unclear context|no stated stage)\b|모호|맥락.*(없|미확인)", s, re.IGNORECASE):
            window = s + (" " + sentences[i + 1] if i + 1 < len(sentences) else "")
            if re.search(r"\b(take-repair|defect repair|confirm|check|verify)\b|결함 복구|상태 확인|점검", window, re.IGNORECASE):
                ambiguous_handled = True
                break
    if not ambiguous_handled:
        problems.append("ambiguous requests must check take-repair or confirm stage in the same or next sentence")

    # (d) take-repair.md cross-links back to voice-mix-finishing.md
    if take_repair_text is not None:
        if "voice-mix-finishing.md" not in take_repair_text:
            problems.append("take-repair.md missing cross-link pointer to voice-mix-finishing.md")

    return problems


def test_voice_mix_finishing_file_exists() -> None:
    """1. The voice-mix-finishing.md reference document must exist and be non-empty."""
    assert FINISHING.is_file(), (
        f"Missing required specification document: {FINISHING}"
    )
    content = FINISHING.read_text(encoding="utf-8").strip()
    assert len(content) > 100, f"{FINISHING} is unexpectedly empty"


def test_pointers_in_dependent_files_exist_and_resolve() -> None:
    """2. All dependent files must contain resolving pointer links to voice-mix-finishing.md."""
    missing_pointers: list[str] = []
    broken_links: list[str] = []

    for rel in POINTER_SOURCES:
        source_path = ROOT / rel
        assert source_path.is_file(), f"Source file does not exist: {source_path}"
        text = source_path.read_text(encoding="utf-8")
        if "voice-mix-finishing.md" not in text:
            missing_pointers.append(rel)
            continue

        links = re.findall(
            r"\[([^\]]+)\]\(([^)]*voice-mix-finishing\.md(?:#[^)]*)?)\)", text
        )
        if not links:
            missing_pointers.append(f"{rel} (names file but lacks markdown link)")
            continue

        for label, target in links:
            path_part, _, anchor_part = target.partition("#")
            resolved_file = (source_path.parent / path_part).resolve()
            if not resolved_file.is_file():
                broken_links.append(f"{rel} -> {target} (file not found)")
            elif anchor_part:
                target_text = resolved_file.read_text(encoding="utf-8")
                slug = anchor_part.lower().replace(" ", "-")
                if f"#{anchor_part}" not in target_text and f"{{#{anchor_part}}}" not in target_text:
                    headings = [
                        re.sub(r"[^\w\s-]", "", h.split(maxsplit=1)[-1].strip().lower()).replace(" ", "-")
                        for h in target_text.splitlines() if h.startswith("#")
                    ]
                    if slug not in headings:
                        broken_links.append(f"{rel} -> {target} (anchor not found)")

    assert not missing_pointers, (
        f"Files missing pointer to voice-mix-finishing.md: {missing_pointers}"
    )
    assert not broken_links, (
        f"Broken pointer links to voice-mix-finishing.md: {broken_links}"
    )


def test_boundary_rules_and_cross_links() -> None:
    """3. Ownership boundaries between take-repair and voice-mix-finishing must be explicit."""
    assert FINISHING.is_file(), (
        f"Missing required specification document: {FINISHING}"
    )
    text = FINISHING.read_text(encoding="utf-8")
    tr_text = (ROOT / "video-production-assets/references/take-repair.md").read_text(encoding="utf-8")

    problems = check_boundary_rules(text, tr_text)
    assert not problems, f"Boundary rule violations:\n" + "\n".join(problems)


def test_no_prescriptive_words_on_empirical_numbers() -> None:
    """4. Image-derived empirical baseline numbers must not have prescriptive terms attached."""
    assert FINISHING.is_file(), (
        f"Missing required specification document: {FINISHING}"
    )
    text = FINISHING.read_text(encoding="utf-8")
    violations = check_prescriptive_words(text)
    assert not violations, (
        f"Prescriptive words attached to empirical numbers:\n" + "\n".join(violations)
    )


def test_no_boost_contradiction() -> None:
    """5. Boost must not be claimed as air-only when 150-300 Hz body boost is also recommended."""
    assert FINISHING.is_file(), (
        f"Missing required specification document: {FINISHING}"
    )
    text = FINISHING.read_text(encoding="utf-8")
    problems = check_boost_contradiction(text)
    assert not problems, (
        f"Boost contradiction violations:\n" + "\n".join(problems)
    )


def test_mandatory_inclusions_present() -> None:
    """6. Document must include volume-matched A/B, listening verification, delivery policy, non-destructive output, bypass path, and mute protection."""
    assert FINISHING.is_file(), (
        f"Missing required specification document: {FINISHING}"
    )
    text = FINISHING.read_text(encoding="utf-8")
    problems = check_mandatory_inclusions(text)
    assert not problems, (
        f"Mandatory inclusion violations:\n" + "\n".join(problems)
    )
