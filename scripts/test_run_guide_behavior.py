"""Offline tests for the behavioral runner's evidence contract, never model calls."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("run_guide_behavior", Path(__file__).with_name("run_guide_behavior.py"))
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def wire(*events):
    return "\n".join(json.dumps(e, ensure_ascii=False) for e in events) + "\n"


def final(text="final", reason="stop"):
    return {"type": "message_end", "message": {"role": "assistant", "stopReason": reason,
            "model": "test-model", "content": [{"type": "text", "text": text}]}}


class FingerprintTests(unittest.TestCase):
    def test_installed_support_manifest_matches_source_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'one').mkdir()
            (root / 'one/SKILL.md').write_text('same skill', encoding='utf-8')
            manifest = json.dumps({'skills': ['one']})
            (root / 'manifest.json').write_text(manifest, encoding='utf-8')
            source = runner.fingerprint(root)
            (root / 'manifest.json').unlink()
            support = root / 'video-production-assets/support'
            support.mkdir(parents=True)
            (support / 'manifest.json').write_text(manifest, encoding='utf-8')
            self.assertEqual(source, runner.fingerprint(root))

    def test_repository_manifest_has_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'manifest.json').write_text('{}', encoding='utf-8')
            self.assertEqual(runner.package_manifest(root), root / 'manifest.json')


class TraceTests(unittest.TestCase):
    def test_uses_authoritative_message_not_delta(self):
        stream = wire({"type": "message_update", "assistantMessageEvent": {"type": "text_delta", "delta": "stale"}},
                      final("authoritative"), {"type": "agent_settled", "aborted": False})
        trace = runner.parse_events(stream, Path.cwd())
        self.assertEqual(trace["final_text"], "authoritative")
        self.assertEqual(trace["final_stop_reason"], "stop")
        self.assertTrue(trace["settled"])

    def test_unicode_line_separator_is_not_jsonl_boundary(self):
        trace = runner.parse_events(wire(final("a\u2028b")), Path.cwd())
        self.assertEqual(trace["final_text"], "a\u2028b")
        self.assertFalse(trace["protocol_errors"])

    def test_agent_end_does_not_replace_settled(self):
        trace = runner.parse_events(wire(final(), {"type": "agent_end", "willRetry": True}), Path.cwd())
        self.assertFalse(trace["settled"])

    def test_error_length_abort_and_invalid_json_are_preserved(self):
        for reason in ("error", "length", "aborted"):
            with self.subTest(reason=reason):
                trace = runner.parse_events(wire(final(reason=reason)), Path.cwd())
                self.assertTrue(trace["protocol_errors"])
        trace = runner.parse_events("not json\n", Path.cwd())
        self.assertEqual(trace["protocol_errors"], ["invalid JSONL record 1"])

    def test_successful_read_is_bound_to_start_arguments(self):
        root = Path.cwd()
        owner = runner.OWNER["F04"]
        stream = wire({"type": "tool_execution_start", "toolCallId": "x", "toolName": "read", "args": {"path": owner, "limit": 10}},
                      {"type": "tool_execution_end", "toolCallId": "x", "toolName": "read", "isError": False})
        trace = runner.parse_events(stream, root)
        self.assertEqual(trace["reads"][0]["local_path"], owner)
        self.assertEqual(trace["reads"][0]["limit"], 10)
        self.assertTrue(trace["reads"][0]["success"])
        self.assertEqual(trace["tool_calls"][0]["args"]["path"], owner)

    def test_failed_read_is_not_consumption_evidence(self):
        stream = wire({"type": "tool_execution_start", "toolCallId": "x", "toolName": "read", "args": {"path": "missing.md"}},
                      {"type": "tool_execution_end", "toolCallId": "x", "toolName": "read", "isError": True})
        trace = runner.parse_events(stream, Path.cwd())
        self.assertFalse(trace["reads"][0]["success"])
        self.assertTrue(trace["tool_errors"])


class ExecutionTests(unittest.TestCase):
    def execute_fake(self, reason="stop", settled=True, tool="read", changed=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "outputs"
            out.mkdir()
            owner = runner.OWNER["F04"]
            p = root / owner
            p.parent.mkdir(parents=True)
            p.write_text("owner", encoding="utf-8")
            events = [{"type": "tool_execution_start", "toolCallId": "x", "toolName": tool, "args": {"path": owner}},
                      {"type": "tool_execution_end", "toolCallId": "x", "toolName": tool, "isError": False}, final(reason=reason)]
            if settled:
                events.append({"type": "agent_settled", "aborted": False})
            with patch.object(runner.subprocess, "Popen") as popen, patch.object(runner, "fingerprint", return_value={"sha256": "new" if changed else "old"}):
                process = popen.return_value
                process.communicate.return_value = (wire(*events).encode(), b"")
                process.returncode = 0
                result = runner.execute({"id": "F04-test", "prompt": "원문\n그대로"}, root, out,
                    {"executable": "pi", "provider": "test", "model": "test", "timeout_seconds": 3}, "old")
            record = json.loads((out / "F04-test.attempt.json").read_text())
            return result, record

    def test_completed_run_is_unreviewed_not_pass(self):
        result, record = self.execute_fake()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["verdict"], "UNREVIEWED")
        self.assertEqual(record["prompt"], "원문\n그대로")
        self.assertEqual(record["command"][-1], record["prompt"])
        self.assertIn("--no-mcp", record["command"])
        self.assertIn("--no-context-files", record["command"])
        self.assertIn("read,grep,find,ls", record["command"])
        self.assertNotIn("--api-key", record["command"])

    def test_zero_exit_with_length_or_missing_settled_is_error(self):
        self.assertEqual(self.execute_fake(reason="length")[0]["status"], "execution_error")
        self.assertEqual(self.execute_fake(settled=False)[0]["status"], "execution_error")

    def test_missing_owner_read_and_changed_sources_are_rejected(self):
        self.assertEqual(self.execute_fake(tool="grep")[0]["status"], "owner_not_read")
        self.assertEqual(self.execute_fake(changed=True)[0]["status"], "source_mutated")

    def test_save_new_preserves_earlier_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "attempt.json"
            runner.save_new(path, {"first": True})
            with self.assertRaises(FileExistsError):
                runner.save_new(path, {"second": True})
            self.assertEqual(json.loads(path.read_text()), {"first": True})


if __name__ == "__main__":
    unittest.main()
