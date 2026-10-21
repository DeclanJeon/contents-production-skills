"""Filesystem and raster checks for composed page bundles."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from output_manifest import OutputManifest
from page_spec import PageSpec
from platform_profiles import PlatformProfile


@dataclass(frozen=True, slots=True)
class ValidationBundle:
    spec: PageSpec
    manifest: OutputManifest
    output_dir: Path
    profile: PlatformProfile


@dataclass(frozen=True, slots=True)
class ModuleFileResult:
    total_height: int
    errors: tuple[str, ...]


def _safe_output_path(root: Path, relative: str) -> Path | None:
    """Resolve a manifest path only when it stays inside the output directory."""
    requested = Path(relative)
    if requested.is_absolute():
        return None
    resolved = (root / requested).resolve()
    if resolved == root or root not in resolved.parents:
        return None
    return resolved


def image_size(path: Path) -> tuple[int, int] | None:
    """Read image dimensions or return None for an unreadable image."""
    try:
        with Image.open(path) as image:
            image.load()
            return image.size
    except OSError:
        return None


def check_source_images(spec: PageSpec, spec_path: Path) -> tuple[str, ...]:
    """Require every declared original product image to decode."""
    errors: list[str] = []
    for image in spec.product_images:
        raw = Path(image.path).expanduser()
        path = raw if raw.is_absolute() else spec_path.parent / raw
        if image_size(path) is None:
            errors.append(f"product image {image.id} is missing or unreadable: {path}")
    return tuple(errors)


def check_module_files(bundle: ValidationBundle) -> ModuleFileResult:
    """Check module identity, path safety, dimensions, and configured byte limits."""
    errors: list[str] = []
    spec = bundle.spec
    manifest = bundle.manifest
    if manifest.module_count != len(spec.modules):
        errors.append("manifest module count does not match page-spec")
    if len(manifest.modules) != len(spec.modules):
        errors.append("manifest module records do not match page-spec")

    total_height = 0
    for expected, record in zip(spec.modules, manifest.modules, strict=False):
        if expected.id != record.id:
            errors.append(f"manifest order mismatch for module {expected.id}")
        path = _safe_output_path(bundle.output_dir, record.file)
        if path is None:
            errors.append(f"unsafe module file path: {record.file}")
            continue
        size = image_size(path)
        if size is None:
            errors.append(f"module image is missing or unreadable: {path}")
            continue
        width, height = size
        if width != spec.output.width_px or height != expected.height_px:
            errors.append(
                f"{path.name} has dimensions {width}x{height}; expected "
                f"{spec.output.width_px}x{expected.height_px}"
            )
        if (width, height) != (record.width_px, record.height_px):
            errors.append(f"manifest dimensions do not match {path.name}")
        if record.file_bytes != path.stat().st_size:
            errors.append(f"manifest byte count does not match {path.name}")
        configured_limit = spec.output.max_file_bytes
        profile_limit = bundle.profile.max_file_bytes
        effective_limit = (
            min(configured_limit, profile_limit)
            if configured_limit is not None and profile_limit is not None
            else configured_limit or profile_limit
        )
        if effective_limit is not None and path.stat().st_size > effective_limit:
            errors.append(f"{path.name} exceeds the configured file-size limit")
        total_height += expected.height_px
    return ModuleFileResult(total_height, tuple(errors))


def check_preview(bundle: ValidationBundle, expected_height: int) -> tuple[str, ...]:
    """Check that the joined review preview matches the module stack."""
    errors: list[str] = []
    relative = bundle.manifest.preview_file
    preview = _safe_output_path(bundle.output_dir, relative)
    if preview is None:
        return (f"unsafe preview path: {relative}",)
    size = image_size(preview)
    expected = (bundle.spec.output.width_px, expected_height)
    if size != expected:
        errors.append(f"long preview dimensions are {size}; expected {expected}")
    return tuple(errors)


def check_slices(bundle: ValidationBundle, preview_height: int) -> tuple[str, ...]:
    """Check slice count, dimensions, total height, and byte limits."""
    errors: list[str] = []
    spec = bundle.spec
    files = bundle.manifest.slice_files
    slice_height = spec.output.slice_height_px
    if slice_height is None:
        return ("page-spec.output.slice_height_px is required for long-page slice validation",)
    expected_count = math.ceil(preview_height / slice_height)
    if len(files) != expected_count:
        errors.append(f"manifest has {len(files)} slices; expected {expected_count}")
    total_height = 0
    effective_limit = (
        min(spec.output.max_file_bytes, bundle.profile.max_file_bytes)
        if spec.output.max_file_bytes is not None and bundle.profile.max_file_bytes is not None
        else spec.output.max_file_bytes or bundle.profile.max_file_bytes
    )
    for relative in files:
        path = _safe_output_path(bundle.output_dir, relative)
        if path is None:
            errors.append(f"unsafe slice path: {relative}")
            continue
        size = image_size(path)
        if size is None:
            errors.append(f"slice is missing or unreadable: {relative}")
            continue
        width, height = size
        if width != spec.output.width_px or height > slice_height:
            errors.append(f"slice dimensions are invalid: {relative} has {size}")
        if effective_limit is not None and path.stat().st_size > effective_limit:
            errors.append(f"slice exceeds the configured file-size limit: {relative}")
        total_height += height
    if total_height != preview_height:
        errors.append(
            f"slice heights total {total_height}px; preview height is {preview_height}px"
        )
    return tuple(errors)
