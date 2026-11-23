#!/usr/bin/env python3
"""Build and verify the Prompt Motion absorption ledger.

The archive (``prompts.csv`` + ``gifs/``) stays outside this repository. This
script reads it, writes a ledger with keys, hashes, duplicate groups and
evidence levels, merges the hand coding from ``docs/research/prompt-motion-coding.csv``
and never writes prompt text.

Usage::

    python3 scripts/prompt_motion_ledger.py build ARCHIVE_DIR
    python3 scripts/prompt_motion_ledger.py groups ARCHIVE_DIR      # representative keys to code
    python3 scripts/prompt_motion_ledger.py verify ARCHIVE_DIR      # snapshot hash + copy check

Exit codes: 0 ok, 1 verification problems, 2 unusable input.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "research" / "prompt-motion-absorption-ledger.csv"
CODING = ROOT / "docs" / "research" / "prompt-motion-coding.csv"
SNAPSHOT_SHA256 = "1bc3b16ebdf61d3176bcaaf9ddb9dc6c2157bbd33b9fae13d5cff7d789f55e8e"
FIELDS = ["entry_id", "variant", "page_url", "tags", "prompt_sha256", "dup_group", "format",
          "techniques", "evidence", "disposition", "target", "reason", "visual_check"]
CODED = ["format", "techniques", "disposition", "target", "reason", "visual_check"]
EVIDENCE = {"tested_default_example": "tested", "template_default_example": "tested",
            "original_example": "original_example", "template_tested_no_item_example": "template_tested",
            "untested_no_example": "untested", "skill_example": "skill"}
WORD_RUN = 8
HANGUL_RUN = 20
WORD = re.compile(r"[A-Za-z0-9']+")
HANGUL = re.compile(r"[\uac00-\ud7a3]")


def normalized_sha(text: str) -> str:
    return hashlib.sha256(" ".join(text.lower().split()).encode()).hexdigest()


def read_archive(archive: Path) -> list[dict[str, str]]:
    path = archive / "prompts.csv"
    if not path.is_file():
        raise SystemExit(2)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def key(row: dict[str, str]) -> str:
    return f"{row['entry_id']}:{row['variant']}"


def base_rows(archive: Path) -> list[dict[str, str]]:
    first: dict[str, str] = {}
    out = []
    for row in read_archive(archive):
        digest = normalized_sha(row["prompt"]) if row["prompt"].strip() else ""
        group = first.setdefault(digest, key(row)) if digest else key(row)
        out.append({"entry_id": row["entry_id"], "variant": row["variant"],
                    "page_url": row["page_url"] or row["gallery_url"], "tags": row["tags"],
                    "prompt_sha256": digest, "dup_group": group,
                    "evidence": EVIDENCE[row["example_status"]]})
    return out


def read_coding() -> dict[str, dict[str, str]]:
    with CODING.open(encoding="utf-8", newline="") as handle:
        return {row["dup_group"]: row for row in csv.DictReader(handle)}


def build(archive: Path) -> int:
    coding = read_coding()
    rows = base_rows(archive)
    missing = sorted({r["dup_group"] for r in rows} - set(coding))
    extra = sorted(set(coding) - {r["dup_group"] for r in rows})
    if missing or extra:
        print(json.dumps({"missing_coding": missing[:20], "missing_count": len(missing), "unknown": extra}))
        return 1
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            code = coding[row["dup_group"]]
            merged = {**row, **{field: code[field] for field in CODED}}
            if merged["dup_group"] != f"{row['entry_id']}:{row['variant']}" and merged["disposition"] == "absorb":
                merged["disposition"] = "reference"
                merged["target"] = ""
                merged["reason"] = f"{merged['dup_group']}와 같은 본문"
            writer.writerow({field: merged[field] for field in FIELDS})
    print(json.dumps({"ledger": str(LEDGER.relative_to(ROOT)), "rows": len(rows)}))
    return 0


def groups(archive: Path) -> int:
    seen = set()
    for row in base_rows(archive):
        if row["dup_group"] not in seen:
            seen.add(row["dup_group"])
            print(row["dup_group"])
    return 0


def shingles(text: str) -> tuple[set[tuple[str, ...]], set[str]]:
    words = [w.lower() for w in WORD.findall(text)]
    runs = {tuple(words[i:i + WORD_RUN]) for i in range(len(words) - WORD_RUN + 1)
            if sum(w.isalpha() for w in words[i:i + WORD_RUN]) >= WORD_RUN - 2}
    compact = "".join(text.split())
    hangul = {compact[i:i + HANGUL_RUN] for i in range(len(compact) - HANGUL_RUN + 1)
              if len(HANGUL.findall(compact[i:i + HANGUL_RUN])) >= HANGUL_RUN // 2}
    return runs, hangul


def verify(archive: Path) -> int:
    problems = []
    digest = hashlib.sha256((archive / "prompts.csv").read_bytes()).hexdigest()
    if digest != SNAPSHOT_SHA256:
        problems.append(f"snapshot hash {digest} != {SNAPSHOT_SHA256}")
    source_words: set[tuple[str, ...]] = set()
    source_hangul: set[str] = set()
    for row in read_archive(archive):
        for text in (row["prompt"], row["site_translation"]):
            words, hangul = shingles(text)
            source_words |= words
            source_hangul |= hangul
    skills = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["skills"]
    for name in skills:
        for path in sorted(p for p in (ROOT / name).rglob("*.md") if "support" not in p.relative_to(ROOT).parts):
            words, hangul = shingles(path.read_text(encoding="utf-8"))
            for hit in sorted(words & source_words)[:3]:
                problems.append(f"{path.relative_to(ROOT)}: copied words {' '.join(hit)!r}")
            for hit in sorted(hangul & source_hangul)[:3]:
                problems.append(f"{path.relative_to(ROOT)}: copied text {hit!r}")
    for line in problems:
        print(line)
    print(json.dumps({"problems": len(problems)}))
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("build", "groups", "verify"))
    parser.add_argument("archive", type=Path)
    args = parser.parse_args(argv)
    return {"build": build, "groups": groups, "verify": verify}[args.command](args.archive)


if __name__ == "__main__":
    sys.exit(main())
