# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_evaluation.py
"""Verify pinned execution evidence before aggregating manual craft verdicts."""
from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from writing_eval_manifest import RunManifest, RunSlot
from writing_eval_codex_tools import INITIAL, INJECTED, EXPECTED
from writing_eval_source_paths import resolve_document_read
from writing_eval_references import SourcePage, verified_page_references, is_reference_address
from writing_eval_wire import (
    ContentBlock as ContentBlock, WireMessage as WireMessage, ReadArgs as ReadArgs,
    WireEvent as WireEvent, RunReceipt as RunReceipt,
)
from writing_eval_snapshot import EvaluationContractError, Snapshot, digest, verify_snapshot, safe_evidence_path

Verdict = Literal["PASS", "FAIL", "INCONCLUSIVE", "SKIPPED"]


class ReviewedRun(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    run_id: str
    verdict: Verdict
    reason: str = Field(min_length=1)
    evidence_path: str
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    blocking: bool = False


class ReviewSummary(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    verdict: Literal["PASS", "FAIL", "INCONCLUSIVE"]
    missing: int
    invalid_evidence: int
    blockers: int
    improved_cases: tuple[str, ...]


def verify_trace(receipt: RunReceipt, slot: RunSlot, snapshot: Snapshot) -> bool:
    pending: dict[str, str] = {}
    qualified: set[str] = set()
    physical: set[str] = set()
    source_reads: dict[str, Path] = {}
    page_references: dict[str, dict[str, str]] = {}
    offered: dict[str, str] = {}
    pending_offers: dict[str, dict[str, str]] = {}
    requested_refs: dict[str, str] = {}
    selected: set[str] = set()
    read_owner = False
    settled_count = 0
    final_count = 0
    readonly = frozenset({"read", "read_reference", "grep", "find", "ls"})
    allowed = {"single": readonly, "conversation": readonly, "fixture": frozenset({"read", "read_reference", "edit", "write"})}[slot.kind]
    for event in receipt.trace:
        if event.toolName is not None and event.toolName not in allowed:
            return False
        if event.isError or event.aborted:
            return False
        handle_read = event.toolName == "read_reference" or (event.toolName == "read" and event.args is not None and event.args.path is not None and is_reference_address(event.args.path))
        if event.type == "tool_execution_start" and event.toolName == "read" and not handle_read and event.args and event.args.path and event.toolCallId:
            if event.args.path == "fixture/draft.md":
                if slot.kind != "fixture" or event.args.relative_to is not None:
                    return False
                pending[event.toolCallId] = "fixture/draft.md"
            else:
                try:
                    path = resolve_document_read(snapshot.root, event.args.path, event.args.relative_to)
                except (EvaluationContractError, OSError, UnicodeError):
                    return False
                pending[event.toolCallId] = path.relative_to(snapshot.root).as_posix()
                if event.args.relative_to is not None:
                    qualified.add(event.toolCallId)
                    physical.discard(event.toolCallId)
        if event.type == "reference_offered" and event.toolCallId and event.args and event.args.reference_id and event.args.path and event.args.relative_to:
            try:
                target = resolve_document_read(snapshot.root, event.args.path, None)
                document = resolve_document_read(snapshot.root, event.args.relative_to, None)
            except (EvaluationContractError, OSError, UnicodeError):
                return False
            if (source_reads.get(event.toolCallId) != document or
                    page_references.get(event.toolCallId, {}).get(event.args.reference_id) != target.relative_to(snapshot.root).as_posix()):
                return False
            pending_offers.setdefault(event.toolCallId, {})[event.args.reference_id] = target.relative_to(snapshot.root).as_posix()
        if event.type == "tool_execution_start" and handle_read and event.toolCallId:
            identifier = (event.args.reference_id if event.toolName == "read_reference" else event.args.path) if event.args else None
            if identifier is None or identifier not in offered:
                return False
            pending[event.toolCallId] = offered[identifier]
            requested_refs[event.toolCallId] = identifier
            qualified.add(event.toolCallId)
            physical.discard(event.toolCallId)
            selected.discard(event.toolCallId)
        if event.type == "reference_selected" and event.toolCallId:
            if (event.args is None or event.args.reference_id != requested_refs.get(event.toolCallId)
                    or event.args.path != pending.get(event.toolCallId)):
                return False
            selected.add(event.toolCallId)
        if event.type == "tool_execution_end" and event.toolName in {"read", "read_reference"} and event.toolCallId:
            if event.toolCallId in requested_refs and event.toolCallId not in selected:
                return False
            if event.toolCallId in qualified and event.toolCallId not in physical:
                return False
            qualified.discard(event.toolCallId)
            offered.update(pending_offers.pop(event.toolCallId, {}))
            read_owner |= pending.pop(event.toolCallId, None) == slot.owner
        if event.type == "controlled_read" and event.path:
            actual = Path(event.path).resolve()
            if event.toolCallId in requested_refs and event.toolCallId not in selected:
                return False
            if event.toolCallId is not None:
                source_reads[event.toolCallId] = actual
                if actual.is_relative_to(snapshot.root) and event.offset is not None and event.returned_lines is not None and event.content_sha256 is not None:
                    try:
                        page = SourcePage(document=actual.relative_to(snapshot.root).as_posix(), offset=event.offset,
                            returned_lines=event.returned_lines, content_sha256=event.content_sha256)
                        refs = verified_page_references(snapshot.root, page)
                    except (EvaluationContractError, OSError, UnicodeError, ValueError):
                        return False
                    page_references[event.toolCallId] = {r.reference_id: r.target for r in refs}
            if event.toolCallId in qualified:
                expected = pending.get(event.toolCallId)
                if expected is not None and actual == snapshot.root / expected:
                    physical.add(event.toolCallId)
        if event.type == "message_end" and event.message:
            final_count += int(event.message.successful_text())
        if event.type == "agent_settled":
            settled_count += 1
    fixture_order = True
    if slot.kind == "fixture":
        inserted = next((n for n, e in enumerate(receipt.trace) if e.type == "user_edit_inserted"), -1)
        written = next((n for n, e in enumerate(receipt.trace) if e.type == "fixture_written"), -1)
        fixture_order = inserted >= 0 and written > inserted and any(
            e.type == "tool_execution_end" and e.toolName == "read"
            for e in receipt.trace[inserted + 1:written]
        )
    return read_owner and final_count == slot.stages and settled_count == slot.stages and fixture_order and not qualified


class FixtureEvent(WireEvent):
    sha256: str | None = None


def verify_fixture_files(folder: Path, trace: tuple[WireEvent, ...]) -> bool:
    """Verify physical byte preservation and the controlled race, not a PASS assertion."""
    events_path = folder / "tools.jsonl"
    fixture = folder / "fixture/draft.md"
    if any(p.is_symlink() for p in (events_path, fixture.parent, fixture)):
        return False
    if fixture.read_bytes() != EXPECTED.encode():
        return False
    events = tuple(FixtureEvent.model_validate_json(line) for line in events_path.read_bytes().splitlines() if line.strip())
    legacy_page_projection = all(e.offset is None and e.returned_lines is None and e.content_sha256 is None for e in trace)
    page_fields: set[str] = {"offset", "returned_lines", "content_sha256"} if legacy_page_projection else set()
    normalized = [e.model_dump(exclude={"sha256"} | page_fields) for e in events]
    recorded = [e.model_dump(exclude=page_fields) for e in trace if e.type not in {"message_end", "agent_settled"}]
    if normalized != recorded:
        return False
    initial = inserted = fresh = written = writing = False
    read_id: str | None = None
    read_sha: str | None = None
    writable = {"fixture/draft.md", str(fixture.resolve())}
    for event in events:
        if event.isError or event.aborted:
            return False
        if event.type == "tool_execution_start":
            if event.toolName == "read":
                read_id, read_sha = event.toolCallId, None
            elif event.toolName in {"edit", "write"}:
                if not fresh or event.args is None or event.args.path not in writable:
                    return False
                writing = True
        elif event.type == "controlled_read" and event.path == str(fixture.resolve()):
            read_sha = event.sha256
        elif event.type == "tool_execution_end" and event.toolName == "read" and event.toolCallId == read_id:
            initial |= not inserted and read_sha == digest(INITIAL.encode())
            fresh |= inserted and read_sha == digest(INJECTED.encode())
            read_id, read_sha = None, None
        elif event.type == "user_edit_inserted":
            if not initial or inserted or event.sha256 != digest(INJECTED.encode()):
                return False
            inserted = True
        elif event.type == "fixture_written":
            if not fresh or not writing or event.sha256 != digest(EXPECTED.encode()):
                return False
            written, writing = True, False
    return initial and inserted and fresh and written and not writing


def aggregate_results(records: list[ReviewedRun], manifest: RunManifest, evidence_root: Path) -> ReviewSummary:
    slots = {slot.id: slot for slot in manifest.runs}
    seen: set[str] = set()
    valid: dict[str, Verdict] = {}
    invalid = 0
    blockers = 0
    snapshots = {"baseline": manifest.baseline_snapshot, "candidate": manifest.candidate_snapshot}
    snapshot_ok = {}
    for condition, snapshot in snapshots.items():
        try:
            snapshot_ok[condition] = snapshot is not None and verify_snapshot(snapshot)
        except (EvaluationContractError, OSError):
            snapshot_ok[condition] = False
    for record in records:
        if record.run_id in seen or record.run_id not in slots:
            invalid += 1
            continue
        seen.add(record.run_id)
        slot = slots[record.run_id]
        snapshot = snapshots[slot.condition]
        try:
            path = safe_evidence_path(evidence_root, record.evidence_path)
            data = path.read_bytes()
            receipt = RunReceipt.model_validate_json(data)
            if digest(data) != record.evidence_sha256 or receipt.run_id != slot.id or receipt.input_sha256 != slot.input_sha256:
                raise EvaluationContractError("Evidence identity/hash mismatch")
            if snapshot is None or not snapshot_ok[slot.condition] or receipt.source_before != snapshot.sha256 or receipt.source_after != snapshot.sha256:
                raise EvaluationContractError("Evidence source snapshot mismatch")
            if receipt.status != "completed" or not verify_trace(receipt, slot, snapshot):
                raise EvaluationContractError("Incomplete execution/owner-read evidence")
            if slot.kind == "fixture" and not verify_fixture_files(path.parent, receipt.trace):
                raise EvaluationContractError("Invalid fixture order or final byte evidence")
            valid[slot.id] = record.verdict
            blockers += int(record.blocking)
        except (OSError, UnicodeError, ValidationError, EvaluationContractError):
            invalid += 1
    missing = len(slots) - len(seen & slots.keys())
    verdict: Literal["PASS", "FAIL", "INCONCLUSIVE"] = "PASS"
    candidate_failed = any(value == "FAIL" and slots[key].condition == "candidate" for key, value in valid.items())
    if blockers or candidate_failed:
        verdict = "FAIL"
    elif missing or invalid or any(v in {"INCONCLUSIVE", "SKIPPED"} for v in valid.values()):
        verdict = "INCONCLUSIVE"
    improved = tuple(sorted(case_id for case_id in {s.case_id for s in manifest.runs}
        if any(valid.get(s.id) == "FAIL" for s in manifest.runs if s.case_id == case_id and s.condition == "baseline")
        and all(valid.get(s.id) == "PASS" for s in manifest.runs if s.case_id == case_id and s.condition == "candidate")))
    return ReviewSummary(verdict=verdict, missing=missing, invalid_evidence=invalid, blockers=blockers, improved_cases=improved)
