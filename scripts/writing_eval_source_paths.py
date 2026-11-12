# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 -m pytest -q scripts/test_writing_eval_relative_read.py
"""One path boundary shared by source delivery and receipt verification; no fallback."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from writing_eval_snapshot import EXCLUDED, EvaluationContractError


def runtime_markdown_path(root: Path, requested: str) -> Path:
    """Resolve a root-relative runtime file without following symlink components."""
    anchor = root.resolve(strict=True)
    relative = Path(requested)
    if (not requested or relative.is_absolute() or not relative.parts or "\\" in requested or "\x00" in requested
            or any((p.startswith(".") and p != "..") or p in EXCLUDED for p in relative.parts)
            or relative.name.startswith("test_") or relative.suffix != ".md"):
        raise EvaluationContractError("Only relative runtime Markdown is readable")
    target = anchor / relative
    if any(p.is_symlink() for p in (target, *target.parents) if p.is_relative_to(anchor)):
        raise EvaluationContractError("Source symlink refused")
    # Deny a resolved escape before the strict target-existence check.
    resolved = target.resolve(strict=False)
    if not resolved.is_relative_to(anchor):
        raise EvaluationContractError("Source escape refused")
    resolved = target.resolve(strict=True)
    if not resolved.is_file():
        raise EvaluationContractError("Runtime source must be a Markdown file")
    return resolved


def resolve_document_read(root: Path, requested: str, relative_to: str | None) -> Path:
    """Explicit source-document context resolves local hrefs; None preserves root reads."""
    if relative_to is None:
        return runtime_markdown_path(root, requested)
    if relative_to == "fixture/draft.md" or requested == "fixture/draft.md":
        raise EvaluationContractError("Fixture virtual paths cannot be document-qualified")
    base = runtime_markdown_path(root, relative_to)
    try:
        link = urlsplit(requested)
        if re.search(r"%(?![0-9a-fA-F]{2})", link.path):
            raise EvaluationContractError("Malformed percent escape in Markdown reference")
        decoded = unquote(link.path, errors="strict")
    except (ValueError, UnicodeError) as exc:
        raise EvaluationContractError("Invalid local Markdown reference") from exc
    if link.scheme or link.netloc or link.query or Path(decoded).is_absolute() or "\\" in decoded or "\x00" in decoded:
        raise EvaluationContractError("Only contained local Markdown references are readable")
    relative = base.relative_to(root.resolve(strict=True))
    target = relative.parent / decoded if decoded else relative
    return runtime_markdown_path(root, target.as_posix())
