"""Shared synthetic fixtures for page-builder regression tests."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rendering import FONT_CANDIDATES


@dataclass(frozen=True, slots=True)
class PageFixtureOptions:
    platform: str = "smartstore"
    max_file_bytes: int | None = 20_971_520
    module_count: int = 3
    background: str = "product.jpg"
    slice_height_px: int | None = None


DEFAULT_OPTIONS = PageFixtureOptions()


def font_path() -> str:
    """Return an installed Korean-capable font for deterministic raster fixtures."""
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            return str(path)
    raise AssertionError("test environment needs a CJK-capable system font")


def write_product_photo(path: Path) -> None:
    """Write a synthetic, non-commercial product fixture."""
    image = Image.new("RGB", (640, 480), "#d6d0c5")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((110, 80, 530, 410), radius=28, fill="#59636b")
    draw.rectangle((150, 120, 260, 360), fill="#68747c")
    draw.rectangle((270, 120, 380, 360), fill="#68747c")
    draw.rectangle((390, 120, 490, 360), fill="#68747c")
    image.save(path, format="JPEG", quality=92)


def make_page_spec(
    root: Path,
    options: PageFixtureOptions = DEFAULT_OPTIONS,
) -> Path:
    """Create a temporary evidence-linked page-spec fixture."""
    photo = root / "product.jpg"
    write_product_photo(photo)
    facts = [
        {
            "id": "product-kind",
            "value": "데스크 오거나이저",
            "source": "user",
            "evidence": {"kind": "user_statement", "locator": "intake.category"},
            "publish": True,
        },
        {
            "id": "compartment-count",
            "value": 3,
            "source": "user",
            "evidence": {
                "kind": "user_statement",
                "locator": "intake.product_facts.compartments",
            },
            "publish": True,
        },
        {
            "id": "body-color",
            "value": "짙은 회색",
            "source": "visible",
            "evidence": {
                "kind": "visible_image_region",
                "locator": "front photo body",
                "asset_id": "front-photo",
                "region": [0.15, 0.15, 0.7, 0.7],
            },
            "publish": True,
        },
        {
            "id": "rust-proof",
            "value": "방청 처리",
            "source": "unconfirmed",
            "evidence": {"kind": "unverified", "locator": "not supplied"},
            "publish": False,
        },
    ]
    modules = [
        {
            "id": "hero",
            "type": "hero",
            "title": "모아 3칸 데스크 오거나이저",
            "copy": "책상 도구를 세 칸으로 나눠 담아요",
            "fact_ids": ["product-kind", "compartment-count"],
            "background_image": options.background,
            "image_asset_id": "front-photo",
            "layout": "image-top",
            "height_px": 900,
        },
        {
            "id": "compartments",
            "type": "feature",
            "title": "세 칸 구성",
            "copy": "확인된 세 칸 구조를 한눈에 보여줍니다",
            "fact_ids": ["compartment-count"],
            "background_image": options.background,
            "image_asset_id": "front-photo",
            "layout": "image-left",
            "height_px": 900,
        },
        {
            "id": "color-detail",
            "type": "detail",
            "title": "짙은 회색",
            "copy": "사진에서 확인되는 색상입니다",
            "fact_ids": ["body-color"],
            "background_image": options.background,
            "image_asset_id": "front-photo",
            "layout": "specs",
            "height_px": 900,
        },
    ][:options.module_count]
    data = {
        "version": "1.0",
        "platform": options.platform,
        "locale": "ko-KR",
        "product_name": "모아 3칸 데스크 오거나이저",
        "category": "home",
        "product_images": [
            {"id": "front-photo", "path": photo.name, "view": "front"}
        ],
        "facts": facts,
        "style": {
            "background": "#F3F0EA",
            "surface": "#FFFFFF",
            "text": "#24282B",
            "accent": "#75848B",
            "font_path": font_path(),
            "font_size_px": 44,
            "content_margin_px": 48,
        },
        "output": {
            "width_px": 860,
            "slice_height_px": options.slice_height_px,
            "format": "jpg",
            "quality": 86,
            "max_file_bytes": options.max_file_bytes,
            "platform_confirmed": False,
        },
        "modules": modules,
    }
    path = root / "page-spec.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
