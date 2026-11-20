"""Checks for the creative-production entry description and frontier growth."""
from __future__ import annotations

import re
from pathlib import Path

import routing_regression

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "creative-production" / "SKILL.md"
MAIN_FRONTIER_WORDS = 2820
FRONTIER_GROWTH_CAP = 60

EXCLUSIONS = (
    "standalone writing",
    "social posts",
    "standalone images",
    "ordinary design",
    "application development",
    "audio-only",
)
PARTIAL_VIDEO_CONCEPTS = {
    "shorts/reels editing": r"shorts.*reels|reels.*shorts",
    "re-edit or clip extraction": r"re-edit\w*.*clip|extract\w* clips",
    "captions/lower thirds": r"captions.*lower thirds",
    "ad/promo video script": r"(ad|promo)\w*.*video scripts?",
    "motion-graphics style": r"motion-graphics style",
}


def description() -> str:
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(r"^description:(.*?)^---\s*$", text, re.DOTALL | re.MULTILINE)
    assert match, "frontmatter description not found"
    return " ".join(match.group(1).split()).lower()


def test_description_keeps_exclusions() -> None:
    text = description()
    missing = [phrase for phrase in EXCLUSIONS if phrase not in text]
    assert not missing, missing


def test_description_covers_partial_video_work() -> None:
    text = description()
    missing = [name for name, pattern in PARTIAL_VIDEO_CONCEPTS.items() if not re.search(pattern, text)]
    assert not missing, missing


def test_version_is_2_6() -> None:
    assert re.search(r"^version: 2\.6$", SKILL.read_text(encoding="utf-8"), re.MULTILINE)


def test_frontier_growth_bounded() -> None:
    words = routing_regression.measure(routing_regression.FRONTIER)["words"]
    assert words - MAIN_FRONTIER_WORDS <= FRONTIER_GROWTH_CAP, words
