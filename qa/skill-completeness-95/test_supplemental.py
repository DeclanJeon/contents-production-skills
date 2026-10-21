"""Supplemental cases stay separate and use their declared owner reads."""
import importlib.util
from pathlib import Path
import sys
import unittest

QA = Path(__file__).resolve().parent
sys.path.insert(0, str(QA))
spec = importlib.util.spec_from_file_location('run_supplemental', QA / 'run_supplemental.py')
supplemental = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supplemental)


class SupplementalCases(unittest.TestCase):
    def test_case_uses_manifest_owner_and_required_checkout_paths(self):
        paths = ['higgsfield-websites/SKILL.md', 'higgsfield-websites/references/website-flow.md']
        scenario = {'id': 'parent-P1', 'owner': 'higgsfield-websites',
                    'prompt': 'Review publish gate.', 'required_reads': paths}
        case = supplemental.case_for(scenario, Path('supplemental-manifest.json'))
        self.assertEqual(case['id'], 'M-NORMAL-parent-P1')
        self.assertEqual(case['supplemental_required_reads'], paths)
        self.assertEqual(supplemental.runner.required_reads(case), paths)
        context = supplemental.runner.case_context(case)
        for path in paths:
            self.assertIn(path, context)
    def test_selected_scenarios_run_only_named_cases_in_manifest_order(self):
        scenarios = [
            {'id': 'FIRST'},
            {'id': 'CAST-SSOT'},
            {'id': 'LAST'},
        ]
        select = getattr(supplemental, 'select_scenarios', None)
        self.assertTrue(callable(select), 'runner must expose scenario selection')
        self.assertEqual(select(scenarios, ['CAST-SSOT']), [scenarios[1]])
        with self.assertRaises(ValueError):
            select(scenarios, ['CAST-SSOT', 'CAST-SSOT'])
        with self.assertRaises(ValueError):
            select(scenarios, ['UNKNOWN'])

    def test_max_time_override_accepts_positive_seconds_only(self):
        parse_max_time = getattr(supplemental, 'parse_max_time', None)
        self.assertTrue(callable(parse_max_time), 'runner must validate max time')
        self.assertEqual(parse_max_time('420'), 420)
        for value in ('0', '-1', 'later'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_max_time(value)
