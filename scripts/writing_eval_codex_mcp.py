# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2,<3"]
# ///
# How to run: python3 scripts/writing_eval_codex_mcp.py SNAPSHOT EVENTS [FIXTURE]
"""Local stdio MCP boundary; source-only unless an isolated fixture is provided."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from pydantic import BaseModel, Field, JsonValue, ValidationError

from writing_eval_codex_tools import SourceTools, ToolArguments, FindArguments
from writing_eval_snapshot import EvaluationContractError


class Request(BaseModel):
    jsonrpc: str
    id: int | str | None = None
    method: str
    params: JsonValue = None


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, JsonValue] = Field(default_factory=dict)


class Initialize(BaseModel):
    protocolVersion: str


def handle(request: Request, tools: SourceTools) -> dict[str, JsonValue]:
    match request.method:
        case "initialize":
            version = Initialize.model_validate(request.params).protocolVersion
            return {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": {"name": "writing-eval", "version": "2"}}
        case "ping":
            return {}
        case "resources/list" | "resources/templates/list":
            return {"resources" if request.method == "resources/list" else "resourceTemplates": []}
        case "prompts/list":
            return {"prompts": []}
        case "tools/list":
            names = ["read", "find"] if tools.draft is None else ["read", "edit", "write"]
            descriptions = {
                "read": "Read a root-relative Markdown filename OR an exact offered ref_... address using the same path argument. First read the named owner filename; afterwards copy read_arguments from the companion reference menu. No tool switch or path calculation is needed. Legacy explicit-context addressing remains available: read package Markdown. For an actual Markdown [label](href) link use path=exact href and relative_to=the containing document's root-relative filename, NOT a directory. Bare inline-code assets/, references/, scripts/ paths are skill-relative: prefix their owning skill name and omit relative_to, or find first. Already root-qualified paths also omit relative_to. Without relative_to, path is root-relative. "
                    + ("The additional virtual path fixture/draft.md is available. " if tools.draft is not None else "")
                    + "Line offsets are 1-based (0 also means start). Large reads return a byte-bounded page with next_offset; continue there.",
                "find": "Locate runtime Markdown filenames by case-insensitive query substring, optionally scoped to a root-relative directory in path. Legacy path-only calls use path as the query. Use for uncertain filenames; at most 100 allowed runtime matches, never file contents.",
                "edit": "Replace one unique exact text only in fixture/draft.md. Requires an initial full inspection AND a subsequent fresh full read immediately before writing.",
                "write": "Write only fixture/draft.md. Requires an initial full inspection AND a subsequent fresh full read; preserve user edits.",
            }
            ordinary_schema = ToolArguments.model_json_schema()
            del ordinary_schema["properties"]["relative_to"]
            schemas: dict[str, JsonValue] = {"read": ToolArguments.model_json_schema(), "edit": ordinary_schema, "write": ordinary_schema,
                "find": FindArguments.model_json_schema()}
            return {"tools": [{"name": name, "description": descriptions[name], "inputSchema": schemas[name]} for name in names]}
        case "tools/call":
            call = ToolCall.model_validate(request.params)
            try:
                allowed = {"read", "find"} if tools.draft is None else {"read", "edit", "write"}
                if call.name not in allowed:
                    raise EvaluationContractError("Tool not exposed by this source/fixture capability")
                result = tools.call(call.name, call.arguments)
                content: list[JsonValue] = [{"type": "text", "text": result}]
                if tools.last_references:
                    menu = json.dumps({"instruction": "Use the SAME read tool with each offered read_arguments object. Keep the ref_ address exactly; do not construct paths or change tools.",
                        "references": [{**r.model_dump(), "read_arguments": {"path": r.reference_id}} for r in tools.last_references]}, ensure_ascii=False)
                    content.append({"type": "text", "text": menu})
                return {"content": content, "isError": False}
            except (EvaluationContractError, OSError, UnicodeError, ValidationError) as exc:
                return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
        case _:
            raise EvaluationContractError(f"Unsupported method: {request.method}")


def main() -> None:
    tools = SourceTools(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]) if len(sys.argv) > 3 else None)
    for line in sys.stdin:
        if not line.strip():
            continue
        identifier: int | str | None = None
        failed = True
        try:
            request = Request.model_validate_json(line)
            identifier = request.id
            if identifier is None:
                continue
            result = handle(request, tools)
            failed = result.get("isError") is True
            response: dict[str, JsonValue] = {"jsonrpc": "2.0", "id": identifier, "result": result}
        except (EvaluationContractError, ValidationError) as exc:
            response = {"jsonrpc": "2.0", "id": identifier, "error": {"code": -32602, "message": str(exc)}}
        print(json.dumps(response, ensure_ascii=False), flush=True)
        tools.delivered(failed)


if __name__ == "__main__":
    main()
