"""Guard delegated flexible edits using existing approved edit-plan metadata."""
from __future__ import annotations

from collections.abc import Mapping
from sequence_contract import Json, SequenceError, frame_at, parse_fps, table


def validate_timing_change(current: Mapping[str, Json], candidate: Mapping[str, Json],
                           delta: Mapping[str, Json]) -> None:
    """Enforce old approved policies, not permissions invented in the new delta."""
    policies = [a for a in table(current, 'artifacts').values()
                if a.get('type') == 'edit_plan' and a.get('status') == 'approved'
                and isinstance(a.get('timing_policy'), dict)]
    changed = current.get('target_duration_s') != candidate.get('target_duration_s')
    inputs = delta.get('input_versions', {})
    if changed and not any(inputs.get(a['id']) == a['version'] for a in policies):
        raise SequenceError('timing_authority', 'target_duration_s', 'pinned approved edit_plan timing_policy required')
    fps = parse_fps(current.get('fps'))
    for artifact in policies:
        policy = artifact['timing_policy']
        mode = policy.get('duration')
        if mode not in ('fixed', 'flexible'):
            raise SequenceError('timing_policy', artifact['id'], 'duration must be fixed or flexible')
        if changed and mode == 'fixed':
            raise SequenceError('fixed_duration', artifact['id'], 'approved total duration is locked')
        anchors = policy.get('anchors', [])
        if not isinstance(anchors, list):
            raise SequenceError('timing_policy', artifact['id'], 'anchors must be an array')
        for anchor in anchors:
            if not isinstance(anchor, dict) or anchor.get('table') not in ('shots', 'audio_cues', 'captions', 'panels'):
                raise SequenceError('timing_policy', artifact['id'], 'unsupported anchor table')
            key, field, frame = anchor.get('id'), anchor.get('field'), anchor.get('frame')
            if field not in ('start_s', 'end_s', 'frame_time_s') or type(frame) is not int or frame < 0:
                raise SequenceError('timing_policy', artifact['id'], 'invalid frame anchor')
            values = []
            for project in (current, candidate):
                source = {'panels': project.get('storyboard', {}).get('panels', [])} if anchor['table'] == 'panels' else project
                row = table(source, anchor['table']).get(key)
                if row is None or field not in row:
                    raise SequenceError('fixed_anchor', str(key), 'locked anchor missing')
                values.append(frame_at(row[field], fps))
            if values != [frame, frame]:
                raise SequenceError('fixed_anchor', str(key), 'approved event frame cannot move')
