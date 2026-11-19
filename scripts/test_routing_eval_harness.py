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
    assert reported == [
        "video-production-assets=['R06', 'R13', 'R14', 'R15', 'R20', 'R25', 'R26', 'R31']"
    ]


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
    """File capture means a big payload cannot fill a pipe buffer and stall.

    256 KiB comfortably exceeds the usual 64 KiB pipe buffer, which is what
    this is guarding against, while staying cheap enough to run under load.
    """
    size = 256 * 1024
    out, _err, _rc = routing_eval.run_bounded(
        ["/bin/sh", "-c", f"head -c {size} /dev/zero | tr '\\0' 'x'"],
        "", 120, dict(routing_eval.os.environ),
    )
    assert len(out) == size, f"expected {size} bytes, got {len(out)}"


def test_dangerous_is_reachable_for_every_case() -> None:
    """Guard against a vacuous "0 dangerous": every case must have a wrong
    answer that would cross an axis, otherwise the grade could never fire."""
    routes = _routes()
    cases = routing_eval.load_cases()
    assert cases

    def crosses(expected: str, other: str) -> bool:
        a, b = routes[expected], routes[other]
        return (a["media_axis"] != b["media_axis"]
                or bool(a["authority_axis"]) != bool(b["authority_axis"]))

    for case in cases:
        expected = case["route_id"]
        alternatives = [r for r in routes if r != expected and crosses(expected, r)]
        assert alternatives, (
            f"{case['case_id']} ({expected}) has no axis-crossing alternative, "
            "so 'dangerous' could never fire for it"
        )


def test_sweep_reports_dangerous_and_fails_the_run(tmp_path: Path) -> None:
    """A model that crosses the media axis must make the run exit non-zero."""
    original = routing_eval.dispatch
    # C10 expects R10 (text-only storyboard); R22 is executed_media with a
    # spatial-verification authority, so answering R22 is an axis crossing.
    routing_eval.dispatch = lambda *a, **k: ("", "ROUTE: R22 - deliberate crossing")
    try:
        out = tmp_path / "dangerous-run"
        code = routing_eval.main(["--case", "C10", "--repeat", "2", "--out", str(out),
                                  "--timeout", "1", "--retries", "0"])
    finally:
        routing_eval.dispatch = original

    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["tally"].get("dangerous") == 2
    assert summary["dangerous"] == ["C10"]
    assert summary["flaky"] == [], "a consistent wrong answer is not flaky"
    assert code == 1, "a dangerous answer must fail the run"


def test_crashes_are_not_reported_as_stably_wrong(tmp_path: Path) -> None:
    """A run of exit-101s must not be summarised as 'consistently wrong'.

    A real degraded run listed fourteen transport failures as stably wrong,
    which reads as a routing problem when nothing was answered at all.
    """
    original = routing_eval.dispatch

    def always_crashes(*_a, **_k):
        raise RuntimeError("codex exit 101: transport channel closed")

    routing_eval.dispatch = always_crashes
    try:
        out = tmp_path / "crashed-run"
        routing_eval.main(["--case", "C10", "--repeat", "2", "--out", str(out),
                           "--timeout", "1", "--retries", "0"])
    finally:
        routing_eval.dispatch = original

    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    entry = summary["results"][0]
    assert entry["judgement"] == "no_data", entry["judgement"]
    assert summary["stable_wrong"] == []
    assert summary["stable_correct"] == 0
    assert summary["decided_cases"] == 0
    assert summary["stable_accuracy"] == 0.0, "no data must not look like 0% accuracy"
    assert summary["infrastructure_failures"] == 2


def test_unanswered_is_not_stably_wrong(tmp_path: Path) -> None:
    """An agent that refuses to commit to a route answered nothing."""
    original = routing_eval.dispatch
    routing_eval.dispatch = lambda *a, **k: ("", "I am not sure which module to use.")
    try:
        out = tmp_path / "unanswered-run"
        routing_eval.main(["--case", "C10", "--repeat", "2", "--out", str(out),
                           "--timeout", "1", "--retries", "0"])
    finally:
        routing_eval.dispatch = original

    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["results"][0]["judgement"] == "unanswered"
    assert summary["stable_wrong"] == []


def test_instruction_does_not_pre_empt_the_skill_reading_list() -> None:
    """The harness must not tell the router which files to read.

    It used to name routing.csv explicitly. That let the router skip the
    skill's own reading list -- including the disambiguation table -- and still
    score 100%, so the measurement was of the harness's list, not the skill's.
    """
    instruction = routing_eval.INSTRUCTION
    assert "SKILL.md" in instruction, "the router entry point is not named"
    for leaked in ("routing.csv", "routing-disambiguation.csv", "policy.md"):
        assert leaked not in instruction, (
            f"the instruction names {leaked}, so the router can skip the "
            "skill's own reading list")


def test_instruction_asks_for_the_machine_readable_answer() -> None:
    assert "ROUTE:" in routing_eval.INSTRUCTION
    assert "WHY:" in routing_eval.INSTRUCTION


def test_fixture_allowlist_covers_every_frontier_file(tmp_path: Path) -> None:
    """The allowlist must be derived, not typed.

    It was once a handwritten list of two paths. When a third required file was
    added, some runs refused to answer at all ("required ... is outside the
    permitted reading list") and others ignored the restriction, so the same
    defect appeared as both an unanswered case and a correct one.
    """
    sandbox = tmp_path / "fixture"
    sandbox.mkdir()
    routing_eval.build_sandbox(sandbox, {"creative-production"})
    allowlist = (sandbox / "AGENTS.md").read_text(encoding="utf-8")

    for rel in routing_eval.FRONTIER_FILES:
        assert f"`{rel}`" in allowlist, f"allowlist omits {rel}"


def test_every_frontier_file_is_present_in_the_fixture(tmp_path: Path) -> None:
    sandbox = tmp_path / "fixture"
    sandbox.mkdir()
    routing_eval.build_sandbox(sandbox, set())
    missing = [rel for rel in routing_eval.FRONTIER_FILES
               if not (sandbox / rel).is_file()]
    assert not missing, f"fixture missing frontier files: {missing}"


def test_handoff_parsing_reads_the_three_fields() -> None:
    text = ("ROUTE: R18\n"
            "SLOTS: camera_timing_lens_motion_design | text_only |\n"
            "ARTIFACT: a numeric camera design for the chase\n")
    parsed = routing_eval.parse_handoff(text)
    assert parsed["route"] == "R18"
    assert parsed["slots"].split("|")[0].strip() == "camera_timing_lens_motion_design"
    assert parsed["artifact"].startswith("a numeric camera design")


def test_handoff_flags_a_right_route_that_never_opens_its_owner() -> None:
    """This is the defect route accuracy cannot see.

    A coordinator can name R18 and still produce R18's work from memory, never
    opening camera-spatial-design/SKILL.md or the references the row lists. The
    label is correct and the output is unauthorised by the skill.
    """
    routes = {"R18": {"owner": "camera-spatial-design",
                      "required_read": "camera-spatial-design/references/camera-design.md",
                      "deliverable_kind": "camera_timing_lens_motion_design",
                      "media_axis": "text_only", "authority_axis": ""}}
    parsed = {"route": "R18", "artifact": "a camera design",
              "slots": "camera_timing_lens_motion_design | text_only |"}
    reads = ["creative-production/SKILL.md",
             "creative-production/references/routing.csv"]

    checks = routing_eval.handoff_checks("R18", "R18", routes, parsed, reads)
    assert checks["owner_loaded"] is False
    assert checks["required_read_missing"] == [
        "camera-spatial-design/references/camera-design.md"]
    assert checks["slots_match"] is True

    good = reads + ["camera-spatial-design/SKILL.md",
                    "camera-spatial-design/references/camera-design.md"]
    checks = routing_eval.handoff_checks("R18", "R18", routes, parsed, good)
    assert checks["owner_loaded"] is True
    assert checks["required_read_missing"] == []


def test_handoff_slots_must_match_the_expected_row_not_the_chosen_one() -> None:
    """A wrong route with self-consistent slots is still wrong."""
    routes = {
        "R17": {"owner": "storyboarding-video", "required_read": "",
                "deliverable_kind": "narrative_camera_planning",
                "media_axis": "text_only", "authority_axis": ""},
        "R18": {"owner": "camera-spatial-design", "required_read": "",
                "deliverable_kind": "camera_timing_lens_motion_design",
                "media_axis": "text_only", "authority_axis": ""},
    }
    parsed = {"route": "R18", "artifact": "x",
              "slots": "camera_timing_lens_motion_design | text_only |"}
    checks = routing_eval.handoff_checks("R18", "R17", routes, parsed, [])
    assert checks["slots_match"] is False, (
        "comparing against the chosen row would let any wrong route pass")


def test_handoff_instruction_demands_slots_and_artifact() -> None:
    text = routing_eval.HANDOFF_INSTRUCTION
    for token in ("ROUTE:", "SLOTS:", "ARTIFACT:"):
        assert token in text
    for leaked in ("routing.csv", "routing-disambiguation.csv", "policy.md"):
        assert leaked not in text, f"the handoff instruction names {leaked}"


def test_handoff_accepts_the_word_none_for_no_authority() -> None:
    """Four correct answers were scored wrong because "none" is a truthy string."""
    routes = {"R10": {"owner": "storyboarding-video", "required_read": "",
                      "deliverable_kind": "ordinary_or_complete_storyboard",
                      "media_axis": "text_only", "authority_axis": ""}}
    for token in ("none", "N/A", "-", ""):
        parsed = {"route": "R10", "artifact": "a board",
                  "slots": f"ordinary_or_complete_storyboard | text_only | {token}"}
        checks = routing_eval.handoff_checks("R10", "R10", routes, parsed, [])
        assert checks["slots_match"] is True, token


def test_handoff_accepts_a_concrete_media_axis_when_the_row_says_varies() -> None:
    """`varies` describes the route, so committing to one axis cannot contradict it."""
    routes = {"R14": {"owner": "video-production-assets", "required_read": "",
                      "deliverable_kind": "film_short_full_lifecycle",
                      "media_axis": "varies", "authority_axis": ""}}
    for axis in ("text_only", "none_or_stills", "executed_media", "varies"):
        parsed = {"route": "R14", "artifact": "a plan",
                  "slots": f"film_short_full_lifecycle | {axis} |"}
        checks = routing_eval.handoff_checks("R14", "R14", routes, parsed, [])
        assert checks["slots_match"] is True, axis


def test_handoff_still_rejects_a_genuinely_different_media_axis() -> None:
    routes = {"R14": {"owner": "video-production-assets", "required_read": "",
                      "deliverable_kind": "film_short_full_lifecycle",
                      "media_axis": "varies", "authority_axis": ""}}
    parsed = {"route": "R14", "artifact": "a plan",
              "slots": "film_short_full_lifecycle | nonsense_axis |"}
    checks = routing_eval.handoff_checks("R14", "R14", routes, parsed, [])
    assert checks["slots_match"] is False, "the varies rule must not accept anything"


def _contract(route_id: str) -> list[dict[str, str]]:
    return routing_eval.load_artifact_contract()[route_id]


def test_artifact_checker_catches_prose_instead_of_the_slot_table() -> None:
    """The exact failure of a coordinator that never opened the board contract."""
    prose = ("연출 아이디어를 정리했습니다. 인물이 창가로 걸어가며 감정이 바뀝니다.\n"
             "아래는 스토리보드 초안입니다.")
    results = routing_eval.check_artifact(prose, _contract("R10"), "보드 만들어줘")
    failed = {r["check_id"] for r in results if not r["passed"]}
    assert failed == {"slot_table_rows", "no_bare_prose_board"}, failed


def test_artifact_checker_passes_a_contract_shaped_board() -> None:
    board = "\n".join(
        f"{row}: 기록" for row in
        ("추적", "시간", "피사체", "카메라", "공간", "VFX", "발화", "음향", "패널"))
    results = routing_eval.check_artifact(board, _contract("R10"), "보드 만들어줘")
    assert all(r["passed"] is True for r in results), [r for r in results if r["passed"] is not True]


def test_artifact_checker_catches_a_fabricated_blend() -> None:
    """No Blender on this host, so a .blend claim is invented."""
    claimed = "previs.blend을 생성했습니다. 카메라 경로도 검증 완료입니다."
    results = routing_eval.check_artifact(claimed, _contract("R22"), "3D 검증해줘")
    failed = {r["check_id"] for r in results if not r["passed"]}
    assert "no_invented_artifacts" in failed
    assert "no_false_blend_claim" in failed

    honest = "Blender 실행 환경이 없어 수치 설계만 반환합니다. 3D 가림은 UNVERIFIED."
    results = routing_eval.check_artifact(honest, _contract("R22"), "3D 검증해줘")
    assert all(r["passed"] is True for r in results)


def test_artifact_checker_catches_the_wrong_panel_count() -> None:
    prompt = "패널 6개로 뽑아줘"
    short = "P01: 시작\nP02: 행동\nP03: 결과\nP04: 여운"
    results = routing_eval.check_artifact(short, _contract("R11"), prompt)
    assert [r["passed"] for r in results] == [False]
    exact = "\n".join(f"P{i:02d}: 비트" for i in range(1, 7))
    results = routing_eval.check_artifact(exact, _contract("R11"), prompt)
    assert all(r["passed"] is True for r in results)


def test_artifact_checker_catches_pts_written_as_a_cut_time() -> None:
    claim = "컷 시각 = source_pts_s 로 기록했습니다."
    results = routing_eval.check_artifact(claim, _contract("R26"), "컷 분석해줘")
    assert not all(r["passed"] for r in results)


def test_every_artifact_contract_row_cites_a_real_source() -> None:
    """A check whose source line does not exist is an invented requirement."""
    contract = routing_eval.load_artifact_contract()
    assert contract, "the artifact contract is empty"
    problems = []
    for route_id, rows in contract.items():
        for row in rows:
            path = row["source"].split(":")[0]
            if not (routing_eval.ROOT / path).is_file():
                problems.append(f"{route_id}/{row['check_id']} cites missing {path}")
    assert not problems, problems


def test_every_artifact_contract_row_targets_a_real_route() -> None:
    routes = routing_eval.load_routes()
    problems = [row["route_id"] for rows in
                routing_eval.load_artifact_contract().values()
                for row in rows if row["route_id"] not in routes]
    assert not problems, f"unknown route in contract: {sorted(set(problems))}"


def test_parse_artifact_keeps_the_multiline_body() -> None:
    text = "ROUTE: R10\nSLOTS: a | b |\nARTIFACT:\n추적: x\n카메라: y\n"
    parsed = routing_eval.parse_artifact(text)
    assert parsed["route"] == "R10"
    assert "추적: x" in parsed["artifact"] and "카메라: y" in parsed["artifact"]


def test_missing_input_is_not_applicable_not_a_failure() -> None:
    """The skills require reporting a blocker instead of inventing content.

    Scoring a blocker report as a failed contract check would penalise exactly
    the behaviour every owner skill demands, so a declared missing input moves
    content-presence checks to n/a instead of fail.
    """
    blocked = ("분석할 레퍼런스 영상이 첨부되지 않았습니다. 실제 검사 범위: 없음. "
               "카메라 이동은 모두 UNVERIFIED입니다.")
    results = routing_eval.check_artifact(blocked, _contract("R16"),
                                          "이 레퍼런스 영상 카메라 무빙 분석해줘")
    verdicts = {r["check_id"]: r["passed"] for r in results}
    assert verdicts["evidence_labels"] is True, "UNVERIFIED is a legal evidence label"

    blocked_cut = "레퍼런스 영상이 제공되지 않아 컷 분해를 진행할 수 없습니다."
    results = routing_eval.check_artifact(blocked_cut, _contract("R26"),
                                          "이 레퍼런스 영상 컷 분해해줘")
    verdicts = {r["check_id"]: r["passed"] for r in results}
    assert verdicts["no_pts_equality"] is True, "forbidden-claim checks always apply"
    assert verdicts["detector_candidate"] is None, "content checks become n/a"


def test_inventing_content_when_input_is_missing_still_fails() -> None:
    """n/a must not become a hiding place: a fabricated board still fails."""
    fabricated = ("원본이 없지만 30초 보드를 만들었습니다. "
                  "previs.blend을 생성했습니다.")
    results = routing_eval.check_artifact(fabricated, _contract("R22"), "3D 검증")
    verdicts = {r["check_id"]: r["passed"] for r in results}
    assert verdicts["no_invented_artifacts"] is False
    assert verdicts["no_false_blend_claim"] is False
