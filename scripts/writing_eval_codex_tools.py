# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: imported by writing_eval_codex_mcp.py; never invokes a model.
"""Capability-limited package reads and one controlled concurrent-edit fixture."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from writing_eval_snapshot import EXCLUDED, EvaluationContractError, digest
from writing_eval_source_paths import resolve_document_read, runtime_markdown_path
from writing_eval_references import SourceReference, index_references, is_reference_address, restore_references

INITIAL = 'B01: 처음 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n'
INJECTED = 'B01: 사용자 수정 문장입니다.\nB02: 루마를 봅니다.\nB03: 끝 문장입니다.\n'
EXPECTED = 'B01: 사용자 수정 문장입니다.\nB02: 옷의 전체 윤곽을 봅니다.\nB03: 끝 문장입니다.\n'


class ToolArguments(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")
    path: str
    relative_to: str | None = Field(default=None, description="Read only: root-relative SOURCE DOCUMENT filename containing the literal href in path. Omit for root-relative reads.")
    offset: int = Field(default=1, ge=0, strict=True, description="1-based line number; 0 is an alias for the start")
    limit: int | None = Field(default=None, ge=1, strict=True, description="Requested line count; output remains byte-bounded")
    oldText: str | None = None
    newText: str | None = None
    content: str | None = None


class FindArguments(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    query: str | None = None
    path: str = ""


class ReferenceArguments(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    reference_id: str
    offset: int = Field(default=1, ge=0, strict=True)
    limit: int | None = Field(default=None, ge=1, strict=True)


class SourceTools:
    """Mutable state belongs to one MCP process; tools cannot execute commands."""
    root: Path
    events: Path
    draft: Path | None
    max_calls: int
    calls: int
    injected: bool
    reread: bool
    pending: Literal["initial", "reread"] | None
    active_tool: tuple[str, str] | None
    references: dict[str, SourceReference]
    last_references: tuple[SourceReference, ...]

    def __init__(self, root: Path, events: Path, fixture: Path | None) -> None:
        self.root = root.resolve(strict=True)
        self.events = events
        self.draft = None
        self.max_calls = 64
        self.calls = 0
        self.injected = False
        self.reread = False
        self.pending = None
        self.active_tool = None
        self.references = {}
        self.last_references = ()
        if events.resolve().is_relative_to(self.root):
            raise EvaluationContractError("Tool evidence must be outside source")
        self.references = {r.reference_id:r for r in restore_references(self.root, events)}
        if fixture is not None:
            if fixture.resolve().is_relative_to(self.root):
                raise EvaluationContractError("Fixture must be outside source")
            fixture.mkdir(exist_ok=False)
            self.draft = fixture / "draft.md"
            with self.draft.open("x", encoding="utf-8", newline="") as stream:
                _ = stream.write(INITIAL)

    def emit(self, event: dict[str, JsonValue]) -> None:
        with self.events.open("a", encoding="utf-8") as stream:
            _ = stream.write(json.dumps(event, ensure_ascii=False) + "\n")

    def source_path(self, requested: str) -> Path:
        return runtime_markdown_path(self.root, requested)

    def find_source(self, query: str, within: str = "") -> str:
        if self.draft is not None or Path(query).is_absolute() or ".." in Path(query).parts:
            raise EvaluationContractError("Source-only contained lookup required")
        scope = Path(within)
        if scope.is_absolute() or any(p == ".." or p.startswith(".") or p in EXCLUDED for p in scope.parts):
            raise EvaluationContractError("Find scope must be a contained runtime path")
        target = self.root / scope
        if any(p.is_symlink() for p in (target, *target.parents) if p.is_relative_to(self.root)):
            raise EvaluationContractError("Find scope symlink refused")
        matches: list[str] = []
        for target in sorted(self.root.rglob("*.md")):
            if not target.is_file():
                continue
            relative = target.relative_to(self.root)
            if within and not relative.is_relative_to(scope):
                continue
            if relative.name.startswith("test_") or any(p.startswith(".") or p in EXCLUDED for p in relative.parts):
                continue
            if query.casefold() in relative.as_posix().casefold():
                _ = self.source_path(relative.as_posix())
                matches.append(relative.as_posix())
        return "\n".join(matches[:100]) if matches else "No matching runtime Markdown paths"

    def read_document(self, args: ToolArguments) -> str:
        is_fixture = args.path == "fixture/draft.md"
        if is_fixture:
            if args.relative_to is not None:
                raise EvaluationContractError("Fixture virtual paths cannot be document-qualified")
            if self.draft is None:
                raise EvaluationContractError("Fixture capability unavailable")
            target = self.draft
        else:
            target = resolve_document_read(self.root, args.path, args.relative_to)
            if args.relative_to is not None:
                self.emit({"type": "reference_resolved", "path": str(target),
                    "args": {"path": args.path, "relative_to": args.relative_to}})
        contents = target.read_text(encoding="utf-8")
        start = max(1, args.offset) - 1
        lines = contents.split("\n")
        requested = lines[start:start + args.limit] if args.limit is not None else lines[start:]
        selected: list[str] = []
        used = 0
        for line in requested:
            # Account for JSON string escaping too, leaving room for page metadata.
            cost = len(json.dumps(line, ensure_ascii=False).encode()) - 2 + (2 if selected else 0)
            if used + cost > 48_000:
                break
            selected.append(line)
            used += cost
        if requested and not selected:
            raise EvaluationContractError("Single line exceeds tool page capacity")
        text = "\n".join(selected)
        returned = text
        if len(selected) < len(requested):
            returned = json.dumps({"type": "partial_read", "next_offset": start + len(selected) + 1,
                "text": text}, ensure_ascii=False)
        self.emit({"type": "controlled_read", "path": str(target),
            "toolCallId": self.active_tool[0] if self.active_tool is not None else None, "sha256": digest(returned.encode()),
            "content_sha256": digest(text.encode()), "offset": max(1, args.offset), "returned_lines": len(selected)})
        if not is_fixture:
            self.last_references = index_references(self.root, target, text)
            for reference in self.last_references:
                self.emit({"type": "reference_offered", "toolCallId": self.active_tool[0] if self.active_tool is not None else None,
                    "path": str(self.root / reference.target), "args": {"path": reference.target,
                        "relative_to": reference.document, "reference_id": reference.reference_id}})
        if is_fixture and text == INITIAL and not self.injected:
            self.pending = "initial"
        elif is_fixture and text == INJECTED and self.injected:
            self.pending = "reread"
        return returned

    def read_reference(self, selection: ReferenceArguments) -> str:
        reference = self.references.get(selection.reference_id)
        if reference is None:
            raise EvaluationContractError("Unknown/unoffered source reference ID; read its source page first")
        target = self.source_path(reference.target)
        identifier = self.active_tool[0] if self.active_tool is not None else None
        self.emit({"type": "reference_selected", "toolCallId": identifier, "path": str(target),
            "args": {"path": reference.target, "reference_id": reference.reference_id}})
        return self.read_document(ToolArguments(path=reference.target, offset=selection.offset, limit=selection.limit))

    def call(self, name: str, raw: dict[str, JsonValue]) -> str:
        self.pending = None
        self.last_references = ()
        self.calls += 1
        self.active_tool = (f"{os.getpid()}-{self.calls}", name)
        identifier = self.active_tool[0]
        self.emit({"type": "tool_execution_start", "toolName": name, "toolCallId": identifier, "args": raw})
        if self.calls > self.max_calls:
            raise EvaluationContractError("Tool-call budget exceeded")
        if "relative_to" in raw and name != "read":
            raise EvaluationContractError("Document context is read-only")
        if name == "read_reference":
            return self.read_reference(ReferenceArguments.model_validate(raw))
        if name == "find":
            lookup = FindArguments.model_validate(raw)
            return self.find_source(lookup.query if lookup.query is not None else lookup.path,
                lookup.path if lookup.query is not None else "")
        args = ToolArguments.model_validate(raw)
        is_fixture = args.path == "fixture/draft.md"
        if name == "read":
            if is_reference_address(args.path):
                if args.relative_to is not None:
                    raise EvaluationContractError("Reference handles already contain context")
                return self.read_reference(ReferenceArguments(reference_id=args.path, offset=args.offset, limit=args.limit))
            return self.read_document(args)
        if name not in {"edit", "write"} or not is_fixture or self.draft is None:
            raise EvaluationContractError("Only fixture/draft.md is writable")
        if not self.injected or not self.reread:
            raise EvaluationContractError("Delivered full initial read and post-insertion re-read required")
        if name == "edit":
            current = self.draft.read_text(encoding="utf-8")
            if not args.oldText or args.newText is None or current.count(args.oldText) != 1:
                raise EvaluationContractError("Edit must match exactly once")
            content = current.replace(args.oldText, args.newText)
        else:
            if args.content is None:
                raise EvaluationContractError("Missing write content")
            content = args.content
        with self.draft.open("w", encoding="utf-8", newline="") as stream:
            _ = stream.write(content)
        self.emit({"type": "fixture_written", "sha256": digest(content.encode())})
        return "Updated fixture/draft.md"

    def delivered(self, failed: bool = False) -> None:
        """Called AFTER stdout flush: insertion never precedes read completion."""
        if self.active_tool is None:
            return
        identifier, name = self.active_tool
        self.emit({"type": "tool_execution_end", "toolName": name, "toolCallId": identifier, "isError": failed})
        if not failed:
            for reference in self.last_references:
                self.references[reference.reference_id] = reference
        if not failed and self.pending == "initial" and self.draft is not None:
            with self.draft.open("w", encoding="utf-8", newline="") as stream:
                _ = stream.write(INJECTED)
            self.injected = True
            self.emit({"type": "user_edit_inserted", "sha256": digest(INJECTED.encode())})
        elif not failed and self.pending == "reread":
            self.reread = True
            self.emit({"type": "fixture_reread"})
        self.pending = None
        self.active_tool = None
