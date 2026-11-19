"""Packaged taxonomy/rules stay loadable and the checker enforces them."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import concept_check  # noqa: E402

REFS = Path(__file__).resolve().parents[1] / "references"
TAX = yaml.safe_load((REFS / "concept-taxonomy.yaml").read_text(encoding="utf-8"))
RULES = yaml.safe_load((REFS / "concept-rules.yaml").read_text(encoding="utf-8"))
BASE = {"format": "short_drama", "genre": ["comedy"], "narrative": "ending_first",
        "direction": {"texture": "cinematic", "expression": "live_action", "sound": "music_driven"},
        "emotion_arc": ["laughter", "empathy"], "production_method": "live_action_ai",
        "duration": "s60", "aspect": "r9_16"}


def test_user_lists_are_complete() -> None:
    axes = {a["id"]: a for a in TAX["axes"]}
    count = lambda axis: sum(len(g["items"]) for g in axes[axis]["groups"])  # noqa: E731
    assert len(axes["format"]["groups"]) == 12
    assert count("culture_style") == 22 and count("romance_concept") == 24
    assert count("story_nature") == 23 and count("narrative") == 12
    fantasy = next(g for g in axes["world"]["groups"] if g["id"] == "fantasy_world")
    assert len(fantasy["items"]) == 24
    assert [i["id"] for i in axes["duration"]["groups"][0]["items"]] == ["s15", "s30", "s60", "s90"]


def test_rules_only_reference_known_items() -> None:
    axes = concept_check.index(TAX)
    for rule in RULES["compatibility"] + RULES["direction_rules"]:
        for key, val in rule["when"].items():
            wanted = val if isinstance(val, list) else [val]
            if key.startswith("direction."):
                assert set(wanted) <= axes["direction"]["groups"][key.split(".", 1)[1]], rule["id"]
            else:
                assert set(wanted) <= axes[key]["all"], (rule["id"], key)


def test_clean_selection_passes() -> None:
    report = concept_check.check(BASE, TAX, RULES)
    assert report["ok"] and report["missing_required"] == [] and report["unknown_values"] == []


def test_missing_required_axes_are_listed() -> None:
    sel = {k: v for k, v in BASE.items() if k not in ("narrative", "direction")}
    assert set(concept_check.check(sel, TAX, RULES)["missing_required"]) == {"narrative", "direction"}


def test_blocking_rule_and_override() -> None:
    sel = dict(BASE, production_method="stickman_method", direction=dict(BASE["direction"], texture="photoreal"))
    assert "C001" in concept_check.check(sel, TAX, RULES)["blocking"]
    sel["overrides"] = ["C001"]
    assert concept_check.check(sel, TAX, RULES)["blocking"] == []


def test_no_speech_cannot_be_overridden() -> None:
    sel = dict(BASE, constraints=["no_speech"], overrides=["C100"], direction=dict(BASE["direction"], sound="dialogue_driven"))
    assert "C100" in concept_check.check(sel, TAX, RULES)["blocking"]


def test_1990s_melodrama_forbids_smartphones() -> None:
    sel = dict(BASE, era="y1990s", culture_style="k_drama")
    rules = concept_check.check(sel, TAX, RULES)["direction_rules"]
    assert "D_kr_melo_1990s" in rules["applied"] and "스마트폰" in rules["forbidden_props"]


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = tmp_path / "good.json"
    good.write_text(json.dumps({"selection": BASE}), encoding="utf-8")
    assert concept_check.main([str(good)]) == 0
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(dict(BASE, narrative="nope")), encoding="utf-8")
    assert concept_check.main([str(bad)]) == 0  # unknown values are reported, not blocking
    assert "unknown value" in capsys.readouterr().out
    assert concept_check.main([str(tmp_path / "missing.json")]) == 2
