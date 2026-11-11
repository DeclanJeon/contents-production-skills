"""Static/installed contracts, not a model or media quality benchmark."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "video-production-assets/references"
GUIDE = REFS / "korean-script-postediting.md"


def test_references_and_anchors_exist():
    guide = GUIDE.read_text(encoding="utf-8")
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', guide))
    assert anchors == {"scope", "workflow", "dialogue", "narration", "packet", "gates", "handoff"}
    for term in ("제안 전용", "기본 적용 보류", "QA-only", "무음", "승인본", "기존 음성",
                 "독립 검토", "최대 1회", "미검증", "최초 원문"):
        assert term in guide
    for file in (GUIDE, REFS / "korean-script-postediting-patterns.md"):
        for link in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding="utf-8")):
            if "://" not in link:
                path, _, anchor = link.partition("#")
                target = (file.parent / path) if path else file
                assert target.is_file(), link
                if target == GUIDE and anchor:
                    assert anchor in anchors


def test_packet_example_runs_against_cli(tmp_path):
    guide = GUIDE.read_text(encoding="utf-8")
    example = json.loads(re.search(r'```json\n(.*?)\n```', guide, re.S).group(1))
    source = "안녕"
    assert example["source_sha256"] == hashlib.sha256(source.encode()).hexdigest()
    for name, value in (("source.md", source), ("candidate.md", source),
                        ("packet.json", json.dumps(example, ensure_ascii=False))):
        (tmp_path / name).write_text(value, encoding="utf-8")
    cli = ROOT / "video-production-assets/scripts/korean_script_postediting.py"
    run = subprocess.run([sys.executable, str(cli), "--source", "source.md",
                          "--candidate", "candidate.md", "--packet", "packet.json"],
                         cwd=tmp_path, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    assert json.loads(run.stdout)["scope"] == ["S01/SP01"]


def test_patterns_have_upstream_mapping_and_genre_guards():
    patterns = (REFS / "korean-script-postediting-patterns.md").read_text(encoding="utf-8")
    for i in range(1, 9):
        assert f"KP{i:02d}" in patterns
    for term in ("원본", "발동", "대사", "내레이션", "보존", "예시"):
        assert term in patterns
    assert "100자 장문 삽입" in patterns and "강제하지 않는다" in patterns


def test_behavior_suite_has_all_required_classes():
    suite = json.loads((ROOT / "qa/korean-script-postediting-cases.json").read_text(encoding="utf-8"))
    assert suite["schema"] == "korean-script-postediting-cases/1"
    required = {"translationese", "already_good", "two_speakers", "subtext", "mixed_quote",
                "enumeration", "poetic", "modality", "approved_audio", "qa_only",
                "no_speech", "short_negation", "retry_stop"}
    assert required <= {c["kind"] for c in suite["cases"]}
    assert len({c["id"] for c in suite["cases"]}) == len(suite["cases"])
    for case in suite["cases"]:
        assert all(key in case for key in ("prompt", "source", "locked", "must_preserve",
                                          "should_improve", "forbidden_actions"))
        assert case["must_preserve"] and case["forbidden_actions"]


def test_provenance_is_pinned_and_notice_preserved():
    provenance = (REFS / "upstream/im-not-ai-provenance.md").read_text(encoding="utf-8")
    assert "b37e0206d31fffd9149bf57168d4d62eb2086bee" in provenance
    assert "SequenceMatcher" in provenance and "bigram" in provenance
    assert len(re.findall(r'`[a-f0-9]{64}`', provenance)) >= 4
    notice = (REFS / "upstream/im-not-ai-LICENSE.txt").read_text(encoding="utf-8")
    assert "MIT License" in notice and "Copyright (c) 2026 epoko77-ai" in notice
    assert 'THE SOFTWARE IS PROVIDED "AS IS"' in notice


def test_each_owner_reaches_current_stage_reference():
    owners = {
        "video-production-assets/SKILL.md": "references/korean-script-postediting.md#scope",
        "video-production-assets/references/03-screenplay.md": "korean-script-postediting.md#workflow",
        "video-production-assets/references/22-dialogue-lipsync.md": "korean-script-postediting.md#handoff",
        "video-production-assets/references/12-qa.md": "korean-script-postediting.md#gates",
        "creative-production/references/production-routing.md": "../../video-production-assets/references/korean-script-postediting.md#scope",
        "integrations/skill-routing.md": "../video-production-assets/references/korean-script-postediting.md#scope",
    }
    for owner, pointer in owners.items():
        assert pointer in (ROOT / owner).read_text(encoding="utf-8"), owner
    for name in ("README.md", "USAGE_GUIDE.md", "CHANGELOG.md", "integrations/package-provenance.md"):
        assert "korean-script-postediting" in (ROOT / name).read_text(encoding="utf-8"), name


def test_no_schema_template_manifest_expansion():
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert "humanize-korean" not in manifest["skills"]
    assert not any("postediting" in skill for skill in manifest["skills"])
    template = ROOT / "video-production-assets/assets/03-screenplay-template.md"
    assert "korean-script-postediting" not in template.read_text(encoding="utf-8")
    contract = (REFS / "contract.md").read_text(encoding="utf-8")
    assert "korean-script-postediting/1" not in contract


def test_installed_postediting_runs_without_repo_or_home_dependencies(tmp_path, monkeypatch):
    import install_package

    repo, destination = tmp_path / "fixture", tmp_path / "installed"
    home = tmp_path / "decoy-home"
    home.mkdir()
    (home / "untouched").write_text("keep", encoding="utf-8")
    monkeypatch.setenv("CODEX_HOME", str(home))
    repo.mkdir()
    manifest = {"version": "0.0-test", "skills": ["video-production-assets", "creative-production"],
                "entry_skill": "creative-production", "support_skill": "video-production-assets"}
    (repo / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for name in ("examples", "qa"):
        (repo / name).mkdir()
        (repo / name / "placeholder.txt").write_text("fixture", encoding="utf-8")
    files = ["video-production-assets/SKILL.md", "creative-production/SKILL.md",
             "creative-production/references/production-routing.md"]
    files += ["video-production-assets/scripts/" + name for name in
              ("korean_script_packet.py", "korean_script_postediting.py")]
    files += ["video-production-assets/references/" + name for name in
              ("korean-script-postediting.md", "korean-script-postediting-patterns.md",
               "22-dialogue-lipsync.md", "contract.md", "upstream/im-not-ai-provenance.md",
               "upstream/im-not-ai-LICENSE.txt")]
    for name in files:
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    install_package.install(destination, repo_root=repo, exclude_derived_support=True)
    guide = destination / "video-production-assets/references/korean-script-postediting.md"
    example = json.loads(re.search(r'```json\n(.*?)\n```', guide.read_text(encoding="utf-8"), re.S).group(1))
    (tmp_path / "source.md").write_bytes("안녕".encode())
    (tmp_path / "packet.json").write_text(json.dumps(example), encoding="utf-8")
    cli = destination / "video-production-assets/scripts/korean_script_postediting.py"
    run = subprocess.run([sys.executable, "-B", str(cli), "--source", "source.md", "--candidate",
                          "source.md", "--packet", "packet.json"], cwd=tmp_path,
                         capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    assert json.loads(run.stdout)["exit_code"] == 0
    assert not (destination / "docs").exists()
    assert list(home.iterdir()) == [home / "untouched"]
    for file in (guide, guide.with_name("korean-script-postediting-patterns.md"),
                 guide.parent / "upstream/im-not-ai-provenance.md"):
        for link in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding="utf-8")):
            if "://" not in link:
                relative = link.split("#")[0]
                target = (file.parent / relative) if relative else file
                assert target.is_file(), link
