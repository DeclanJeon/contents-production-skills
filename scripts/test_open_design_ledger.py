"""Tests for scripts/open_design_ledger.py. Pure functions plus the committed ledger; no network."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import open_design_ledger  # noqa: E402
from open_design_ledger import (  # noqa: E402
    LEDGER_COLUMNS,
    AbsorbedRowMismatchError,
    FetchResult,
    IndeterminateFetchError,
    decide,
    detect_license,
    main,
    parse_source,
    raw_url,
    read_ledger,
    refresh,
    write_ledger,
)

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


def test_detect_license_rejects_lookalikes():
    assert detect_license("MIT-0 License\n\nCopyright") is None
    assert detect_license("MIT No Attribution\n") is None
    assert detect_license("                                 Apache License\n Version 1.1\n") is None
    assert detect_license("Apache License\n") is None
    assert detect_license("Apache License\n Version 2.0, January 2004\n") == "Apache-2.0"


def test_detect_license_requires_complete_apache_version_line():
    assert detect_license("                                 Apache License\n                           Version 2.0, January 2004\n") == "Apache-2.0"
    assert detect_license("Apache License\n  Version   2.0  \n") == "Apache-2.0"
    assert detect_license("Apache License\nVersion 2.0 (Non-Commercial)\n") is None
    assert detect_license("Apache License\nVersion 2.0.1\n") is None


def test_cached_download_removes_temporary_file_when_replace_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(open_design_ledger, "_download", lambda url: (200, b"body"))

    def fail_replace(source, destination):
        raise OSError("replace failed")

    monkeypatch.setattr(open_design_ledger.os, "replace", fail_replace)
    destination = tmp_path / "repo" / "LICENSE"
    with pytest.raises(OSError):
        open_design_ledger._cached_download("https://example.invalid/LICENSE", destination)
    assert list(destination.parent.iterdir()) == []


def test_decide_requires_allowlisted_license():
    out = decide(absorb_row(), FetchResult(200, "h", "GPL-3.0"))
    assert out["decision"] == "exclude"
    assert "no upstream LICENSE" in out["reason"]
    assert out["status"] == "n/a"


def test_decide_rejects_indeterminate_status():
    with pytest.raises(IndeterminateFetchError):
        decide(absorb_row(), FetchResult(503, None, None))


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


MIT_TEXT = b"MIT License\n\nCopyright (c) x\n"
SKILL_TEXT = b"# skill\n"
REPO = "o/r"
SKILL_SOURCE = f"https://github.com/{REPO}/blob/main/skills/x/SKILL.md"


def ledger_row(**overrides) -> dict:
    row = {column: "" for column in LEDGER_COLUMNS}
    row.update(slug="x", name="x", repo=REPO, license="MIT", decision="absorb", target="08-animation",
               reason="craft", source=SKILL_SOURCE, status="planned")
    row.update(overrides)
    return row


def stub_network(monkeypatch, responses: dict[str, tuple[int, bytes]], commit: str = PINNED) -> None:
    monkeypatch.setattr(open_design_ledger, "resolve_commit", lambda repo, ref: commit)

    def fake_download(url: str) -> tuple[int, bytes]:
        return responses.get(url.rsplit("/", 1)[-1], (404, b""))

    monkeypatch.setattr(open_design_ledger, "_download", fake_download)


def test_refresh_transient_skill_failure_aborts_without_rewrite(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [ledger_row()])
    before = ledger.read_text(encoding="utf-8")
    stub_network(monkeypatch, {"SKILL.md": (503, b""), "LICENSE": (200, MIT_TEXT)})
    with pytest.raises(IndeterminateFetchError):
        refresh(ledger, tmp_path / "cache")
    assert ledger.read_text(encoding="utf-8") == before
    assert main(["refresh", "--ledger", str(ledger), "--cache", str(tmp_path / "cache")]) == 2
    assert ledger.read_text(encoding="utf-8") == before


def test_refresh_transient_license_failure_aborts_without_rewrite(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [ledger_row()])
    before = ledger.read_text(encoding="utf-8")
    stub_network(monkeypatch, {"SKILL.md": (200, SKILL_TEXT), "LICENSE": (500, b"")})
    with pytest.raises(IndeterminateFetchError):
        refresh(ledger, tmp_path / "cache")
    assert ledger.read_text(encoding="utf-8") == before


def test_refresh_network_error_aborts(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [ledger_row()])
    stub_network(monkeypatch, {"SKILL.md": (0, b"")})
    with pytest.raises(IndeterminateFetchError):
        refresh(ledger, tmp_path / "cache")


def test_refresh_confirmed_absence_excludes(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [ledger_row(slug="gone"), ledger_row(slug="nolicense", source=SKILL_SOURCE)])
    stub_network(monkeypatch, {"SKILL.md": (200, SKILL_TEXT)})
    rows = {row["slug"]: row for row in refresh(ledger, tmp_path / "cache")}
    assert rows["gone"]["decision"] == "exclude"
    assert "no upstream LICENSE" in rows["gone"]["reason"]
    stub_network(monkeypatch, {})
    write_ledger(ledger, [ledger_row(slug="gone")])
    assert refresh(ledger, tmp_path / "cache2")[0]["reason"] == "source unavailable"


def absorbed_row() -> dict:
    return ledger_row(
        source=f"https://github.com/{REPO}/blob/{PINNED}/skills/x/SKILL.md", commit=PINNED,
        sha256=hashlib.sha256(SKILL_TEXT).hexdigest(), upstream_license="MIT", status="absorbed",
    )


def test_refresh_preserves_absorbed_when_pin_and_hash_unchanged(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [absorbed_row()])
    stub_network(monkeypatch, {"SKILL.md": (200, SKILL_TEXT), "LICENSE": (200, MIT_TEXT)})
    rows = refresh(ledger, tmp_path / "cache")
    assert rows[0]["status"] == "absorbed"
    assert read_ledger(ledger)[0]["status"] == "absorbed"


def test_refresh_fails_loudly_when_absorbed_row_changes(tmp_path, monkeypatch, capsys):
    ledger = tmp_path / "ledger.csv"
    write_ledger(ledger, [absorbed_row()])
    before = ledger.read_text(encoding="utf-8")
    stub_network(monkeypatch, {"SKILL.md": (200, b"# changed\n"), "LICENSE": (200, MIT_TEXT)})
    with pytest.raises(AbsorbedRowMismatchError) as caught:
        refresh(ledger, tmp_path / "cache")
    assert caught.value.slugs == ["x"]
    assert ledger.read_text(encoding="utf-8") == before
    assert main(["refresh", "--ledger", str(ledger), "--cache", str(tmp_path / "cache2")]) == 1
    assert "x" in capsys.readouterr().err
