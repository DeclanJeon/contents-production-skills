#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3"]
# ///

# ─── How to run ───
# 1. Install uv (if not installed):
#      curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Run directly (no venv, no pip install needed):
#      uv run validate_output.py --spec page-spec.json --output output/product
# 3. Or make executable and run:
#      chmod +x validate_output.py && ./validate_output.py --help
# ──────────────────

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, assert_never

from pydantic import ValidationError

from errors import PageSpecError
from output_checks import (
    ValidationBundle,
    check_module_files,
    check_preview,
    check_slices,
    check_source_images,
    image_size,
)
from output_manifest import (
    OutputManifest,
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
    OutputMode,
    PlatformRegistry,
    PlatformProfile,
    PLATFORM_REGISTRY_PATH,
    load_platform_registry,
)


@dataclass(frozen=True, slots=True)
class ValidationReport:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.errors


def validate_bundle(spec_path: Path, output_dir: Path) -> ValidationReport:
    """Check a composed bundle without claiming human visual or seller approval."""
    errors: list[str] = []
    warnings: list[str] = []
    spec_path = spec_path.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    try:
        spec = load_page_spec(spec_path)
        registry: PlatformRegistry = load_platform_registry(PLATFORM_REGISTRY_PATH)
    except PageSpecError as exc:
        return ValidationReport((str(exc),), ())

    profile = registry.for_platform(spec.platform)
    errors.extend(check_source_images(spec, spec_path))
    brief_path = output_dir / "brief.json"
    expected_brief = PageBrief(
        product_name=spec.product_name,
        platform=spec.platform,
        locale=spec.locale,
        category=spec.category,
        product_images=spec.product_images,
        facts=spec.facts,
    )
    try:
        brief = PageBrief.model_validate_json(brief_path.read_bytes())
    except OSError as exc:
        errors.append(f"brief is missing or unreadable: {exc}")
    except ValidationError as exc:
        errors.append(f"brief is invalid: {exc}")
    else:
        if brief != expected_brief:
            errors.append("brief facts do not match the source page-spec")

    for module in spec.modules:
        background_image = module.background_image
        if background_image is None:
            continue
        raw = Path(background_image).expanduser()
        background = raw if raw.is_absolute() else spec_path.parent / raw
        if image_size(background) is None:
            errors.append(f"module {module.id} background is missing or unreadable")

    copy_path = output_dir / "copy.md"
    if not copy_path.is_file():
        errors.append("missing copy.md")
    else:
        try:
            copy_text = copy_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"copy.md is unreadable: {exc}")
        else:
            if copy_text != render_copy_markdown(spec):
                errors.append("copy.md does not match the exact page-spec text")

    bundled_spec_path = output_dir / "page-spec.json"
    try:
        bundled_spec = load_page_spec(bundled_spec_path)
    except PageSpecError as exc:
        errors.append(str(exc))
    else:
        if bundled_spec != spec:
            errors.append("bundled page-spec does not match the source page-spec")

    manifest_path = output_dir / "manifest.json"
    try:
        manifest = OutputManifest.model_validate_json(manifest_path.read_bytes())
    except OSError as exc:
        errors.append(f"manifest is missing or unreadable: {exc}")
        return ValidationReport(tuple(errors), tuple(warnings))
    except ValidationError as exc:
        errors.append(f"manifest is invalid: {exc}")
        return ValidationReport(tuple(errors), tuple(warnings))

    bundle = ValidationBundle(spec, manifest, output_dir, profile)
    if manifest.platform is not spec.platform or manifest.output_mode is not profile.output_mode:
        errors.append("manifest platform or output mode does not match the platform profile")
    match manifest.readiness.plan_review:
        case ReviewReadiness.NOT_RECORDED:
            pass
        case ReviewReadiness.REQUIRED:
            errors.append("manifest cannot claim a user plan review from the compositor")
        case unreachable:
            assert_never(unreachable)
    match manifest.readiness.asset_visual_review:
        case ReviewReadiness.REQUIRED:
            pass
        case ReviewReadiness.NOT_RECORDED:
            errors.append("manifest must leave actual asset visual review unresolved")
        case unreachable:
            assert_never(unreachable)
    match manifest.readiness.platform_profile:
        case ProfileReadiness.VERIFIED:
            if not spec.output.platform_confirmed:
                errors.append("manifest cannot verify an unconfirmed platform profile")
        case ProfileReadiness.SELLER_CONFIRMATION_REQUIRED:
            if spec.output.platform_confirmed:
                errors.append("manifest must reflect the confirmed platform profile")
            if profile.requires_seller_confirmation:
                match manifest.readiness.upload_readiness:
                    case UploadReadiness.BLOCKED:
                        pass
                    case UploadReadiness.HUMAN_REVIEW_REQUIRED:
                        errors.append("upload readiness must be blocked until seller confirmation")
                    case unreachable:
                        assert_never(unreachable)
        case unreachable:
            assert_never(unreachable)
    if any(module.preview_only for module in spec.modules):
        match manifest.readiness.upload_readiness:
            case UploadReadiness.BLOCKED:
                pass
            case UploadReadiness.HUMAN_REVIEW_REQUIRED:
                errors.append("concept-only modules must block upload readiness")
            case unreachable:
                assert_never(unreachable)
    module_files = check_module_files(bundle)
    errors.extend(module_files.errors)
    total_height = module_files.total_height
    errors.extend(check_preview(bundle, total_height))
    match profile.output_mode:
        case OutputMode.LONG_PAGE_SLICES:
            errors.extend(check_slices(bundle, total_height))
        case OutputMode.MODULE_IMAGES:
            if manifest.slice_files:
                errors.append("module-image profile must not declare long-page slices")
        case unreachable:
            assert_never(unreachable)

    warnings.extend(manifest.warnings)
    if profile.requires_seller_confirmation and not spec.output.platform_confirmed:
        warnings.append("seller-center export profile is not confirmed")
        if manifest.readiness.upload_readiness is not UploadReadiness.BLOCKED:
            errors.append("manifest must block upload readiness until profile confirmation")
    warnings.append("human product-identity and visual review is still required")
    warnings.append("validator success does not establish factual or commercial performance")
    return ValidationReport(tuple(errors), tuple(dict.fromkeys(warnings)))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a product-detail output bundle.")
    parser.add_argument("--spec", required=True, type=Path, help="Source page-spec.json")
    parser.add_argument("--output", required=True, type=Path, help="Composed output directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    report = validate_bundle(args.spec, args.output)
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if report.errors:
        print(f"validation failed: {len(report.errors)} error(s)", file=sys.stderr)
        return 1
    print(f"validation passed with {len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
