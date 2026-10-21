"""Seller-platform export profiles and their evidence records."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from errors import PageSpecError
from page_facts import is_http_url
from page_spec import OutputFormat, Platform

PLATFORM_REGISTRY_PATH = (
    Path(__file__).resolve().parents[1] / "references" / "platform-profiles.json"
)


class OutputMode(str, Enum):
    LONG_PAGE_SLICES = "long_page_slices"
    MODULE_IMAGES = "module_images"


class PlatformSource(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    title: str
    url: str
    publisher: str

    @model_validator(mode="after")
    def source_url_is_http(self) -> Self:
        if not is_http_url(self.url):
            raise ValueError("platform source URL must use HTTP or HTTPS")
        return self


class PlatformProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    id: Platform
    display_name: str
    locale: str
    output_mode: OutputMode
    default_width_px: int | None
    slice_height_px: int | None
    format: OutputFormat
    quality: int = Field(ge=60, le=100)
    max_file_bytes: int | None
    total_height_warning_px: int | None
    initial_visible_height_px: int | None
    text_in_detail_images: str
    synthetic_visuals: str
    evidence_level: str
    requires_seller_confirmation: bool
    verified_at: str
    sources: tuple[PlatformSource, ...]
    warnings: tuple[str, ...]


class PlatformRegistry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    schema_version: str
    researched_at: str
    profiles: tuple[PlatformProfile, ...]

    def for_platform(self, platform: Platform) -> PlatformProfile:
        for profile in self.profiles:
            if profile.id is platform:
                return profile
        raise PageSpecError(
            PLATFORM_REGISTRY_PATH,
            f"no profile configured for {platform.value}",
        )

    @model_validator(mode="after")
    def profile_ids_are_unique(self) -> Self:
        profile_ids = [profile.id for profile in self.profiles]
        if len(profile_ids) != len(set(profile_ids)):
            raise ValueError("platform profile IDs must be unique")
        return self


def load_platform_registry(path: Path = PLATFORM_REGISTRY_PATH) -> PlatformRegistry:
    """Parse the platform registry at the JSON input boundary."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise PageSpecError(path, str(exc)) from exc
    try:
        return PlatformRegistry.model_validate_json(raw)
    except ValidationError as exc:
        raise PageSpecError(path, str(exc)) from exc
