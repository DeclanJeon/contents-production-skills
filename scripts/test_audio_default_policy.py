"""Voice/sound default policy: one canonical rule, pointer-only dependents.

The package states the in-request voice-and-sound default once, in
``creative-production/references/video-generation-planning.md`` section 3b,
and dependent surfaces point at it instead of restating it. These checks
lock that shape: the canonical rule keeps the three overrides and the mute
protection, no provider is named in the rule, and every pointer resolves to
the canonical anchor in the installed tree.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import install_package

ROOT: Final = Path(__file__).resolve().parents[1]
CANONICAL: Final = (
    ROOT / "creative-production/references/video-generation-planning.md"
)
ANCHOR: Final = "3b-voice-and-sound-design-are-in-request-by-default"
POINTER_FILES: Final = (
    "video-production-assets/references/11-ai-handoff.md",
    "video-production-assets/references/22-dialogue-lipsync.md",
    "video-production-assets/references/09-edit.md",
    "video-production-assets/references/edit-sound-language-catalog.md",
    "video-production-assets/references/storyboard-contract.md",
    "video-production-assets/references/24-production-execution.md",
    "video-production-assets/references/21-generated-video-qa-retry.md",
    "video-production-assets/assets/11-ai-handoff-template.md",
    "video-production-assets/assets/performance-cue-template.md",
    "ai-camera-control/references/control-contract.md",
    "ai-camera-control/assets/camera-control-template.md",
    "creative-production/SKILL.md",
    "creative-production/references/production-routing-optional.md",
    "creative-production/references/storyboard-timing-to-prompt.md",
)
PROVIDER_NAMES: Final = (
    "elevenlabs", "fish audio", "fish_audio", "typecast", "higgsfield",
    "openai", "gemini", "veo", "seedance", "kling", "runway",
)


def _canonical_section() -> str:
    """Return the section 3b body up to the next same-or-higher heading."""
    text = CANONICAL.read_text(encoding="utf-8")
    match = re.search(r"^### 3b\..*$", text, flags=re.M)
    assert match, "video-generation-planning.md lost its §3b heading"
    rest = text[match.end():]
    stop = re.search(r"^###? ", rest, flags=re.M)
    return rest if stop is None else rest[: stop.start()]


def test_canonical_rule_declares_default_and_keeps_overrides() -> None:
    body = _canonical_section()
    # Default: voice design and sound design belong in the same request.
    assert "same video request" in body
    assert "voice design" in body and "sound design" in body
    assert re.search(r"no reference voice/sound", body)
    assert re.search(r"named no external", body)
    assert re.search(r"no audio asset is attached", body)
    # Enumerated elements the default must cover.
    for element in ("dialogue", "SFX", "ambience", "VFX sound"):
        assert element in body, f"§3b no longer enumerates {element!r}"
    # Overrides survive and are never silently replaced.
    assert "not silently replaced" in body
    assert "reference voice" in body
    assert re.search(r"explicitly named external", body)
    assert "attached audio file" in body
    # Mute protection and honest unsupported handling.
    assert "no_audio" in body and "stays mute" in body
    assert "UNSUPPORTED" in body and "UNVERIFIED" in body


def test_canonical_rule_names_no_provider() -> None:
    body = _canonical_section().lower()
    leaked = [name for name in PROVIDER_NAMES if name in body]
    assert not leaked, f"§3b names provider(s): {leaked}"


def test_dependents_point_at_the_canonical_rule() -> None:
    missing = [rel for rel in POINTER_FILES if ANCHOR not in (ROOT / rel).read_text(encoding="utf-8")]
    assert not missing, f"pointer(s) lost the §3b anchor: {missing}"


def test_installed_pointers_resolve_inside_the_pack(tmp_path: Path) -> None:
    target = tmp_path / "installed"
    result = install_package.install(target, repo_root=ROOT, exclude_derived_support=True)
    broken: list[tuple[str, str]] = []
    for skill in result.installed:
        for path in skill.rglob("*.md"):
            if "support" in path.relative_to(skill).parts:
                continue
            body = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for ref in re.findall(r"\]\(([^)]+)\)", body):
                if ANCHOR not in ref:
                    continue
                rel = ref.split("#")[0]
                dest = (path.parent / rel).resolve()
                if not dest.is_relative_to(target.resolve()) or not dest.is_file():
                    broken.append((str(path), ref))
    assert not broken, f"installed §3b pointer(s) do not resolve: {broken}"
