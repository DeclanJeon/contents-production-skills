"""Timing promotion requires an existing pinned delegated editing authority."""
import copy
import json
import pytest
from test_validate_project import project
from update_project import prepare_update, apply_update


def timing_update():
    p = project()
    p['artifacts'][0].update(type='edit_plan', status='approved',
        approval={'by': 'fixture', 'at': '2026-11-17', 'evidence': 'synthetic delegated edit authorization'},
        timing_policy={'duration': 'flexible', 'anchors': []})
    d = {'project_id': p['project_id'], 'base_version': '1', 'version': '2',
         'input_versions': {'A01': '1'}, 'owner_artifact_ids': ['A01'],
         'project': {'target_duration_s': 1},
         'changes': {'artifacts': [{'id': 'A01', 'version': '2'}], 'shots': [{'id': 'SH01', 'end_s': 1}]}}
    return p, d


def test_flexible_duration_and_shots_promote_together(tmp_path):
    # Given
    p, d = timing_update(); path = tmp_path / 'project.json'; path.write_text(json.dumps(p))
    # When
    apply_update(path, d)
    # Then
    saved = json.loads(path.read_text())
    assert (saved['target_duration_s'], saved['shots'][0]['end_s'], saved['version']) == (1, 1, '2')


def test_unpinned_timing_permission_does_not_authorize_change():
    # Given
    p, d = timing_update(); d['input_versions'] = {}
    # When / Then
    with pytest.raises(ValueError, match='timing_authority'):
        prepare_update(p, d)


def test_fixed_duration_cannot_be_shortened():
    # Given
    p, d = timing_update(); p['artifacts'][0]['timing_policy']['duration'] = 'fixed'
    # When / Then
    with pytest.raises(ValueError, match='fixed_duration'):
        prepare_update(p, d)


def test_locked_anchor_cannot_be_moved():
    # Given
    p, d = timing_update()
    p['artifacts'][0]['timing_policy']['anchors'] = [{'table': 'shots', 'id': 'SH01', 'field': 'end_s', 'frame': 48}]
    # When / Then
    with pytest.raises(ValueError, match='fixed_anchor'):
        prepare_update(p, d)


def test_invalid_related_cue_keeps_original_ledger_bytes(tmp_path):
    # Given
    p, d = timing_update(); p['audio_mode'] = 'no_dialogue'
    p['audio_cues'] = [{'id': 'AU01', 'start_s': 0, 'end_s': 2, 'layer': 'music'}]
    path = tmp_path / 'project.json'; original = json.dumps(p).encode(); path.write_bytes(original)
    # When / Then
    with pytest.raises(ValueError, match='candidate rejected'):
        apply_update(path, d)
    assert path.read_bytes() == original
    assert not (tmp_path / '.project.json.lock').exists()
