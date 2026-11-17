"""Regression cases discovered while self-reviewing input and selection boundaries."""
from fractions import Fraction
import hashlib
import json
import subprocess
import struct
import pytest
from sequence_contract import parse_fps, read_document, SequenceError
from sequence_test_fixture import prepared_plan
from test_sequence_media import prepared_edit
from validate_sequence import validate_sequence
from sequence_media import render_sequence


def test_required_event_outside_selected_raw_frames_cannot_be_hidden_by_trim(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    record = next(r for r in q['checks'] if r['kind'] == 'selected_requirement')
    record['event_ranges'] = [{'cut_id': 'SH01', 'source_asset_id': 'VIDEO0',
        'source_in_frame': 0, 'source_out_frame': 12, 'final_in_frame': 0, 'final_out_frame': 12}]
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert 'required_event_range' in {b['code'] for b in result['blockers']}


def test_generation_requires_actual_pinned_request_snapshot(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'submission_snapshot' in {b['code'] for b in result['blockers']}


def test_request_clause_must_exist_in_actual_request_bytes(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); path = tmp_path / 'request.json'
    path.write_text(json.dumps({'params': {'prompt': 'actual unrelated request'}}))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    p['asset_registry'].append({'id': 'REQUEST', 'kind': 'document', 'version': '1', 'status': 'available', 'path': path.name, 'sha256': digest})
    q['inputs']['assets']['REQUEST'] = {'version': '1', 'sha256': digest}
    q['submission_asset_id'] = 'REQUEST'
    for req in q['requirements']:
        req.update(request_clause='required action not submitted', control_status='SOFT_PROMPT')
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'submission_clause' in {b['code'] for b in result['blockers']}


def test_first_shot_generation_does_not_require_unproduced_future_exits(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); q['focus']['shot_ids'] = ['SH01']
    for req in q['requirements']:
        if req['shot_id'] == 'SH01':
            req.update(request_clause='synthetic submitted clause', control_status='SOFT_PROMPT')
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'predecessor_selection' not in {b['code'] for b in result['blockers']}
    assert 'submission_mapping' not in {b['code'] for b in result['blockers']}


def test_following_generation_requires_reviewed_actual_exit_not_just_asset_name(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); q['focus']['shot_ids'] = ['SH02']
    q['cuts'][0]['source_asset_id'] = 'invented-result'
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'predecessor_selection' in {b['code'] for b in result['blockers']}


def test_required_camera_direction_cannot_disappear_from_projection(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    q['requirements'] = [r for r in q['requirements'] if r['kind'] != 'direction']
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert not result['ready']


def test_actual_edit_needs_observed_not_merely_planned_boundary_state(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['links'][0]['evidence'] = 'planned'
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert 'actual_state' in {b['code'] for b in result['blockers']}


def test_approved_plan_does_not_authorize_unlisted_shots(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    next(a for a in p['artifacts'] if a['id'] == 'EDIT')['execution_scope'] = {'shot_ids': ['SH01'], 'operations': ['edit']}
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert 'execution_scope' in {b['code'] for b in result['blockers']}


def test_numeric_project_fps_recovers_exact_common_rational():
    # Given / When / Then
    assert parse_fps(float(Fraction(24000, 1001))) == Fraction(24000, 1001)


def test_exponent_overflow_is_not_a_valid_json_number(tmp_path):
    # Given
    path = tmp_path / 'bad.json'; path.write_text('{"unused": 1e999}')
    # When / Then
    with pytest.raises(SequenceError):
        read_document(path)


@pytest.mark.parametrize('mutation', [
    lambda q: q['owner'].update(artifact_id=[]),
    lambda q: q['requirements'][0].update(panel_ids=[{}]),
    lambda q: q.update(include_source_audio='yes'),
    lambda q: q['checks'][0].update(observed_asset_ids=[{}]),
    lambda q: q['links'][0].update(relation=[]),
    lambda q: q['policy'].update(locked_one_take_shot_ids=None),
])
def test_malformed_inner_metadata_is_blocked_not_crashed(tmp_path, mutation):
    # Given
    p, q = prepared_plan(tmp_path); mutation(q)
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert not result['ready']


def test_removing_shot_and_its_requirements_cannot_hide_missing_story(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    q['cuts'] = [q['cuts'][0]]; q['cuts'][0]['final_out_frame'] = 96
    q['requirements'] = [r for r in q['requirements'] if r['shot_id'] == 'SH01']; q['links'] = []
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert 'shot_coverage' in {b['code'] for b in result['blockers']}


def test_old_image_observation_does_not_apply_to_new_asset_version(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); q['checks'][0]['asset_versions']['IM01'] = 'old'
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert not result['ready']


def test_changed_source_range_invalidates_boundary_and_event_observations(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    cut = q['cuts'][0]; cut.update(source_in_frame=13, source_out_frame=61)
    for record in q['checks']:
        if record['target'] == 'cut:SH01':
            record.update({k: cut[k] for k in ('source_asset_id', 'source_in_frame', 'source_out_frame')})
            record['cut_ranges']['SH01'] = {k: cut[k] for k in ('source_asset_id', 'source_in_frame', 'source_out_frame', 'final_in_frame', 'final_out_frame')}
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert not result['ready']
    assert any(b['locator'].startswith('link:') for b in result['blockers'])


def test_nonzero_source_pts_does_not_lose_selected_audio(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    source = tmp_path / 'VIDEO0.mkv'; shifted = tmp_path / 'shifted.mkv'
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(source), '-c', 'copy', '-output_ts_offset', '10', str(shifted)], check=True)
    row = next(a for a in p['asset_registry'] if a['id'] == 'VIDEO0')
    row.update(path=shifted.name, sha256=hashlib.sha256(shifted.read_bytes()).hexdigest())
    q['inputs']['assets']['VIDEO0']['sha256'] = row['sha256']
    # When
    result = render_sequence(p, q, tmp_path, 'shifted-edit')
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(tmp_path / result['video_path']),
                              '-map', '0:a:0', '-f', 's16le', '-ac', '2', '-ar', '48000', '-'], capture_output=True, check=True).stdout
    # Then: four seconds of 48kHz stereo signed 16-bit PCM, not one missing shot.
    assert len(decoded) == 4 * 48000 * 2 * 2
    samples = struct.unpack('<' + 'h' * (len(decoded) // 2), decoded)[::2][:48000]
    crossings = sum(a <= 0 < b for a, b in zip(samples, samples[1:]))
    assert 298 <= crossings <= 302, 'first selected second must retain the 300Hz first source, not silence/600Hz'
