"""Scoped context follows edit neighbors and explicit narrative history."""
import copy
import pytest
from test_validate_storyboard import board
from sequence_contract import SequenceError
from sequence_context import build_sequence_context


def test_following_shot_receives_predecessor_frames_without_adopting_latest_take():
    # Given
    p = board(); before = copy.deepcopy(p)
    p['generation_attempts'] = [{'id': 'TRY1', 'shot_id': 'SH01', 'attempt': 1,
                                'route': 'fixture', 'result': 'reject'}]
    # When
    result = build_sequence_context(p, ['SH02'])
    # Then
    assert result['focus']['shot_ids'] == ['SH02']
    assert {s['id'] for s in result['context']['shots']} == {'SH01', 'SH02'}
    assert result['cuts'][1]['final_in_frame'] == 48
    assert result['links'][0]['planned_out_panel_id'] == 'P02'
    assert result['links'][0]['planned_in_panel_id'] == 'P03'
    assert result['cuts'][0]['source_asset_id'] is None
    assert result['context']['generation_attempts'][0]['result'] == 'reject'
    assert before['shots'] == p['shots']


def test_explicit_history_survives_cutaway():
    # Given
    p = board()
    p['shots'].append(dict(p['shots'][1], id='SH03', start_s=4, end_s=6, speech=[]))
    p['target_duration_s'] = 6
    projection = build_sequence_context(p, ['SH01', 'SH02', 'SH03'])
    projection['links'][1]['history_shot_ids'] = ['SH01']
    # When
    result = build_sequence_context(p, ['SH03'], projection)
    # Then
    assert {s['id'] for s in result['context']['shots']} == {'SH01', 'SH02', 'SH03'}


def test_unknown_focus_is_rejected():
    # Given / When / Then
    with pytest.raises(SequenceError, match='focus'):
        build_sequence_context(board(), ['missing'])


def test_empty_focus_does_not_implicitly_load_whole_project():
    # Given / When / Then
    with pytest.raises(SequenceError, match='focus'):
        build_sequence_context(board(), [])


def test_unresolved_owner_selection_is_explicit():
    # Given
    p = board()
    # When
    result = build_sequence_context(p, ['SH01'])
    # Then
    assert result['owner']['artifact_id'] is None
    assert result['requirements'][0]['evidence'] == 'planned'
    assert result['requirements'][0]['source_locator'] == 'paragraph 1'
