"""The speed-ramp limit is real, documented, and enforced.

`project.json` takes one scalar `playback_rate` per shot, so a ramp inside a single
shot cannot be represented. The failure this guards against is a plan that claims a
smooth ramp (a curve, a rate list) while the machine-readable schedule records a
single constant rate -- the claim and the artifact then disagree, and nothing catches
it until someone watches the output.

So: the validator must reject a non-scalar rate, and both the owning contract and the
editing procedure must say how a ramp is actually represented.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Final

import pytest

ROOT: Final = Path(__file__).resolve().parents[1]
VALIDATOR: Final = ROOT / "video-production-assets/scripts/validate_project.py"
CONTRACT: Final = ROOT / "video-production-assets/references/contract-project.md"
EDIT_PROCEDURE: Final = ROOT / "video-production-assets/references/09-edit.md"
CATALOG: Final = ROOT / "video-production-assets/references/edit-sound-language-catalog.md"


def project(rate: object) -> dict[str, object]:
    return {
        "project_id": "RAMPCHECK", "version": "1.0", "schema_version": "1.1",
        "fps": 24, "aspect_ratio": "9:16", "target_duration_s": 1.0,
        "scenes": [{"id": "S01", "purpose": "ramp"}],
        "characters": [],
        "shots": [{
            "id": "SH01", "scene_id": "S01", "character_ids": [],
            "start_s": 0.0, "end_s": 1.0, "source_duration_s": 1.0,
            "purpose": "ramped action", "start_state": "ready", "end_state": "done",
            "source_duration_status": "estimated", "playback_rate": rate,
        }],
        "claims": [],
        "artifacts": [{"id": "A01", "type": "edit_plan", "kind": "edit_plan",
                       "path": "edit_plan.md", "version": "1.0", "status": "draft"}],
        "audio_mode": "no_audio", "audio_cues": [], "captions": [],
    }


def validate(tmp_path: Path, rate: object) -> tuple[int, dict[str, object]]:
    path = tmp_path / "project.json"
    path.write_text(json.dumps(project(rate)), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path), "--profile", "plan"],
        capture_output=True, text=True, check=False,
    )
    return result.returncode, json.loads(result.stdout)


@pytest.mark.parametrize("rate", [[0.5, 2.0], {"at_s": 0.4, "rate": 2.0}, "ramp"])
def test_a_rate_curve_is_rejected(tmp_path: Path, rate: object) -> None:
    code, report = validate(tmp_path, rate)

    assert code != 0
    assert any("playback_rate" in error for error in report["errors"]), report


def test_a_scalar_rate_still_validates(tmp_path: Path) -> None:
    code, report = validate(tmp_path, 0.5)  # slow motion needs less source than supplied

    assert code == 0, report


def test_the_contract_and_the_edit_procedure_state_the_limit() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")
    procedure = EDIT_PROCEDURE.read_text(encoding="utf-8")
    catalog = CATALOG.read_text(encoding="utf-8")

    assert "샷당 스칼라 하나" in contract
    assert "연속 cut 행" in procedure and "인접 shot" in procedure
    assert "샷당 스칼라" in catalog
