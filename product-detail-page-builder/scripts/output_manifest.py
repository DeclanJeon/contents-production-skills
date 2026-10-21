"""Typed metadata for observed page-builder output files."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict

from page_spec import Platform
from platform_profiles import OutputMode


class ProfileReadiness(str, Enum):
    VERIFIED = "verified"
    SELLER_CONFIRMATION_REQUIRED = "seller_confirmation_required"


class UploadReadiness(str, Enum):
    BLOCKED = "blocked"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


class ReviewReadiness(str, Enum):
    NOT_RECORDED = "not_recorded"
    REQUIRED = "required"


class ModuleArtifact(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    id: str
    file: str
    width_px: int
    height_px: int
    file_bytes: int


class OutputReadiness(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    plan_review: ReviewReadiness
    platform_profile: ProfileReadiness
    asset_visual_review: ReviewReadiness
    upload_readiness: UploadReadiness


class OutputManifest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    schema_version: str
    platform: Platform
    output_mode: OutputMode
    module_count: int
    modules: tuple[ModuleArtifact, ...]
    preview_file: str
    slice_files: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    readiness: OutputReadiness
