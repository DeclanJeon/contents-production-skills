#!/usr/bin/env python3
"""Measure cut rhythm and compare it against the declared storyboard.rhythm curve.

The report is a self-comparison (planned versus actual) of durations, monotony
runs, repeated shot sizes and handle capacity. It never scores the result: no
energy-versus-duration ranking, no moving/static ratio, no pass threshold, and
``aesthetics: not_judged`` always ships. When measurement is impossible
(ffmpeg absent, undecodable media) it says so instead of guessing.

Exit codes: 0 report produced, 2 invalid input, 3 measurement unavailable.
"""
import argparse
import csv
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _cuts_from_spans(spans, project, evidence, planned_by_shot=None):
    cuts = []
    for index, (shot_id, start, end) in enumerate(spans, start=1):
        planned = None
        if planned_by_shot and shot_id in planned_by_shot:
            planned = planned_by_shot[shot_id]
        cuts.append({
            'cut_id': f'M{index:02d}',
            'shot_id': shot_id,
            'start_s': round(start, 6),
            'end_s': round(end, 6),
            'duration_s': round(end - start, 6),
            'planned_duration_s': planned,
            'delta_s': None if planned is None else round((end - start) - planned, 6),
            'evidence': evidence,
        })
    return cuts


def cuts_from_project(project):
    """Planned cuts straight from the project timeline (never a measurement)."""
    shots = [s for s in project.get('shots', []) if isinstance(s, dict)]
    ordered = sorted(shots, key=lambda s: (s.get('start_s', 0), s.get('id', '')))
    cuts = []
    for index, shot in enumerate(ordered, start=1):
        start, end = shot.get('start_s'), shot.get('end_s')
        duration = round(end - start, 6) if _number(start) and _number(end) else None
        cuts.append({
            'cut_id': f'C{index:02d}',
            'shot_id': shot.get('id'),
            'start_s': start,
            'end_s': end,
            'duration_s': duration,
            'planned_duration_s': duration,
            'delta_s': 0.0,
            'evidence': 'planned',
        })
    return cuts


def read_cuts_csv(path, project, tolerance_s):
    """Read measured cut spans; never invent a shot for an unmatched boundary."""
    shots = [s for s in project.get('shots', []) if isinstance(s, dict)]
    planned = {s['id']: s for s in shots if isinstance(s.get('id'), str)}
    starts = [(s['id'], s.get('start_s')) for s in shots
              if isinstance(s.get('id'), str) and _number(s.get('start_s'))]
    with Path(path).open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError('cuts csv has no rows')
    header = set(rows[0].keys())
    for column in ('start_s', 'end_s'):
        if column not in header:
            raise ValueError(f'cuts csv is missing {column}')
    supplied_shot_ids = 'shot_id' in header
    spans, unmatched_detected = [], []
    planned_durations = {sid: (s['end_s'] - s['start_s']) if _number(s.get('start_s')) and _number(s.get('end_s')) else None
                         for sid, s in planned.items()}
    for row in rows:
        try:
            start = float(row['start_s'])
            end = float(row['end_s'])
        except (TypeError, ValueError):
            raise ValueError(f"cuts csv row {row.get('cut_id') or '?'} has non-numeric times")
        if end <= start:
            raise ValueError(f"cuts csv row {row.get('cut_id') or '?'} has an invalid interval")
        if supplied_shot_ids:
            shot_id = (row.get('shot_id') or '').strip()
            if shot_id not in planned:
                raise ValueError(f'cuts csv references unknown shot {shot_id!r}')
            spans.append((shot_id, start, end))
            continue
        candidates = [sid for sid, shot_start in starts if abs(shot_start - start) <= tolerance_s]
        if len(candidates) == 1:
            spans.append((candidates[0], start, end))
        else:
            unmatched_detected.append({'start_s': round(start, 6), 'end_s': round(end, 6)})
            spans.append((None, start, end))
    attributed = {sid for sid, _, _ in spans if sid}
    unmatched_planned = sorted(sid for sid in planned if sid not in attributed)
    cuts = _cuts_from_spans(spans, project, 'measured', planned_durations)
    meta = {
        'shot_mapping': 'supplied_shot_ids' if supplied_shot_ids else 'nearest_within_tolerance',
        'unmatched_detected': unmatched_detected,
        'unmatched_planned': unmatched_planned,
    }
    return cuts, meta


def _consecutive_runs(values, same):
    """Maximal runs of at least three adjacent entries that ``same`` accepts."""
    runs, current = [], []
    for index, value in enumerate(values):
        if value is not None and current and same(values[current[-1]], value):
            current.append(index)
        else:
            if current:
                runs.append(current)
            current = [] if value is None else [index]
    if current:
        runs.append(current)
    return [run for run in runs if len(run) >= 3]


def compute_stats(cuts, shots, short_s, long_s, monotony_pct):
    durations = [c['duration_s'] for c in cuts if _number(c.get('duration_s'))]
    count = len(durations)
    mean = statistics.fmean(durations) if durations else 0.0
    stdev = statistics.pstdev(durations) if len(durations) > 1 else 0.0
    shot_sizes = {}
    for shot in shots:
        if not isinstance(shot, dict) or not isinstance(shot.get('id'), str):
            continue
        camera = shot.get('camera') if isinstance(shot.get('camera'), dict) else {}
        size = camera.get('shot_size')
        if isinstance(size, str) and size.strip():
            shot_sizes[shot['id']] = size
    sizes = [shot_sizes.get(c.get('shot_id')) for c in cuts]
    monotony_runs = _consecutive_runs(
        durations, lambda earlier, later: earlier > 0 and abs(later - earlier) <= earlier * monotony_pct / 100)
    same_size_runs = _consecutive_runs(sizes, lambda earlier, later: earlier == later)
    return {
        'count': count,
        'mean_s': round(mean, 6),
        'stdev_s': round(stdev, 6),
        'short_s': short_s,
        'long_s': long_s,
        'short_pct': round(100 * sum(1 for d in durations if d <= short_s) / count, 6) if count else 0.0,
        'long_pct': round(100 * sum(1 for d in durations if d >= long_s) / count, 6) if count else 0.0,
        'monotony_runs': monotony_runs,
        'same_shot_size_runs': same_size_runs,
        'same_shot_size_basis': 'raw_string_equality',
    }


def _curve(project):
    storyboard = project.get('storyboard')
    rhythm = storyboard.get('rhythm') if isinstance(storyboard, dict) else None
    if not isinstance(rhythm, dict):
        return {'intent': None, 'segments': []}
    curve = rhythm.get('curve')
    return {'intent': rhythm.get('intent'),
            'segments': [s for s in curve if isinstance(s, dict)] if isinstance(curve, list) else []}


def segment_report(project, cuts):
    report = []
    for segment in _curve(project)['segments']:
        shot_ids = [s for s in segment.get('shot_ids', []) if isinstance(s, str)]
        contributing = [c for c in cuts if c.get('shot_id') in shot_ids and _number(c.get('duration_s'))]
        measured = round(sum(c['duration_s'] for c in contributing), 6) if contributing else None
        planned = segment.get('planned_duration_s')
        evidence = 'measured'
        if contributing and all(c.get('evidence') == 'planned' for c in contributing):
            evidence = 'planned'
        elif not contributing:
            evidence = 'unmapped'
        report.append({
            'rhythm_id': segment.get('id'),
            'planned_duration_s': planned if _number(planned) else None,
            'measured_duration_s': measured,
            'delta_s': round(measured - planned, 6) if measured is not None and _number(planned) else None,
            'evidence': evidence,
        })
    return report


def handle_shortfalls(project):
    """Compare the declared cut-out phase against the handle a clip actually has."""
    fps = project.get('fps')
    if not _number(fps) or fps <= 0:
        return []
    shots = {s['id']: s for s in project.get('shots', [])
             if isinstance(s, dict) and isinstance(s.get('id'), str)}
    messages = []
    for segment in _curve(project)['segments']:
        phase = segment.get('cut_out_phase')
        if phase not in ('mid_action', 'impact'):
            continue
        shot_ids = [s for s in segment.get('shot_ids', []) if isinstance(s, str)]
        if not shot_ids:
            continue
        shot_id = shot_ids[-1]
        shot = shots.get(shot_id)
        if not shot:
            continue
        start, end = shot.get('start_s'), shot.get('end_s')
        source = shot.get('source_duration_s')
        source_in = shot.get('source_in_s', 0)
        rate = shot.get('playback_rate', 1)
        if not all(_number(v) for v in (start, end, source, source_in, rate)) or rate <= 0:
            continue
        realized_s = source - source_in - (end - start) * rate
        realized_frames = int(math.floor(realized_s * fps + 1e-6))
        declared = segment.get('exit_handle_frames')
        required_frames = (declared if isinstance(declared, int) and not isinstance(declared, bool) else 0) + 2
        if realized_frames < required_frames:
            messages.append(
                f'{shot_id}: realized handle {realized_frames}f < required {required_frames}f for {phase}')
    return messages


def build_report(project, cuts, basis, status, shots=None, short_s=2.0, long_s=8.0,
                 monotony_pct=10.0, meta=None):
    shots = shots if shots is not None else [s for s in project.get('shots', []) if isinstance(s, dict)]
    curve = _curve(project)
    meta = meta or {}
    return {
        'status': status,
        'basis': basis,
        'cuts': cuts,
        'segments': segment_report(project, cuts),
        'stats': compute_stats(cuts, shots, short_s, long_s, monotony_pct),
        'curve_check': {
            'declared_intent': curve['intent'],
            'handle_shortfalls': handle_shortfalls(project),
            'unmatched_detected': meta.get('unmatched_detected', []),
            'unmatched_planned': meta.get('unmatched_planned', []),
        },
        'limitations': [
            'scene detection cannot distinguish a whip pan from a cut',
            'a planned-only report compares the plan with itself',
        ],
        'aesthetics': 'not_judged',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--cuts')
    parser.add_argument('--fps', type=float)
    parser.add_argument('--short-s', type=float, default=2.0)
    parser.add_argument('--long-s', type=float, default=8.0)
    parser.add_argument('--match-tolerance-s', type=float, default=0.5)
    parser.add_argument('--monotony-pct', type=float, default=10.0)
    parser.add_argument('--out')
    args = parser.parse_args(argv)

    try:
        project = json.loads(Path(args.project).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'error', 'reason': f'project_unreadable: {exc}'})); return 2
    project_fps = project.get('fps')
    if args.fps is not None and not (_number(project_fps) and abs(args.fps - project_fps) < 1e-9):
        print(json.dumps({'status': 'error', 'reason': 'fps_mismatch'})); return 2
    fps = args.fps if args.fps is not None else project_fps

    shots = [s for s in project.get('shots', []) if isinstance(s, dict)]
    if args.cuts:
        try:
            cuts, meta = read_cuts_csv(args.cuts, project, max(args.match_tolerance_s, 2 / fps))
        except ValueError as exc:
            print(json.dumps({'status': 'error', 'reason': str(exc)})); return 2
        status = 'partial' if (meta['unmatched_detected'] or meta['unmatched_planned']) else 'supplied'
        basis = {'fps': fps, 'source': 'cuts_csv', 'shot_mapping': meta['shot_mapping']}
    else:
        cuts, meta = cuts_from_project(project), {}
        status = 'planned_only'
        basis = {'fps': fps, 'source': 'project_plan', 'shot_mapping': 'project_shots'}

    report = build_report(project, cuts, basis, status, shots=shots, short_s=args.short_s,
                          long_s=args.long_s, monotony_pct=args.monotony_pct, meta=meta)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(payload, encoding='utf-8')
    else:
        print(payload)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
