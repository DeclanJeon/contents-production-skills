"""Evidence-linked product images and fact models."""

from __future__ import annotations

from datetime import date
from enum import Enum
from math import isfinite
from urllib.parse import urlsplit
from typing import Self, assert_never

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FactSource(str, Enum):
    USER = "user"
    VISIBLE = "visible"
    OFFICIAL_SOURCE = "official_source"
    UNCONFIRMED = "unconfirmed"


class EvidenceKind(str, Enum):
    USER_STATEMENT = "user_statement"
    VISIBLE_IMAGE_REGION = "visible_image_region"
    OFFICIAL_SOURCE = "official_source"
    UNVERIFIED = "unverified"


class ImageView(str, Enum):
    FRONT = "front"
    BACK = "back"
    SIDE = "side"
    TOP = "top"
    BOTTOM = "bottom"
    DETAIL = "detail"
    PACKAGING = "packaging"
    SCALE = "scale"
    UNKNOWN = "unknown"


def is_http_url(value: str) -> bool:
    """Accept only absolute HTTP(S) URLs with a host."""
    parsed = urlsplit(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


class Evidence(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    kind: EvidenceKind
    locator: str = Field(min_length=1)
    asset_id: str | None = None
    region: tuple[float, float, float, float] | None = None
    url: str | None = None
    checked_at: str | None = None

    @model_validator(mode="after")
    def evidence_has_required_locator(self) -> Self:
        match self.kind:
            case EvidenceKind.VISIBLE_IMAGE_REGION:
                if self.asset_id is None or self.region is None:
                    raise ValueError("visible evidence requires an image ID and region")
                x, y, width, height = self.region
                if (
                    x < 0
                    or y < 0
                    or width <= 0
                    or height <= 0
                    or x + width > 1
                    or y + height > 1
                ):
                    raise ValueError("visible evidence region must be a positive normalized box")
            case EvidenceKind.OFFICIAL_SOURCE:
                if self.url is None or self.checked_at is None:
                    raise ValueError("official-source evidence requires URL and check date")
                if not is_http_url(self.url):
                    raise ValueError("official-source evidence URL must use HTTP or HTTPS")
                try:
                    date.fromisoformat(self.checked_at)
                except ValueError as exc:
                    raise ValueError("official-source checked_at must be an ISO date") from exc
            case EvidenceKind.USER_STATEMENT | EvidenceKind.UNVERIFIED:
                pass
            case unreachable:
                assert_never(unreachable)
        return self


class ProductImage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    path: str = Field(min_length=1)
    view: ImageView
    notes: str = ""


class Fact(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    value: str | int | float | bool
    source: FactSource
    evidence: Evidence
    publish: bool
    unit: str | None = None

    @model_validator(mode="after")
    def evidence_matches_source(self) -> Self:
        expected_kind = {
            FactSource.USER: EvidenceKind.USER_STATEMENT,
            FactSource.VISIBLE: EvidenceKind.VISIBLE_IMAGE_REGION,
            FactSource.OFFICIAL_SOURCE: EvidenceKind.OFFICIAL_SOURCE,
            FactSource.UNCONFIRMED: EvidenceKind.UNVERIFIED,
        }[self.source]
        if self.evidence.kind is not expected_kind:
            raise ValueError(f"{self.source.value} facts require {expected_kind.value} evidence")
        match self.source:
            case FactSource.UNCONFIRMED:
                if self.publish:
                    raise ValueError("unconfirmed facts cannot be publishable")
            case FactSource.USER | FactSource.VISIBLE | FactSource.OFFICIAL_SOURCE:
                pass
            case unreachable:
                assert_never(unreachable)
        match self.value:
            case float() as numeric_value:
                if not isfinite(numeric_value):
                    raise ValueError("fact numeric values must be finite")
            case str() | int() | bool():
                pass
            case unreachable:
                assert_never(unreachable)
        return self
