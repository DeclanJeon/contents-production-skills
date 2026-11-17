"""Pre-generation AV guards; native snapshots here are synthetic declarations."""
import pytest
from av_handoff_test_fixture import (prepared_handoff, prepared_history_handoff,
                                     add_history_bindings, rewrite_document)
from validate_sequence import validate_sequence


def codes(result):
    return {b['code'] for b in result['blockers']}


def test_return_after_insert_requires_native_historical_state_bindings(tmp_path):
    p, q = prepared_history_handoff(tmp_path)
    result = validate_sequence(p, q, 'generation', tmp_path)
    assert 'visual_reference' in codes(result), result['blockers']
    assert 'audio_reference' in codes(result), result['blockers']
    assert not result['ready']


def test_complete_return_history_reaches_actual_native_request(tmp_path):
    p, q = prepared_history_handoff(tmp_path)
    add_history_bindings(p, q, tmp_path)
    result = validate_sequence(p, q, 'generation', tmp_path)
    assert result['ready'], result['blockers']


@pytest.mark.parametrize('kind', ['source_range', 'source_audio'])
def test_historical_source_needs_its_own_current_inspection(tmp_path, kind):
    p, q = prepared_history_handoff(tmp_path)
    add_history_bindings(p, q, tmp_path)
    q['checks'] = [r for r in q['checks'] if not (r['target'] == 'cut:SH01' and r['kind'] == kind)]
    result = validate_sequence(p, q, 'generation', tmp_path)
    assert any(b['code'] == 'missing_inspection' and b['locator'] == 'cut:SH01'
               for b in result['blockers']), result['blockers']
    assert not result['ready']


def test_history_cannot_name_the_current_unproduced_shot(tmp_path):
    p, q = prepared_handoff(tmp_path)
    q['links'][0].update(history_shot_ids=['SH02'], history_state_evidence='not actual prior state')
    result = validate_sequence(p, q, 'generation', tmp_path)
    assert 'history_reference' in codes(result), result['blockers']


def test_complete_native_handoff_is_ready_but_not_conditioning_proof(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert result['ready'], result['blockers']
    assert result['aesthetics'] == 'not_judged'


def test_first_shot_and_first_voice_do_not_need_nonexistent_previous_audio(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['focus']['shot_ids'] = ['SH01']
    next(a for a in p['artifacts'] if a['id'] == 'EXEC')['execution_scope']['shot_ids'] = ['SH01']
    next(a for a in p['artifacts'] if a['id'] == 'VO01')['status'] = 'draft'
    q['checks'] = [r for r in q['checks'] if r['kind'] not in ('source_audio', 'voice_anchor')]
    composition = next(b for b in q['generation_handoff']['bindings'] if b['purpose'] == 'current_composition')
    composition.update(reference_asset_id='IM01', request_clause='Use only the approved first composition.')
    q['generation_handoff']['bindings'] = [composition]
    image = next(a for a in p['asset_registry'] if a['id'] == 'IM01')
    rewrite_document(p, q, tmp_path, 'UPLOADS', lambda d: d['records'][-1].update(reference_asset_id='IM01', sha256=image['sha256']))
    rewrite_document(p, q, tmp_path, 'REQUEST', lambda d: d['message'].update(
        reference_ids=[composition['native_reference_id']], text='synthetic required direction\n' + composition['request_clause']))
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert result['ready'], result['blockers']


def test_silent_film_preserves_explicit_no_audio_and_needs_no_audio_reference(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); p['audio_mode'] = 'no_audio'; p['audio_cues'] = []
    for shot in p['shots']:
        shot['speech'] = []; shot['audio_cue_ids'] = []
    for panel in p['storyboard']['panels']:
        panel['speech_ids'] = []; panel['audio_cue_ids'] = []
    q['requirements'] = [r for r in q['requirements'] if r['kind'] != 'speech']
    q['include_source_audio'] = False
    q['checks'] = [r for r in q['checks'] if r['kind'] not in ('source_audio', 'voice_anchor')]
    q['generation_handoff']['bindings'] = [b for b in q['generation_handoff']['bindings'] if b['modality'] != 'audio']
    rewrite_document(p, q, tmp_path, 'REQUEST', lambda d: d['message'].update(
        reference_ids=[b['native_reference_id'] for b in q['generation_handoff']['bindings']], audio_policy='no_audio'))
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert result['ready'], result['blockers']


def test_predecessor_audio_must_be_heard_before_next_generation(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['checks'] = [r for r in q['checks'] if not (r['target'] == 'cut:SH01' and r['kind'] == 'source_audio')]
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'predecessor_audio' in codes(result)


def test_reference_package_is_not_optional(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); q.pop('generation_handoff')
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'generation_handoff' in codes(result)


@pytest.mark.parametrize('purpose,expected', [('visual_state', 'visual_reference'),
    ('audio_context', 'audio_reference'), ('voice_identity', 'voice_anchor'),
    ('current_composition', 'composition_reference')])
def test_each_required_modality_must_reach_request(tmp_path, purpose, expected):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['generation_handoff']['bindings'] = [b for b in q['generation_handoff']['bindings'] if b['purpose'] != purpose]
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert expected in codes(result)


@pytest.mark.parametrize('change,expected', [
    (lambda d: d['message'].pop('reference_ids'), 'reference_selection'),
    (lambda d: d['message'].update(reference_ids=[]), 'reference_selection'),
    (lambda d: d['message'].update(reference_ids=['00000000-0000-4000-8000-000000001001']), 'reference_selection'),
    (lambda d: d.update(expected_revision=6), 'session_revision'),
    (lambda d: d.update(session_id='00000000-0000-4000-8000-000000000999'), 'session_binding'),
])
def test_native_wire_ids_and_revision_are_checked(tmp_path, change, expected):
    # Given
    p, q = prepared_handoff(tmp_path); rewrite_document(p, q, tmp_path, 'REQUEST', change)
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert expected in codes(result)


@pytest.mark.parametrize('field,value,expected', [('state', 'pending', 'reference_readiness'),
    ('model_requirement', 'candidate', 'reference_readiness'), ('asset_archived', True, 'reference_readiness'),
    ('role', 'first_frame', 'reference_role')])
def test_native_readiness_cannot_silently_degrade_to_candidate(tmp_path, field, value, expected):
    # Given
    p, q = prepared_handoff(tmp_path)
    rewrite_document(p, q, tmp_path, 'REFS', lambda d: d['result']['structuredContent']['items'][0].update({field: value}))
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert expected in codes(result)


def test_reference_instruction_must_be_in_actual_request_not_only_metadata(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['generation_handoff']['bindings'][0]['request_clause'] = 'missing reference import/exclusion instruction'
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'reference_clause' in codes(result)


def test_reference_parent_hash_must_match_selected_take(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    next(a for a in p['asset_registry'] if a['id'] == 'REF_VIDEO')['sequence_slice']['source_sha256'] = '0' * 64
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'reference_range' in codes(result)


def test_upload_record_must_bind_actual_local_bytes_to_native_asset(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    rewrite_document(p, q, tmp_path, 'UPLOADS', lambda d: d['records'][0].update(sha256='0' * 64))
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'upload_binding' in codes(result)


def test_previous_raw_tail_cannot_be_uploaded_as_selected_exit(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['generation_handoff']['bindings'][0]['reference_asset_id'] = 'VIDEO0'
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'reference_range' in codes(result)


def test_unknown_transport_is_blocked_not_assumed_compatible(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); q['generation_handoff']['adapter'] = 'invented'
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'transport_adapter' in codes(result)


def test_previous_frame_must_not_override_new_angle_first_frame(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['generation_handoff']['bindings'][0]['role'] = 'first_frame'
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'angle_reference' in codes(result)


def test_empty_observation_flag_cannot_waive_actual_prior_media(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    q['links'][0]['requires_actual_predecessor'] = False
    q['cuts'][0]['source_asset_id'] = None
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'predecessor_selection' in codes(result)
