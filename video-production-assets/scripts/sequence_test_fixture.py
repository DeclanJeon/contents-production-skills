"""Synthetic declarations for gate tests; not perceptually approved footage."""
import hashlib
from pathlib import Path
from PIL import Image
from test_validate_storyboard import board
from sequence_context import build_sequence_context


def prepared_plan(root: Path):
    p = board()
    p['artifacts'].append({'id': 'EDIT', 'type': 'edit_plan', 'version': '1',
        'status': 'approved', 'approval': {'by': 'fixture', 'at': '2026-11-17', 'evidence': 'synthetic test authorization'},
        'dependencies': [], 'dependency_versions': {},
        'execution_scope': {'shot_ids': ['SH01', 'SH02'], 'operations': ['edit', 'export']}})
    for row in p['asset_registry']:
        path = root / f'{row["id"]}.png'
        Image.new('RGB', (16, 16), 'white').save(path)
        row.update(path=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), status='verified')
    evidence = root / 'evidence.txt'; evidence.write_text('synthetic declarations; not actual quality inspection')
    p['asset_registry'].append({'id': 'EVIDENCE', 'version': '1', 'kind': 'document', 'status': 'available',
        'path': evidence.name, 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()})
    q = build_sequence_context(p, ['SH01', 'SH02'])
    q['owner'].update(artifact_id='EDIT', artifact_version='1')
    q['inputs'] = {'artifact_versions': {'EDIT': '1', 'SYN': '1'},
                   'assets': {a['id']: {'version': a['version'], 'sha256': a['sha256']} for a in p['asset_registry']}}
    q['links'][0].update(relation='angle_change', state_out={'door': 'closed'}, state_in={'door': 'closed'})
    for panel in p['storyboard']['panels']:
        q['checks'].append(check('panel:' + panel['id'], 'plan_image', [panel['image_asset_id']], 'opened_image'))
    q['checks'].append(check('scope', 'plan_timing', [], 'continuous_playback'))
    return p, q


def check(target, kind, observed, method='frame_step'):
    return {'target': target, 'kind': kind, 'status': 'pass', 'method': method,
            'evidence_asset_id': 'EVIDENCE', 'observed_asset_ids': observed,
            'asset_versions': {aid: '1' for aid in observed},
            'observation': 'synthetic observation for testing record validation only'}
