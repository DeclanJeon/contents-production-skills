"""Parser safety tests; synthetic events are not model execution evidence."""
import hashlib
import json
from pathlib import Path
import unittest

from event_trace import parse_trace


ROOT = Path(__file__).resolve().parent


def wire(*events):
    return '\n'.join(json.dumps(event) for event in events)


def final(text='Completed'):
    return {'type': 'message_end', 'message': {'role': 'assistant',
            'content': [{'type': 'text', 'text': text}], 'stopReason': 'stop'}}


END = {'type': 'agent_end', 'messages': []}


def read_events(path='input.md', source=True, error=False):
    result = {'content': [{'type': 'text', 'text': 'read result'}]}
    if source:
        result['details'] = {'meta': {'source': {'type': 'path', 'value': path}}}
    return [
        {'type': 'tool_execution_start', 'toolCallId': 'r1', 'toolName': 'read',
         'args': {'path': path}},
        {'type': 'tool_execution_end', 'toolCallId': 'r1', 'toolName': 'read',
         'result': result, 'isError': error},
    ]


class EventTraceTests(unittest.TestCase):
    def test_reported_local_read_and_quoted_error_are_not_failure(self):
        events = read_events()
        text = 'The example says "cannot read", "file not found", and "usage limit".'
        trace = parse_trace(wire(*events, final(text), END), ROOT)
        self.assertEqual(trace['final_text'], text)
        self.assertEqual(trace['protocol_errors'], [])
        self.assertEqual(trace['tool_errors'], [])
        record = trace['reads'][0]
        self.assertTrue(record['success'])
        self.assertTrue(record['source_confirmed'])
        self.assertEqual(record['local_path'], 'input.md')
        canonical = json.dumps(events[1]['result'], sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        self.assertEqual(record['result_sha256'], hashlib.sha256(canonical.encode()).hexdigest())

    def test_actual_error_is_associated_with_call(self):
        trace = parse_trace(wire(*read_events(error=True), final(), END), ROOT)
        self.assertFalse(trace['reads'][0]['success'])
        self.assertEqual(trace['tool_errors'][0]['tool_call_id'], 'r1')
        self.assertEqual(trace['tool_errors'][0]['tool_name'], 'read')
        self.assertEqual(trace['external_reads'], [])

    def test_args_only_read_cannot_certify_local_source(self):
        trace = parse_trace(wire(*read_events(source=False), final(), END), ROOT)
        record = trace['reads'][0]
        self.assertEqual(record['requested_path'], 'input.md')
        self.assertFalse(record['source_confirmed'])
        self.assertIsNone(record['resolved_path'])
        self.assertIsNone(record['local_path'])

    def test_external_and_global_sources_are_retained(self):
        for path in ('E:/Book/06_Book/book.txt', 'skill://global', str(ROOT.parent / 'outside.md')):
            with self.subTest(path=path):
                trace = parse_trace(wire(*read_events(path), final(), END), ROOT)
                self.assertIsNone(trace['reads'][0]['local_path'])
                self.assertEqual(trace['external_reads'], trace['reads'])
                self.assertEqual(trace['reads'][0]['resolved_path'], path)

    def test_last_completed_answer_ignores_tool_use_and_deltas(self):
        commentary = {'type': 'message_end', 'message': {'role': 'assistant',
                      'content': [{'type': 'text', 'text': 'Reading'}, {'type': 'toolCall', 'id': 'r1'}],
                      'stopReason': 'toolUse'}}
        trace = parse_trace(wire({'type': 'session_start'}, final('first'),
                                {'type': 'message_update'}, final('last'), commentary, END), ROOT)
        self.assertEqual(trace['final_text'], 'last')
        self.assertEqual(trace['protocol_errors'], [])

    def test_malformed_truncated_and_invalid_events_are_rejected(self):
        valid = wire(final(), END)
        for malformed in ('{', '[]', '{"type":1}', '{"type":"message_end","message":null}',
                          '{"type":"tool_execution_end","toolCallId":"x","isError":"false"}'):
            with self.subTest(malformed=malformed):
                self.assertTrue(parse_trace(valid + '\n' + malformed, ROOT)['protocol_errors'])
        trace = parse_trace(wire(*read_events()[:1], final(), END), ROOT)
        self.assertTrue(trace['protocol_errors'])

    def test_missing_agent_or_final_never_completes_protocol(self):
        self.assertFalse(parse_trace(wire(final()), ROOT)['agent_completed'])
        for events in ((final(),), (END,), (END, final()),
                       ({'type': 'message_end', 'message': {'role': 'assistant', 'content':
                         [{'type': 'text', 'text': 'partial'}], 'stopReason': 'length'}}, END)):
            with self.subTest(events=events):
                self.assertTrue(parse_trace(wire(*events), ROOT)['protocol_errors'])


if __name__ == '__main__':
    unittest.main()
