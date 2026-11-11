"""Offline A/B planning and CLI filesystem contracts."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

import korean_postediting_eval as ev

ROOT = Path(__file__).resolve().parents[1]


def suite_data():
    return json.loads((ROOT / "qa/korean-script-postediting-cases.json").read_bytes())


def cases():
    return ev.load_cases(json.dumps(suite_data(), ensure_ascii=False).encode())


def batch(profile=None):
    return ev.build_batch(cases(), ("UNIQUE_GUIDE", "UNIQUE_PATTERNS"),
                          profile or ev.Profile(None, None, "low"))


def test_real_suite_builds_26_jobs():
    result = batch()
    assert len(result.jobs) == 26
    assert len({job.id for job in result.jobs}) == 26
    assert result.jobs[0].condition == "baseline"
    assert result.jobs[2].condition == "postediting"
    assert ev.render_batch(result) == ev.render_batch(result)


def test_same_user_prompt_and_rubric_withheld():
    result = batch()
    for case in result.cases:
        pair = [job for job in result.jobs if job.case_id == case.id]
        assert pair[0].prompt == pair[1].prompt
        payload = json.loads(pair[0].prompt)
        assert payload == {"request": case.prompt, "source": case.source, "locked": list(case.locked)}
        assert "must_preserve" not in payload and "forbidden_actions" not in payload
    frozen = ev.render_batch(result)
    assert "UNREVIEWED" in frozen["review.md"]


def test_treatment_only_receives_guides():
    result = batch()
    assert "UNIQUE_GUIDE" not in result.baseline_system
    assert "UNIQUE_GUIDE" in result.postediting_system
    assert "UNIQUE_PATTERNS" in result.postediting_system
    assert result.postediting_system.startswith(result.baseline_system)


def test_unselected_profile_has_no_command():
    plan = json.loads(ev.render_batch(batch())["plan.json"])
    assert plan["planned_invocations"] == 26
    assert plan["execution"] == "not_run" and plan["default_application"] == "held"
    assert all(job["command"] is None for job in plan["jobs"])


def test_selected_commands_disable_all_tools():
    plan = json.loads(ev.render_batch(batch(ev.Profile("test-provider", "test-model", "low")))["plan.json"])
    for job in plan["jobs"]:
        command = job["command"]
        for flag in ("--no-tools", "--no-mcp", "--no-extensions", "--no-skills",
                     "--no-context-files", "--no-session", "--no-approve", "--offline"):
            assert flag in command
        assert command[command.index("--model") + 1] == "test-model"
        assert command[command.index("--provider") + 1] == "test-provider"


@pytest.mark.parametrize("bad", ["id", "duplicate", "source", "locked", "rubric", "schema"])
def test_suite_rejects_unsafe_duplicate_or_malformed_case(bad):
    data = suite_data()
    if bad == "id":
        data["cases"][0]["id"] = "../../escape"
    if bad == "duplicate":
        data["cases"].append(copy.deepcopy(data["cases"][0]))
    if bad == "source":
        del data["cases"][0]["source"]
    if bad == "locked":
        data["cases"][0]["locked"] = [12]
    if bad == "rubric":
        data["cases"][0]["must_preserve"] = []
    if bad == "schema":
        data["schema"] = "other"
    with pytest.raises(ev.EvalError):
        ev.load_cases(json.dumps(data).encode())


@pytest.mark.parametrize("profile", [("p", None, "low"), (None, "m", "low"), ("", "", "low"),
                                      ("p", "m", "invented")])
def test_profile_rejects_partial_or_invalid_settings(profile):
    with pytest.raises(ev.EvalError):
        ev.build_batch(cases(), ("guide", "patterns"), ev.Profile(*profile))


def test_commands_use_exact_user_payload():
    result = batch(ev.Profile("test-provider", "test-model", "low"))
    for item in json.loads(ev.render_batch(result)["plan.json"])["jobs"]:
        expected = next(job.prompt for job in result.jobs if job.id == item["id"])
        assert item["command"][-1] == expected


def test_prepare_cli_creates_only_new_output(tmp_path):
    cli = Path(__file__).with_name("run_korean_postediting_eval.py")
    destination = tmp_path / "batch"
    command = [sys.executable, str(cli), "prepare", "--output", str(destination)]
    run = subprocess.run(command, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    plan = json.loads((destination / "plan.json").read_bytes())
    assert plan["planned_invocations"] == 26 and plan["execution"] == "not_run"
    before = {str(p.relative_to(destination)): p.read_bytes() for p in destination.rglob("*") if p.is_file()}
    again = subprocess.run(command, capture_output=True, text=True, check=False)
    assert again.returncode == 2
    assert before == {str(p.relative_to(destination)): p.read_bytes() for p in destination.rglob("*") if p.is_file()}


def test_output_symlink_and_collision_are_zero_write(tmp_path):
    import run_korean_postediting_eval as cli
    existing = tmp_path / "keep"
    existing.mkdir()
    (existing / "original").write_bytes(b"keep")
    with pytest.raises(ev.EvalError):
        cli.save_new_bundle(existing, {"plan.json": "bad"})
    link = tmp_path / "link"
    try:
        link.symlink_to(existing, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation unavailable on this platform")
    with pytest.raises(ev.EvalError):
        cli.save_new_bundle(link / "out", {"plan.json": "bad"})
    with pytest.raises(ev.EvalError):
        cli.save_new_bundle(tmp_path / "bad", {"../escape": "bad"})
    assert not (tmp_path / "bad").exists()
    assert sorted(p.name for p in existing.iterdir()) == ["original"]


def test_cli_has_no_execution_option(tmp_path, monkeypatch):
    import run_korean_postediting_eval as cli
    def forbidden_process(*args, **kwargs):
        pytest.fail("must never invoke a subprocess/model")
    monkeypatch.setattr(subprocess, "Popen", forbidden_process)
    assert cli.main(["prepare", "--output", str(tmp_path / "safe"), "--provider", "p", "--model", "m"]) == 0
    with pytest.raises(SystemExit) as error:
        cli.main(["prepare", "--output", str(tmp_path / "unsafe"), "--execute"])
    assert error.value.code == 2 and not (tmp_path / "unsafe").exists()
