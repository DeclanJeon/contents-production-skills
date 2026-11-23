"""Offline checks for the Prompt Motion absorption ledger (no archive needed)."""
from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "research" / "prompt-motion-absorption-ledger.csv"
CODING = ROOT / "docs" / "research" / "prompt-motion-coding.csv"
FIELDS = ["entry_id", "variant", "page_url", "tags", "prompt_sha256", "dup_group", "format",
          "techniques", "evidence", "disposition", "target", "reason", "visual_check"]
FORMATS = {"showreel", "product_film", "explainer", "character_short", "realtime_3d",
           "logo_bumper", "edit_assist", "other"}
EVIDENCE = {"tested", "original_example", "template_tested", "untested", "skill"}
DISPOSITIONS = {"absorb", "example", "reference", "exclude"}
VARIANTS = {"original": 234, "improved_default": 211, "template_default": 2, "skill_no_public_prompt": 3}
TECHNIQUE = re.compile(r"T-[a-z0-9-]+")
ANCHOR = re.compile(r"\{#([^}]+)\}")


def rows() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def skill_dirs() -> list[Path]:
    return [ROOT / name for name in json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["skills"]]


def skill_markdown() -> list[Path]:
    return [path for folder in skill_dirs() for path in folder.rglob("*.md")]


def anchors(path: Path) -> set[str]:
    return set(ANCHOR.findall(path.read_text(encoding="utf-8")))


def test_ledger_shape_and_enums() -> None:
    data = rows()
    assert list(data[0]) == FIELDS
    assert len(data) == 450
    assert len({(r["entry_id"], r["variant"]) for r in data}) == 450
    assert Counter(r["variant"] for r in data) == VARIANTS
    keys = {f"{r['entry_id']}:{r['variant']}" for r in data}
    for r in data:
        key = f"{r['entry_id']}:{r['variant']}"
        assert r["format"] in FORMATS, key
        assert r["evidence"] in EVIDENCE, key
        assert r["disposition"] in DISPOSITIONS, key
        assert r["dup_group"] in keys, key
        assert r["visual_check"] in ("", "pass", "mismatch"), key
        assert r["page_url"].startswith("https://prompt-motion.com/"), key
        assert all(TECHNIQUE.fullmatch(t) for t in filter(None, r["techniques"].split(";"))), key
        if r["format"] == "other" or r["disposition"] in ("reference", "exclude"):
            assert r["reason"].strip(), key
        if r["variant"] == "skill_no_public_prompt":
            assert r["prompt_sha256"] == "" and r["evidence"] == "skill"
        else:
            assert re.fullmatch(r"[0-9a-f]{64}", r["prompt_sha256"]), key


def test_duplicate_rows_share_coding() -> None:
    by_group: dict[str, set[tuple[str, str, str]]] = {}
    for r in rows():
        by_group.setdefault(r["dup_group"], set()).add((r["format"], r["techniques"], r["prompt_sha256"]))
    assert all(len(values) == 1 for values in by_group.values())


def test_targets_resolve() -> None:
    for r in rows():
        if r["disposition"] in ("absorb", "example"):
            path, _, anchor = r["target"].partition("#")
            target = ROOT / path
            assert target.is_file(), r["target"]
            if anchor:
                assert anchor in anchors(target), r["target"]
        else:
            assert r["target"] == "", r["entry_id"]


def test_untested_rows_are_not_cited_as_absorb_evidence_alone() -> None:
    absorbed: dict[str, set[str]] = {}
    for r in rows():
        if r["disposition"] == "absorb":
            for technique in filter(None, r["techniques"].split(";")):
                absorbed.setdefault(technique, set()).add(r["evidence"])
    assert absorbed, "no absorbed techniques"


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    return [p for p in out if not p.startswith((".worktrees/", ".ultragoal/", ".omo/", ".omx/"))]


def test_hygiene_no_archive_media_or_prompt_text() -> None:
    files = tracked_files()
    entry_ids = {r["entry_id"] for r in rows()}
    assert not [p for p in files if Path(p).stem in entry_ids or "prompt-motion" in p and p.endswith((".gif", ".mp4"))]
    assert not [p for p in files if p.endswith("prompts.csv")]
    assert not (ROOT / "docs" / "research" / "prompt-motion-gallery.tsv").exists()
    for path in skill_markdown():
        text = path.read_text(encoding="utf-8")
        for needle in ("<direction>", "<structure>", "<gotchas>", "npx skills add", "/plugin install"):
            assert needle not in text, f"{path.relative_to(ROOT)}: {needle}"


CLAIM_WORDS = ("예제에서 확인", "효과가 입증", "효과적", "검증된")
SOURCE_LINE = re.compile(r"^출처: Prompt Motion (.+?) · 근거 (.+?) · 확인 2026-11-23", re.MULTILINE)


def technique_sections() -> dict[str, list[tuple[Path, str]]]:
    found: dict[str, list[tuple[Path, str]]] = {}
    for path in skill_markdown():
        body = path.read_text(encoding="utf-8")
        for match in re.finditer(r"^#{2,4} .*\{#(t-[a-z0-9-]+)\}\s*$", body, re.MULTILINE):
            rest = body[match.end():]
            end = re.search(r"^#{2,4} ", rest, re.MULTILINE)
            found.setdefault(match.group(1), []).append((path, rest[: end.start()] if end else rest))
    return found


def absorbed() -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    for r in rows():
        if r["disposition"] == "absorb":
            technique = r["target"].partition("#")[2]
            out.setdefault(technique, []).append(r)
    return out


def test_each_absorbed_technique_has_one_canonical_section() -> None:
    sections = technique_sections()
    for technique, cited in absorbed().items():
        places = sections.get(technique, [])
        assert len(places) == 1, (technique, [str(p.relative_to(ROOT)) for p, _ in places])
        path, body = places[0]
        assert Path(cited[0]["target"].partition("#")[0]) == path.relative_to(ROOT), technique
    assert set(sections) == set(absorbed()), set(sections) ^ set(absorbed())


def test_sections_cite_ledger_rows_and_match_evidence() -> None:
    sections = technique_sections()
    for technique, cited in absorbed().items():
        _, body = sections[technique][0]
        match = SOURCE_LINE.search(body)
        assert match, f"{technique}: missing source line"
        ids = {r["entry_id"] for r in cited}
        assert {part.strip() for part in match.group(1).split(",")} == ids, technique
        evidence = {r["evidence"] for r in cited}
        if evidence <= {"untested"}:
            assert "관찰된 프롬프트 패턴" in body, technique
            assert not any(word in body for word in CLAIM_WORDS), technique
        if "예제에서 확인" in body:
            assert any(r["visual_check"] == "pass" for r in cited), technique


def test_copy_detector_flags_word_runs_and_ignores_numbers() -> None:
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import prompt_motion_ledger as ledger

    source, _ = ledger.shingles("Rebuild the real interface as vector layers so its parts can move")
    copied, _ = ledger.shingles("우리는 rebuild the real interface as vector layers so its parts 를 쓴다")
    assert source & copied
    numbers, _ = ledger.shingles("cubic bezier 0 16 1 0 3 1 easing")
    assert not numbers
    _, hangul = ledger.shingles("가나다라마바사아자차카타파하가나다라마바사아자차")
    assert hangul
