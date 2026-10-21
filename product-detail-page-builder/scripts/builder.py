"""Page-spec-driven compositor orchestration."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import assert_never

from PIL import Image

from errors import PageSpecError, RenderError
from output_manifest import (
    ModuleArtifact,
    OutputManifest,
    OutputReadiness,
    ProfileReadiness,
    ReviewReadiness,
    UploadReadiness,
)
from page_spec import (
    PageBrief,
    PageSpec,
    load_page_spec,
    render_copy_markdown,
)
from platform_profiles import (
    PLATFORM_REGISTRY_PATH,
    OutputMode,
    PlatformRegistry,
    load_platform_registry,
)
from rendering import (
    MAX_PREVIEW_PIXELS,
    RenderContext,
    find_font,
    render_module,
    render_preview,
)

@dataclass(frozen=True, slots=True)
class ComposeRequest:
    spec_path: Path
    output_dir: Path


@dataclass(frozen=True, slots=True)
class OutputPathError(Exception):
    path: Path

    def __str__(self) -> str:
        return f"refusing to overwrite existing output directory: {self.path}"


@dataclass(frozen=True, slots=True)
class ManifestInput:
    spec: PageSpec
    registry: PlatformRegistry
    module_paths: tuple[Path, ...]
    output_dir: Path
    warnings: tuple[str, ...]


def _preflight_inputs(spec: PageSpec, spec_path: Path) -> None:
    """Open every source image and bound preview allocation before output writes."""
    if sum(module.height_px for module in spec.modules) * spec.output.width_px > MAX_PREVIEW_PIXELS:
        raise RenderError(
            f"preview would exceed {MAX_PREVIEW_PIXELS} pixels; reduce module heights"
        )
    for module in spec.modules:
        background_image = module.background_image
        if background_image is None:
            continue
        raw_path = Path(background_image).expanduser()
        image_path = raw_path if raw_path.is_absolute() else spec_path.parent / raw_path
        if not image_path.is_file():
            raise RenderError(f"module {module.id} background image is missing: {image_path}")
        try:
            with Image.open(image_path) as image:
                image.verify()
        except OSError as exc:
            raise RenderError(f"module {module.id} background image is unreadable", image_path) from exc


def _write_text_outputs(spec: PageSpec, spec_path: Path, output_dir: Path) -> None:
    """Write the exact input spec, a fact brief, and its approved copy draft."""
    shutil.copyfile(spec_path, output_dir / "page-spec.json")
    brief = PageBrief(
        product_name=spec.product_name,
        platform=spec.platform,
        locale=spec.locale,
        category=spec.category,
        product_images=spec.product_images,
        facts=spec.facts,
    )
    (output_dir / "brief.json").write_text(
        json.dumps(brief.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "copy.md").write_text(render_copy_markdown(spec), encoding="utf-8")


def _profile_warnings(spec: PageSpec, registry: PlatformRegistry) -> tuple[str, ...]:
    """Combine profile cautions with the seller confirmation state."""
    profile = registry.for_platform(spec.platform)
    warnings = list(spec.warnings)
    warnings.extend(profile.warnings)
    if spec.category.casefold() in {"food", "food-and-beverage", "식품", "식음료"}:
        warnings.append(
            "확인된 식품 표시사항(식품유형, 원재료/함량, 알레르기, 영양, 원산지, "
            "보관 및 소비기한)이 없으면 해당 내용을 추정하지 말고 판매 전 확인"
        )
    if profile.requires_seller_confirmation and not spec.output.platform_confirmed:
        warnings.append("seller-center profile confirmation is required before upload")
    if profile.total_height_warning_px is not None:
        total_height = sum(module.height_px for module in spec.modules)
        if total_height > profile.total_height_warning_px:
            warnings.append(
                f"total detail height {total_height}px exceeds the "
                f"{profile.total_height_warning_px}px profile warning threshold"
            )
    for module in spec.modules:
        if module.preview_only:
            warnings.append(f"module {module.id} is concept-only and not upload-configured")
    return tuple(dict.fromkeys(warnings))


def _manifest(state: ManifestInput) -> OutputManifest:
    """Build observed file metadata without asserting human review."""
    spec = state.spec
    profile = state.registry.for_platform(spec.platform)
    artifacts = tuple(
        ModuleArtifact(
            id=module.id,
            file=path.relative_to(state.output_dir).as_posix(),
            width_px=spec.output.width_px,
            height_px=module.height_px,
            file_bytes=path.stat().st_size,
        )
        for module, path in zip(spec.modules, state.module_paths, strict=True)
    )
    profile_state = (
        ProfileReadiness.VERIFIED
        if spec.output.platform_confirmed
        else ProfileReadiness.SELLER_CONFIRMATION_REQUIRED
    )
    has_concept_only_module = any(module.preview_only for module in spec.modules)
    upload_state = (
        UploadReadiness.BLOCKED
        if has_concept_only_module
        or (profile.requires_seller_confirmation and not spec.output.platform_confirmed)
        else UploadReadiness.HUMAN_REVIEW_REQUIRED
    )
    readiness = OutputReadiness(
        plan_review=ReviewReadiness.NOT_RECORDED,
        platform_profile=profile_state,
        asset_visual_review=ReviewReadiness.REQUIRED,
        upload_readiness=upload_state,
    )
    return OutputManifest(
        schema_version="1.0",
        platform=spec.platform,
        output_mode=profile.output_mode,
        module_count=len(artifacts),
        modules=artifacts,
        preview_file="detail-page-preview.jpg",
        readiness=readiness,
        warnings=state.warnings,
    )


def compose_page(request: ComposeRequest) -> OutputManifest:
    """Compose modules and the long preview without overwriting existing files."""
    spec_path = request.spec_path.expanduser().resolve()
    output_dir = request.output_dir.expanduser().resolve()
    if output_dir.exists():
        raise OutputPathError(output_dir)
    spec = load_page_spec(spec_path)
    registry = load_platform_registry(PLATFORM_REGISTRY_PATH)
    profile = registry.for_platform(spec.platform)
    match profile.output_mode:
        case OutputMode.MODULE_IMAGES:
            pass
        case OutputMode.LONG_PAGE_SLICES:
            if spec.output.slice_height_px is None:
                raise PageSpecError(
                    spec_path,
                    "output.slice_height_px is required by the long-page slice profile",
                )
        case unreachable:
            assert_never(unreachable)
    _preflight_inputs(spec, spec_path)
    font_path = find_font(spec)

    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "modules").mkdir()
    context = RenderContext(spec, spec_path, output_dir / "modules", font_path)
    module_paths = tuple(render_module(module, context) for module in spec.modules)
    render_preview(
        module_paths,
        output_dir / "detail-page-preview.jpg",
        spec.output.width_px,
    )
    _write_text_outputs(spec, spec_path, output_dir)
    warnings = _profile_warnings(spec, registry)
    manifest = _manifest(ManifestInput(spec, registry, module_paths, output_dir, warnings))
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest
