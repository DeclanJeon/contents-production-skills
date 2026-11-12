# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_reference_handles.py
"""Bounded reference metadata from actual source pages; never fetches a target's bytes."""
from pathlib import Path
import re
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from writing_eval_snapshot import EvaluationContractError, digest
from writing_eval_source_paths import resolve_document_read, runtime_markdown_path
from writing_eval_wire import WireEvent


class SourceReference(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    reference_id: str
    document: str
    literal: str
    target: str


def is_reference_address(value: str) -> bool:
    return re.fullmatch(r"ref_[0-9a-f]{24}", value) is not None


class SourcePage(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    document: str
    offset: int = Field(ge=1)
    returned_lines: int = Field(ge=0)
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


def verified_page_references(root: Path, page: SourcePage) -> tuple[SourceReference, ...]:
    """Reconstruct the delivered slice from immutable source, then verify its hash."""
    document = runtime_markdown_path(root, page.document)
    lines = document.read_text(encoding="utf-8").split("\n")
    text = "\n".join(lines[page.offset - 1:page.offset - 1 + page.returned_lines])
    if digest(text.encode()) != page.content_sha256:
        raise EvaluationContractError("Source page hash does not match immutable source")
    return index_references(root, document, text)


def restore_references(root: Path, events: Path) -> tuple[SourceReference, ...]:
    """Rehydrate only prior delivered source-page offers from this case's append-only log."""
    if not events.is_file():
        return ()
    active: set[str] = set()
    pages: dict[str, dict[str, SourceReference]] = {}
    pending: dict[str, dict[str, SourceReference]] = {}
    restored: dict[str, SourceReference] = {}
    for line in events.read_bytes().splitlines():
        event = WireEvent.model_validate_json(line)
        identifier = event.toolCallId
        if identifier is None:
            continue
        if event.type == "tool_execution_start" and event.toolName in {"read", "read_reference"}:
            active.add(identifier)
            pages.pop(identifier, None)
            pending.pop(identifier, None)
        if event.type == "controlled_read" and identifier in active and event.path:
            document = Path(event.path).resolve()
            if document.is_relative_to(root) and event.offset is not None and event.returned_lines is not None and event.content_sha256 is not None:
                page = SourcePage(document=document.relative_to(root).as_posix(), offset=event.offset,
                    returned_lines=event.returned_lines, content_sha256=event.content_sha256)
                pages[identifier] = {r.reference_id:r for r in verified_page_references(root, page)}
        if event.type == "reference_offered" and identifier in pages and event.args and event.args.reference_id:
            reference = pages[identifier].get(event.args.reference_id)
            if reference is None or event.args.path != reference.target or event.args.relative_to != reference.document:
                raise EvaluationContractError("Prior reference offer does not match its actual source page")
            pending.setdefault(identifier, {})[reference.reference_id] = reference
        if event.type == "tool_execution_end" and identifier in active:
            if not event.isError and not event.aborted:
                restored.update(pending.pop(identifier, {}))
            active.discard(identifier)
    return tuple(restored.values())


def index_references(root: Path, document: Path, text: str) -> tuple[SourceReference, ...]:
    """Resolve actual hrefs and explicit skill-relative inline paths, with no fallback."""
    base = document.relative_to(root).as_posix()
    pattern = r"""\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|(?P<bare>(?:[^()\s]|\([^()\n]*\))+))(?:\s+(?:"[^"\n]*"|'[^'\n]*'|\([^()\n]*\)))?\s*\)"""
    markdown = list(re.finditer(pattern, text))
    links: list[tuple[str, bool]] = [(m.group("angle") or m.group("bare"), True) for m in markdown]
    for match in re.finditer(r"`((?:assets|references|scripts)/[^`\n]+\.md)`", text):
        if not any(m.start() <= match.start() < m.end() for m in markdown):
            links.append((match.group(1), False))
    found: dict[str, SourceReference] = {}
    used = 0
    for literal, is_href in links:
        try:
            target = (resolve_document_read(root, literal, base) if is_href
                else runtime_markdown_path(root, document.relative_to(root).parts[0] + "/" + literal))
        except (EvaluationContractError, OSError, UnicodeError):
            continue  # Not a readable reference, not an attempted target read or alternate-base retry.
        relative = target.relative_to(root).as_posix()
        identifier = "ref_" + digest((base + "\0" + literal + "\0" + relative).encode())[:24]
        item = SourceReference(reference_id=identifier, document=base, literal=literal, target=relative)
        cost = len(item.model_dump_json().encode())
        if used + cost > 12000 or len(found) >= 16:
            break
        if identifier not in found:
            found[identifier] = item
            used += cost
    return tuple(found.values())
