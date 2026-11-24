"""Navigation and fail-closed requirements for optional production recipes."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CREATIVE = ROOT / "creative-production" / "references"
ASSETS = ROOT / "video-production-assets" / "references"


@pytest.mark.parametrize(
    ("path", "heading", "required"),
    [
        pytest.param(
            CREATIVE / "narration-subtitle-handoff.md", "Local timing draft",
            ("SYSTRAN/faster-whisper", "m-bain/whisperX", "actual playback",
             "display text", "do not install", "provisional"),
            id="test_local_caption_timing",
        ),
        pytest.param(
            ASSETS / "09a-short-form-edit-recipes.md", "토킹헤드 실수 컷",
            ("EditAtlas/skills", "의도적인 쉼", "원본 시간", "편집본 시간", "재전사", "청취", "단어 타이밍이 없으면 원본을 재생"),
            id="test_talking_head_cleanup",
        ),
        pytest.param(
            ASSETS / "15-delivery.md", "편집 가능한 타임라인 인계",
            ("AcademySoftwareFoundation/OpenTimelineIO", "대상 편집기", "다시 열", "미디어 재연결",
             "오디오 오프셋", "unverified"),
            id="test_editable_timeline_delivery",
        ),
        pytest.param(
            ASSETS / "08-animation.md", "손그림 2D 제작 인계",
            ("opentoonz/opentoonz", "pencil2d/pencil", "노출표", "레이어", "알파", "재생"),
            id="test_hand_drawn_handoff",
        ),
        pytest.param(
            ASSETS / "31-external-video-decomposition.md", "컷 경계만 필요한 경우",
            ("Breakthrough/PySceneDetect", "DETECTOR_CANDIDATE", "수작업", "자동 설치하지 않는다",
             "경계 양쪽", "전체 분해"),
            id="test_cut_only_candidate",
        ),
    ],
)
def test_optional_craft_contract(path: Path, heading: str, required: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    if path.name == "31-external-video-decomposition.md":
        assert "전체 분해에서 rea-video CLI 미설치" in text
        assert "컷 경계 후보만 필요 | [컷 전용 경로]" in text
    marker = f"## {heading}\n"
    assert marker in text
    section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    for requirement in required:
        assert requirement.casefold() in section.casefold()
