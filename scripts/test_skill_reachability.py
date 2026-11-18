"""Every packaged skill must be reachable from the order-issuing skill.

`creative-production` routes one request to one owner. A skill that is neither a
route owner nor named by a declared pointer is capability the coordinator cannot
invoke, no matter how complete the skill itself is. Two were found that way: the
provider executor lane had no route, and the community-shorts pipeline was named
only in a citation.

A skill may be deliberate outside `routing.csv` -- a provider mode chosen after a
route, or a specialist reached from an owner table. Those go in SECONDARY_POINTERS
with the file and phrase that name them, so removing the pointer fails here
instead of silently orphaning the skill.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
ROUTING: Final = ROOT / "creative-production/references/routing.csv"
MANIFEST: Final = ROOT / "manifest.json"

# skill -> (package-relative pointer file, phrase that has to appear in the same block)
SECONDARY_POINTERS: Final[dict[str, tuple[str, str]]] = {
    "topic-demand-selection": (
        "silent-satire-animatic/SKILL.md", "topic-demand-selection"),
    "open-3d-production": (
        "creative-production/references/production-routing.md", "open-3d-production"),
    "higgsfield-soul-id": (
        "creative-production/references/production-routing-optional.md",
        "higgsfield-soul-id"),
    "higgsfield-video-explainer": (
        "creative-production/references/production-routing-optional.md",
        "higgsfield-video-explainer"),
    "higgsfield-video-replicate": (
        "creative-production/references/production-routing-optional.md",
        "higgsfield-video-replicate"),
    "higgsfield-youtube-thumbnail": (
        "creative-production/references/production-routing-optional.md",
        "higgsfield-youtube-thumbnail"),
}


def manifest_skills() -> list[str]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["skills"]


def route_owners() -> set[str]:
    with ROUTING.open(encoding="utf-8", newline="") as handle:
        return {row["owner"] for row in csv.DictReader(handle)}


def pointer_problems(skills: list[str]) -> list[str]:
    problems: list[str] = []
    for skill, (pointer, phrase) in SECONDARY_POINTERS.items():
        if skill not in skills:
            problems.append(f"{skill} is registered as a pointer target but not packaged")
            continue
        path = ROOT / pointer
        if not path.is_file():
            problems.append(f"{skill}: pointer file missing: {pointer}")
            continue
        blocks = [b for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")) if b.strip()]
        if not any(phrase in block for block in blocks):
            problems.append(f"{skill}: {pointer} no longer names it")
    return problems


def unreachable_skills(skills: list[str], owners: set[str]) -> list[str]:
    return [skill for skill in skills
            if skill not in owners and skill not in SECONDARY_POINTERS]


def reachability_problems(skills: list[str], owners: set[str]) -> list[str]:
    problems = [f"{skill} has no route and no declared pointer"
                for skill in unreachable_skills(skills, owners)]
    problems += pointer_problems(skills)
    return problems


def test_every_packaged_skill_is_reachable() -> None:
    assert reachability_problems(manifest_skills(), route_owners()) == []


def test_the_gap_this_test_was_written_for_is_closed() -> None:
    """The executor lane and the community-shorts pipeline each had no entry."""
    owners = route_owners()
    assert "higgsfield-generate" in owners
    assert "community-shorts-stills-pipeline" in owners


def test_new_skills_must_declare_a_route_or_a_pointer() -> None:
    skills = manifest_skills()
    owners = route_owners()
    problems = reachability_problems(skills + ["invented-skill"], owners)
    assert any("invented-skill" in problem for problem in problems)


def test_dropped_pointer_is_detected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    skill, (pointer, phrase) = next(iter(SECONDARY_POINTERS.items()))
    mutated: dict[str, tuple[str, str]] = dict(SECONDARY_POINTERS)
    mutated[skill] = (pointer, "문구가 사라진 포인터")
    monkeypatch.setattr(__name__ + ".SECONDARY_POINTERS", mutated)

    problems = pointer_problems(manifest_skills())

    assert any(skill in problem for problem in problems), problems


def test_removed_route_is_detected() -> None:
    owners = route_owners() - {"community-shorts-stills-pipeline"}

    problems = reachability_problems(manifest_skills(), owners)

    assert any("community-shorts-stills-pipeline" in problem for problem in problems)
