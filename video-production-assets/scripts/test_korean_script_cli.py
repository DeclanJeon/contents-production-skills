"""Subprocess contract: JSON outcomes and no input writes."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_korean_script_postediting import packet

CLI = Path(__file__).with_name("korean_script_postediting.py")


@pytest.mark.parametrize("exit_code", [0, 1, 2, 3])
def test_cli_read_only_exit_codes(tmp_path, exit_code):
    before = "정말 고마워."
    after = {0: before, 1: "정말 고마워!", 2: "전부 다른 문장", 3: before}[exit_code]
    data = packet(before)
    data["units"][0].update(after=after, reason="표현 교정")
    if exit_code == 3:
        data["source_sha256"] = "0" * 64
    contents = {"source.md": before.encode(), "candidate.md": after.encode(),
                "packet.json": json.dumps(data, ensure_ascii=False).encode()}
    for name, value in contents.items():
        (tmp_path / name).write_bytes(value)
    run = subprocess.run([sys.executable, str(CLI), "--source", "source.md",
                          "--candidate", "candidate.md", "--packet", "packet.json"],
                         cwd=tmp_path, capture_output=True, text=True, check=False)
    assert run.returncode == exit_code, run.stdout + run.stderr
    assert json.loads(run.stdout)["exit_code"] == exit_code
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == contents


@pytest.mark.parametrize("mode", ["missing", "json", "utf8", "schema", "arguments"])
def test_cli_malformed_input_returns_json_3(tmp_path, mode):
    source = tmp_path / "source.md"
    candidate = tmp_path / "candidate.md"
    scope = tmp_path / "packet.json"
    source.write_bytes(b"abc")
    candidate.write_bytes(b"abc")
    data = packet("abc")
    if mode == "schema":
        data["schema"] = "unsupported"
    scope.write_text(json.dumps(data), encoding="utf-8")
    if mode == "missing":
        source = tmp_path / "absent"
    if mode == "json":
        scope.write_bytes(b"{")
    if mode == "utf8":
        source.write_bytes(b"\xff")
    args = ["--source", str(source), "--candidate", str(candidate), "--packet", str(scope)]
    if mode == "arguments":
        args = []
    run = subprocess.run([sys.executable, str(CLI), *args], capture_output=True, text=True, check=False)
    assert run.returncode == 3
    assert json.loads(run.stdout)["exit_code"] == 3


def test_cli_json_works_with_ascii_stdout(tmp_path):
    source = tmp_path / "source.md"
    source.write_bytes("안녕".encode())
    scope = tmp_path / "scope.json"
    scope.write_text(json.dumps(packet("안녕")), encoding="utf-8")
    run = subprocess.run([sys.executable, str(CLI), "--source", str(source),
                          "--candidate", str(source), "--packet", str(scope)],
                         env={**os.environ, "PYTHONIOENCODING": "ascii"},
                         capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout)["scope"] == ["S01/SP01"]


def test_help_does_not_need_files():
    run = subprocess.run([sys.executable, str(CLI), "--help"], capture_output=True, text=True, check=False)
    assert run.returncode == 0 and "--source" in run.stdout


@pytest.mark.parametrize("malformation", ["surrogate", "duplicate", "nonfinite"])
def test_cli_rejects_ambiguous_json_or_invalid_unicode(tmp_path, malformation):
    source = tmp_path / "source.md"
    source.write_bytes(b"abc")
    data = packet("abc")
    if malformation == "surrogate":
        data["units"][0]["locator"] = "\ud800"
    raw = json.dumps(data)
    if malformation == "duplicate":
        raw = raw.replace('"editable": true', '"editable": false, "editable": true')
    if malformation == "nonfinite":
        raw = raw.replace('"start": 0', '"start": 0, "unknown": NaN')
    scope = tmp_path / "scope.json"
    scope.write_text(raw, encoding="utf-8")
    run = subprocess.run([sys.executable, str(CLI), "--source", str(source), "--candidate",
                          str(source), "--packet", str(scope)], capture_output=True,
                         text=True, check=False)
    assert run.returncode == 3, run.stdout + run.stderr
    assert json.loads(run.stdout)["exit_code"] == 3
