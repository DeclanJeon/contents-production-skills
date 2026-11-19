#!/usr/bin/env python3
"""Validate a concept selection against the packaged taxonomy and rules.

Usage: python concept_check.py selection.json [--taxonomy PATH] [--rules PATH]

Prints one JSON report: unknown values, missing required axes, compatibility
issues (error/warn/info, override-aware), and the merged direction-rule packs.
Exit code 1 when a blocking error remains, 2 on unreadable input, else 0.
Read-only: never writes files or calls a network.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "references"
NO_SPEECH_BLOCKED = ("dialogue_driven", "narration_driven")


def load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # PyYAML; only needed when the checker actually runs

    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def index(taxonomy: dict[str, Any]) -> dict[str, Any]:
    axes: dict[str, Any] = {}
    for axis in taxonomy["axes"]:
        groups = {g["id"]: {i["id"] for i in g["items"]} for g in axis["groups"]}
        axes[axis["id"]] = {"axis": axis, "groups": groups, "all": set().union(*groups.values())}
    return axes


def values(sel: dict[str, Any], key: str) -> list[str]:
    if key.startswith("direction."):
        value = (sel.get("direction") or {}).get(key.split(".", 1)[1])
    else:
        value = sel.get(key)
    if value in (None, "", [], {}):
        return []
    return list(value) if isinstance(value, list) else [value]


def matches(sel: dict[str, Any], when: dict[str, Any]) -> bool:
    for key, expected in when.items():
        wanted = expected if isinstance(expected, list) else [expected]
        if not set(values(sel, key)) & set(wanted):
            return False
    return True


def unknown_values(sel: dict[str, Any], axes: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for axis_id, meta in axes.items():
        if axis_id == "direction":
            for group, item in (sel.get("direction") or {}).items():
                if group not in meta["groups"]:
                    problems.append(f"direction.{group}: unknown group")
                elif item not in meta["groups"][group]:
                    problems.append(f"direction.{group}: unknown value {item!r}")
            continue
        for item in values(sel, axis_id):
            if item not in meta["all"]:
                problems.append(f"{axis_id}: unknown value {item!r}")
        limit = meta["axis"].get("max")
        if limit and len(values(sel, axis_id)) > limit:
            problems.append(f"{axis_id}: more than {limit} values")
    return problems


def missing_required(sel: dict[str, Any], axes: dict[str, Any]) -> list[str]:
    missing = []
    for axis_id, meta in axes.items():
        axis = meta["axis"]
        if not axis.get("required"):
            continue
        if axis_id == "direction":
            if not sel.get("direction"):
                missing.append("direction")
        elif not values(sel, axis_id) and not (axis_id == "duration" and sel.get("duration_custom_s")):
            missing.append(axis_id)
    return missing


def compatibility(sel: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    overrides = set(sel.get("overrides") or [])
    issues = []
    for rule in rules["compatibility"]:
        if matches(sel, rule["when"]):
            overridden = bool(rule.get("override")) and rule["id"] in overrides
            issues.append({"rule": rule["id"], "severity": "info" if overridden else rule["severity"],
                           "message": rule["msg"], "fix": rule.get("fix"), "overridden": overridden})
    if "no_speech" in (sel.get("constraints") or []) and (sel.get("direction") or {}).get("sound") in NO_SPEECH_BLOCKED:
        issues.append({"rule": "C100", "severity": "error", "message": "no-speech constraint with a dialogue/narration sound axis",
                       "fix": "choose silent, music-driven or ASMR sound", "overridden": False})
    return issues


def direction_rules(sel: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {"applied": []}
    for pack in rules["direction_rules"]:
        if not matches(sel, pack["when"]):
            continue
        merged["applied"].append(pack["id"])
        for key, value in pack["rules"].items():
            if isinstance(value, list):
                merged.setdefault(key, [])
                merged[key] += [v for v in value if v not in merged[key]]
            else:
                merged.setdefault(key, value)
    return merged


def check(sel: dict[str, Any], taxonomy: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    axes = index(taxonomy)
    issues = compatibility(sel, rules)
    blocking = [i["rule"] for i in issues if i["severity"] == "error"]
    unknown = unknown_values(sel, axes)
    return {"unknown_values": unknown, "missing_required": missing_required(sel, axes), "compatibility": issues,
            "blocking": blocking, "direction_rules": direction_rules(sel, rules),
            "ok": not blocking and not unknown}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("selection")
    parser.add_argument("--taxonomy", default=str(REFS / "concept-taxonomy.yaml"))
    parser.add_argument("--rules", default=str(REFS / "concept-rules.yaml"))
    args = parser.parse_args(argv)
    try:
        sel = json.loads(Path(args.selection).read_text(encoding="utf-8"))
        sel = sel.get("selection", sel)
        report = check(sel, load_yaml(Path(args.taxonomy)), load_yaml(Path(args.rules)))
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["blocking"] else 1


if __name__ == "__main__":
    sys.exit(main())
