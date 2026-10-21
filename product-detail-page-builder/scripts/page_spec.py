"""Typed page specification and platform-profile contracts."""

from __future__ import annotations

from datetime import date
from enum import Enum
from pathlib import Path
from typing import Self, assert_never

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from errors import PageSpecError
from page_facts import (
    Evidence,
    EvidenceKind,
    Fact,
    FactSource,
    ImageView,
    ProductImage,
    is_http_url,
)


class Platform(str, Enum):
    SMARTSTORE = "smartstore"
    COUPANG = "coupang"
    CUSTOM = "custom"


class ModuleLayout(str, Enum):
    TEXT_ONLY = "text-only"
    IMAGE_TOP = "image-top"
    IMAGE_FULL = "image-full"
    IMAGE_LEFT = "image-left"
    IMAGE_RIGHT = "image-right"
    PHOTO_ONLY = "photo-only"
    SPECS = "specs"


class ImageFit(str, Enum):
    CONTAIN = "contain"
    COVER = "cover"


class OutputFormat(str, Enum):
    JPG = "jpg"
    PNG = "png"


class ModuleType(str, Enum):
    HERO = "hero"
    BENEFIT = "benefit"
    FEATURE = "feature"
    DETAIL = "detail"
    SCENE = "scene"
    USE = "use"
    SPECS = "specs"
    PACKAGE = "package"
    CARE = "care"
    CLOSING = "closing"


class Style(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    background: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    surface: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    text: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    accent: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")
    font_path: str | None
    font_size_px: int = Field(default=44, ge=16, le=160)
    content_margin_px: int = Field(default=48, ge=16, le=300)


class OutputSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    width_px: int = Field(ge=480, le=5000)
    slice_height_px: int | None = Field(default=None, ge=400, le=10000)
    format: OutputFormat
    quality: int = Field(ge=60, le=100)
    max_file_bytes: int | None = Field(ge=1)
    platform_confirmed: bool = False
    platform_confirmation_source: str | None = None
    platform_confirmation_checked_at: str | None = None

    @model_validator(mode="after")
    def confirmed_profile_has_evidence(self) -> Self:
        if self.platform_confirmed and (
            self.platform_confirmation_source is None
            or self.platform_confirmation_checked_at is None
        ):
            raise ValueError("confirmed platform profiles require source and check date")
        if self.platform_confirmation_source is not None and not is_http_url(
            self.platform_confirmation_source
        ):
            raise ValueError("platform confirmation source must use HTTP or HTTPS")
        if self.platform_confirmation_checked_at is not None:
            try:
                date.fromisoformat(self.platform_confirmation_checked_at)
            except ValueError as exc:
                raise ValueError("platform confirmation check date must be ISO format") from exc
        return self


class PageModule(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        populate_by_name=True,
    )

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    type: ModuleType
    title: str = Field(max_length=120)
    copy_text: str = Field(alias="copy", max_length=500)
    fact_ids: tuple[str, ...]
    background_image: str | None
    layout: ModuleLayout
    height_px: int = Field(ge=400, le=2500)
    image_fit: ImageFit = ImageFit.CONTAIN
    image_asset_id: str | None = None
    preview_only: bool = False


class PageSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    version: str = Field(pattern=r"^1\.0$")
    platform: Platform
    locale: str = Field(min_length=2)
    product_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    product_images: tuple[ProductImage, ...] = Field(min_length=1)
    facts: tuple[Fact, ...]
    style: Style
    output: OutputSpec
    warnings: tuple[str, ...] = ()
    modules: tuple[PageModule, ...] = Field(min_length=1, max_length=12)

    @model_validator(mode="after")
    def references_are_publishable(self) -> Self:
        match self.platform:
            case Platform.SMARTSTORE | Platform.COUPANG:
                if self.locale != "ko-KR":
                    raise ValueError(f"{self.platform.value} output locale must be ko-KR")
            case Platform.CUSTOM:
                pass
            case unreachable:
                assert_never(unreachable)
        image_ids = [image.id for image in self.product_images]
        fact_ids = [fact.id for fact in self.facts]
        if len(image_ids) != len(set(image_ids)):
            raise ValueError("product image IDs must be unique")
        if len(fact_ids) != len(set(fact_ids)):
            raise ValueError("fact IDs must be unique")

        facts_by_id = {fact.id: fact for fact in self.facts}
        module_ids = [module.id for module in self.modules]
        if len(module_ids) != len(set(module_ids)):
            raise ValueError("module IDs must be unique")
        for module in self.modules:
            if (module.title or module.copy_text) and not module.fact_ids:
                raise ValueError(f"text module {module.id} must cite fact IDs")
            match module.layout:
                case ModuleLayout.PHOTO_ONLY:
                    if module.background_image is None or not module.background_image:
                        raise ValueError(
                            f"photo-only module {module.id} requires a background image"
                        )
                    if module.title or module.copy_text or module.fact_ids:
                        raise ValueError(
                            f"photo-only module {module.id} cannot contain text or claims"
                        )
                case ModuleLayout.TEXT_ONLY:
                    if module.background_image is not None or module.image_asset_id is not None:
                        raise ValueError(
                            f"text-only module {module.id} cannot reference a background image"
                        )
                    if not module.title and not module.copy_text:
                        raise ValueError(f"text-only module {module.id} must contain copy")
                case (
                    ModuleLayout.IMAGE_TOP
                    | ModuleLayout.IMAGE_FULL
                    | ModuleLayout.IMAGE_LEFT
                    | ModuleLayout.IMAGE_RIGHT
                    | ModuleLayout.SPECS
                ):
                    if module.background_image is None or not module.background_image:
                        raise ValueError(
                            f"image module {module.id} requires a background image"
                        )
                case unreachable:
                    assert_never(unreachable)
            for fact_id in module.fact_ids:
                fact = facts_by_id.get(fact_id)
                if fact is None:
                    raise ValueError(f"module {module.id} references missing fact {fact_id}")
                if not fact.publish:
                    raise ValueError(f"module {module.id} references unpublished fact {fact_id}")
                match fact.source:
                    case FactSource.UNCONFIRMED:
                        raise ValueError(
                            f"module {module.id} references unconfirmed fact {fact_id}"
                        )
                    case FactSource.USER | FactSource.VISIBLE | FactSource.OFFICIAL_SOURCE:
                        pass
                    case unreachable:
                        assert_never(unreachable)
            if module.image_asset_id is not None and module.image_asset_id not in image_ids:
                raise ValueError(
                    f"module {module.id} references missing product image {module.image_asset_id}"
                )
        for fact in self.facts:
            match fact.source:
                case FactSource.VISIBLE:
                    if fact.evidence.asset_id not in image_ids:
                        raise ValueError(f"visible fact {fact.id} references a missing image")
                    if fact.evidence.region is None:
                        raise ValueError(f"visible fact {fact.id} requires an image region")
                case FactSource.USER | FactSource.OFFICIAL_SOURCE | FactSource.UNCONFIRMED:
                    pass
                case unreachable:
                    assert_never(unreachable)
        return self


class PageBrief(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    product_name: str
    platform: Platform
    locale: str
    category: str
    product_images: tuple[ProductImage, ...]
    facts: tuple[Fact, ...]


def render_copy_markdown(spec: PageSpec) -> str:
    """Serialize the exact approved module copy for human review."""
    sections = [
        f"## {module.title}\n\n{module.copy_text}".rstrip()
        for module in spec.modules
        if module.title or module.copy_text
    ]
    return "\n\n".join(sections) + "\n"


def load_page_spec(path: Path) -> PageSpec:
    """Parse a page specification at the JSON input boundary."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise PageSpecError(path, str(exc)) from exc
    try:
        return PageSpec.model_validate_json(raw)
    except ValidationError as exc:
        raise PageSpecError(path, str(exc)) from exc
