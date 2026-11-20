"""Tests for scripts/open_design_ledger.py. Pure functions plus the committed ledger; no network."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from open_design_ledger import FetchResult, decide, detect_license, parse_source, raw_url  # noqa: E402

LEDGER = Path(__file__).resolve().parents[1] / "docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv"
PINNED = "709b10fd9ac5e33f996e035361cbb365d7ff79ae"
SKILL_PATH = "library/skills/openmotion-ad-script/SKILL.md"


def absorb_row() -> dict:
    return {"slug": "x", "decision": "absorb", "target": "08-animation", "reason": "craft",
            "commit": PINNED, "sha256": "", "upstream_license": "", "status": ""}


def test_parse_pinned_and_main():
    ref = parse_source(f"https://github.com/nexu-io/openmotion/blob/{PINNED}/{SKILL_PATH}")
    assert (ref.repo, ref.ref, ref.path) == ("nexu-io/openmotion", PINNED, SKILL_PATH)
    assert len(ref.ref) == 40
    main = parse_source("https://github.com/o/r/blob/main/skills/x/SKILL.md")
    assert (main.repo, main.ref, main.path) == ("o/r", "main", "skills/x/SKILL.md")


def test_raw_url():
    ref = parse_source(f"https://github.com/nexu-io/openmotion/blob/{PINNED}/{SKILL_PATH}")
    assert raw_url(ref, "abc") == f"https://raw.githubusercontent.com/nexu-io/openmotion/abc/{SKILL_PATH}"


def test_unavailable_source_becomes_exclude():
    out = decide(absorb_row(), FetchResult(404, None, None))
    assert out["decision"] == "exclude"
    assert out["reason"] == "source unavailable"
    assert out["status"] == "n/a"


def test_license_must_match_repo_file():
    out = decide(absorb_row(), FetchResult(200, "h", None))
    assert out["decision"] == "exclude"
    assert "no upstream LICENSE" in out["reason"]
    ok = decide(absorb_row(), FetchResult(200, "h", "MIT"))
    assert ok["decision"] == "absorb"
    assert ok["status"] == "planned"
    assert ok["sha256"] == "h"
    assert ok["upstream_license"] == "MIT"


def test_detect_license_first_line():
    assert detect_license("MIT License\n\nCopyright") == "MIT"
    assert detect_license("\nThe MIT License (MIT)\n") == "MIT"
    assert detect_license("                                 Apache License\n Version 2.0") == "Apache-2.0"
    assert detect_license("GNU GENERAL PUBLIC LICENSE\n") is None
    assert detect_license("") is None


def test_non_absorb_rows_are_untouched_by_decide():
    row = {"decision": "out_of_scope", "reason": "r", "status": ""}
    out = decide(row, FetchResult(404, None, None))
    assert out["decision"] == "out_of_scope"
    assert out["status"] == "n/a"
    assert out["reason"] == "r"


def test_ledger_vocabulary():
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    for row in rows:
        assert row["decision"] in {"absorb", "exclude", "out_of_scope"}, row["slug"]
        assert row["status"] in {"planned", "absorbed", "n/a"}, row["slug"]
        assert (row["decision"] == "absorb") == (row["status"] in {"planned", "absorbed"}), row["slug"]
        if row["decision"] == "absorb":
            assert row["upstream_license"] in {"MIT", "Apache-2.0"}, row["slug"]
            assert len(row["commit"]) == 40, row["slug"]
