#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3"]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run export_slices.py --spec page-spec.json --output output/product
# 3. Or make executable and run:
#      chmod +x export_slices.py && ./export_slices.py --help
# ──────────────────

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, assert_never

from PIL import Image
from pydantic import ValidationError

from errors import PageSpecError
from output_manifest import OutputManifest
from page_spec import OutputFormat, PageSpec, load_page_spec
from platform_profiles import (
    OutputMode,
    PlatformProfile,
    PlatformRegistry,
    PLATFORM_REGISTRY_PATH,
    load_platform_registry,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export configured module or long-page images.")
    parser.add_argument("--spec", required=True, type=Path, help="Input page-spec.json")
    parser.add_argument("--output", required=True, type=Path, help="Composed output directory")
    return parser


def _save_slice(request: SliceRequest) -> None:
    """Save one image slice in the requested format with deterministic settings."""
    match request.format:
        case OutputFormat.JPG:
            request.image.save(
                request.path,
                format="JPEG",
                quality=request.quality,
                optimize=True,
            )
        case OutputFormat.PNG:
            request.image.save(request.path, format="PNG", optimize=True)
        case unreachable:
            assert_never(unreachable)


@dataclass(frozen=True, slots=True)
class SliceRequest:
    image: Image.Image
    path: Path
    format: OutputFormat
    quality: int


def _export_long_page(
    spec: PageSpec,
    profile: PlatformProfile,
    output_dir: Path,
) -> tuple[str, ...]:
    """Split a preview into ordered, bounded-height files."""
    preview_path = output_dir / "detail-page-preview.jpg"
    width = spec.output.width_px
    slice_height = spec.output.slice_height_px
    if slice_height is None:
        raise PageSpecError(
            output_dir / "page-spec.json",
            "output.slice_height_px is required by the long-page slice profile",
        )
    quality = spec.output.quality
    extension = spec.output.format.value
    max_file_bytes = spec.output.max_file_bytes or profile.max_file_bytes
    slices_dir = output_dir / "slices"
    if slices_dir.exists():
        raise PageSpecError(slices_dir, "slice directory already exists; refusing overwrite")
    with tempfile.TemporaryDirectory(prefix=".slices-", dir=output_dir) as temporary:
        temporary_slices = Path(temporary) / "slices"
        temporary_slices.mkdir()
        files: list[str] = []
        with Image.open(preview_path) as preview:
            if preview.width != width:
                raise PageSpecError(preview_path, "preview width differs from page-spec")
            height = preview.height
            for start in range(0, height, slice_height):
                end = min(start + slice_height, height)
                region = preview.crop((0, start, width, end))
                name = f"slice-{len(files) + 1:03d}.{extension}"
                path = temporary_slices / name
                _save_slice(SliceRequest(region, path, spec.output.format, quality))
                if max_file_bytes is not None and path.stat().st_size > max_file_bytes:
                    raise PageSpecError(
                        path,
                        f"slice is {path.stat().st_size} bytes; configured limit is {max_file_bytes}",
                    )
                files.append((slices_dir / name).relative_to(output_dir).as_posix())
        temporary_slices.rename(slices_dir)
    return tuple(files)


def export_slices(spec_path: Path, output_dir: Path) -> tuple[str, ...]:
    """Export slices for long-page profiles; module-image profiles need no slicing."""
    spec = load_page_spec(spec_path.expanduser().resolve())
    registry: PlatformRegistry = load_platform_registry(PLATFORM_REGISTRY_PATH)
    profile = registry.for_platform(spec.platform)
    match profile.output_mode:
        case OutputMode.MODULE_IMAGES:
            return ()
        case OutputMode.LONG_PAGE_SLICES:
            preview_path = output_dir / "detail-page-preview.jpg"
            if not preview_path.is_file():
                raise PageSpecError(preview_path, "composed long-page preview is missing")
            slice_files = _export_long_page(spec, profile, output_dir)
            _update_manifest(output_dir, slice_files)
            return slice_files
        case unreachable:
            assert_never(unreachable)


def _update_manifest(output_dir: Path, slice_files: tuple[str, ...]) -> None:
    """Record observed slice paths in the existing output manifest."""
    manifest_path = output_dir / "manifest.json"
    try:
        manifest = OutputManifest.model_validate_json(manifest_path.read_bytes())
    except OSError as exc:
        raise PageSpecError(manifest_path, str(exc)) from exc
    except ValidationError as exc:
        raise PageSpecError(manifest_path, str(exc)) from exc
    updated = manifest.model_copy(update={"slice_files": slice_files})
    manifest_path.write_text(
        json.dumps(updated.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        slice_files = export_slices(args.spec, args.output)
    except (PageSpecError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"exported {len(slice_files)} slice(s) to {args.output.expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
