"""Synthetic native receipts exercise transport checks, not provider behavior."""
import copy
import hashlib
import json
import subprocess
from sequence_contract import file_hash
from test_sequence_media import prepared_edit
from sequence_test_fixture import check
from test_validate_preproduction import image_package

SESSION = '00000000-0000-4000-8000-000000000100'


def prepared_handoff(root):
    p, q = prepared_edit(root)
    package = image_package(root)
    known = {a['id'] for a in package['asset_registry']}
    package['asset_registry'].extend(a for a in p['asset_registry'] if a['id'] not in known)
    package['artifacts'].append(next(a for a in p['artifacts'] if a['id'] == 'EDIT'))
    p = package
    approval = {'by': 'fixture', 'at': '2026-11-17', 'evidence': 'synthetic explicit authority'}
    p['artifacts'].extend([
        {'id': 'REVIEW', 'type': 'preproduction_review', 'version': '1', 'status': 'approved',
         'approval': approval, 'dependencies': ['SHEET'], 'dependency_versions': {'SHEET': '1'}},
        {'id': 'EXEC', 'type': 'video_execution_plan', 'version': '1', 'status': 'approved',
         'approval': approval, 'dependencies': ['REVIEW'], 'dependency_versions': {'REVIEW': '1'},
         'execution_scope': {'shot_ids': ['SH02'], 'operations': ['generation']}}])
    q['focus']['shot_ids'] = ['SH02']; q['cuts'][1]['scene_id'] = 'S02'
    q['execution_artifact_id'] = 'EXEC'
    q['links'][0]['predecessor_state_evidence'] = 'observed'
    for r in q['requirements']:
        r.update(request_clause='synthetic required direction', control_status='SOFT_PROMPT')

    def asset(aid, path, kind='document', **extra):
        row = {'id': aid, 'version': '1', 'kind': kind, 'status': 'available',
               'path': path.name, 'sha256': file_hash(path), **extra}
        p['asset_registry'].append(row)
        return row

    def document(aid, name, data):
        path = root / name; path.write_text(json.dumps(data))
        return asset(aid, path)

    video, audio = root / 'previous-selected.mkv', root / 'previous-selected.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(root / 'VIDEO0.mkv'),
        '-vf', 'trim=start_frame=12:end_frame=60,setpts=PTS-STARTPTS',
        '-af', 'atrim=start=0.5:end=2.5,asetpts=PTS-STARTPTS', '-c:v', 'ffv1', '-c:a', 'pcm_s16le', str(video)], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vn', '-c:a', 'pcm_s16le', str(audio)], check=True)
    parent = next(a for a in p['asset_registry'] if a['id'] == 'VIDEO0')
    lineage = {'source_asset_id': 'VIDEO0', 'source_asset_version': parent['version'], 'source_sha256': parent['sha256'],
               'source_in_frame': 12, 'source_out_frame': 60,
               'source_fps': {'num': 24, 'den': 1}}
    asset('REF_VIDEO', video, 'video', source_asset_ids=['VIDEO0'], sequence_slice=lineage)
    asset('REF_AUDIO', audio, 'audio', source_asset_ids=['VIDEO0'], sequence_slice=lineage)
    voice = next(a for a in p['artifacts'] if a['id'] == 'VO01')
    voice.update(status='verified', asset_ids=['REF_AUDIO'], evidence='synthetic voice anchor declaration')
    bindings, items, uploads = [], [], []
    choices = [('REF_VIDEO', 'video', 'visual_state', 'reference', 'SH01'),
               ('REF_AUDIO', 'audio', 'audio_context', 'reference', 'SH01'),
               ('REF_AUDIO', 'audio', 'voice_identity', 'voice_timbre', None),
               ('IM03', 'image', 'current_composition', 'first_frame', None)]
    registry = {a['id']: a for a in p['asset_registry']}
    for index, (aid, modality, purpose, role, source_cut) in enumerate(choices, 1):
        rid = f'00000000-0000-4000-8000-{index:012d}'
        native = f'00000000-0000-4000-8000-{index+1000:012d}'
        bindings.append({'key': purpose, 'reference_asset_id': aid, 'modality': modality,
            'purpose': purpose, 'source_cut_id': source_cut, 'voice_artifact_id': 'VO01' if purpose == 'voice_identity' else None,
            'native_reference_id': rid, 'native_asset_id': native, 'role': role,
            'imports': ['relevant_state'], 'excludes': ['repeat_dialogue', 'repeat_action', 'previous_camera'],
            'request_clause': f'Use input {index} for {purpose}; preserve relevant state, exclude dialogue/action replay and previous camera.'})
        items.append({'id': rid, 'asset_id': native, 'state': 'ready', 'kind': modality,
                      'role': role, 'model_requirement': 'required', 'asset_archived': False, 'has_audio': modality != 'image'})
        uploads.append({'reference_asset_id': aid, 'sha256': registry[aid]['sha256'],
                        'native_asset_id': native, 'native_reference_id': rid,
                        'status': 'confirmed', 'put_status': 200})
    request = {'session_id': SESSION, 'expected_revision': 7, 'client_message_id': 'synthetic-id',
        'idempotency_key': 'synthetic-no-submit', 'message': {'text': 'synthetic required direction\n' + '\n'.join(b['request_clause'] for b in bindings),
        'reference_ids': [b['native_reference_id'] for b in bindings],
        'video_model_selection': 'singularity-full-v2', 'audio_policy': 'prompt_only'}}
    document('REQUEST', 'request.json', request)
    document('CAP', 'capability.json', {'capability_id': 'ludyte.task-agent', 'contract_version': '1.14.0',
        'message_input_schema': {'properties': {'reference_ids': {'type': 'array', 'maxItems': 12,
        'items': {'type': 'string', 'format': 'uuid'}}, 'video_model_selection': {'enum': ['singularity-full-v2']},
        'audio_policy': {'enum': ['prompt_only', 'no_audio']}}}})
    document('SESSION', 'session.json', {'tool': 'mcp__Ludyte__get_session', 'arguments': {'session_id': SESSION},
        'result': {'structuredContent': {'session_id': SESSION, 'revision': 7}}})
    document('REFS', 'references.json', {'tool': 'mcp__Ludyte__get_session_assets', 'arguments': {'session_id': SESSION},
        'result': {'structuredContent': {'items': items, 'next_cursor': None}}})
    document('UPLOADS', 'uploads.json', {'records': uploads, 'limits': 'synthetic upload declarations, not real uploads'})
    q['checks'].append(check('voice:VO01', 'voice_anchor', ['REF_AUDIO'], 'listening'))
    q['submission_asset_id'] = 'REQUEST'
    q['generation_handoff'] = {'adapter': 'ludyte', 'tool': 'mcp__Ludyte__send_message',
        'contract_asset_id': 'CAP', 'session_snapshot_asset_id': 'SESSION',
        'references_snapshot_asset_id': 'REFS', 'uploads_asset_id': 'UPLOADS', 'bindings': bindings}
    q['inputs'] = {'artifact_versions': {a['id']: a['version'] for a in p['artifacts']},
                   'assets': {a['id']: {'version': a['version'], 'sha256': a['sha256']} for a in p['asset_registry']}}
    return p, q


def prepared_history_handoff(root):
    """Return after an insert; identical source bytes still need explicit cut roles."""
    p, q = prepared_handoff(root)
    p['target_duration_s'] = 6
    following = next(s for s in p['shots'] if s['id'] == 'SH02')
    following['start_s'] += 2; following['end_s'] += 2
    for speech in following.get('speech', []):
        speech['start_s'] += 2; speech['end_s'] += 2
    insert = copy.deepcopy(p['shots'][0])
    insert.update(id='INSERT', start_s=2, end_s=4, beat_ids=['B_INSERT'], speech=[])
    p['shots'].insert(1, insert)
    p['storyboard']['beats'].insert(1, dict(p['storyboard']['beats'][0], id='B_INSERT'))
    for cue in p['audio_cues']:
        cue['end_s'] = 6
    panels = []
    for panel in p['storyboard']['panels']:
        if panel['shot_id'] == 'SH02':
            panel['frame_time_s'] += 2
        elif panel['shot_id'] == 'SH01':
            row = copy.deepcopy(panel)
            row.update(id='INSERT_' + panel['id'], shot_id='INSERT',
                       frame_time_s=panel['frame_time_s'] + 2, beat_ids=['B_INSERT'], speech_ids=[])
            panels.append(row)
    p['storyboard']['panels'].extend(panels)
    p['storyboard']['panels'].sort(key=lambda row: row['frame_time_s'])
    selected = copy.deepcopy(q['cuts'][0])
    selected.update(cut_id='INSERT', shot_id='INSERT', final_in_frame=48, final_out_frame=96,
                    planned_panel_ids=[r['id'] for r in panels])
    q['cuts'][1]['final_in_frame'] += 48; q['cuts'][1]['final_out_frame'] += 48
    q['cuts'].insert(1, selected)
    q['links'][0].update(key='SH01->INSERT', to_cut_id='INSERT')
    link = copy.deepcopy(q['links'][0])
    link.update(key='INSERT->SH02', from_cut_id='INSERT', to_cut_id='SH02',
                history_shot_ids=['SH01'], history_state_evidence='synthetic declared return state')
    q['links'].append(link)
    requirements = []
    for req in q['requirements']:
        if req['shot_id'] == 'SH02':
            req['final_in_frame'] += 48; req['final_out_frame'] += 48
        elif req['shot_id'] == 'SH01' and req['kind'] != 'speech':
            row = copy.deepcopy(req)
            row.update(key='INSERT:' + req['key'], shot_id='INSERT', cut_ids=['INSERT'],
                       panel_ids=[r['id'] for r in panels], final_in_frame=48, final_out_frame=96,
                       entity_id='B_INSERT' if req['kind'] == 'beat' else 'INSERT')
            requirements.append(row)
    q['requirements'].extend(requirements)
    original_checks = copy.deepcopy(q['checks'])
    for record in original_checks:
        if record['target'] == 'cut:SH01':
            row = copy.deepcopy(record); row['target'] = 'cut:INSERT'; q['checks'].append(row)
    q['checks'].extend(check('panel:' + row['id'], 'plan_image', [row['image_asset_id']], 'opened_image') for row in panels)
    for record in q['checks']:
        if 'cut_ranges' in record:
            record['cut_ranges'] = {c['cut_id']: {k: c[k] for k in
                ('source_asset_id', 'source_in_frame', 'source_out_frame', 'final_in_frame', 'final_out_frame')}
                for c in q['cuts'] if c['source_asset_id'] in record['observed_asset_ids']}
    for binding in q['generation_handoff']['bindings']:
        if binding['source_cut_id'] == 'SH01':
            binding['source_cut_id'] = 'INSERT'
    # Keep the complete image-backed package valid after inserting two panels.
    from render_storyboard_sheet import render_sheet
    from split_storyboard import split_storyboard
    sheet = render_sheet(p, root, 'history-sheet.png')
    sheet_asset = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
    sheet_asset.update(path='history-sheet.png', sha256=sheet['sha256'],
                       panel_ids=sheet['panel_ids'], source_asset_ids=sheet['source_asset_ids'],
                       source_sha256=sheet['source_sha256'])
    folder = root / 'history-extracts'
    split_storyboard(p, root, folder, ['history-sheet.png'])
    for index, path in enumerate(sorted(folder.rglob('*'))):
        if not path.is_file():
            continue
        row = {'id': f'HISTORY_EXTRACT{index}', 'version': '1', 'kind': 'image',
               'status': 'available', 'path': path.relative_to(root).as_posix(), 'sha256': file_hash(path)}
        if path.name == 'split-manifest.json':
            next(a for a in p['asset_registry'] if a['id'] == 'SPLIT').update(path=row['path'], sha256=row['sha256'])
        else:
            p['asset_registry'].append(row)
    q['inputs']['assets'] = {a['id']: {'version': a['version'], 'sha256': a['sha256']} for a in p['asset_registry']}
    return p, q


def add_history_bindings(p, q, root):
    """Select separate native roles for the historical cut, not just its neighbor."""
    h = q['generation_handoff']
    previous = [b for b in h['bindings'] if b['source_cut_id'] == 'INSERT']
    refs = json.loads((root / 'references.json').read_text())['result']['structuredContent']['items']
    uploads = json.loads((root / 'uploads.json').read_text())['records']
    for index, original in enumerate(previous, 20):
        binding = copy.deepcopy(original)
        binding.update(key='history_' + original['key'], source_cut_id='SH01',
                       native_reference_id=f'00000000-0000-4000-8000-{index:012d}')
        h['bindings'].append(binding)
        ref = dict(next(r for r in refs if r['id'] == original['native_reference_id']), id=binding['native_reference_id'])
        receipt = dict(next(r for r in uploads if r['native_reference_id'] == original['native_reference_id']),
                       native_reference_id=binding['native_reference_id'])
        rewrite_document(p, q, root, 'REFS', lambda d: d['result']['structuredContent']['items'].append(ref))
        rewrite_document(p, q, root, 'UPLOADS', lambda d: d['records'].append(receipt))
    rewrite_document(p, q, root, 'REQUEST', lambda d: d['message'].update(reference_ids=[b['native_reference_id'] for b in h['bindings']]))


def rewrite_document(p, q, root, aid, change):
    row = next(a for a in p['asset_registry'] if a['id'] == aid)
    path = root / row['path']; doc = json.loads(path.read_text()); change(doc)
    path.write_text(json.dumps(doc)); row['sha256'] = file_hash(path)
    q['inputs']['assets'][aid]['sha256'] = row['sha256']
