#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3", "pytest>=8"]
# ///

# ─── How to run ───
#      uv run test_page_export.py
# ──────────────────

from __future__ import annotations

import json
from pathlib import Path

import pytest

import page_builder_test_support

from builder import ComposeRequest, compose_page
from errors import PageSpecError
from export_slices import export_slices
from validate_output import validate_bundle


def test_long_page_profile_exports_bounded_slices(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(
        tmp_path,
        page_builder_test_support.PageFixtureOptions(
            platform="custom",
            slice_height_px=800,
        ),
    )
    output_dir = tmp_path / "long-page-assets"
    manifest = compose_page(ComposeRequest(spec_path, output_dir))

    slices = export_slices(spec_path, output_dir)
    updated_manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest.output_mode.value == "long_page_slices"
    assert len(slices) == 4
    assert updated_manifest["slice_files"] == list(slices)
    assert validate_bundle(spec_path, output_dir).errors == ()


def test_slice_size_failure_leaves_no_partial_slice_directory(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(
        tmp_path,
        page_builder_test_support.PageFixtureOptions(
            platform="custom",
            max_file_bytes=1,
            slice_height_px=800,
        ),
    )
    output_dir = tmp_path / "bounded-assets"
    compose_page(ComposeRequest(spec_path, output_dir))

    with pytest.raises(PageSpecError):
        export_slices(spec_path, output_dir)

    assert not (output_dir / "slices").exists()


def test_long_page_profile_requires_slice_height_before_output_creation(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(
        tmp_path,
        page_builder_test_support.PageFixtureOptions(platform="custom"),
    )
    output_dir = tmp_path / "missing-slice-height"

    with pytest.raises(PageSpecError):
        compose_page(ComposeRequest(spec_path, output_dir))

    assert not output_dir.exists()


def test_coupang_requires_confirmation_and_keeps_module_exports(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(
        tmp_path,
        page_builder_test_support.PageFixtureOptions(platform="coupang"),
    )
    output_dir = tmp_path / "coupang-assets"
    manifest = compose_page(ComposeRequest(spec_path, output_dir))

    assert manifest.output_mode.value == "module_images"
    assert manifest.readiness.upload_readiness.value == "blocked"
    assert export_slices(spec_path, output_dir) == ()
    assert manifest.slice_files == ()
    assert validate_bundle(spec_path, output_dir).errors == ()
