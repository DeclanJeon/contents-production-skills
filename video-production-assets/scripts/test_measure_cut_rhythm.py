"""Cut-rhythm measurement regressions.

The report is a measurement of plan-versus-actual. It never scores aesthetics:
no energy/duration ranking, no moving/static ratio, no pass threshold.
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

from measure_cut_rhythm import (build_report, compute_stats, cuts_from_project,
                                handle_shortfalls, main, read_cuts_csv,
                                segment_report)
from test_validate_storyboard import RHYTHM_VALID, board, with_rhythm


def write_cuts(dirpath, rows, header=('cut_id', 'start_s', 'end_s')):
    path = Path(dirpath) / 'cuts.csv'
    with path.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(list(header))
        w.writerows(rows)
    return path


def cut(cut_id, shot_id, start, end):
    return {'cut_id': cut_id, 'shot_id': shot_id, 'start_s': start, 'end_s': end,
            'duration_s': round(end - start, 6),
            'planned_duration_s': round(end - start, 6), 'delta_s': 0.0}


class MeasurementTests(unittest.TestCase):
    def test_planned_only_uses_project_shot_boundaries(self):
        cuts = cuts_from_project(board())
        self.assertEqual([c['shot_id'] for c in cuts], ['SH01', 'SH02'])
        self.assertEqual([c['duration_s'] for c in cuts], [2.0, 2.0])
        self.assertTrue(all(c['delta_s'] == 0 for c in cuts))

    def test_cuts_csv_durations_and_stats(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_cuts(d, [('M1', 0, 4.0), ('M2', 4, 8.1), ('M3', 8.1, 12.3),
                                  ('M4', 12.3, 13.3), ('M5', 13.3, 22.3), ('M6', 22.3, 25.3)])
            cuts, meta = read_cuts_csv(path, board(), 0.5)
        stats = compute_stats(cuts, board()['shots'], 2.0, 8.0, 10.0)
        self.assertEqual(stats['count'], 6)
        self.assertAlmostEqual(stats['mean_s'], 4.2167, places=3)
        self.assertAlmostEqual(stats['stdev_s'], 2.4072, places=3)
        self.assertAlmostEqual(stats['short_pct'], 16.667, places=2)
        self.assertAlmostEqual(stats['long_pct'], 16.667, places=2)
        self.assertEqual(stats['same_shot_size_basis'], 'raw_string_equality')

    def test_monotony_run_detected(self):
        cuts = [cut(f'M{i}', None, start, start + duration)
                for i, (start, duration) in enumerate(
                    [(0, 3.0), (3.0, 3.1), (6.1, 2.9), (9.0, 7.0)])]
        stats = compute_stats(cuts, [], 2.0, 8.0, 10.0)
        self.assertIn([0, 1, 2], stats['monotony_runs'])

    def test_same_shot_size_runs_raw_string_equality(self):
        shots = [{'id': f'SH0{i}', 'start_s': i, 'end_s': i + 1,
                  'camera': {'shot_size': size, 'movement': 'static'}}
                 for i, size in enumerate(['medium', 'medium', 'medium', 'close'], start=1)]
        cuts = [cut(f'M{i}', f'SH0{i}', i, i + 1) for i in range(1, 5)]
        stats = compute_stats(cuts, shots, 2.0, 8.0, 10.0)
        self.assertIn([0, 1, 2], stats['same_shot_size_runs'])
        self.assertEqual(stats['same_shot_size_basis'], 'raw_string_equality')

    def test_unmatched_detected_cut_reports_partial(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_cuts(d, [('M1', 0, 1.1), ('M2', 1.1, 2.0),
                                  ('M3', 2.0, 3.9), ('M4', 3.9, 4.0)])
            cuts, meta = read_cuts_csv(path, board(), 0.5)
        self.assertTrue(meta['unmatched_detected'])
        report = build_report(board(), cuts, {'fps': 24, 'source': 'cuts_csv'}, 'partial')
        self.assertEqual(report['status'], 'partial')
        self.assertEqual(report['aesthetics'], 'not_judged')

    def test_fps_mismatch_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d) / 'project.json'
            proj.write_text(json.dumps(board()))
            self.assertEqual(main(['--project', str(proj), '--fps', '30']), 2)

    def test_cuts_csv_unknown_shot_id_is_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_cuts(d, [('M1', 0, 2.0, 'SH99')],
                              header=('cut_id', 'start_s', 'end_s', 'shot_id'))
            with self.assertRaises(ValueError):
                read_cuts_csv(path, board(), 0.5)

    def test_handle_shortfall_uses_realized_capacity(self):
        p = with_rhythm(board(), RHYTHM_VALID)
        for shot in p['shots']:
            shot['source_duration_s'] = shot['end_s'] - shot['start_s']
        shortfalls = handle_shortfalls(p)
        self.assertTrue(any('SH02' in m for m in shortfalls), shortfalls)
        self.assertFalse(any('SH01' in m for m in shortfalls), shortfalls)

    def test_segment_report_compares_planned_and_measured(self):
        cuts = [cut('M1', 'SH01', 0, 2.0), cut('M2', 'SH02', 2.0, 4.0)]
        segments = segment_report(with_rhythm(board(), RHYTHM_VALID), cuts)
        self.assertEqual([s['rhythm_id'] for s in segments], ['RB01', 'RB02'])
        self.assertEqual(segments[0]['measured_duration_s'], 2.0)
        self.assertEqual(segments[0]['delta_s'], 0.0)
        self.assertEqual(segments[0]['evidence'], 'measured')

    def test_planned_only_report_marks_basis(self):
        with tempfile.TemporaryDirectory() as d:
            proj = Path(d) / 'project.json'
            proj.write_text(json.dumps(with_rhythm(board(), RHYTHM_VALID)))
            out = Path(d) / 'report.json'
            self.assertEqual(main(['--project', str(proj), '--out', str(out)]), 0)
            report = json.loads(out.read_text())
        self.assertEqual(report['status'], 'planned_only')
        self.assertEqual(report['basis']['source'], 'project_plan')


if __name__ == '__main__':
    unittest.main()
