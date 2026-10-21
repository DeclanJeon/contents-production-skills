#!/usr/bin/env python3
"""Install the global `blender-mcp-server` launcher and point MCP hosts at it.

The launcher is a PATH command, so the MCP registration no longer embeds a
checkout path: if the skill package moves, the recorded skill root or the
installed-skill roots keep resolving.

    python3 blender-previsualization/mcp/install_global_launcher.py
    python3 blender-previsualization/mcp/install_global_launcher.py --update-pi

Steps:
1. copy the launcher to ``<target-dir>/blender-mcp-server`` (default
   ``~/.local/bin``) and make it executable;
2. record the resolved skill root in ``~/.config/blender-mcp/skill_root``;
3. with ``--update-pi``, rewrite the ``blender`` entry of
   ``~/.pi/agent/mcp.json`` to use the launcher command;
4. always print the Codex ``config.toml`` snippet to add.

Nothing is installed into a system directory and no package manager is used.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path

LAUNCHER_NAME = "blender-mcp-server"
LAUNCHER_SOURCE = Path(__file__).resolve().parent / "blender_mcp_server_launcher.py"
SKILL_ROOT = Path(__file__).resolve().parent.parent


def install_launcher(target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / LAUNCHER_NAME
    shutil.copyfile(LAUNCHER_SOURCE, target)
    mode = os.stat(target).st_mode
    os.chmod(target, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


def record_skill_root(root: Path) -> Path:
    config_dir = Path.home() / ".config" / "blender-mcp"
    config_dir.mkdir(parents=True, exist_ok=True)
    target = config_dir / "skill_root"
    target.write_text(str(root) + "\n", encoding="utf-8")
    return target


def update_pi_config(command: str) -> bool:
    path = Path.home() / ".pi" / "agent" / "mcp.json"
    if not path.is_file():
        return False
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return False
    servers = config.setdefault("mcpServers", {})
    entry = servers.get("blender")
    if not isinstance(entry, dict):
        return False
    entry["command"] = command
    entry.pop("args", None)
    entry.setdefault("description", "Blender previs runner (blender-previsualization skill adapter, CLI-backed)")
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target-dir", default=str(Path.home() / ".local" / "bin"), help="directory for the launcher (default ~/.local/bin)")
    parser.add_argument("--update-pi", action="store_true", help="rewrite the blender entry of ~/.pi/agent/mcp.json to use the launcher")
    args = parser.parse_args()

    if not LAUNCHER_SOURCE.is_file():
        sys.stderr.write(f"launcher source missing: {LAUNCHER_SOURCE}\n")
        return 2
    target = install_launcher(Path(args.target_dir).expanduser())
    recorded = record_skill_root(SKILL_ROOT)
    print(f"launcher installed: {target}")
    print(f"skill root recorded: {recorded}")
    on_path = shutil.which(LAUNCHER_NAME)
    print(f"on PATH: {on_path or 'NOT FOUND - add the target dir to PATH'}")
    if args.update_pi:
        print(f"pi mcp.json updated: {update_pi_config(on_path or str(target))}")
    print("\nCodex ~/.codex/config.toml snippet:")
    print("\n[mcp_servers.blender]")
    print(f'command = "{on_path or str(target)}"')
    print("startup_timeout_sec = 60")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
