"""Harness correctness: parsing, leak detection and classification.

These do NOT call a model. They lock the grader so a measured number cannot be
inflated by a parser that silently returns no answer, or by an isolation check
that misreads relative sandbox paths as leaks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Final

import routing_eval

ROOT: Final = Path(__file__).resolve().parents[1]


def _routes() -> dict[str, dict[str, str]]:
    return routing_eval.load_routes()


def _classify(chosen: str | None, expected: str) -> str:
    return routing_eval.classify(chosen, expected, _routes())


def test_parse_accepts_route_prefix_description() -> None:
    # Given: the shape an agent actually produced in the sweep
    text = "ROUTE: R13 — one_production_asset · text_only · video-production-assets.\nWHY: single module"

    # When/Then: the id is extracted, not the whole phrase
    route, why = routing_eval.parse_route(text)
    assert route == "R13"
    assert why


def test_parse_accepts_bare_and_decorated_answers() -> None:
    for text, expected in [
        ("**R24**", "R24"),
        ("r24.", "R24"),
        ("R11 - rough panels", "R11"),
    ]:
        route, _ = routing_eval.parse_route(text)
        assert route == expected, text


def test_parse_returns_none_for_owner_only_answer() -> None:
    # An owner name is not a route id; it must not be silently accepted.
    route, why = routing_eval.parse_route("ROUTE: video-production-assets\nWHY: single module")
    assert route is None
    assert why


def test_owner_answer_is_reported_not_scored() -> None:
    # Given: an owner-only answer
    text = "ROUTE: video-production-assets"
    # When: the sweep inspects it
    reported = routing_eval.resolve_owner_answer(text, _routes())
    # Then: every route for that owner is surfaced for human review
    assert reported == ["video-production-assets=['R06', 'R13', 'R14', 'R15', 'R20', 'R25', 'R26']"]


def test_read_paths_unwraps_the_shell_reader(tmp_path: Path) -> None:
    # Given: the exact command shape observed in a real run
    wire = json.dumps({
        "item": {
            "type": "command_execution",
            "command": "/usr/bin/bash -lc 'cat creative-production/references/routing.csv "
                       "creative-production/SKILL.md'",
        }
    })

    # When: reads are extracted
    reads = routing_eval.read_paths(wire)

    # Then: only the real files appear, never the program name
    assert reads == [
        "creative-production/SKILL.md",
        "creative-production/references/routing.csv",
    ]


def test_relative_sandbox_paths_are_not_leaks(tmp_path: Path) -> None:
    # Given: a relative read inside the fixture (agent runs with -C <sandbox>)
    files = ["creative-production/SKILL.md", "references/routing.csv"]

    # Then: no leak is reported
    assert routing_eval.leaked_outside(files, tmp_path) == []


def test_absolute_read_outside_sandbox_is_a_leak(tmp_path: Path) -> None:
    # Given: an absolute path that escapes the fixture
    outside = ROOT / "creative-production/SKILL.md"

    # Then: it is flagged as a leak
    assert routing_eval.leaked_outside([str(outside)], tmp_path) == [str(outside)]


def test_dangerous_classification_crosses_the_media_axis() -> None:
    routes = _routes()
    # text-only request routed to an executed-media route is dangerous
    assert routing_eval.classify("R24", "R10", routes) == "dangerous"
    # same axis and same authority shape is a near miss, not dangerous
    assert routing_eval.classify("R11", "R10", routes) == "near_miss"
    # identical is correct
    assert routing_eval.classify("R10", "R10", routes) == "correct"


def test_stability_judgement_distinguishes_flaky_from_wrong() -> None:
    """A case that answers correctly once and wrongly once is FLAKY, not correct."""
    routes = _routes()
    # Simulate three trials of the same case where the route changes.
    choices = ["R10", "R11", "R10"]
    verdicts = [_classify(c, "R10") for c in choices]
    distinct = sorted(set(choices))

    assert distinct == ["R10", "R11"]
    assert len(distinct) > 1, "must be treated as flaky"
    assert verdicts.count("correct") == 2
    # A flaky case must never be counted as a stable success.
    stable = len(distinct) == 1
    judgement = ("stable_correct" if stable and verdicts.count("correct") == len(verdicts)
                 else "stable_wrong" if stable else "flaky")
    assert judgement == "flaky"


def test_stable_wrong_is_not_hidden_by_majority() -> None:
    """A consistently wrong route is a finding, not a 0% flake."""
    routes = _routes()
    choices = ["R11", "R11", "R11"]
    verdicts = [_classify(c, "R10") for c in choices]
    distinct = sorted(set(choices))
    stable = len(distinct) == 1
    judgement = ("stable_correct" if stable and verdicts.count("correct") == len(verdicts)
                 else "stable_wrong" if stable else "flaky")
    assert judgement == "stable_wrong"
    assert verdicts.count("correct") == 0


def test_sandbox_seals_codex_home_so_installed_skills_are_invisible(tmp_path: Path) -> None:
    """The fixture must carry its own CODEX_HOME, or the real install leaks in."""
    sandbox = tmp_path / "fixture"
    sandbox.mkdir()
    routing_eval.build_sandbox(sandbox, {"creative-production"})

    home = sandbox / ".codex-home"
    assert home.is_dir(), "sealed CODEX_HOME missing"
    assert (home / "skills").is_dir(), "sealed skills dir missing"

    # The fixture must be readable through the sandbox-relative path the agent uses.
    assert (sandbox / "creative-production/references/routing.csv").is_file()
    assert (sandbox / "skills/creative-production/references/routing.csv").is_file()

    # AGENTS.md must explicitly forbid reading the installed trees.
    instructions = (sandbox / "AGENTS.md").read_text(encoding="utf-8")
    assert "~/.codex/skills" in instructions
    assert "~/.agents" in instructions


def test_sandbox_auth_copy_is_owner_only(tmp_path: Path) -> None:
    """If auth is carried over it must not be world- or group-readable."""
    import stat

    source_auth = Path.home() / ".codex/auth.json"
    if not source_auth.is_file():
        import pytest
        pytest.skip("no local codex auth to mirror")

    sandbox = tmp_path / "fixture"
    sandbox.mkdir()
    routing_eval.build_sandbox(sandbox, set())

    copied = sandbox / ".codex-home/auth.json"
    assert copied.is_file(), "auth not copied into sealed home"
    mode = stat.S_IMODE(copied.stat().st_mode)
    assert mode & (stat.S_IRWXG | stat.S_IRWXO) == 0, (
        f"auth copy is too permissive: {oct(mode)}"
    )


def test_run_bounded_kills_children_that_inherit_the_pipe() -> None:
    """Regression: a grandchild holding stdout made the sweep hang forever.

    `subprocess.run(timeout=)` kills only the direct child, so communicate()
    waits for an EOF the surviving grandchild never sends. A real sweep stalled
    indefinitely at case B06 because of this.
    """
    import time

    started = time.monotonic()
    command = [
        "/usr/bin/env", "bash", "-c",
        # The background child inherits stdout; the parent exits quickly.
        "sleep 300 & sleep 300",
    ]
    try:
        routing_eval.run_bounded(command, "", 2, dict(routing_eval.os.environ))
    except TimeoutError as error:
        assert "exceeded 2s" in str(error)
    else:
        raise AssertionError("expected a TimeoutError")

    elapsed = time.monotonic() - started
    # The kill must return promptly; a hang here would be the original bug.
    assert elapsed < 15, f"run_bounded took {elapsed:.1f}s to give up"


def test_run_bounded_returns_output_for_a_normal_command() -> None:
    out, err, _rc = routing_eval.run_bounded(
        ["/bin/sh", "-c", "printf hello; printf oops >&2"], "", 10,
        dict(routing_eval.os.environ),
    )
    assert out == "hello"
    assert err == "oops"


def test_run_bounded_passes_stdin() -> None:
    out, _err, _rc = routing_eval.run_bounded(
        ["/bin/sh", "-c", "cat"], "prompt text\n", 10, dict(routing_eval.os.environ)
    )
    assert out == "prompt text\n"


def test_run_bounded_survives_a_detached_grandchild() -> None:
    """A descendant in its own session must not stop the call from returning."""
    import time

    started = time.monotonic()
    out, _err, _rc = routing_eval.run_bounded(
        ["/usr/bin/env", "bash", "-c", "setsid sleep 300 & echo done"],
        "", 10, dict(routing_eval.os.environ),
    )
    assert out.strip() == "done"
    assert time.monotonic() - started < 10


def test_run_bounded_returns_large_output_without_deadlock() -> None:
    """File capture means a big payload cannot fill a pipe buffer and stall."""
    out, _err, _rc = routing_eval.run_bounded(
        ["/bin/sh", "-c", "head -c 1000000 /dev/zero | tr '\\0' 'x'"],
        "", 30, dict(routing_eval.os.environ),
    )
    assert len(out) == 1_000_000
