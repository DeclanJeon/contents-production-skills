#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3", "pytest>=8"]
# ///

# ─── How to run ───
#      uv run test_page_output.py
# ──────────────────

from __future__ import annotations

import json
from pathlib import Path

import pytest

import page_builder_test_support

from builder import ComposeRequest, OutputPathError, compose_page
from errors import RenderError
from page_spec import render_copy_markdown, load_page_spec
from validate_output import validate_bundle


def test_smartstore_exports_module_assets_and_validates_bundle(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    output_dir = tmp_path / "published-assets"
    manifest = compose_page(ComposeRequest(spec_path, output_dir))

    assert manifest.module_count == 3
    assert manifest.output_mode.value == "module_images"
    assert manifest.readiness.upload_readiness.value == "blocked"
    assert all((output_dir / module.file).is_file() for module in manifest.modules)
    page = load_page_spec(spec_path)
    assert (output_dir / "copy.md").read_text(encoding="utf-8") == render_copy_markdown(page)

    report = validate_bundle(spec_path, output_dir)

    assert report.errors == ()
    assert report.warnings
    assert manifest.slice_files == ()
    assert not (output_dir / "slices").exists()
    assert (output_dir / "detail-page-preview.jpg").is_file()


def test_existing_output_directory_is_never_overwritten(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    output_dir = tmp_path / "user-output"
    output_dir.mkdir()
    sentinel = output_dir / "keep.txt"
    sentinel.write_text("user-owned", encoding="utf-8")

    with pytest.raises(OutputPathError):
        compose_page(ComposeRequest(spec_path, output_dir))

    assert sentinel.read_text(encoding="utf-8") == "user-owned"


def test_text_only_module_renders_without_repeating_product_photo(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    module = data["modules"][1]
    module["layout"] = "text-only"
    module["background_image"] = None
    module["image_asset_id"] = None
    spec_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    output_dir = tmp_path / "text-only-assets"

    manifest = compose_page(ComposeRequest(spec_path, output_dir))
    report = validate_bundle(spec_path, output_dir)

    assert (output_dir / "modules/compartments.jpg").is_file()
    assert manifest.modules[1].file == "modules/compartments.jpg"
    assert report.errors == ()


def test_missing_background_stops_before_output_creation(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(
        tmp_path,
        page_builder_test_support.PageFixtureOptions(background="missing.png"),
    )
    output_dir = tmp_path / "no-partial-output"

    with pytest.raises(RenderError):
        compose_page(ComposeRequest(spec_path, output_dir))

    assert not output_dir.exists()
