#!/usr/bin/env python3
"""Locks the still-asset generation contract that S07/S07b depend on.

Prompts alone are not assets: the package must keep the inventory, the
dependency order, the bounded concurrency, the no-retry rule for uncertain
jobs, hash registration and the available-is-not-verified distinction
reachable from the coordinator and from `video-production-assets`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "video-production-assets/references/32-still-asset-generation-jobs.md"

REQUIRED = [
    "7뷰",
    "정면·후면·착용 전신 3면",
    "establishing·reverse·lateral·top-down",
    "소품",
    "LOOK",
    "컷 시작·끝 프레임",
    "최대 5개",
    "자동 재시도하지 않는다",
    "sha256",
    "파일이 있다는 뜻일 뿐",
    "`verified`",
    "assets/image_prompts.json",
    "assets/image_outputs.json",
    "assets/asset_registry.json",
]

LINKS = [
    ("video-production-assets/SKILL.md", "references/32-still-asset-generation-jobs.md"),
    ("video-production-assets/references/module-index.md", "32-still-asset-generation-jobs.md"),
    ("creative-production/SKILL.md", "../video-production-assets/references/32-still-asset-generation-jobs.md"),
    ("creative-production/references/skill-map.md", "S07b"),
]


def test_reference_keeps_the_contract() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    missing = [phrase for phrase in REQUIRED if phrase not in text]
    assert not missing, missing


def test_contract_is_reachable_from_owner_and_coordinator() -> None:
    for relative, needle in LINKS:
        assert needle in (ROOT / relative).read_text(encoding="utf-8"), relative


def test_relative_links_resolve() -> None:
    for path in (REFERENCE, ROOT / "creative-production/SKILL.md"):
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("mailto:"):
                continue
            assert (path.parent / target).exists(), f"{path.name}: {target}"


def test_parallel_cap_is_a_host_limit_not_a_project_option() -> None:
    text = REFERENCE.read_text(encoding="utf-8")
    assert "프로젝트별이 아니라" in text
    assert "비용 승인" in text and "아니다" in text
