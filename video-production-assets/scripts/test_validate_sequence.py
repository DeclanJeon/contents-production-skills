"""Data/evidence gates do not certify the truth of supplied observations."""
import copy
import pytest
from sequence_test_fixture import prepared_plan
from validate_sequence import validate_sequence


def test_complete_plan_records_are_ready_but_not_quality_certification(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert result['ready'], result['blockers']
    assert result['aesthetics'] == 'not_judged'
    assert result['execution_authorized'] is False


@pytest.mark.parametrize('mutation,code', [
    (lambda q: q['requirements'].pop(0), 'requirement_coverage'),
    (lambda q: q['checks'].pop(0), 'missing_inspection'),
    (lambda q: q['links'][0]['state_in'].update(door='open'), 'state_conflict'),
    (lambda q: q['links'][0].update(relation='unresolved'), 'link_relation'),
    (lambda q: q['owner'].update(project_version='old'), 'stale_project'),
    (lambda q: q['inputs']['artifact_versions'].update(SYN='old'), 'stale_artifact'),
    (lambda q: q['requirements'][0].update(panel_ids=[]), 'requirement_panel'),
    (lambda q: q['cuts'][1].update(final_in_frame=49), 'timeline_gap'),
    (lambda q: q['checks'][0].update(method='page_text'), 'missing_inspection'),
    (lambda q: q['checks'][0].update(status='unverified'), 'missing_inspection'),
    (lambda q: q['requirements'][-1].update(text='changed line'), 'speech_mismatch'),
])
def test_incomplete_or_conflicting_plan_is_blocked(tmp_path, mutation, code):
    # Given
    p, q = prepared_plan(tmp_path); mutation(q)
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert code in {b['code'] for b in result['blockers']}
    assert not result['ready']


def test_approved_state_change_needs_specific_reason_and_source(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    q['links'][0]['state_in']['door'] = 'open'
    q['links'][0]['allowed_changes'] = [{'field': 'door', 'from': 'closed', 'to': 'open',
                                      'reason': 'scripted elision', 'source_locator': 'script paragraph 2'}]
    q['links'][0]['relation'] = 'time_elision'
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert result['ready'], result['blockers']


def test_generation_without_current_execution_plan_is_not_authorized(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    # When
    result = validate_sequence(p, q, 'generation', tmp_path)
    # Then
    assert 'execution_authority' in {b['code'] for b in result['blockers']}


def test_independent_editorial_neighbor_does_not_block_generation(tmp_path):
    # Given: source-scoped cross-cut with no inherited state from the neighbor.
    p, q = prepared_plan(tmp_path)
    q['focus']['shot_ids'] = ['SH02']
    q['links'][0].update(relation='cross_cut', state_in={}, state_out={},
                        state_not_applicable_reason='No shared state',
                        generation_independence={'reason': 'Separate subject and location',
                                                 'source_locator': 'S02 in edit brief'})
    # When
    codes = {b['code'] for b in validate_sequence(p, q, 'generation', tmp_path)['blockers']}
    # Then: only the generation dependency is waived, not submission authority.
    assert 'predecessor_selection' not in codes
    assert 'actual_state' not in codes
    assert 'execution_authority' in codes


def test_edit_without_actual_selected_sources_cannot_be_ready(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); q['execution_artifact_id'] = 'EDIT'
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert 'source_selection' in {b['code'] for b in result['blockers']}


def test_asset_bytes_changed_after_review_invalidate_gate(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    (tmp_path / 'IM01.png').write_bytes(b'changed')
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert 'asset_hash' in {b['code'] for b in result['blockers']}


def test_unknown_document_shape_returns_actionable_failure(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); q['cuts'] = [None]
    # When
    result = validate_sequence(p, q, 'edit', tmp_path)
    # Then
    assert not result['ready']
    assert result['blockers'][0]['code'] == 'projection_shape'


def test_no_audio_policy_is_preserved(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path); p['audio_mode'] = 'no_audio'
    q['audio_tracks'] = [{'asset_id': 'EVIDENCE'}]
    # When
    result = validate_sequence(p, q, 'plan', tmp_path)
    # Then
    assert 'audio_policy' in {b['code'] for b in result['blockers']}
