#!/usr/bin/env python3
"""Build scoped sequence context, never infer actual take selection or approval."""
from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
from collections.abc import Mapping, Sequence

from project_index import build_index
from sequence_contract import (Document, FORMAT, Json, SequenceError, frame_at,
                               parse_fps, read_document, read_projection, table)


def _bootstrap(project: Mapping[str, Json]) -> Document:
    fps = parse_fps(project.get('fps'))
    shots = sorted(table(project, 'shots').values(), key=lambda s: s['start_s'])
    storyboard = project.get('storyboard', {})
    panels = storyboard.get('panels', [])
    cuts, links, requirements = [], [], []
    beats = {b['id']: b for b in storyboard.get('beats', [])}
    for shot in shots:
        start, end = frame_at(shot['start_s'], fps), frame_at(shot['end_s'], fps)
        sid = shot['id']
        selected = sorted((p for p in panels if p['shot_id'] == sid), key=lambda p: p['frame_time_s'])
        cuts.append({'cut_id': sid, 'shot_id': sid, 'scene_id': shot['scene_id'],
                     'final_in_frame': start, 'final_out_frame': end,
                     'source_asset_id': None, 'source_in_frame': None, 'source_out_frame': None,
                     'source_fps': None, 'source_frame_count': None, 'playback_rate': 1,
                     'transition': 'hard_cut', 'evidence': 'planned',
                     'planned_panel_ids': [p['id'] for p in selected]})
        for bid in shot.get('beat_ids', []):
            beat = beats.get(bid, {})
            requirements.append({'key': f'{sid}:beat:{bid}', 'kind': 'beat', 'entity_id': bid,
                                 'shot_id': sid, 'source_locator': beat.get('synopsis_locator'),
                                 'description': beat.get('event'), 'cut_ids': [sid],
                                 'panel_ids': [p['id'] for p in selected if bid in p.get('beat_ids', [])],
                                 'final_in_frame': start, 'final_out_frame': end, 'evidence': 'planned'})
        requirements.append({'key': f'{sid}:direction:{sid}', 'kind': 'direction', 'entity_id': sid,
                             'shot_id': sid, 'source_locator': f'{sid}/purpose+camera+states', 'cut_ids': [sid],
                             'panel_ids': [p['id'] for p in selected], 'final_in_frame': start, 'final_out_frame': end,
                             'direction': {k: copy.deepcopy(shot.get(k)) for k in ('purpose', 'camera', 'start_state', 'end_state')},
                             'evidence': 'planned'})
        for speech in shot.get('speech', []):
            requirements.append({'key': f'{sid}:speech:{speech["id"]}', 'kind': 'speech',
                                 'entity_id': speech['id'], 'shot_id': sid,
                                 'source_locator': f'{sid}/speech/{speech["id"]}',
                                 'text': speech['text'], 'character_id': speech.get('character_id'),
                                 'cut_ids': [sid], 'panel_ids': [p['id'] for p in selected if speech['id'] in p.get('speech_ids', [])],
                                 'final_in_frame': frame_at(speech['start_s'], fps),
                                 'final_out_frame': frame_at(speech['end_s'], fps), 'evidence': 'planned'})
    by_shot = {s['id']: s for s in shots}
    for previous, following in zip(cuts, cuts[1:]):
        links.append({'key': f'{previous["cut_id"]}->{following["cut_id"]}',
                      'from_cut_id': previous['cut_id'], 'to_cut_id': following['cut_id'],
                      'relation': 'unresolved', 'history_shot_ids': [],
                      'state_out': {}, 'state_in': {}, 'allowed_changes': [],
                      'planned_out_state': by_shot[previous['shot_id']]['end_state'],
                      'planned_in_state': by_shot[following['shot_id']]['start_state'],
                      'planned_out_panel_id': (previous['planned_panel_ids'] or [None])[-1],
                      'planned_in_panel_id': (following['planned_panel_ids'] or [None])[0],
                      'evidence': 'planned'})
    return {'format': FORMAT, 'phase': 'plan',
            'owner': {'project_id': project['project_id'], 'project_version': project['version'],
                      'artifact_id': None, 'artifact_version': None},
            'inputs': {'artifact_versions': {}, 'assets': {}},
            'time_basis': {'fps': {'num': fps.numerator, 'den': fps.denominator}, 'frame_origin': 0,
                           'audio_sample_rate': 48000},
            'requirements': requirements, 'links': links, 'cuts': cuts, 'checks': [],
            'audio_tracks': [], 'policy': {'duration': 'fixed', 'anchors': [], 'locked_one_take_shot_ids': []}}


def build_sequence_context(project: Mapping[str, Json], shot_ids: Sequence[str],
                           projection: Mapping[str, Json] | None = None) -> Document:
    """Include edit neighbors and explicit story history; preserve all input pins."""
    shots = table(project, 'shots')
    focus = set(shot_ids)
    if not focus or focus - shots.keys():
        raise SequenceError('focus', 'shot_ids', 'explicit known shot scope required')
    result = copy.deepcopy(dict(projection)) if projection is not None else _bootstrap(project)
    cuts = result.get('cuts', [])
    if not isinstance(cuts, list) or not all(isinstance(c, dict) and c.get('shot_id') in shots for c in cuts):
        raise SequenceError('cuts', 'projection', 'cuts must reference existing shots')
    selected_cuts = {c['cut_id'] for c in cuts if c['shot_id'] in focus}
    related = set(focus)
    links = result.get('links', [])
    pending = set(selected_cuts)
    seen = set()
    while pending:
        cid = pending.pop()
        if cid in seen:
            continue
        seen.add(cid)
        for link in links:
            if link.get('to_cut_id') == cid:
                source = next((c for c in cuts if c['cut_id'] == link.get('from_cut_id')), None)
                if source is None:
                    raise SequenceError('link_source', str(cid), 'unknown predecessor cut')
                related.add(source['shot_id'])
                for sid in link.get('history_shot_ids', []):
                    if sid not in shots:
                        raise SequenceError('history', str(cid), 'unknown narrative shot')
                    related.add(sid)
    # Immediate successors are needed to choose an exit, not to load the entire film.
    for a, b in zip(cuts, cuts[1:]):
        if a['shot_id'] in focus:
            related.add(b['shot_id'])
    result['focus'] = {'shot_ids': sorted(focus), 'context_shot_ids': sorted(related)}
    result['context'] = build_index(project, sorted(related))
    result['limits'] = 'Derived context only; agent must inspect media, resolve narrative state and obtain execution authority.'
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--shot', action='append', default=[])
    parser.add_argument('--all', action='store_true', help='explicit whole-timeline scope')
    parser.add_argument('--projection', type=Path)
    args = parser.parse_args()
    try:
        project = read_document(args.project)
        projection = read_projection(args.projection) if args.projection else None
        ids = list(table(project, 'shots')) if args.all else args.shot
        print(json.dumps(build_sequence_context(project, ids, projection), ensure_ascii=False, indent=2))
        return 0
    except (SequenceError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
