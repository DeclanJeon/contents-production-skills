"""Deferred integration tests: python -m unittest discover -s qa/skill-completeness-95 -p test_run_cases.py"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('run_cases', Path(__file__).with_name('run_cases.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def wire(case, root, text='answer', include_reads=True):
    events = []
    for index, path in enumerate(runner.required_reads(case) if include_reads else []):
        call = str(index)
        events += [
            {'type': 'tool_execution_start', 'toolCallId': call, 'toolName': 'read', 'args': {'path': path}},
            {'type': 'tool_execution_end', 'toolCallId': call, 'toolName': 'read', 'isError': False,
             'result': {'content': [{'type': 'text', 'text': 'local file display'}],
                        'details': {'meta': {'source': {'type': 'path', 'value': str(root / path)}}}}},
        ]
    events += [{'type': 'message_end', 'message': {'role': 'assistant',
                'content': [{'type': 'text', 'text': text}], 'stopReason': 'stop'}},
               {'type': 'agent_end', 'messages': []}]
    return ('\n'.join(json.dumps(event) for event in events) + '\n').encode()


class FrozenCases(unittest.TestCase):
    def setUp(self):
        self.manifest = runner.build_manifest(runner.ROOT)

    def test_supplemental_case_uses_its_exact_checkout_reads_and_context(self):
        paths = ['higgsfield-websites/SKILL.md', 'higgsfield-websites/references/website-flow.md']
        case = {
            'id': 'M-NORMAL-parent-P1',
            'assertion': {'text': '| supplemental | higgsfield-websites | actual'},
            'supplemental_required_reads': paths,
        }
        self.assertEqual(runner.required_reads(case), paths)
        context = runner.case_context(case)
        self.assertIn('Read only the checkout files expressly listed in the user request', context)
        for path in paths:
            self.assertIn(path, context)
    def test_official_case_set_and_exact_fence_bytes(self):
        self.assertEqual(set(c['id'] for c in self.manifest['cases']), runner.EXPECTED)
        for case in self.manifest['cases']:
            source = case['source']
            lines = (runner.ROOT / source['path']).read_bytes().splitlines(keepends=True)
            self.assertEqual(case['prompt'].encode(), b''.join(lines[source['start_line'] - 1:source['end_line']]))

    def test_missing_duplicate_scoring_and_missing_s1_rejected(self):
        for operation in ('missing', 'duplicate', 'scoring', 's1'):
            manifest = copy.deepcopy(self.manifest)
            if operation == 'missing':
                manifest['cases'].pop()
            elif operation == 'duplicate':
                manifest['cases'].append(copy.deepcopy(manifest['cases'][0]))
            elif operation == 'scoring':
                manifest['cases'][0]['id'] = 'Scoring'
            else:
                manifest['cases'] = [c for c in manifest['cases'] if c['id'] != 'S1a']
            with self.subTest(operation=operation), self.assertRaises(ValueError):
                runner.validate_manifest(manifest)

    def test_changed_prompt_cannot_reuse_cache(self):
        case = self.manifest['cases'][0]
        profile = {'model': 'one', 'series': 'readonly'}
        key = runner.identity(case, 'tree-a', profile)
        trace = runner.parse_trace(wire(case, runner.ROOT).decode(), runner.ROOT)
        previous = {'identity': key, 'status': 'completed', 'exit_code': 0, 'stdout': 'answer',
                    'output_mode': 'json', 'structured_evidence': trace,
                    'required_reads': runner.required_reads(case)}
        self.assertTrue(runner.reusable(previous, key))
        self.assertFalse(runner.reusable({'identity': key, 'status': 'completed',
                                         'exit_code': 0, 'stdout': 'answer'}, key))
        for changed_case, tree, changed_profile in [
            ({**case, 'prompt_sha256': 'changed'}, 'tree-a', profile),
            (case, 'tree-b', profile),
            (case, 'tree-a', {**profile, 'model': 'two'}),
            (case, 'tree-a', {**profile, 'series': 'other'}),
        ]:
            self.assertFalse(runner.reusable(previous, runner.identity(changed_case, tree, changed_profile)))

    def test_failure_classes_never_reused(self):
        for stdout, stderr, code, timeout, expected in [
            ('  ', '', 0, False, 'blank-output'),
            ('partial', '', -1, True, 'timeout'),
            ('partial', 'Cannot read required file', 0, False, 'file-read-failure'),
            ('partial', 'permission denied', 1, False, 'permission-error'),
            ('partial', '', 1, False, 'nonzero-exit'),
        ]:
            with self.subTest(expected=expected):
                status = runner.classify(stdout, stderr, code, timeout)
                self.assertEqual(status, expected)
                self.assertFalse(runner.reusable({'identity': 'k', 'status': status,
                                                  'stdout': stdout, 'stderr': stderr, 'exit_code': code}, 'k'))

    def test_tree_covers_assets_config_and_ignores_run_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'skill' / 'assets').mkdir(parents=True)
            asset = root / 'skill/assets/a.bin'
            asset.write_bytes(b'first')
            before = runner.tree_fingerprint(root)
            (root / 'qa').mkdir()
            (root / 'qa/evidence.json').write_text('{}')
            self.assertEqual(before, runner.tree_fingerprint(root))
            asset.write_bytes(b'second')
            after = runner.tree_fingerprint(root)
            self.assertNotEqual(before, after)
            (root / 'manifest.json').write_text('{}')
            self.assertNotEqual(after, runner.tree_fingerprint(root))

    def test_archival_doc_images_do_not_replace_instruction_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / 'docs'
            docs.mkdir()
            image = docs / 'historical-frame.png'
            image.write_bytes(b'old archive image')
            guide = docs / 'instructions.md'
            guide.write_text('first instruction')
            before = runner.tree_fingerprint(root)
            image.write_bytes(b'new archive image')
            self.assertEqual(before, runner.tree_fingerprint(root))
            guide.write_text('changed instruction')
            self.assertNotEqual(before, runner.tree_fingerprint(root))

    def test_failed_attempt_survives_success_and_success_remains_unreviewed(self):
        case = self.manifest['cases'][0]
        profile = {'executable': 'omp', 'model': 'model', 'max_time': 90}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            process = unittest.mock.Mock()
            process.communicate.side_effect = [(b'partial', b'failure'), (wire(case, root), b'')]
            process.returncode = 1
            with patch.object(runner.subprocess, 'Popen', return_value=process), patch.object(runner, 'tree_fingerprint', return_value='tree'):
                first = runner.execute(case, root, root / 'runs', profile, 'tree')
                process.returncode = 0
                second = runner.execute(case, root, root / 'runs', profile, 'tree')
                third = runner.execute(case, root, root / 'runs', profile, 'tree')
            self.assertEqual(first['verdict'], 'ERROR')
            self.assertEqual(second['verdict'], 'UNREVIEWED')
            self.assertEqual(third, second)
            attempts = sorted((root / 'runs' / case['id']).glob('attempt-*.json'))
            self.assertEqual(len(attempts), 2)
            self.assertEqual(attempts[0].with_suffix('.stdout').read_bytes(), b'partial')

    def test_timeout_preserves_partial_output(self):
        case = self.manifest['cases'][0]
        profile = {'executable': 'omp', 'model': 'model', 'max_time': 90}
        process = unittest.mock.Mock()
        process.communicate.side_effect = [subprocess.TimeoutExpired('omp', 105), (b'partial', b'timed out')]
        process.returncode = -1
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(runner.subprocess, 'Popen', return_value=process), patch.object(runner.subprocess, 'run'), patch.object(runner, 'tree_fingerprint', return_value='tree'):
                record = runner.execute(case, root, root / 'runs', profile, 'tree')
            self.assertEqual(record['status'], 'timeout')
            self.assertEqual(Path(record['command'][0]).name, 'omp')
            self.assertEqual((root / 'runs' / case['id'] / 'attempt-0001.stdout').read_bytes(), b'partial')

    def test_mutation_invalidates_completed_response(self):
        case = self.manifest['cases'][0]
        process = unittest.mock.Mock()
        process.communicate.return_value = (wire(case, runner.ROOT), b'')
        process.returncode = 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(runner.subprocess, 'Popen', return_value=process), patch.object(runner, 'tree_fingerprint', return_value='new-tree'):
                record = runner.execute(case, root, root / 'runs', {'executable': 'omp', 'model': 'm', 'max_time': 90}, 'old-tree')
            self.assertEqual(record['status'], 'tree-mutated')
            self.assertEqual(record['verdict'], 'ERROR')

    def test_quoted_failure_prose_is_not_an_execution_error(self):
        case = self.manifest['cases'][0]
        answer = 'Quoted examples: cannot read; file not found; usage limit.'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            process = unittest.mock.Mock(returncode=0)
            process.communicate.return_value = (wire(case, root, answer), b'')
            with patch.object(runner.subprocess, 'Popen', return_value=process), patch.object(runner, 'tree_fingerprint', return_value='tree'):
                result = runner.execute(case, root, root / 'runs',
                                        {'executable': 'omp', 'model': 'm', 'max_time': 180}, 'tree')
            self.assertEqual(result['stdout'], answer)
            self.assertEqual(result['status'], 'completed')
            self.assertEqual(result['verdict'], 'UNREVIEWED')

    def test_missing_checkout_reads_are_not_cacheable(self):
        case = self.manifest['cases'][0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            process = unittest.mock.Mock(returncode=0)
            process.communicate.return_value = (wire(case, root, include_reads=False), b'')
            with patch.object(runner.subprocess, 'Popen', return_value=process), patch.object(runner, 'tree_fingerprint', return_value='tree'):
                result = runner.execute(case, root, root / 'runs',
                                        {'executable': 'omp', 'model': 'm', 'max_time': 180}, 'tree')
            self.assertEqual(result['status'], 'checkout-read-missing')
            self.assertEqual(result['missing_required_reads'], runner.required_reads(case))
            self.assertEqual(result['verdict'], 'ERROR')
            self.assertFalse(runner.reusable(result, result['identity']))


if __name__ == '__main__':
    unittest.main()
