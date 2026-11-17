#!/usr/bin/env python3
"""Check sequence data and recorded evidence, never certify perceptual truth."""
from __future__ import annotations

import argparse
from collections.abc import Mapping
import json
from pathlib import Path

from sequence_contract import (Document, FORMAT, PHASES, FrameSpan, Json, SequenceError,
                               checked_assets, frame_at, number, parse_fps,
                               read_document, read_projection, table)
from validate_project import validate

RELATIONS = frozenset(('continuous_action', 'angle_change', 'reaction', 'spatial_move',
                       'time_elision', 'cross_cut', 'flashback', 'intentional_discontinuity'))


def _inspect(project: Mapping[str, Json], q: Mapping[str, Json], phase: str,
             root: Path | None) -> Document:
    blockers = []
    def fail(code: str, where: str, detail: str) -> None:
        blockers.append({'code': code, 'locator': where, 'detail': detail})
    if q.get('format') != FORMAT or phase not in PHASES:
        raise SequenceError('projection_format', 'format/phase', 'unknown projection format or phase')
    for key in ('owner', 'inputs', 'time_basis'):
        if not isinstance(q.get(key), dict):
            raise SequenceError('projection_shape', key, 'expected object')
    for key in ('requirements', 'links', 'cuts', 'checks'):
        if not isinstance(q.get(key), list) or not all(isinstance(x, dict) for x in q[key]):
            raise SequenceError('projection_shape', key, 'expected object rows')
    owner, inputs = q['owner'], q['inputs']
    artifacts, assets, shots = (table(project, name) for name in ('artifacts', 'asset_registry', 'shots'))
    for error in validate(project):
        fail('canonical_contract', 'project.json', error)
    if owner.get('project_id') != project.get('project_id'):
        fail('project_identity', 'owner', 'wrong project')
    if owner.get('project_version') != project.get('version'):
        fail('stale_project', 'owner', 'rebuild context from current project')
    aid = owner.get('artifact_id')
    if not isinstance(aid, str) or aid not in artifacts:
        fail('owner_artifact', 'owner', 'assign a registered versioned owner')
    elif artifacts[aid].get('version') != owner.get('artifact_version') or artifacts[aid].get('status') == 'stale':
        fail('stale_artifact', aid, 'owner changed or is stale')
    versions, pins = inputs.get('artifact_versions'), inputs.get('assets')
    if not isinstance(versions, dict) or not isinstance(pins, dict):
        raise SequenceError('projection_shape', 'inputs', 'artifact_versions/assets objects required')
    if not isinstance(aid, str) or aid not in versions:
        fail('input_versions', 'owner', 'owner must be pinned')
    for key, version in versions.items():
        if key not in artifacts or artifacts[key].get('version') != version or artifacts[key].get('status') == 'stale':
            fail('stale_artifact', key, 'input changed or is stale')
    for key, pin in pins.items():
        row = assets.get(key)
        if not isinstance(pin, dict) or row is None or pin.get('version') != row.get('version') or pin.get('sha256') != row.get('sha256'):
            fail('stale_asset', key, 'version/hash pin differs from ledger')
        elif root is not None:
            try:
                checked_assets(project, root, [key])
            except SequenceError as exc:
                fail(exc.code, exc.locator, exc.detail)
    if root is None:
        fail('media_root', 'base_dir', 'actual file/hash evidence requires project root')
    fps = parse_fps(q['time_basis'].get('fps'))
    if fps != parse_fps(project.get('fps')):
        fail('timeline_fps', 'time_basis', 'must match project frame basis')
    if q['time_basis'].get('frame_origin') != 0:
        fail('frame_origin', 'time_basis', 'expected zero-based timeline')
    cuts, by_cut, cursor = q['cuts'], {}, 0
    for cut in cuts:
        cid, sid = cut.get('cut_id'), cut.get('shot_id')
        if not isinstance(cid, str) or not cid or cid in by_cut:
            raise SequenceError('cut_identity', 'cuts', 'nonempty unique cut_id required')
        by_cut[cid] = cut
        if not isinstance(sid, str) or sid not in shots:
            fail('shot_reference', cid, 'unknown shot'); continue
        span = FrameSpan(cut.get('final_in_frame'), cut.get('final_out_frame'))
        if span.start != cursor:
            fail('timeline_gap', cid, 'cuts must cover timeline without gaps/overlaps')
        cursor = span.end
        if cut.get('scene_id') != shots[sid].get('scene_id'):
            fail('scene_reference', cid, 'cut scene differs from shot')
        if cut.get('transition', 'hard_cut') != 'hard_cut':
            fail('unsupported_transition', cid, 'V1 executable adapter supports hard cuts only')
    if not cuts:
        fail('empty_sequence', 'cuts', 'sequence is empty')
    policy = q.get('policy', {})
    if not isinstance(policy, dict):
        raise SequenceError('projection_shape', 'policy', 'expected object')
    if policy.get('duration', 'fixed') != 'flexible' and cursor != frame_at(project.get('target_duration_s'), fps):
        fail('fixed_duration', 'timeline', 'fixed total duration changed')
    if type(q.get('include_source_audio', False)) is not bool:
        raise SequenceError('projection_shape', 'include_source_audio', 'expected bool')
    covered_shots = {c.get('shot_id') for c in cuts}
    if covered_shots != set(shots):
        fail('shot_coverage', 'cuts', 'all canonical shots must remain covered; cannot erase requirements by dropping a shot')
    focus = q.get('focus', {})
    generation_shots = focus.get('shot_ids', []) if isinstance(focus, dict) else []
    if phase == 'generation' and (not isinstance(generation_shots, list) or not generation_shots or
            any(not isinstance(s, str) or s not in shots for s in generation_shots)):
        raise SequenceError('generation_scope', 'focus', 'explicit current generation shot_ids required')
    panels = project.get('storyboard', {}).get('panels', [])
    panel_by_id = {p['id']: p for p in panels}
    beats = {b['id']: b for b in project.get('storyboard', {}).get('beats', [])}
    expected = set()
    speech_by_id = {}
    for sid in covered_shots:
        if sid not in shots:
            continue
        expected.update((sid, 'beat', bid) for bid in shots[sid].get('beat_ids', []))
        expected.add((sid, 'direction', sid))
        for speech in shots[sid].get('speech', []):
            expected.add((sid, 'speech', speech['id']))
            speech_by_id[speech['id']] = speech
    actual, req_keys = set(), set()
    for req in q['requirements']:
        key = req.get('key')
        if not isinstance(key, str) or not key or key in req_keys:
            raise SequenceError('requirement_identity', 'requirements', 'unique local key required')
        req_keys.add(key)
        sid, kind, entity = req.get('shot_id'), req.get('kind'), req.get('entity_id')
        if not all(isinstance(x, str) for x in (sid, kind, entity)):
            raise SequenceError('requirement_shape', key, 'shot/kind/entity identifiers required')
        actual.add((sid, kind, entity))
        if not req.get('source_locator'):
            fail('source_locator', key, 'requirement must locate the source script/direction')
        ids = req.get('cut_ids', [])
        if not isinstance(ids, list) or not ids or any(not isinstance(c, str) or c not in by_cut or by_cut[c]['shot_id'] != sid for c in ids):
            fail('requirement_cut', key, 'missing or incompatible implementing cuts')
            continue
        rspan = FrameSpan(req.get('final_in_frame'), req.get('final_out_frame'))
        if rspan.start < min(by_cut[c]['final_in_frame'] for c in ids) or rspan.end > max(by_cut[c]['final_out_frame'] for c in ids):
            fail('requirement_trimmed', key, 'required event outside selected timeline range')
        pids = req.get('panel_ids', [])
        if not isinstance(pids, list) or not pids or any(not isinstance(pid, str) or pid not in panel_by_id or panel_by_id[pid]['shot_id'] != sid for pid in pids):
            fail('requirement_panel', key, 'bind actual planned evidence panels')
        if kind == 'direction' and sid in shots:
            canonical = {k: shots[sid].get(k) for k in ('purpose', 'camera', 'start_state', 'end_state')}
            if req.get('direction') != canonical:
                fail('direction_mismatch', key, 'camera/purpose/states differ from canonical direction')
        if kind == 'speech' and entity in speech_by_id:
            speech = speech_by_id[entity]
            if req.get('text') != speech['text'] or req.get('character_id') != speech.get('character_id'):
                fail('speech_mismatch', key, 'literal text/speaker differ from canonical speech')
        if phase == 'generation' and sid in generation_shots and (not req.get('request_clause') or req.get('control_status') not in ('HARD_CONTROL', 'SOFT_PROMPT')):
            fail('submission_mapping', key, 'bind requirement to actual final request clause/control')
    if expected - actual:
        fail('requirement_coverage', 'requirements', f'missing canonical beat/speech/direction rows: {sorted(expected - actual)}')
    if phase == 'generation':
        submission = q.get('submission_asset_id')
        if not isinstance(submission, str) or submission not in pins:
            fail('submission_snapshot', 'submission_asset_id', 'actual final request JSON must be registered and pinned')
        elif root is not None:
            try:
                request = read_document(checked_assets(project, root, [submission])[submission])
                def strings(value: Json) -> list[str]:
                    if isinstance(value, str):
                        return [value]
                    if isinstance(value, dict):
                        return [s for v in value.values() for s in strings(v)]
                    if isinstance(value, list):
                        return [s for v in value for s in strings(v)]
                    return []
                clauses = strings(request)
                for req in q['requirements']:
                    clause = req.get('request_clause')
                    if req.get('shot_id') in generation_shots and isinstance(clause, str) and not any(clause in text for text in clauses):
                        fail('submission_clause', req['key'], 'mapped clause absent from actual final request')
            except (SequenceError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                fail('submission_snapshot', submission, str(exc))

    def inspected(target: str, kind: str, method: str, observed: list[str], cut: Document | None = None) -> Document | None:
        for record in q['checks']:
            if record.get('target') != target or record.get('kind') != kind or record.get('status') != 'pass' or record.get('method') != method:
                continue
            evidence = record.get('evidence_asset_id')
            seen = record.get('observed_asset_ids', [])
            if not isinstance(seen, list) or not all(isinstance(i, str) for i in seen) or not set(observed).issubset(seen) or not isinstance(evidence, str) or evidence not in pins or not record.get('observation'):
                continue
            if any(not isinstance(i, str) or i not in pins for i in seen):
                continue
            observed_versions = record.get('asset_versions', {})
            if not isinstance(observed_versions, dict) or any(observed_versions.get(i) != pins[i].get('version') for i in observed):
                continue
            if phase in ('generation', 'edit', 'export') and kind in ('source_range', 'source_audio', 'boundary_motion', 'boundary_audio', 'selected_requirement'):
                snapshots = record.get('cut_ranges', {})
                relevant = [c for c in cuts if c.get('source_asset_id') in observed]
                if not isinstance(snapshots, dict) or any(snapshots.get(c['cut_id']) != {k: c.get(k) for k in
                        ('source_asset_id', 'source_in_frame', 'source_out_frame', 'final_in_frame', 'final_out_frame')} for c in relevant):
                    continue
            if cut is not None and any(record.get(k) != cut.get(k) for k in ('source_asset_id', 'source_in_frame', 'source_out_frame')):
                continue
            return record
        fail('missing_inspection', target, f'{kind} needs {method}, actual evidence and current selected scope')
        return None

    for panel in panels:
        if panel['shot_id'] in covered_shots:
            image = panel.get('image_asset_id') or panel.get('source_sheet_asset_id')
            inspected('panel:' + panel['id'], 'plan_image', 'opened_image', [image] if image else [])
    inspected('scope', 'plan_timing', 'continuous_playback', [])
    pairs = {(a['cut_id'], b['cut_id']) for a, b in zip(cuts, cuts[1:])}
    got_pairs = set()
    for link in q['links']:
        a, b = link.get('from_cut_id'), link.get('to_cut_id')
        if not isinstance(a, str) or not isinstance(b, str) or (a, b) not in pairs or (a, b) in got_pairs:
            fail('link_reference', str(link.get('key')), 'expected exactly one link per adjacent cut'); continue
        got_pairs.add((a, b))
        key = link.get('key', a + '->' + b)
        if not isinstance(link.get('relation'), str) or link['relation'] not in RELATIONS:
            fail('link_relation', key, 'agent must resolve narrative/camera relationship')
        out, incoming = link.get('state_out'), link.get('state_in')
        if not isinstance(out, dict) or not isinstance(incoming, dict):
            raise SequenceError('state_shape', key, 'state_out/state_in objects required')
        if not out and not incoming and not link.get('state_not_applicable_reason'):
            fail('missing_state', key, 'observe relevant state or state explicit non-applicability')
        changes = link.get('allowed_changes', [])
        if not isinstance(changes, list) or not all(isinstance(c, dict) for c in changes):
            raise SequenceError('state_shape', key, 'allowed_changes must contain specific change records')
        for field in out.keys() | incoming.keys():
            if field not in out or field not in incoming or out[field] != incoming[field]:
                permitted = any(c.get('field') == field and c.get('from') == out.get(field) and c.get('to') == incoming.get(field)
                                and c.get('reason') and c.get('source_locator') for c in changes)
                if not permitted:
                    fail('state_conflict', key + '/' + field, 'no sourced permitted state delta')
        history = link.get('history_shot_ids', [])
        if not isinstance(history, list) or any(not isinstance(s, str) or s not in shots for s in history):
            fail('history_reference', key, 'unknown narrative predecessor')
        if history and not link.get('history_state_evidence'):
            fail('history_evidence', key, 'reappearance needs state history evidence, not edit neighbor alone')
        needs_predecessor = phase in ('edit', 'export') or phase == 'generation' and by_cut[b]['shot_id'] in generation_shots
        if needs_predecessor and link.get('requires_actual_predecessor', True):
            predecessor = by_cut[a]
            source_id = predecessor.get('source_asset_id')
            if not isinstance(source_id, str) or source_id not in pins:
                fail('predecessor_selection', key, 'no actual registered selected predecessor exit')
            elif phase == 'generation':
                FrameSpan(predecessor.get('source_in_frame'), predecessor.get('source_out_frame'))
                inspected('cut:' + a, 'source_range', 'continuous_playback', [source_id], predecessor)
                if link.get('predecessor_state_evidence') != 'observed':
                    fail('actual_state', key, 'predecessor exit must be observed before dependent generation')
        if phase in ('edit', 'export'):
            if link.get('evidence') != 'observed':
                fail('actual_state', key, 'selected boundary state must be observed, not planned')
            observed = [by_cut[c].get('source_asset_id') for c in (a, b)]
            if all(isinstance(x, str) for x in observed):
                inspected('link:' + key, 'boundary_motion', 'continuous_playback', observed)
                if project.get('audio_mode') != 'no_audio':
                    inspected('link:' + key, 'boundary_audio', 'listening', observed)
    if pairs != got_pairs:
        fail('link_coverage', 'links', 'all adjacent boundaries must be accounted for')
    if project.get('audio_mode') == 'no_audio' and (q.get('audio_tracks') or q.get('include_source_audio')):
        fail('audio_policy', 'audio_tracks', 'silent deliverable cannot add source or external sound')
    authorized = False
    if phase != 'plan':
        execution_id = q.get('execution_artifact_id')
        authority = artifacts.get(execution_id) if isinstance(execution_id, str) else None
        required_type = 'video_execution_plan' if phase == 'generation' else 'edit_plan'
        authorized = bool(authority and authority.get('type') == required_type and authority.get('status') == 'approved'
                          and versions.get(execution_id) == authority.get('version') and authority.get('approval'))
        if not authorized:
            fail('execution_authority', 'execution_artifact_id', 'current approved, pinned execution/edit plan required')
        else:
            scope = authority.get('execution_scope', {})
            scoped_shots = scope.get('shot_ids', []) if isinstance(scope, dict) else []
            operations = scope.get('operations', []) if isinstance(scope, dict) else []
            if not isinstance(scoped_shots, list) or not all(isinstance(s, str) for s in scoped_shots) or not set(generation_shots if phase == 'generation' else covered_shots).issubset(scoped_shots) or phase not in operations:
                fail('execution_scope', execution_id, 'approved scope must name every shot and this operation')
        if authorized and cursor != frame_at(project.get('target_duration_s'), fps):
            if authority.get('timing_policy', {}).get('duration') != 'flexible':
                fail('timing_authority', execution_id, 'length change lacks approved flexible timing policy')
    counts = {}
    for cut in cuts:
        counts[cut.get('shot_id')] = counts.get(cut.get('shot_id'), 0) + 1
    locked_takes = policy.get('locked_one_take_shot_ids', [])
    if not isinstance(locked_takes, list) or not all(isinstance(s, str) for s in locked_takes):
        raise SequenceError('projection_shape', 'locked_one_take_shot_ids', 'expected shot id array')
    for sid in locked_takes:
        if counts.get(sid, 0) > 1:
            fail('locked_one_take', sid, 'internal edited cuts violate locked continuous take')
    if phase in ('edit', 'export'):
        for cut in cuts:
            cid, source = cut['cut_id'], cut.get('source_asset_id')
            if not isinstance(source, str) or source not in pins:
                fail('source_selection', cid, 'explicit registered selected source required'); continue
            span = FrameSpan(cut.get('source_in_frame'), cut.get('source_out_frame'))
            count = cut.get('source_frame_count')
            if type(count) is not int or span.end > count:
                fail('source_bounds', cid, 'selection exceeds measured source frames')
            source_fps = parse_fps(cut.get('source_fps'))
            rate = number(cut.get('playback_rate', 1), cid)
            if rate != 1 or source_fps != fps:
                fail('conform_required', cid, 'V1 requires explicitly conformed same-FPS 1x sources')
            if span.length != cut['final_out_frame'] - cut['final_in_frame']:
                fail('source_length', cid, 'selected and final frame counts differ')
            inspected('cut:' + cid, 'source_range', 'continuous_playback', [source], cut)
            if project.get('audio_mode') != 'no_audio':
                inspected('cut:' + cid, 'source_audio', 'listening', [source], cut)
        for req in q['requirements']:
            target = 'requirement:' + req['key']
            selected_record = inspected(target, 'selected_requirement', 'continuous_playback',
                      [by_cut[c]['source_asset_id'] for c in req.get('cut_ids', []) if c in by_cut and isinstance(by_cut[c].get('source_asset_id'), str)])
            valid_event = False
            for record in [selected_record] if selected_record is not None else []:
                events = record.get('event_ranges', [])
                if not isinstance(events, list) or not events or not all(isinstance(e, dict) for e in events):
                    continue
                valid_event = True
                for event in events:
                    cid = event.get('cut_id')
                    cut = by_cut.get(cid) if isinstance(cid, str) else None
                    if cut is None or cid not in req['cut_ids'] or not isinstance(cut.get('source_in_frame'), int):
                        valid_event = False; break
                    source_span = FrameSpan(event.get('source_in_frame'), event.get('source_out_frame'))
                    start = cut['final_in_frame'] + source_span.start - cut['source_in_frame']
                    end = start + source_span.length
                    if (event.get('source_asset_id') != cut.get('source_asset_id') or
                            source_span.start < cut['source_in_frame'] or source_span.end > cut['source_out_frame'] or
                            event.get('final_in_frame') != start or event.get('final_out_frame') != end or
                            start < req['final_in_frame'] or end > req['final_out_frame']):
                        valid_event = False; break
                if valid_event:
                    break
            if not valid_event:
                fail('required_event_range', target, 'bind actual required event source frames to retained final frames; trimming cannot erase the event')
    if phase == 'export':
        output = q.get('output_asset_id')
        if not isinstance(output, str) or output not in pins:
            fail('output_asset', 'output_asset_id', 'actual registered output and current pin required')
        else:
            inspected('scope', 'playback', 'continuous_playback', [output])
            inspected('scope', 'final_requirements', 'continuous_playback', [output])
            if project.get('audio_mode') != 'no_audio':
                inspected('scope', 'listening', 'listening', [output])
    return {'ready': not blockers, 'phase': phase, 'execution_authorized': authorized,
            'blockers': blockers, 'aesthetics': 'not_judged',
            'limits': 'Checks declared records, provenance, frame arithmetic and actual file hashes; does not attest observations, approval truth or provider behavior.'}


def validate_sequence(project: Mapping[str, Json], projection: Mapping[str, Json],
                      phase: str, base_dir: Path | None = None) -> Document:
    """Return actionable blockers; malformed external documents never become ready."""
    try:
        return _inspect(project, projection, phase, base_dir)
    except SequenceError as exc:
        return {'ready': False, 'phase': phase, 'execution_authorized': False,
                'blockers': [{'code': exc.code, 'locator': exc.locator, 'detail': exc.detail}],
                'aesthetics': 'not_judged'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('projection', type=Path)
    parser.add_argument('--phase', required=True, choices=PHASES)
    args = parser.parse_args()
    try:
        result = validate_sequence(read_document(args.project), read_projection(args.projection),
                                   args.phase, args.project.resolve().parent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['ready'] else 1
    except (SequenceError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'ready': False, 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
