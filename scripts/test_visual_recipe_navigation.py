"""Exercise public owner-to-recipe links through a real isolated installation.

Removing an owner route or its destination fragment breaks this contract.
These tests validate navigation, not creative wording or artistic quality.
"""

from pathlib import Path
import re
from typing import Final

import pytest

import install_package

ROOT: Final = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("owner", "reference", "fragment"),
    [
        ("04-performance.md", "performance-and-style-recipes.md", "status-negotiation"),
        ("04-performance.md", "performance-and-style-recipes.md", "action-and-agency"),
        ("06-shots.md", "performance-and-style-recipes.md", "competing-threats"),
        ("03-screenplay.md", "world-rules-and-information-recipes.md", "illustrative-inserts"),
        ("09-edit.md", "world-rules-and-information-recipes.md", "elapsed-time-and-progress"),
    ],
)
def test_recipe_is_reachable_from_installed_stage_owner(
    tmp_path: Path, owner: str, reference: str, fragment: str,
) -> None:
    # Given: the real package, copied to an otherwise empty skill root.
    target = tmp_path / "skills"
    install_package.install(target, repo_root=ROOT, exclude_derived_support=True)
    owner_path = target / "video-production-assets" / "references" / owner

    # When: following the documented owner-to-recipe route.
    links = re.findall(r"\]\(([^)]+)\)", owner_path.read_text(encoding="utf-8"))
    route = f"{reference}#{fragment}"

    # Then: the local destination exists and its public fragment resolves.
    assert route in links, f"installed owner has no recipe route: {owner} -> {route}"
    destination = (owner_path.parent / reference).resolve()
    assert destination.is_relative_to(target.resolve()) and destination.is_file()
    anchors = re.findall(
        r'<a\s+id="([^"]+)"\s*>', destination.read_text(encoding="utf-8"),
    )
    assert fragment in anchors, f"installed recipe fragment is missing: {route}"
