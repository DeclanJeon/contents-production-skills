#!/usr/bin/env python3
"""Blender MCP server for the blender-previsualization skill.

Exposes the skill's own Blender adapter over MCP (stdio JSON-RPC). It is a
thin, restricted execution surface:

* it runs exactly one command shape - the packaged ``build_previs.py`` through
  the Blender CLI - and never a user-supplied command;
* it never installs anything, and reports a missing Blender runtime instead of
  trying to fetch one;
* it refuses to write into an existing output folder, matching the adapter;
* the artifacts it produces are the same ones the skill's acceptance contract
  requires (previs.blend, per-shot PNGs, numerical-analysis.json,
  blender-inspection.json, manifest.json).

The canonical path for this skill stays the CLI. This server exists so an
agent that can only reach MCP can still execute and inspect a real Blender
previs with the same evidence contract.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SERVER_NAME = "blender-previs"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"
MAX_TIMEOUT_S = 3600
SERVER_FILE = Path(__file__).resolve()


def skill_root_candidates():
    """Ordered candidate skill roots for locating the packaged adapter.

    Order: explicit environment override, the recorded global root, then the
    usual installed-skill roots. This keeps the server usable from any
    working directory and any checkout location.
    """
    roots = []
    env_root = os.environ.get("BLENDER_PREVIS_SKILL_ROOT")
    if env_root:
        roots.append(Path(env_root).expanduser())
    recorded = Path.home() / ".config" / "blender-mcp" / "skill_root"
    if recorded.is_file():
        try:
            roots.append(Path(recorded.read_text(encoding="utf-8").strip()))
        except OSError:
            pass
    home = Path.home()
    for base in (".codex/skills", ".pi/agent/skills", ".claude/skills", ".agents/skills"):
        roots.append(home / base / "blender-previsualization")
    roots.append(SERVER_FILE.parent.parent)
    return roots


def resolve_adapter():
    """Absolute path of the packaged build_previs.py, or None when missing."""
    env_adapter = os.environ.get("BLENDER_PREVIS_ADAPTER")
    if env_adapter:
        candidate = Path(env_adapter).expanduser()
        if candidate.is_file():
            return candidate.resolve()
    for root in skill_root_candidates():
        candidate = root / "scripts" / "build_previs.py"
        if candidate.is_file():
            return candidate.resolve()
    return None

TOOLS = [
    {
        "name": "blender_version",
        "description": "Report the Blender runtime available on this host and its exact version string. Does not install anything.",
        "inputSchema": {
            "type": "object",
            "properties": {"executable": {"type": "string", "description": "Optional absolute path to the Blender binary."}},
            "additionalProperties": False,
        },
    },
    {
        "name": "blender_previs",
        "description": "Run the packaged Blender previs adapter for a camera-spatial-1.0 spec and return the manifest summary plus the artifact list. Writes to a new output folder only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "spec_path": {"type": "string", "description": "Absolute path to a camera-spatial-1.0 camera spec JSON."},
                "output_dir": {"type": "string", "description": "Absolute path of a NEW output folder. An existing folder is refused."},
                "mode": {"type": "string", "enum": ["smoke", "stills", "sequence"], "description": "smoke = first shot/one frame; stills = start/mid/end per shot; sequence = every local frame."},
                "proxy": {"type": "string", "enum": ["box", "figure"], "description": "Subject proxy. box = abstract; figure = stylized clay body for readable framing/headroom."},
                "engine": {"type": "string", "enum": ["cycles", "eevee"], "description": "Render engine for the preview frames. cycles is the reference look."},
                "render_map": {"type": "string", "description": "JSON string for --render-map, e.g. {\"SH01\":[0,24,47]}. Local 0-based frames only."},
                "focus_map_path": {"type": "string", "description": "Absolute path to an adapter-local focus map JSON (rack-focus preview)."},
                "look_cards_path": {"type": "string", "description": "Absolute path to an adapter-local look-card map JSON (approved look as a camera-facing card)."},
                "executable": {"type": "string", "description": "Optional absolute path to the Blender binary."},
                "timeout_s": {"type": "integer", "description": "Optional wall-clock limit in seconds (max 3600)."},
            },
            "required": ["spec_path", "output_dir"],
            "additionalProperties": False,
        },
    },
    {
        "name": "blender_previs_inspect",
        "description": "Read a completed previs output folder and return its manifest summary, rendered frames and inspection scope. Read-only.",
        "inputSchema": {
            "type": "object",
            "properties": {"output_dir": {"type": "string", "description": "Absolute path of a completed previs output folder."}},
            "required": ["output_dir"],
            "additionalProperties": False,
        },
    },
]


def find_blender(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() or shutil.which(explicit) else None
    for name in ("blender",):
        found = shutil.which(name)
        if found:
            return found
    local = Path.home() / ".local" / "bin" / "blender"
    if local.exists():
        return str(local)
    return None


def blender_version_string(executable: str) -> str:
    try:
        out = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable: {exc}"
    return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr).strip() else "unknown"


def tool_blender_version(args: dict) -> dict:
    executable = find_blender(args.get("executable"))
    if not executable:
        return {"content": [{"type": "text", "text": "No Blender runtime found. Install it explicitly if needed; this server never installs anything."}], "isError": True}
    return {"content": [{"type": "text", "text": f"{executable}\n{blender_version_string(executable)}"}]}


def tool_blender_previs(args: dict) -> dict:
    spec_path = Path(args["spec_path"]).expanduser()
    output_dir = Path(args["output_dir"]).expanduser()
    if not spec_path.is_absolute() or not output_dir.is_absolute():
        return {"content": [{"type": "text", "text": "spec_path and output_dir must be absolute paths."}], "isError": True}
    if not spec_path.is_file():
        return {"content": [{"type": "text", "text": f"spec not found: {spec_path}"}], "isError": True}
    if output_dir.exists():
        return {"content": [{"type": "text", "text": f"output folder already exists, refusing to write: {output_dir}"}], "isError": True}
    adapter = resolve_adapter()
    if adapter is None:
        return {"content": [{"type": "text", "text": "Packaged build_previs.py not found. Set BLENDER_PREVIS_SKILL_ROOT or BLENDER_PREVIS_ADAPTER, or install the blender-previsualization skill."}], "isError": True}
    executable = find_blender(args.get("executable"))
    if not executable:
        return {"content": [{"type": "text", "text": "No Blender runtime found. Install it explicitly if needed; this server never installs anything."}], "isError": True}
    cmd = [executable, "--background", "--factory-startup", "--python", str(adapter), "--",
           "--spec", str(spec_path), "--output", str(output_dir),
           "--mode", args.get("mode", "stills"),
           "--proxy", args.get("proxy", "box"),
           "--engine", args.get("engine", "cycles")]
    if args.get("render_map"):
        cmd += ["--render-map", args["render_map"]]
    for flag, key in (("--focus-map", "focus_map_path"), ("--look-cards", "look_cards_path")):
        if args.get(key):
            path = Path(args[key]).expanduser()
            if not path.is_file():
                return {"content": [{"type": "text", "text": f"{flag} file not found: {path}"}], "isError": True}
            cmd += [flag, str(path)]
    timeout = min(int(args.get("timeout_s", 900) or 900), MAX_TIMEOUT_S)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"content": [{"type": "text", "text": f"Blender run exceeded {timeout}s and was stopped. Partial output may exist at {output_dir}."}], "isError": True}
    except OSError as exc:
        return {"content": [{"type": "text", "text": f"Blender run failed to start: {exc}"}], "isError": True}
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-12:]
        return {"content": [{"type": "text", "text": "Blender run produced no manifest.json.\n" + "\n".join(tail)}], "isError": True}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = {
        "status": manifest.get("status"),
        "blender_version": manifest.get("blender_version"),
        "engine": manifest.get("engine"),
        "mode": manifest.get("mode"),
        "proxy_mode": manifest.get("proxy_mode"),
        "scope": manifest.get("scope"),
        "camera_spec": manifest.get("camera_spec"),
        "rendered": manifest.get("rendered"),
        "files": manifest.get("files"),
        "output_dir": str(output_dir),
    }
    return {"content": [{"type": "text", "text": json.dumps(summary, ensure_ascii=False, indent=2)}]}


def tool_blender_previs_inspect(args: dict) -> dict:
    output_dir = Path(args["output_dir"]).expanduser()
    if not output_dir.is_absolute() or not output_dir.is_dir():
        return {"content": [{"type": "text", "text": f"output folder not found: {output_dir}"}], "isError": True}
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        return {"content": [{"type": "text", "text": f"no manifest.json in {output_dir}"}], "isError": True}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    inspection_path = output_dir / "blender-inspection.json"
    inspection = json.loads(inspection_path.read_text(encoding="utf-8")) if inspection_path.is_file() else None
    summary = {
        "manifest": {k: manifest.get(k) for k in ("status", "blender_version", "engine", "mode", "proxy_mode", "scope", "rendered", "files")},
        "inspection_scope": (inspection or {}).get("scope"),
        "inspection_shots": [
            {"shot_id": s.get("shot_id"), "scene_id": s.get("scene_id"), "checks": len(s.get("checks", [])), "rendered": len(s.get("rendered", []))}
            for s in (inspection or {}).get("shots", [])
        ],
        "missing_files": [f for f in manifest.get("files", []) if not (output_dir / f).exists()],
    }
    return {"content": [{"type": "text", "text": json.dumps(summary, ensure_ascii=False, indent=2)}]}


HANDLERS = {
    "blender_version": tool_blender_version,
    "blender_previs": tool_blender_previs,
    "blender_previs_inspect": tool_blender_previs_inspect,
}


def respond(message_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": message_id, "result": result}) + "\n")
    sys.stdout.flush()


def error(message_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()


def handle(message):
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}
    if method == "initialize":
        respond(message_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        })
        return
    if method in ("notifications/initialized", "notifications/cancelled"):
        return
    if method == "ping":
        respond(message_id, {})
        return
    if method == "tools/list":
        respond(message_id, {"tools": TOOLS})
        return
    if method == "tools/call":
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            error(message_id, -32602, f"unknown tool: {name}")
            return
        try:
            respond(message_id, handler(params.get("arguments") or {}))
        except Exception as exc:  # noqa: BLE001 - report, never crash the session
            respond(message_id, {"content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}], "isError": True})
        return
    if message_id is not None:
        error(message_id, -32601, f"method not found: {method}")


def main():
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            message = json.loads(raw)
        except ValueError:
            continue
        if isinstance(message, list):
            for item in message:
                handle(item)
        else:
            handle(message)


if __name__ == "__main__":
    main()
