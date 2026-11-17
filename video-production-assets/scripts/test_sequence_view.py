"""Display-only context: scoped selection must never become execution authority."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from sequence_context import build_sequence_context
from sequence_contract import SequenceError, read_projection
from test_validate_storyboard import board, shot


def view(project, ids, projection=None):
    from sequence_view import build_sequence_focus_view
    return build_sequence_focus_view(project, ids, projection)


def long_board(count=10):
    p = board()
    p['shots'] = [shot(f'SH{i:02}', i * 2, (i + 1) * 2, ()) for i in range(count)]
    p['storyboard']['panels'] = []; p['storyboard']['beats'] = []
    p['target_duration_s'] = count * 2
    return p


def test_format_bootstrap_nulls_and_non_mutation():
    p = board(); before = copy.deepcopy(p)
    full = build_sequence_context(p, ['SH02']); old = copy.deepcopy(full)
    result = view(p, ['SH02'], full)
    assert (result['format'], result['read_only'], result['executable'], result['validation']) == (
        'sequence-focus-view/1', True, False, 'not_run')
    assert result['cuts'][0]['source_asset_id'] is None
    assert result['source']['project_snapshot'] is None
    assert p == before and full == old
    assert build_sequence_context(p, ['SH02']) == old
    assert view(p, ['SH02'])['source']['origin'] == 'bootstrap'


@pytest.mark.parametrize('ids,expected', [(['SH00'], {'SH00','SH01'}),
    (['SH09'], {'SH08','SH09'}), (['SH03','SH07'], {'SH02','SH03','SH04','SH06','SH07','SH08'})])
def test_actual_edit_neighbors_not_entire_prefix(ids, expected):
    result = view(long_board(), ids)
    assert {r['shot_id'] for r in result['cuts']} == expected
    assert {r['shot_id'] for r in result['requirements']} == set(ids)


def test_all_repeated_shot_cuts_and_time_order_neighbors_survive():
    p = long_board(); q = build_sequence_context(p, ['SH03'])
    q['cuts'][7]['shot_id'] = 'SH03'
    q['cuts'].reverse()  # Serialization order is not edit adjacency.
    result = view(p, ['SH03'], q)
    assert {r['cut_id'] for r in result['cuts']} == {'SH02','SH03','SH04','SH06','SH07','SH08'}
    assert set(result['focus']['cut_ids']) == {'SH03','SH07'}


def test_explicit_nonadjacent_history_closure_and_cycle_without_prefix_expansion():
    p = long_board(); q = build_sequence_context(p, ['SH08'])
    q['links'][7]['history_shot_ids'] = ['SH04']
    q['links'][3]['history_shot_ids'] = ['SH01']
    q['links'][0]['history_shot_ids'] = ['SH04']  # a visited-set cycle
    result = view(p, ['SH08'], q)
    assert {r['cut_id'] for r in result['cuts']} == {'SH01','SH04','SH07','SH08','SH09'}
    history = {r['cut_id'] for r in result['focus']['inclusion'] if 'history' in r['reasons']}
    assert history == {'SH01','SH04'}
    assert result['omissions']['cuts']['omitted'] == 5


@pytest.mark.parametrize('ids', [[], ['UNKNOWN']])
def test_invalid_focus_rejected(ids):
    with pytest.raises(SequenceError, match='focus'):
        view(board(), ids)


@pytest.mark.parametrize('history', [['UNKNOWN'], ['SH08']])
def test_invalid_history_is_not_silently_lost(history):
    p = long_board(); q = build_sequence_context(p, ['SH08'])
    q['links'][7]['history_shot_ids'] = history
    with pytest.raises(SequenceError, match='history'):
        view(p, ['SH08'], q)


def test_invalid_projection_or_missing_focus_cut_rejected():
    p = board(); q = build_sequence_context(p, ['SH02'])
    with pytest.raises(SequenceError, match='projection_format'):
        view(p, ['SH02'], {'format': 'invented'})
    q['cuts'] = q['cuts'][:1]
    with pytest.raises(SequenceError, match='focus'):
        view(p, ['SH02'], q)


def test_global_owner_does_not_reinflate_panels_assets_or_pins():
    p = long_board(100)
    for i, s in enumerate(p['shots']):
        aid = f'IMG{i}'
        p['asset_registry'].append({'id': aid, 'kind': 'image', 'version': '1', 'status': 'planned'})
        p['storyboard']['panels'].append({'id': f'PN{i}', 'shot_id': s['id'], 'frame_time_s': s['start_s'],
            'image_asset_id': aid, 'asset_version_refs': {aid: '1'}, 'beat_ids': []})
    p['artifacts'].append({'id':'BOARD','type':'storyboard','version':'1','status':'draft',
        'dependencies': [], 'dependency_versions': {}, 'asset_ids': [a['id'] for a in p['asset_registry']],
        'required_asset_versions': {a['id']: '1' for a in p['asset_registry']}})
    q = build_sequence_context(p, ['SH42']); q['owner']['artifact_id'] = 'BOARD'
    q['inputs']['assets'] = {a['id']: {'version':'1'} for a in p['asset_registry']}
    result = view(p, ['SH42'], q)
    assert len(result['context']['storyboard']['panels']) == 3
    assert {a['id'] for a in result['context']['asset_registry']} == {'IMG41','IMG42','IMG43'}
    assert set(result['inputs']['assets']) == {'IMG41','IMG42','IMG43'}
    assert 'IMG99' not in json.dumps(result)
    owner = next(a for a in result['context']['artifacts'] if a['id'] == 'BOARD')
    assert owner['locator'] and owner['omitted_fields']


def test_master_look_voice_and_selected_source_pins_remain_with_stale_issue():
    p = board()
    p['look_asset_id'] = 'LOOK'
    p['asset_registry'].extend([
        {'id':'LOOK','version':'1','kind':'document','status':'verified'},
        {'id':'MASTER','version':'2','kind':'image','status':'verified'},
        {'id':'DERIV','version':'1','kind':'image','status':'stale','master_asset_ref':{'asset_id':'MASTER','version':'1'}},
        {'id':'VOICE','version':'1','kind':'audio','status':'verified'}])
    p['shots'][0]['asset_ids'] = ['DERIV']
    next(a for a in p['artifacts'] if a['id'] == 'VO01')['asset_ids'] = ['VOICE']
    q = build_sequence_context(p, ['SH02'])
    q['cuts'][0].update(source_asset_id='DERIV', source_in_frame=24, source_out_frame=72,
                       source_fps=24, source_frame_count=96)
    result = view(p, ['SH02'], q)
    assert {'LOOK','MASTER','DERIV','VOICE'} <= {a['id'] for a in result['context']['asset_registry']}
    assert result['cuts'][0]['source_out_frame'] == 72
    assert any(i['code'] == 'stale_pin' for i in result['issues'])


def test_different_focus_handoff_does_not_masquerade_as_current_packet():
    p = board(); q = build_sequence_context(p, ['SH01'])
    q['generation_handoff'] = {'bindings':[{'reference_asset_id':'IM01','request_clause':'do not rewrite me'}]}
    q['submission_asset_id'] = 'REQUEST'
    result = view(p, ['SH02'], q)
    assert result['handoff_applicability'] == 'mismatch'
    assert result['handoff']['scope_shot_ids'] == ['SH01']
    assert 'bindings' not in result['handoff']
    assert q['generation_handoff']['bindings'][0]['request_clause'] == 'do not rewrite me'


def test_same_focus_native_bindings_kept_verbatim_and_assets_closed():
    p = board(); q = build_sequence_context(p, ['SH02'])
    p['asset_registry'].append({'id':'REQUEST','kind':'document','version':'1','status':'planned'})
    q['submission_asset_id'] = 'REQUEST'
    q['generation_handoff'] = {'adapter':'fixture','bindings':[
        {'reference_asset_id':'IM01','purpose':'visual_state','role':'reference','imports':['hand'],
         'excludes':['old_camera'], 'request_clause':'Preserve hand, exclude old camera.'}]}
    result = view(p, ['SH02'], q)
    assert result['handoff_applicability'] == 'applicable'
    assert result['handoff']['bindings'] == q['generation_handoff']['bindings']
    assert 'REQUEST' in {a['id'] for a in result['context']['asset_registry']}


def test_display_view_cannot_be_parsed_as_executable_projection(tmp_path: Path):
    path = tmp_path / 'display.json'; path.write_text(json.dumps(view(board(), ['SH02'])))
    with pytest.raises(SequenceError, match='projection_format'):
        read_projection(path)


def test_real_image_backed_package_keeps_native_lineage_without_global_expansion(tmp_path):
    from av_handoff_test_fixture import prepared_handoff
    p, q = prepared_handoff(tmp_path)
    p['look_asset_id'] = 'LOOK'
    p['asset_registry'].append({'id':'LOOK','kind':'document','version':'1','status':'planned'})
    result = view(p, ['SH02'], q)
    selected = {a['id'] for a in result['context']['asset_registry']}
    assert {'LOOK','REF_VIDEO','REF_AUDIO','VIDEO0','REQUEST','CAP','SESSION','REFS','UPLOADS'} <= selected
    assert result['handoff']['bindings'] == q['generation_handoff']['bindings']
    assert result['cuts'][0]['source_in_frame'] == 12
    assert result['cuts'][0]['source_out_frame'] == 60
    assert any(a['type'] == 'storyboard' for a in result['context']['artifacts'])


@pytest.mark.parametrize('key,value', [('generation_handoff', []), ('focus', []), ('inputs', {'assets':[]})])
def test_malformed_nested_projection_returns_located_error(key, value):
    p = board(); q = build_sequence_context(p, ['SH02']); q[key] = value
    with pytest.raises(SequenceError):
        view(p, ['SH02'], q)


def test_scope_check_retains_only_declared_scope_locator_not_global_pass_claim():
    p = board(); q = build_sequence_context(p, ['SH02'])
    q['checks'] = [{'target':'scope','kind':'source_audio','status':'pass',
                    'observed_asset_ids':['unrelated'], 'cut_ranges':{'unrelated':{}}}]
    result = view(p, ['SH02'], q)
    assert result['checks'][0]['applicability'] == 'not_inferred'
    assert 'unrelated' not in json.dumps(result)


def test_declared_large_history_is_not_cut_to_a_token_cap():
    p = long_board(100); q = build_sequence_context(p, ['SH98'])
    q['links'][97]['history_shot_ids'] = [f'SH{i:02}' for i in range(80)]
    result = view(p, ['SH98'], q)
    assert len(result['cuts']) == 83
    assert all(f'SH{i:02}' in {c['shot_id'] for c in result['cuts']} for i in range(80))


def test_snapshot_hash_and_parse_come_from_one_raw_read(tmp_path: Path, monkeypatch):
    from sequence_contract import read_snapshot
    path = tmp_path / 'project.json'; raw = b'{"project_id":"fixture"}\r\n'
    path.write_bytes(raw)
    original = Path.read_bytes; calls = []
    def read_once(self):
        calls.append(self)
        value = original(self)
        self.write_bytes(b'{"project_id":"mutated"}')
        return value
    monkeypatch.setattr(Path, 'read_bytes', read_once)
    value, snapshot = read_snapshot(path)
    assert value['project_id'] == 'fixture'
    assert snapshot['sha256'] == hashlib.sha256(raw).hexdigest()
    assert calls == [path]
