#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10", "pydantic>=2,<3", "pytest>=8"]
# ///

# ─── How to run ───
#      uv run test_page_spec.py
# ──────────────────

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import page_builder_test_support

from page_spec import PageSpec


def test_page_spec_blocks_publishable_unconfirmed_fact(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    data["facts"][-1]["publish"] = True

    with pytest.raises(ValidationError):
        PageSpec.model_validate_json(json.dumps(data))


def test_page_spec_rejects_missing_fact_reference(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    data["modules"][0]["fact_ids"] = ["not-a-fact"]

    with pytest.raises(ValidationError):
        PageSpec.model_validate_json(json.dumps(data))


def test_unpublished_visible_claim_can_be_recorded_but_not_used(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    data["facts"].append(
        {
            "id": "high-protein-label",
            "value": "High-protein chips",
            "source": "visible",
            "evidence": {
                "kind": "visible_image_region",
                "locator": "front label claim",
                "asset_id": "front-photo",
                "region": [0.1, 0.1, 0.7, 0.2],
            },
            "publish": False,
        }
    )
    PageSpec.model_validate_json(json.dumps(data))
    data["modules"][0]["fact_ids"].append("high-protein-label")

    with pytest.raises(ValidationError):
        PageSpec.model_validate_json(json.dumps(data))


def test_text_only_module_rejects_product_background_reference(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    module = data["modules"][1]
    module["layout"] = "text-only"

    with pytest.raises(ValidationError):
        PageSpec.model_validate_json(json.dumps(data))


def test_platform_confirmation_requires_a_source_and_check_date(tmp_path: Path) -> None:
    spec_path = page_builder_test_support.make_page_spec(tmp_path)
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    data["output"]["platform_confirmed"] = True

    with pytest.raises(ValidationError):
        PageSpec.model_validate_json(json.dumps(data))
