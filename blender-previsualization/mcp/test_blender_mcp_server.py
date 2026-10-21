#!/usr/bin/env python3
"""Tests for the Blender MCP server (no Blender runtime required)."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SERVER = Path(__file__).resolve().parent / "blender_mcp_server.py"
spec = importlib.util.spec_from_file_location("blender_mcp_server", SERVER)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class McpServerTests(unittest.TestCase):
    def call(self, message):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            server.handle(message)
        out = buffer.getvalue().strip()
        return json.loads(out) if out else None

    def test_initialize_advertises_tools_capability(self):
        reply = self.call({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(reply["id"], 1)
        self.assertEqual(reply["result"]["serverInfo"]["name"], "blender-previs")
        self.assertIn("tools", reply["result"]["capabilities"])

    def test_tools_list_exposes_three_tools_with_schemas(self):
        reply = self.call({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = [t["name"] for t in reply["result"]["tools"]]
        self.assertEqual(names, ["blender_version", "blender_previs", "blender_previs_inspect"])
        for tool in reply["result"]["tools"]:
            self.assertIn("inputSchema", tool)
            self.assertEqual(tool["inputSchema"]["type"], "object")

    def test_unknown_tool_is_rejected(self):
        reply = self.call({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "nope", "arguments": {}}})
        self.assertIn("error", reply)

    def test_previs_refuses_existing_output_and_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp)
            spec_file = existing / "spec.json"
            spec_file.write_text("{}", encoding="utf-8")
            reply = self.call({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
                "name": "blender_previs", "arguments": {"spec_path": str(spec_file), "output_dir": str(existing)}}})
            self.assertTrue(reply["result"].get("isError"))
            self.assertIn("refusing", reply["result"]["content"][0]["text"])
            reply = self.call({"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {
                "name": "blender_previs", "arguments": {"spec_path": "relative.json", "output_dir": "relative-out"}}})
            self.assertTrue(reply["result"].get("isError"))
            self.assertIn("absolute", reply["result"]["content"][0]["text"])

    def test_previs_reports_missing_spec_without_running_blender(self):
        reply = self.call({"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {
            "name": "blender_previs", "arguments": {"spec_path": "/nonexistent/spec.json", "output_dir": "/tmp/never-created-by-test"}}})
        self.assertTrue(reply["result"].get("isError"))
        self.assertIn("spec not found", reply["result"]["content"][0]["text"])

    def test_inspect_reports_missing_folder(self):
        reply = self.call({"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {
            "name": "blender_previs_inspect", "arguments": {"output_dir": "/nonexistent/previs"}}})
        self.assertTrue(reply["result"].get("isError"))

    def test_adapter_resolution_prefers_environment_then_installed_roots(self):
        import os
        import tempfile
        previous = {k: os.environ.get(k) for k in ("BLENDER_PREVIS_ADAPTER", "BLENDER_PREVIS_SKILL_ROOT")}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "blender-previsualization"
                (root / "scripts").mkdir(parents=True)
                adapter = root / "scripts" / "build_previs.py"
                adapter.write_text("# adapter\n", encoding="utf-8")
                os.environ["BLENDER_PREVIS_ADAPTER"] = str(adapter)
                self.assertEqual(server.resolve_adapter(), adapter.resolve())
                os.environ.pop("BLENDER_PREVIS_ADAPTER")
                os.environ["BLENDER_PREVIS_SKILL_ROOT"] = str(root)
                self.assertEqual(server.resolve_adapter(), adapter.resolve())
                os.environ["BLENDER_PREVIS_SKILL_ROOT"] = str(Path(tmp) / "missing")
                self.assertIn(Path(tmp) / "missing", server.skill_root_candidates())
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_launcher_finds_the_shipped_server(self):
        launcher = SERVER.parent / "blender_mcp_server_launcher.py"
        self.assertTrue(launcher.is_file())
        spec = importlib.util.spec_from_file_location("blender_mcp_server_launcher", launcher)
        launcher_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launcher_module)
        found = launcher_module.find_server()
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "blender_mcp_server.py")


if __name__ == "__main__":
    unittest.main()
