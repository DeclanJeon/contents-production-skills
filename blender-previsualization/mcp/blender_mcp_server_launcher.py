#!/usr/bin/env python3
"""Global launcher for the blender-previsualization MCP server.

Installs as a PATH command so an MCP host can start the server without
knowing where the skill package lives:

    ~/.local/bin/blender-mcp-server

The launcher resolves the installed skill in this order:

1. ``BLENDER_PREVIS_SKILL_ROOT`` environment variable
2. the root recorded by the installer (``~/.config/blender-mcp/skill_root``)
3. the usual installed-skill roots (``~/.codex/skills``, ``~/.pi/agent/skills``,
   ``~/.claude/skills``, ``~/.agents/skills``)
4. the copy shipped next to this launcher

It then runs that skill's ``mcp/blender_mcp_server.py`` unchanged, so the MCP
contract stays owned by the skill package.
"""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

SERVER_RELATIVE = Path("mcp") / "blender_mcp_server.py"


def candidate_roots():
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
    here = Path(__file__).resolve().parent
    roots.append(here.parent)
    roots.append(here)
    return roots


def find_server():
    for root in candidate_roots():
        candidate = root / SERVER_RELATIVE
        if candidate.is_file():
            return candidate.resolve()
    return None


def main() -> int:
    server = find_server()
    if server is None:
        sys.stderr.write(
            "blender-mcp-server: could not locate blender-previsualization/mcp/blender_mcp_server.py.\n"
            "Set BLENDER_PREVIS_SKILL_ROOT to the installed skill root, or run\n"
            "  python3 <repo>/blender-previsualization/mcp/install_global_launcher.py\n"
        )
        return 2
    sys.argv[0] = str(server)
    runpy.run_path(str(server), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
