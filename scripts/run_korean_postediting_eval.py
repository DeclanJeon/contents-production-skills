# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# python3 scripts/run_korean_postediting_eval.py prepare --output <new-directory>
"""Prepare frozen A/B plans or collect supplied captures. Never calls a model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Final, Literal, assert_never

from korean_postediting_capture import CaptureInput, check_path, collect_capture, relative_name
from korean_postediting_eval import EvalError, Profile, build_batch, load_cases, mapping, parse_json, render_batch

ROOT: Final = Path(__file__).resolve().parents[1]


class Inputs(argparse.Namespace):
    operation: Literal["prepare", "collect"]
    output: Path
    suite: Path
    source_root: Path
    provider: str | None
    model: str | None
    thinking: str
    case_ids: list[str] | None
    run_dir: Path
    job: str
    wire: Path
    stderr: Path | None
    exit_code: int


def save_new_bundle(output: Path, files: dict[str, str | bytes]) -> None:
    """Preflight all names and links; preserve existing files and inputs."""
    check_path(output)
    if output.exists():
        raise EvalError("output already exists; choose a new directory")
    paths = {relative_name(name) for name in files}
    if not paths or len(paths) != len(files):
        raise EvalError("empty bundle or normalized path collision")
    if any(parent in paths for path in paths for parent in path.parents):
        raise EvalError("file/directory collision inside bundle")
    output.mkdir(parents=True, mode=0o700)
    for name, value in files.items():
        target = output / relative_name(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = value.encode("utf-8") if isinstance(value, str) else value
        with target.open("xb") as stream:
            _ = stream.write(data)


def prepare(args: Inputs) -> int:
    cases = load_cases(args.suite.read_bytes())
    if args.case_ids:
        if len(set(args.case_ids)) != len(args.case_ids):
            raise EvalError("duplicate case selection")
        chosen = {c.id for c in cases}.intersection(args.case_ids)
        if chosen != set(args.case_ids):
            raise EvalError("unknown case ID")
        cases = tuple(c for c in cases if c.id in chosen)
    refs = args.source_root / "video-production-assets/references"
    guides = tuple((refs / name).read_bytes().decode("utf-8") for name in
                   ("korean-script-postediting.md", "korean-script-postediting-patterns.md"))
    batch = build_batch(cases, (guides[0], guides[1]), Profile(args.provider, args.model, args.thinking))
    rendered = render_batch(batch)
    # dict is intentionally widened at this I/O boundary; all content was rendered before any write.
    files: dict[str, str | bytes] = dict(rendered)
    save_new_bundle(args.output, files)
    print(json.dumps({"status": "prepared", "planned_invocations": len(batch.jobs),
                      "model_calls": 0, "output": str(args.output), "default_application": "held"}))
    return 0


def collect(args: Inputs) -> int:
    sample = CaptureInput(args.job, args.wire.read_bytes(),
                          args.stderr.read_bytes() if args.stderr else b"", args.exit_code)
    files = collect_capture(args.run_dir, sample)
    record = mapping(parse_json(files["attempt.json"].encode() if isinstance(files["attempt.json"], str)
                                else files["attempt.json"]))
    save_new_bundle(args.output, files)
    print(json.dumps({"status": record["status"], "verdict": "UNREVIEWED", "model_calls": 0,
                      "output": str(args.output), "default_application": "held"}))
    return int(record["status"] != "completed")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="operation", required=True)
    prep = sub.add_parser("prepare", allow_abbrev=False)
    _ = prep.add_argument("--output", type=Path, required=True)
    _ = prep.add_argument("--suite", type=Path, default=ROOT / "qa/korean-script-postediting-cases.json")
    _ = prep.add_argument("--source-root", type=Path, default=ROOT)
    _ = prep.add_argument("--case", dest="case_ids", action="append")
    _ = prep.add_argument("--provider")
    _ = prep.add_argument("--model")
    _ = prep.add_argument("--thinking", default="low")
    coll = sub.add_parser("collect", allow_abbrev=False)
    _ = coll.add_argument("--run-dir", type=Path, required=True)
    _ = coll.add_argument("--job", required=True)
    _ = coll.add_argument("--wire", type=Path, required=True)
    _ = coll.add_argument("--stderr", type=Path)
    _ = coll.add_argument("--exit-code", type=int, required=True)
    _ = coll.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv, namespace=Inputs())
    try:
        match args.operation:
            case "prepare":
                return prepare(args)
            case "collect":
                return collect(args)
            case invalid:
                assert_never(invalid)
    except (EvalError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "input_error", "reason": str(exc)}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
