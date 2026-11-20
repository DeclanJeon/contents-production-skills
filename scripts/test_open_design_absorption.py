"""Checks for the open-design craft absorption: notices, source lines, engine-string and link hygiene."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from open_design_ledger import LEDGER_PATH, detect_license, read_ledger, write_ledger  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REFS = "video-production-assets/references"
UPSTREAM = ROOT / REFS / "upstream"
PROVENANCE = UPSTREAM / "open-design-provenance.md"

TARGET_PATHS: dict[str, list[str]] = {
    "33-motion-style-library": [f"{REFS}/33-motion-style-library.md", f"{REFS}/motion-styles/*.md"],
    "30-marketing-story-craft": [f"{REFS}/30-marketing-story-craft.md"],
    "03-screenplay": [f"{REFS}/03-screenplay.md"],
    "10-evidence": [f"{REFS}/10-evidence.md"],
    "06-shots": [f"{REFS}/06-shots.md"],
    "25-reference-video-analysis": [f"{REFS}/25-reference-video-analysis.md"],
    "13-ideation-brand": [f"{REFS}/13-ideation-brand.md"],
    "08-animation": [f"{REFS}/08a-motion-craft.md"],
    "09-edit": [f"{REFS}/09a-short-form-edit-recipes.md"],
    "19-brand-product-integration": [f"{REFS}/19a-product-promo-formulas.md"],
    "23-finishing-platform": [f"{REFS}/23a-captions-layout.md"],
    "11-ai-handoff": [f"{REFS}/11a-ai-video-prompting.md"],
    "29-reference-driven-production": [f"{REFS}/29a-template-recreation.md"],
    "storytelling-with-still-images": ["storytelling-with-still-images/references/still-motion-recipes.md"],
}

FORBIDDEN_LITERALS = ("openmotion_media_use", "openmotion_assets_use", "npx hyperframes", "hyperframes render")
FORBIDDEN_PATTERN = re.compile(r"\bopenmotion_[a-z_]+_use\b")
LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def source_line(row: dict) -> str:
    return f"출처: {row['repo']}@{row['commit'][:12]} {row['slug']}"


def license_copy_name(repo: str, suffix: str = "LICENSE") -> str:
    return f"{repo.replace('/', '-')}-{suffix}.txt"


def target_files(target: str, root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for pattern in TARGET_PATHS[target]:
        files.extend(sorted(root.glob(pattern)) if "*" in pattern else [root / pattern])
    return [path for path in files if path.is_file()]


def all_target_files(root: Path = ROOT) -> list[Path]:
    return sorted({path for target in TARGET_PATHS for path in target_files(target, root)})


def missing_source_lines(rows: list[dict], root: Path = ROOT) -> list[str]:
    missing = []
    for row in rows:
        if row["status"] != "absorbed":
            continue
        line = source_line(row)
        texts = [path.read_text(encoding="utf-8") for path in target_files(row["target"], root)]
        if not any(line in text.splitlines() for text in texts):
            missing.append(row["slug"])
    return missing


STYLE_TARGET = "33-motion-style-library"
STYLE_INDEX = "33-motion-style-library.md"


def missing_style_links(rows: list[dict], root: Path = ROOT) -> list[str]:
    """Absorbed style rows without a `#od-<slug>` index link whose family file holds that anchor.

    A style written as a section of the index itself counts through its in-file `{#od-<slug>}` anchor.
    """
    references = root / REFS
    index_text = (references / STYLE_INDEX).read_text(encoding="utf-8")
    missing = []
    for row in rows:
        if row["status"] != "absorbed" or row["target"] != STYLE_TARGET:
            continue
        anchor = f"od-{row['slug']}"
        if f"{{#{anchor}}}" in index_text:
            continue
        linked = [
            target.split("#", 1)[0]
            for target in LINK_PATTERN.findall(index_text)
            if target.endswith(f"#{anchor}") and target.startswith("motion-styles/")
        ]
        family_text = (references / linked[0]).read_text(encoding="utf-8") if linked and (references / linked[0]).is_file() else ""
        if f"{{#{anchor}}}" not in family_text:
            missing.append(row["slug"])
    return missing


def absorb_rows() -> list[dict]:
    return [row for row in read_ledger(LEDGER_PATH) if row["decision"] == "absorb"]


def test_target_paths_cover_every_absorb_target():
    assert {row["target"] for row in absorb_rows()} <= set(TARGET_PATHS)


def test_absorbed_rows_have_source_line():
    assert missing_source_lines(read_ledger(LEDGER_PATH)) == []


def test_provenance_lists_every_absorb_repo():
    provenance = PROVENANCE.read_text(encoding="utf-8")
    table_rows = [line for line in provenance.splitlines() if line.startswith("|")]
    rows = absorb_rows()
    assert rows
    for row in rows:
        repo_url = f"https://github.com/{row['repo']}"
        assert any(repo_url in line and row["commit"] in line for line in table_rows), f"{row['repo']}@{row['commit']}"
        assert any(f"`{row['slug']}`" in line and row["sha256"] in line for line in table_rows), row["slug"]
        license_copy = UPSTREAM / license_copy_name(row["repo"])
        assert license_copy.is_file(), license_copy.name
        text = license_copy.read_bytes().decode("utf-8")
        assert detect_license(text) == row["upstream_license"], license_copy.name
        license_sha256 = hashlib.sha256(license_copy.read_bytes()).hexdigest()
        assert any(
            repo_url in line and row["commit"] in line and license_copy.name in line and license_sha256 in line
            for line in table_rows
        ), license_copy.name


def test_no_engine_calls_in_absorbed_files():
    for path in all_target_files():
        text = path.read_text(encoding="utf-8")
        for literal in FORBIDDEN_LITERALS:
            assert literal not in text, f"{path.name}: {literal}"
        assert not FORBIDDEN_PATTERN.search(text), path.name


def test_absorbed_files_links_resolve():
    for path in all_target_files():
        for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            assert (path.parent / target.split("#", 1)[0]).is_file(), f"{path.name}: {target}"


def test_style_index_links_every_style():
    assert missing_style_links(read_ledger(LEDGER_PATH)) == []


def test_detects_corruption(tmp_path):
    rows = read_ledger(LEDGER_PATH)
    row = next(item for item in rows if item["decision"] == "absorb" and item["target"] == "08-animation")
    target_dir = tmp_path / REFS
    target_dir.mkdir(parents=True)
    target_file = target_dir / "08a-motion-craft.md"
    target_file.write_text(f"### 제목 {{#od-{row['slug']}}}\n- 쓰는 곳: 시험\n{source_line(row)}\n", encoding="utf-8")
    ledger_copy = tmp_path / "ledger.csv"
    write_ledger(ledger_copy, [row])

    corrupted = read_ledger(ledger_copy)
    next(item for item in corrupted if item["slug"] == row["slug"])["status"] = "absorbed"
    assert missing_source_lines(corrupted, tmp_path) == []

    target_file.write_text(f"### 제목 {{#od-{row['slug']}}}\n- 쓰는 곳: 시험\n", encoding="utf-8")
    assert missing_source_lines(corrupted, tmp_path) == [row["slug"]]


def test_style_index_detects_missing_link(tmp_path):
    rows = [row for row in read_ledger(LEDGER_PATH) if row["target"] == STYLE_TARGET and row["status"] == "absorbed"]
    row = next(item for item in rows if item["slug"] != "openmotion-design-styles")
    anchor = f"od-{row['slug']}"
    styles_dir = tmp_path / REFS / "motion-styles"
    styles_dir.mkdir(parents=True)
    (styles_dir / "kinetic-type.md").write_text(f"### 제목 {{#{anchor}}}\n", encoding="utf-8")
    index_file = tmp_path / REFS / STYLE_INDEX
    index_file.write_text(f"- [제목](motion-styles/kinetic-type.md#{anchor}) — 요약\n", encoding="utf-8")
    assert missing_style_links([row], tmp_path) == []

    index_file.write_text("- 제목 — 요약\n", encoding="utf-8")
    assert missing_style_links([row], tmp_path) == [row["slug"]]

    index_file.write_text(f"- [제목](motion-styles/kinetic-type.md#{anchor}) — 요약\n", encoding="utf-8")
    (styles_dir / "kinetic-type.md").write_text("### 제목\n", encoding="utf-8")
    assert missing_style_links([row], tmp_path) == [row["slug"]]
