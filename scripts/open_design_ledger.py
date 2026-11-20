#!/usr/bin/env python3
"""Pin open-design absorption sources and verify upstream licenses.

`refresh` reads the absorption ledger, resolves each absorb row to a commit,
downloads the upstream SKILL.md into the git-ignored cache, hashes it, checks
the repository-root LICENSE, and rewrites the ledger.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parents[1] / "docs/superpowers/specs/2026-11-20-open-design-absorption-ledger.csv"
LEDGER_COLUMNS = [
    "slug", "name", "repo", "license", "decision", "target", "reason", "source",
    "commit", "sha256", "upstream_license", "status",
]
LICENSE_FILENAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt")
SOURCE_PATTERN = re.compile(r"^https://github\.com/([^/]+/[^/]+)/blob/([^/]+)/(.+)$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_LICENSES = {"MIT", "Apache-2.0"}
MIT_HEADING = re.compile(r"^(the\s+)?mit\s+license(\s*\(mit\))?$", re.IGNORECASE)
APACHE_HEADING = re.compile(r"^apache\s+license$", re.IGNORECASE)
APACHE_VERSION = re.compile(r"^version\s+2\.0\b", re.IGNORECASE)


class IndeterminateFetchError(RuntimeError):
    """A fetch failed in a way that does not confirm absence (5xx, rate limit, network error)."""


class AbsorbedRowMismatchError(RuntimeError):
    """Absorbed rows whose upstream commit or sha256 changed; completed provenance must be reviewed."""

    def __init__(self, slugs: list[str]):
        super().__init__("absorbed rows changed upstream: " + ", ".join(slugs))
        self.slugs = slugs


@dataclass(frozen=True)
class SourceRef:
    repo: str
    ref: str
    path: str


@dataclass(frozen=True)
class FetchResult:
    status: int
    sha256: str | None
    license_id: str | None


def parse_source(url: str) -> SourceRef:
    match = SOURCE_PATTERN.match(url)
    if not match:
        raise ValueError(f"unsupported source url: {url}")
    return SourceRef(repo=match.group(1), ref=match.group(2), path=match.group(3))


def resolve_commit(repo: str, ref: str) -> str:
    if COMMIT_PATTERN.match(ref):
        return ref
    output = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{repo}", ref],
        check=True, capture_output=True, text=True, timeout=60,
    ).stdout
    lines = [line.split("\t") for line in output.splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"ref not found: {repo}@{ref}")
    preferred = [parts for parts in lines if parts[1] in (f"refs/heads/{ref}", f"refs/tags/{ref}")]
    return (preferred or lines)[0][0]


def raw_url(ref: SourceRef, commit: str) -> str:
    return f"https://raw.githubusercontent.com/{ref.repo}/{commit}/{ref.path}"


def detect_license(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    if MIT_HEADING.match(lines[0]):
        return "MIT"
    if APACHE_HEADING.match(lines[0]) and any(APACHE_VERSION.match(line) for line in lines[1:3]):
        return "Apache-2.0"
    return None


def decide(row: dict, fetched: FetchResult) -> dict:
    updated = dict(row)
    if updated.get("decision") != "absorb":
        updated["status"] = "n/a"
        return updated
    if fetched.status not in (200, 404):
        raise IndeterminateFetchError(f"{updated.get('slug', '?')}: source fetch status {fetched.status}")
    if fetched.status == 404:
        updated.update(decision="exclude", reason="source unavailable", status="n/a")
    elif fetched.license_id not in ALLOWED_LICENSES:
        updated.update(
            decision="exclude",
            reason="no upstream LICENSE (MIT or Apache-2.0) at repository root",
            status="n/a",
        )
    else:
        updated.update(
            status="planned",
            sha256=fetched.sha256,
            upstream_license=fetched.license_id,
            license=fetched.license_id,
        )
    return updated


def _download(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "open-design-ledger"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except urllib.error.URLError:
        return 0, b""


def _cached_download(url: str, destination: Path) -> tuple[int, bytes]:
    if destination.is_file():
        return 200, destination.read_bytes()
    status, body = _download(url)
    if status == 200:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as temporary:
            temporary.write(body)
        os.replace(temporary.name, destination)
    return status, body


def fetch_license(repo: str, commit: str, cache: Path) -> str | None:
    for filename in LICENSE_FILENAMES:
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{filename}"
        status, body = _cached_download(url, cache / repo / commit / filename)
        if status == 200:
            return detect_license(body.decode("utf-8", errors="replace"))
        if status != 404:
            raise IndeterminateFetchError(f"{repo}@{commit}: {filename} fetch status {status}")
    return None


def fetch(ref: SourceRef, commit: str, cache: Path) -> FetchResult:
    status, body = _cached_download(raw_url(ref, commit), cache / ref.repo / commit / ref.path)
    if status == 404:
        return FetchResult(404, None, None)
    if status != 200:
        raise IndeterminateFetchError(f"{ref.repo}@{commit}: {ref.path} fetch status {status}")
    return FetchResult(200, hashlib.sha256(body).hexdigest(), fetch_license(ref.repo, commit, cache))


def read_ledger(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{column: row.get(column) or "" for column in LEDGER_COLUMNS} for row in csv.DictReader(handle)]


def write_ledger(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def refresh(ledger: Path, cache: Path) -> list[dict]:
    rows = read_ledger(ledger)
    absorb_rows = [row for row in rows if row["decision"] == "absorb"]
    original_sources = {row["slug"]: row["source"] for row in absorb_rows}
    previous = {row["slug"]: (row["commit"], row["sha256"]) for row in absorb_rows}
    mismatched: list[str] = []
    refs = {row["slug"]: parse_source(row["source"]) for row in absorb_rows}
    resolved = {(ref.repo, ref.ref): None for ref in refs.values()}
    for repo, ref in resolved:
        resolved[(repo, ref)] = resolve_commit(repo, ref)

    def work(row: dict) -> dict:
        source_ref = refs[row["slug"]]
        commit = resolved[(source_ref.repo, source_ref.ref)]
        row = {**row, "commit": commit}
        if source_ref.ref != commit:
            row["source"] = f"https://github.com/{source_ref.repo}/blob/{commit}/{source_ref.path}"
        decided_row = decide(row, fetch(source_ref, commit, cache))
        if decided_row["decision"] != "absorb":
            decided_row.update(commit="", source=original_sources[row["slug"]])
        if row["status"] == "absorbed":
            unchanged = (
                decided_row["decision"] == "absorb"
                and decided_row["commit"] == previous[row["slug"]][0]
                and decided_row["sha256"] == previous[row["slug"]][1]
            )
            if not unchanged:
                mismatched.append(row["slug"])
            return {**decided_row, "status": "absorbed"} if unchanged else row
        return decided_row

    with ThreadPoolExecutor(max_workers=8) as pool:
        decided = dict(zip((row["slug"] for row in absorb_rows), pool.map(work, absorb_rows)))
    if mismatched:
        raise AbsorbedRowMismatchError(sorted(mismatched))
    result = [decided.get(row["slug"]) or decide(row, FetchResult(0, None, None)) for row in rows]
    write_ledger(ledger, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    refresh_parser = sub.add_parser("refresh", help="pin commits, hash sources, verify licenses (network)")
    refresh_parser.add_argument("--cache", type=Path, default=Path(".cache/open-design"))
    refresh_parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    args = parser.parse_args(argv)
    try:
        rows = refresh(args.ledger, args.cache)
    except IndeterminateFetchError as error:
        print(f"refresh aborted, ledger not rewritten (transient fetch failure): {error}", file=sys.stderr)
        return 2
    except AbsorbedRowMismatchError as error:
        print(f"refresh aborted, ledger not rewritten: {error}", file=sys.stderr)
        return 1
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["decision"]] = counts.get(row["decision"], 0) + 1
    print(counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
