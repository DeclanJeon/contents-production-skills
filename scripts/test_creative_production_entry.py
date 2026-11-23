"""Checks for the creative-production entry description and frontier growth."""
from __future__ import annotations

import re
from pathlib import Path

import routing_regression

try:
    import yaml
except ImportError:  # strict fallback check is used in the frontmatter test
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "creative-production" / "SKILL.md"
MAIN_FRONTIER_WORDS = 2820
FRONTIER_GROWTH_CAP = 120

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
    "ad/promo video script": r"\b(ad|promo) (or (ad|promo) )?video scripts?\b",
    "motion-graphics style": r"motion-graphics style",
}


def description() -> str:
    text = SKILL.read_text(encoding="utf-8")
    match = re.search(r"^description:(.*?)^---\s*$", text, re.DOTALL | re.MULTILINE)
    assert match, "frontmatter description not found"
    return " ".join(match.group(1).split()).lower()


def exclusion_sentence() -> str:
    match = re.search(r"do not use[^.]*\.", description())
    assert match, "'Do not use' sentence not found"
    return match.group(0)


def test_description_keeps_exclusions() -> None:
    sentence = exclusion_sentence()
    missing = [phrase for phrase in EXCLUSIONS if phrase not in sentence]
    assert not missing, missing


def test_description_excludes_video_to_text_repurposing() -> None:
    assert "turning a video into an article or post" in exclusion_sentence()


def package_skill_files() -> list[Path]:
    return sorted(ROOT.glob("*/SKILL.md"))


def frontmatter_block(path: Path) -> str:
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    assert match, f"{path}: frontmatter not found"
    return match.group(1)


def test_every_package_frontmatter_is_valid_yaml() -> None:
    files = package_skill_files()
    assert files
    for path in files:
        block = frontmatter_block(path)
        if yaml is not None:
            data = yaml.safe_load(block)
            assert isinstance(data, dict), path
            assert isinstance(data.get("description"), str), path
            continue
        value_lines = []
        in_description = False
        for line in block.splitlines():
            if line.startswith("description:"):
                in_description = True
                value_lines.append(line.split(":", 1)[1])
            elif in_description and line.startswith((" ", "\t")):
                value_lines.append(line)
            else:
                in_description = False
        value = " ".join(value_lines).strip()
        if not value.startswith(("'", '"', ">", "|")):
            assert ": " not in value, f"{path}: colon-space in plain scalar"


def test_description_covers_partial_video_work() -> None:
    text = description().split("Do not use", 1)[0]
    missing = [name for name, pattern in PARTIAL_VIDEO_CONCEPTS.items() if not re.search(pattern, text)]
    assert not missing, missing


def test_version_is_2_8() -> None:
    assert re.search(r"^version: 2\.8$", SKILL.read_text(encoding="utf-8"), re.MULTILINE)


def test_frontier_growth_bounded() -> None:
    words = routing_regression.measure(routing_regression.FRONTIER)["words"]
    assert words - MAIN_FRONTIER_WORDS <= FRONTIER_GROWTH_CAP, words
