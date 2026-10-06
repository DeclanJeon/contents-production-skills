"""v5.1 asset-integrity gates: finality, lineage drift, multi-sheet, packaging.

Fixture bytes are synthetic contract fixtures, not rendered media samples.
"""
import copy
import csv
import hashlib
import io
import json
import zipfile
import tempfile
import unittest
import os
from unittest.mock import patch
from pathlib import Path
from PIL import Image
from test_validate_project import project
from test_validate_storyboard import board
from test_validate_preproduction import image_package
from package_production import build_package
from update_project import prepare_update
from validate_project import validate


def gate_project():
    """Plan-level project with a look, one master and one derivative asset."""
    p = project()
    p['asset_registry'] = [
        {'id': 'LOOK01', 'kind': 'document', 'version': '1', 'status': 'verified',
         'path': 'bible.md', 'entity_type': 'look', 'role': 'master'},
        {'id': 'CH01M', 'kind': 'image', 'version': '1', 'status': 'verified',
         'path': 'master.png', 'entity_type': 'character', 'role': 'master'},
        {'id': 'CH01D', 'kind': 'image', 'version': '1', 'status': 'verified',
         'path': 'state.png', 'entity_type': 'character', 'role': 'derivative',
         'master_asset_ref': {'asset_id': 'CH01M', 'version': '1'}},
    ]
    p['look_asset_id'] = 'LOOK01'
    return p


def final_board(p, required=None, finality='final', status='reviewed'):
    p['artifacts'].append({
        'id': 'BOARD', 'type': 'storyboard', 'version': '1', 'status': status,
        'finality': finality,
        'required_asset_versions': required if required is not None
        else {'CH01M': '1', 'CH01D': '1', 'LOOK01': '1'},
        'dependencies': [], 'dependency_versions': {}})
    return p


class FinalityGateTests(unittest.TestCase):
    def test_final_artifact_needs_locked_exact_version_assets(self):
        p = final_board(gate_project())
        self.assertEqual(validate(p), [])

    def test_final_rejects_draft_missing_and_version_drift(self):
        # validate() keeps declared-shape checks; lock/availability enforcement
        # lives in the gate so unrelated finality states do not block plan work.
        from asset_gate import check_asset_gate
        cases = [
            ('cannot be declared final', 'cannot be final', lambda p: p['artifacts'][-1].update(status='draft')),
            ('needs required_asset_versions', 'needs required_asset_versions', lambda p: p['artifacts'][-1].pop('required_asset_versions')),
            ('version drift', 'version drift', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(version='2')),
            ('not registered', 'not registered', lambda p: p['artifacts'][-1]['required_asset_versions'].update(GONE='1')),
            ('is not locked', 'is not locked', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'CH01D').update(status='planned')),
            ('is not locked', 'is not locked', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(status='available')),
            ('stale artifact', 'stale artifact', lambda p: p['artifacts'][-1].update(dependencies=['A01'], dependency_versions={'A01': '1'}, status='reviewed') or p['artifacts'][0].update(status='stale')),
        ]
        for validate_fragment, gate_fragment, change in cases:
            with self.subTest(fragment=validate_fragment):
                p = final_board(gate_project())
                change(p)
                self.assertTrue(any(validate_fragment in e or gate_fragment in e
                                    for e in validate(p) + check_asset_gate(p)),
                                validate(p) + check_asset_gate(p))

    def test_final_visual_board_requires_verified_pinned_active_look(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        del p['look_asset_id']
        blockers = check_asset_gate(p)
        self.assertTrue(any('look_asset_id' in b for b in blockers), blockers)
        p = final_board(gate_project())
        p['artifacts'][-1]['required_asset_versions'].pop('LOOK01')
        self.assertTrue(any('must pin the active look' in b for b in check_asset_gate(p)))

    def test_transitive_dependency_chain_blocks_final(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        p['artifacts'].append({'id': 'MID', 'type': 'document', 'version': '1',
                               'status': 'reviewed', 'dependencies': ['A01'],
                               'dependency_versions': {'A01': '1'}})
        p['artifacts'][-2].update(dependencies=['MID'], dependency_versions={'MID': '1'})
        p['artifacts'][0].update(status='draft')
        blockers = check_asset_gate(p)
        self.assertTrue(any('still a draft' in b for b in blockers), blockers)
        p['artifacts'][0].update(version='2')
        blockers = check_asset_gate(p)
        self.assertTrue(any('version drift' in b for b in blockers), blockers)

    def test_preliminary_board_keeps_unfinished_inputs(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project(), finality='preliminary')
        next(a for a in p['asset_registry'] if a['id'] == 'CH01D').update(status='planned')
        self.assertEqual(validate(p), [])
        self.assertEqual(check_asset_gate(p), [])
        p['artifacts'][-1]['finality'] = 'final'
        self.assertTrue(any('is not locked' in e for e in check_asset_gate(p)))

    def test_final_rejects_unavailable_active_look(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        next(a for a in p['asset_registry'] if a['id'] == 'LOOK01').update(status='planned')
        self.assertTrue(any('active look' in e for e in check_asset_gate(p)))

    def test_look_must_reference_a_look_entity(self):
        p = gate_project()
        next(a for a in p['asset_registry'] if a['id'] == 'LOOK01').update(entity_type='prop')
        self.assertTrue(any('look asset' in e for e in validate(p)))
        p['look_asset_id'] = 'NOPE'
        self.assertTrue(any('unknown asset_registry' in e for e in validate(p)))

class AssetGateFunctionTests(unittest.TestCase):
    def test_clear_gate_returns_no_blockers(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        self.assertEqual(check_asset_gate(p), [])

    def test_available_master_blocks_final_even_with_real_file(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(status='available')
        blockers = check_asset_gate(p)
        self.assertTrue(any('CH01M' in b and 'not locked' in b for b in blockers), blockers)

    def test_scoped_gate_ignores_unrelated_final_artifacts(self):
        from asset_gate import check_asset_gate
        p = final_board(gate_project())
        p['artifacts'].append({'id': 'ANIM', 'type': 'animatic', 'version': '1',
                               'status': 'reviewed', 'finality': 'final',
                               'required_asset_versions': {'GONE': '1'},
                               'dependencies': [], 'dependency_versions': {}})
        self.assertTrue(any('GONE' in b for b in check_asset_gate(p)))
        self.assertEqual(check_asset_gate(p, ['BOARD']), [])
        self.assertTrue(any('not registered' in b for b in check_asset_gate(p, ['NOPE'])))

    def test_shared_extraction_readiness_accepts_current_registered_outputs(self):
        from asset_gate import validate_storyboard_extractions
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            self.assertEqual(validate_storyboard_extractions(p, root), [])


class LineageTests(unittest.TestCase):
    def test_derivative_must_pin_current_master_version(self):
        p = gate_project()
        next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(version='2')
        self.assertTrue(any('master version drift' in e for e in validate(p)))

    def test_stale_derivative_may_keep_older_pin(self):
        p = gate_project()
        next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(version='2')
        next(a for a in p['asset_registry'] if a['id'] == 'CH01D').update(status='stale')
        self.assertFalse(any('master version drift' in e for e in validate(p)), validate(p))

    def test_derivative_cannot_derive_from_stale_master(self):
        p = gate_project()
        next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(status='stale')
        self.assertTrue(any('derives from stale master' in e for e in validate(p)))

    def test_final_gate_rejects_unverified_ancestor_through_verified_derivative(self):
        from asset_gate import check_asset_gate
        p = gate_project()
        master = next(a for a in p['asset_registry'] if a['id'] == 'CH01M')
        next(a for a in p['asset_registry'] if a['id'] == 'CH01D').update(
            master_asset_ref={'asset_id': 'CH01M', 'version': '1'})
        p['asset_registry'].append({
            'id': 'CH01D2', 'kind': 'image', 'version': '1', 'status': 'verified',
            'role': 'derivative', 'master_asset_ref': {'asset_id': 'CH01D', 'version': '1'}})
        master.update(status='planned')
        final_board(p, required={'CH01D2': '1', 'LOOK01': '1'})
        blockers = check_asset_gate(p)
        self.assertTrue(any('master asset CH01M is not verified' in item for item in blockers))
        master.update(status='verified')
        self.assertEqual(check_asset_gate(p), [])

    def test_final_gate_rejects_unverified_direct_master_states_and_pin_drift(self):
        from asset_gate import check_asset_gate
        for status in ('planned', 'missing', 'stale', 'available'):
            with self.subTest(status=status):
                p = final_board(gate_project())
                next(a for a in p['asset_registry'] if a['id'] == 'CH01M').update(
                    status=status)
                blockers = check_asset_gate(p)
                self.assertTrue(any('CH01M' in item for item in blockers), blockers)

        p = final_board(gate_project())
        next(a for a in p['asset_registry'] if a['id'] == 'CH01D').update(
            master_asset_ref={'asset_id': 'CH01M', 'version': '2'})
        blockers = check_asset_gate(p)
        self.assertTrue(any('version drift' in item for item in blockers), blockers)

    def test_master_change_stales_derivatives_and_dependents_not_unrelated(self):
        p = final_board(gate_project())
        p['artifacts'].append({'id': 'AUDIO', 'type': 'audio_map', 'version': '1',
                               'status': 'approved',
                               'approval': {'by': 't', 'at': '2026', 'evidence': 'x'},
                               'dependencies': [], 'dependency_versions': {}})
        for aid, kind, parent in [('SHEET', 'storyboard_sheet', 'BOARD'),
                                  ('GEN', 'generation_spec', 'SHEET'),
                                  ('ANIMATIC', 'animatic', 'GEN')]:
            p['artifacts'].append({'id': aid, 'type': kind, 'version': '1',
                                   'status': 'reviewed', 'dependencies': [parent],
                                   'dependency_versions': {parent: '1'}})
        delta = {'project_id': p['project_id'], 'base_version': p['version'], 'version': '2',
                 'changes': {'asset_registry': [{'id': 'CH01M', 'version': '2'}]},
                 'owner_artifact_ids': ['A01'],
                 }
        delta['changes']['artifacts'] = [{'id': 'A01', 'version': '2'}]
        updated, touched, stale = prepare_update(p, delta)
        rows = {a['id']: a for a in updated['asset_registry']}
        self.assertEqual(rows['CH01D']['status'], 'stale')
        self.assertEqual(touched['stale_asset_ids'], ['CH01D'])
        arts = {a['id']: a for a in updated['artifacts']}
        self.assertEqual(arts['BOARD']['status'], 'stale')     # required asset pin drifted
        self.assertEqual(stale, ['ANIMATIC', 'BOARD', 'GEN', 'SHEET'])
        self.assertTrue(all(arts[aid]['status'] == 'stale' for aid in stale))
        self.assertEqual(arts['AUDIO']['status'], 'approved')  # unrelated downstream stays valid

    def test_retired_master_stales_whole_derivative_chain(self):
        p = final_board(gate_project())
        delta = {'project_id': p['project_id'], 'base_version': p['version'], 'version': '2',
                 'changes': {'asset_registry': [{'id': 'CH01M', 'status': 'stale'}]},
                 'owner_artifact_ids': ['A01'],
                 }
        delta['changes']['artifacts'] = [{'id': 'A01', 'version': '2'}]
        updated, touched, stale = prepare_update(p, delta)
        self.assertEqual(touched['stale_asset_ids'], ['CH01D'])
        arts = {a['id']: a for a in updated['artifacts']}
        self.assertEqual(arts['BOARD']['status'], 'stale')


class ProvenanceTests(unittest.TestCase):
    def test_unknown_and_not_exposed_are_valid_provenance_values(self):
        p = project()
        p['asset_registry'] = [{'id': 'IM01', 'kind': 'image', 'version': '1',
                                'status': 'planned', 'prompt': 'real prompt',
                                'provider': 'UNKNOWN', 'seed': 'NOT_EXPOSED',
                                'generation_mode': 'image'}]
        self.assertEqual(validate(p), [])
        p['asset_registry'][0]['prompt'] = ''
        self.assertTrue(any('prompt' in e for e in validate(p)))
        p['asset_registry'][0].update(prompt='real prompt', seed={})
        self.assertTrue(any('seed' in e for e in validate(p)))


class MultiSheetTests(unittest.TestCase):
    def two_sheets(self, root):
        from render_storyboard_sheet import render_sheets, resolve_font
        from split_storyboard import split_storyboard
        p = image_package(root)
        root = Path(root)
        try:
            font = resolve_font()[1]
        except ValueError as exc:
            self.skipTest(str(exc))
        sheets = render_sheets(
            p, root, '04_STORYBOARDS/sheets/multi.png',
            font_path=font, panels_per_sheet=3)['sheets']
        p['asset_registry'] = [a for a in p['asset_registry'] if a['id'] != 'SHEETIMG']
        p['artifacts'] = [a for a in p['artifacts'] if a['id'] != 'SHEET']
        sheet_paths = []
        for index, sheet in enumerate(sheets, 1):
            asset_id = f'SHEETIMG{index}'
            artifact_id = f'SHEET{index}'
            relative = Path(sheet['relative_path']).as_posix()
            sheet_paths.append(relative)
            p['asset_registry'].append({
                'id': asset_id, 'kind': 'storyboard_sheet', 'version': '1',
                'status': 'available', 'path': relative, 'sha256': sheet['sha256'],
                'panel_ids': sheet['panel_ids'], 'sheet_index': sheet['sheet_index'],
                'sheet_count': sheet['sheet_count'],
                'source_asset_ids': sheet['source_asset_ids'],
                'source_sha256': sheet['source_sha256']})
            p['artifacts'].append({
                'id': artifact_id, 'type': 'storyboard_sheet', 'version': '1',
                'status': 'reviewed', 'dependencies': ['BOARD'],
                'dependency_versions': {'BOARD': '1'}, 'asset_ids': [asset_id]})
        p['preproduction']['storyboard_sheet_artifact_ids'] = ['SHEET1', 'SHEET2']
        split_root = root / '04_STORYBOARDS' / 'multi_extracts'
        split_storyboard(p, root, split_root, sheet_paths)
        for index, file in enumerate(sorted(split_root.rglob('*'))):
            if not file.is_file():
                continue
            is_manifest = file.name == 'split-manifest.json'
            p['asset_registry'].append({
                'id': 'SPLIT_MULTI' if is_manifest else f'SPLIT_MULTI_EXTRACT{index}',
                'kind': 'storyboard_split_manifest' if is_manifest else 'image',
                'version': '1', 'status': 'available',
                'path': file.relative_to(root).as_posix(),
                'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
        p['preproduction']['storyboard_split_asset_id'] = 'SPLIT_MULTI'
        return p

    def test_ordered_multi_sheet_package_is_valid(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.two_sheets(root)
            self.assertEqual(validate(p, 'preproduction', root), [])

    def test_sheet_order_gaps_and_duplicates_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            good = self.two_sheets(root)
            p = copy.deepcopy(good)
            p['preproduction']['storyboard_sheet_artifact_ids'] = ['SHEET2', 'SHEET1']
            self.assertTrue(any('story order' in e for e in validate(p, 'preproduction', root)))
            p = copy.deepcopy(good)
            next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG2')['panel_ids'] = ['P04']
            self.assertTrue(validate(p, 'preproduction', root))
            p = copy.deepcopy(good)
            next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG1').update(sheet_index=2)
            self.assertTrue(any('sheet_index' in e for e in validate(p, 'preproduction', root)))

    def test_sheet_registration_must_match_actual_produced_panel_list(self):
        with tempfile.TemporaryDirectory() as root:
            p = self.two_sheets(root)
            sheet = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG1')
            sheet['panel_ids'] = ['P01', 'P02', 'P03', 'P04', 'P05',
                                  'P01', 'P02', 'P03', 'P04', 'P05']
            self.assertTrue(any('panel order' in error
                                for error in validate(p, 'preproduction', root)))


    def test_single_sheet_uses_the_same_ordered_declaration(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            self.assertEqual(validate(p, 'preproduction', root), [])


class PackagingTests(unittest.TestCase):
    def final_package(self, root):
        from render_storyboard_sheet import render_sheets, resolve_font
        from split_storyboard import split_storyboard
        try:
            font = resolve_font()[1]
        except ValueError as exc:
            self.skipTest(str(exc))
        p = image_package(root)
        look = Path(root) / 'look.md'
        look.write_text('# Synthetic LOOK\n', encoding='utf-8')
        p['asset_registry'].append({'id': 'LOOK', 'kind': 'style_world_bible',
                                   'version': '1', 'status': 'verified', 'path': look.name,
                                   'sha256': hashlib.sha256(look.read_bytes()).hexdigest()})
        p['look_asset_id'] = 'LOOK'
        next(a for a in p['asset_registry'] if a['id'] == 'IDENTITY')['status'] = 'verified'
        next(a for a in p['artifacts'] if a['id'] == 'BOARD').update(
            finality='final', required_asset_versions={'LOOK': '1', 'IDENTITY': '1'})
        shots = {s['id']: s for s in p['shots']}
        for panel in p['storyboard']['panels']:
            panel['asset_version_refs'] = {
                aid: '1' for aid in shots[panel['shot_id']].get('asset_ids', []) + ['LOOK']}
        sheet = render_sheets(p, root, '04_STORYBOARDS/sheets/final.png', font_path=font)['sheets'][0]
        current = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
        current.update(path=Path(sheet['relative_path']).as_posix(), sha256=sheet['sha256'],
                       panel_ids=sheet['panel_ids'], source_asset_ids=sheet['source_asset_ids'],
                       source_sha256=sheet['source_sha256'])
        folder = Path(root) / '04_STORYBOARDS/final_extracts'
        split_storyboard(p, root, folder, [sheet['relative_path']])
        for i, file in enumerate(sorted(folder.rglob('*'))):
            if not file.is_file():
                continue
            manifest = file.name == 'split-manifest.json'
            aid = 'FINAL_SPLIT' if manifest else f'FINAL_EXTRACT{i}'
            p['asset_registry'].append({
                'id': aid, 'kind': 'storyboard_split_manifest' if manifest else 'image',
                'version': '1', 'status': 'available', 'path': file.relative_to(root).as_posix(),
                'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
        p['preproduction']['storyboard_split_asset_id'] = 'FINAL_SPLIT'
        return p

    def repeated_scene_final_package(self, root):
        from render_storyboard_sheet import render_sheets, resolve_font
        from split_storyboard import split_storyboard
        p = self.final_package(root)
        shots = {row['id']: row for row in p['shots']}
        second = shots['SH02']
        second.update(end_s=3, source_duration_s=1, beat_ids=['B02'])
        third = copy.deepcopy(second)
        third.update(id='SH03', scene_id='S01', start_s=3, end_s=4,
                     source_duration_s=1, beat_ids=['B03'], speech=[])
        p['shots'].append(third)
        panels = p['storyboard']['panels']
        panels[3].update(frame_time_s=71 / 24, role='end')
        panels[4].update(shot_id='SH03', frame_time_s=3, role='start')
        final_panel = copy.deepcopy(panels[4])
        final_panel.update(id='P06', frame_time_s=95 / 24, role='end')
        panels.append(final_panel)

        font = resolve_font()[1]
        sheet = render_sheets(
            p, root, '04_STORYBOARDS/sheets/repeated.png', font_path=font)['sheets'][0]
        sheet_asset = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
        sheet_asset.update(
            path=Path(sheet['relative_path']).as_posix(), sha256=sheet['sha256'],
            panel_ids=sheet['panel_ids'], sheet_index=sheet['sheet_index'],
            sheet_count=sheet['sheet_count'], source_asset_ids=sheet['source_asset_ids'],
            source_sha256=sheet['source_sha256'])
        p['asset_registry'] = [
            asset for asset in p['asset_registry']
            if asset['id'] != 'FINAL_SPLIT' and not asset['id'].startswith('FINAL_EXTRACT')]
        split_root = Path(root) / '04_STORYBOARDS' / 'repeated_extracts'
        split_storyboard(p, root, split_root, [sheet['relative_path']])
        for index, file in enumerate(sorted(split_root.rglob('*'))):
            if not file.is_file():
                continue
            is_manifest = file.name == 'split-manifest.json'
            p['asset_registry'].append({
                'id': 'REPEAT_SPLIT' if is_manifest else f'REPEAT_EXTRACT{index}',
                'kind': 'storyboard_split_manifest' if is_manifest else 'image',
                'version': '1', 'status': 'available',
                'path': file.relative_to(root).as_posix(),
                'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
        p['preproduction']['storyboard_split_asset_id'] = 'REPEAT_SPLIT'
        return p

    def test_final_package_accepts_repeated_scene_bands_in_chronological_order(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.repeated_scene_final_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'REPEAT_SPLIT')
            manifest = json.loads((Path(root) / split['path']).read_text(encoding='utf-8'))
            scene = next(row for row in manifest['scenes'] if row['scene_id'] == 'S01')
            sheet_path = '04_STORYBOARDS/sheets/repeated.png'
            self.assertEqual(scene['band_sources'], [sheet_path, sheet_path])
            result = build_package(p, Path(root), Path(out), require_final=True)
            self.assertTrue(Path(result['package']).is_dir())

    def test_final_package_requires_registered_current_scene_panel_outputs(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.final_package(root)
            result = build_package(p, Path(root), Path(out), require_final=True)
            exported = Path(result['package'])
            snapshot = json.loads((exported / 'project.json').read_text(encoding='utf-8'))
            self.assertEqual(validate(snapshot, 'preproduction', exported), [])
            for mutation, label in (
                (lambda q: q['preproduction'].pop('storyboard_split_asset_id'),
                 'split manifest'),
                (lambda q: q['asset_registry'].__setitem__(slice(None), [
                    a for a in q['asset_registry']
                    if not (a['id'].startswith('EXTRACT')
                            or a['id'].startswith('FINAL_EXTRACT'))]),
                 'missing registered outputs'),
            ):
                with self.subTest(condition=label):
                    candidate = copy.deepcopy(p)
                    mutation(candidate)
                    with self.assertRaises(ValueError):
                        build_package(candidate, Path(root), Path(out),
                                      require_final=True)

    def test_final_package_rejects_panel_alias_even_with_current_hashes(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.final_package(root)
            split_asset = next(a for a in p['asset_registry'] if a['id'] == 'FINAL_SPLIT')
            split_path = Path(root) / split_asset['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            manifest['entries'][1]['file'] = manifest['entries'][0]['file']
            manifest['entries'][1]['sha256'] = manifest['entries'][0]['sha256']
            split_path.write_text(json.dumps(manifest), encoding='utf-8')
            split_asset['sha256'] = hashlib.sha256(split_path.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, 'crop|panel|source'):
                build_package(p, Path(root), Path(out), require_final=True)
            self.assertFalse(list(Path(out).glob('*.zip')))

    def test_final_package_rejects_wrong_rgb_crop_with_current_p02_path_and_hash(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.final_package(root)
            split_asset = next(a for a in p['asset_registry'] if a['id'] == 'FINAL_SPLIT')
            split_path = Path(root) / split_asset['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            entry = next(row for row in manifest['entries'] if row['panel_id'] == 'P02')
            crop_path = split_path.parent / entry['file']
            with Image.open(crop_path) as image:
                size = image.size
            Image.new('RGB', size, (1, 2, 3)).save(crop_path)
            digest = hashlib.sha256(crop_path.read_bytes()).hexdigest()
            entry['sha256'] = digest
            crop_relative = crop_path.relative_to(root).as_posix()
            crop_asset = next(a for a in p['asset_registry'] if a['path'] == crop_relative)
            crop_asset['sha256'] = digest
            split_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8')
            split_asset['sha256'] = hashlib.sha256(split_path.read_bytes()).hexdigest()
            archive = Path(out) / 'wrong-crop.zip'
            with self.assertRaisesRegex(
                    ValueError, 'split panel pixels do not match source sheet: P02'):
                build_package(p, Path(root), Path(out), zip_path=archive, require_final=True)
            self.assertFalse(archive.exists())

    def test_final_package_rejects_scene_pixels_not_assembled_from_sheet_bands(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.final_package(root)
            split_asset = next(a for a in p['asset_registry'] if a['id'] == 'FINAL_SPLIT')
            split_path = Path(root) / split_asset['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            scene = next(row for row in manifest['scenes'] if row['scene_id'] == 'S01')
            scene_path = split_path.parent / scene['file']
            with Image.open(scene_path) as image:
                size = image.size
            Image.new('RGB', size, (9, 8, 7)).save(scene_path)
            digest = hashlib.sha256(scene_path.read_bytes()).hexdigest()
            scene['sha256'] = digest
            scene_relative = scene_path.relative_to(root).as_posix()
            scene_asset = next(a for a in p['asset_registry'] if a['path'] == scene_relative)
            scene_asset['sha256'] = digest
            split_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8')
            split_asset['sha256'] = hashlib.sha256(split_path.read_bytes()).hexdigest()
            archive = Path(out) / 'wrong-scene.zip'
            with self.assertRaisesRegex(
                    ValueError, 'split scene pixels do not match source bands: S01'):
                build_package(p, Path(root), Path(out), zip_path=archive, require_final=True)
            self.assertFalse(archive.exists())
    def test_directory_package_reopens_as_a_portable_ledger(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = image_package(root)
            package = build_package(p, Path(root), Path(out))
            root_dir = Path(package['package'])
            snapshot = json.loads((root_dir / 'project.json').read_text(encoding='utf-8'))
            self.assertEqual(validate(snapshot, 'preproduction', root_dir), [])
            originals = {a['id']: a for a in p['asset_registry']}
            split = next(a for a in snapshot['asset_registry'] if a['id'] == 'SPLIT')
            directory_split_sha = hashlib.sha256(
                (root_dir / split['path']).read_bytes()).hexdigest()
            self.assertEqual(split['sha256'], directory_split_sha)
            registry = csv.DictReader(io.StringIO(
                (root_dir / '00_MANIFEST' / 'asset_registry.csv').read_text(encoding='utf-8')))
            split_registry = next(row for row in registry if row['id'] == 'SPLIT')
            self.assertEqual(split_registry['sha256'], directory_split_sha)
            for asset in snapshot['asset_registry']:
                packaged = (root_dir / asset['path']).read_bytes()
                if asset['id'] == 'SPLIT':
                    self.assertEqual(hashlib.sha256(packaged).hexdigest(), asset['sha256'])
                    continue
                self.assertEqual(packaged,
                                 (Path(root) / originals[asset['id']]['path']).read_bytes())
            rows = csv.DictReader(io.StringIO(
                (root_dir / '00_MANIFEST' / 'package_manifest.csv').read_text(encoding='utf-8')))
            self.assertEqual({r['packaged_path'] for r in rows},
                             {f.relative_to(root_dir).as_posix()
                              for f in root_dir.rglob('*') if f.is_file()})
            before = (root_dir / 'project.json').read_bytes()
            with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                build_package(p, Path(root), Path(out))
            self.assertEqual((root_dir / 'project.json').read_bytes(), before)

    def test_zip_roundtrip_preserves_registered_bytes_and_history(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = image_package(root)
            (Path(root) / '.history').mkdir()
            (Path(root) / '.history' / '2026-10-06.md').write_text('# event\n', encoding='utf-8')
            target = Path(out) / 'pkg.zip'
            package = build_package(p, Path(root), target, zip_path=target)
            with zipfile.ZipFile(target) as archive:
                names = archive.namelist()
                ledger_name = next(n for n in names if n.endswith('/project.json'))
                prefix = ledger_name.removesuffix('project.json')
                snapshot = json.loads(archive.read(ledger_name))
                originals = {a['id']: a for a in p['asset_registry']}
                for asset in snapshot['asset_registry']:
                    packaged = archive.read(prefix + asset['path'])
                    if asset['id'] == 'SPLIT':
                        self.assertEqual(hashlib.sha256(packaged).hexdigest(), asset['sha256'])
                        continue
                    self.assertEqual(
                        packaged,
                        (Path(root) / originals[asset['id']]['path']).read_bytes())
                self.assertEqual(archive.read(prefix + '.history/2026-10-06.md'),
                                 (Path(root) / '.history/2026-10-06.md').read_bytes())
                with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
                    build_package(p, Path(root), target, zip_path=target)

    def test_equal_basenames_keep_distinct_registered_assets(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = image_package(root)
            for asset_id, folder in [('IM01', 'first'), ('IM02', 'second')]:
                asset = next(a for a in p['asset_registry'] if a['id'] == asset_id)
                destination = Path(root) / folder / 'same.png'
                destination.parent.mkdir()
                destination.write_bytes((Path(root) / asset['path']).read_bytes())
                asset['path'] = f'{folder}/same.png'
            result = build_package(p, Path(root), Path(out))
            exported = Path(result['package'])
            assets = {a['id']: a for a in json.loads(
                (exported / 'project.json').read_text(encoding='utf-8'))['asset_registry']}
            self.assertNotEqual(assets['IM01']['path'], assets['IM02']['path'])
            self.assertNotEqual((exported / assets['IM01']['path']).read_bytes(),
                                (exported / assets['IM02']['path']).read_bytes())

    def test_require_final_refuses_open_gate(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = image_package(root)
            p['artifacts'].append({
                'id': 'FIN', 'type': 'storyboard', 'version': '1', 'status': 'reviewed',
                'finality': 'final', 'required_asset_versions': {'MISSING': '1'},
                'dependencies': [], 'dependency_versions': {}})
            with self.assertRaises(ValueError):
                build_package(p, Path(root), Path(out), require_final=True)

    def test_registered_report_collision_preserves_source_and_publishes_nothing(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = self.final_package(root)
            source = Path(root) / '00_MANIFEST' / 'qa_report.md'
            source.parent.mkdir(parents=True)
            payload = b'registered user file\n'
            source.write_bytes(payload)
            p['asset_registry'].append({
                'id': 'QA_FILE', 'kind': 'document', 'version': '1',
                'status': 'available', 'path': '00_MANIFEST/qa_report.md',
                'sha256': hashlib.sha256(payload).hexdigest()})
            archive = Path(out) / 'blocked.zip'
            with self.assertRaisesRegex(ValueError, 'collides'):
                build_package(p, Path(root), Path(out), zip_path=archive, require_final=True)
            self.assertEqual(source.read_bytes(), payload)
            self.assertFalse(archive.exists())

    def test_casefolded_report_path_collision_preserves_source_and_publishes_nothing(self):
        for zipped in (False, True):
            with self.subTest(zipped=zipped), tempfile.TemporaryDirectory() as root, \
                    tempfile.TemporaryDirectory() as out:
                p = self.final_package(root)
                source = Path(root) / '00_MANIFEST' / 'QA_REPORT.md'
                source.parent.mkdir(parents=True)
                payload = b'registered mixed-case user file\n'
                source.write_bytes(payload)
                p['asset_registry'].append({
                    'id': 'QA_CASE_ALIAS', 'kind': 'document', 'version': '1',
                    'status': 'available', 'path': '00_MANIFEST/QA_REPORT.md',
                    'sha256': hashlib.sha256(payload).hexdigest()})
                archive = Path(out) / 'blocked.zip'
                with self.assertRaisesRegex(ValueError, 'collides'):
                    build_package(p, Path(root), Path(out),
                                  zip_path=archive if zipped else None,
                                  require_final=True)
                self.assertEqual(source.read_bytes(), payload)
                self.assertFalse(archive.exists())
                self.assertFalse(list(Path(out).iterdir()))

    def test_history_symlink_export_rejected_without_external_read(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out:
            p = image_package(root)
            outside = Path(out) / 'external'
            outside.mkdir()
            sentinel = outside / 'sentinel.txt'
            sentinel.write_text('untouched', encoding='utf-8')
            history = Path(root) / '.history'
            try:
                os.symlink(outside, history, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f'directory symlink unavailable: {exc}')
            archive = Path(out) / 'blocked.zip'
            with self.assertRaisesRegex(ValueError, 'history directory'):
                build_package(p, Path(root), Path(out), zip_path=archive)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'untouched')
            self.assertFalse(archive.exists())

    def test_source_mutated_during_zip_or_directory_copy_prevents_publication(self):
        for as_zip in (True, False):
            with self.subTest(as_zip=as_zip), tempfile.TemporaryDirectory() as root, \
                    tempfile.TemporaryDirectory() as out:
                p = image_package(root)
                source = Path(root) / 'race.bin'
                original = b'original bytes'
                source.write_bytes(original)
                p['asset_registry'].append({
                    'id': 'RACE', 'kind': 'document', 'version': '1',
                    'status': 'available', 'path': 'race.bin',
                    'sha256': hashlib.sha256(original).hexdigest()})
                target = Path(out) / 'race.zip'
                path_open = Path.open
                calls = 0

                def mutating_open(path, mode='r', *args, **kwargs):
                    nonlocal calls
                    if path == source and mode == 'rb':
                        calls += 1
                        if calls == 2:
                            source.write_bytes(b'changed during export')
                    return path_open(path, mode, *args, **kwargs)

                with patch.object(Path, 'open', mutating_open):
                    with self.assertRaisesRegex(ValueError, 'changed during package copy'):
                        if as_zip:
                            build_package(p, Path(root), target, zip_path=target)
                        else:
                            build_package(p, Path(root), Path(out))
                if as_zip:
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual(list(Path(out).iterdir()), [])

    def test_relocated_final_zip_extracts_and_repackages_as_current(self):
        with tempfile.TemporaryDirectory() as root, tempfile.TemporaryDirectory() as out, \
                tempfile.TemporaryDirectory() as unpack, tempfile.TemporaryDirectory() as second:
            p = self.final_package(root)
            split_asset = next(a for a in p['asset_registry'] if a['id'] == 'FINAL_SPLIT')
            original_split_path = split_asset['path']
            path_map = {}
            for asset in p['asset_registry']:
                raw = asset.get('path')
                if asset.get('status') not in ('available', 'verified') or not raw:
                    continue
                source = Path(root) / raw
                destination = Path(root) / 'unusual root' / f"{asset['id']}{source.suffix}"
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.rename(destination)
                relocated = destination.relative_to(root).as_posix()
                path_map[raw] = relocated
                asset['path'] = relocated
            split_path = Path(root) / split_asset['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            old_parent = Path(original_split_path).parent
            new_parent = Path(split_asset['path']).parent
            for item in manifest['entries'] + manifest['scenes']:
                old_file = (old_parent / item['file']).as_posix()
                item['file'] = Path(os.path.relpath(path_map[old_file],
                                                     new_parent)).as_posix()
            for entry in manifest['entries']:
                entry['sheet_path'] = path_map[entry['sheet_path']]
            for sheet in manifest['sheets']:
                sheet['path'] = path_map[sheet['path']]
            for scene in manifest['scenes']:
                scene['band_sources'] = [path_map[path]
                                         for path in scene['band_sources']]
            split_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                                  encoding='utf-8')
            split_asset['sha256'] = hashlib.sha256(split_path.read_bytes()).hexdigest()
            original = copy.deepcopy(p)
            archive_path = Path(out) / 'relocated-final.zip'
            build_package(p, Path(root), Path(out), zip_path=archive_path, require_final=True)
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(unpack)
                ledger_name = next(name for name in archive.namelist()
                                   if name.endswith('/project.json'))
            unpacked = Path(unpack) / ledger_name.removesuffix('/project.json')
            snapshot = json.loads((unpacked / 'project.json').read_text(encoding='utf-8'))
            self.assertEqual(validate(snapshot, 'preproduction', unpacked), [])
            split_asset = next(a for a in snapshot['asset_registry'] if a['id'] == 'FINAL_SPLIT')
            split_path = unpacked / split_asset['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            for item in manifest['entries'] + manifest['scenes']:
                derived = split_path.parent / item['file']
                self.assertTrue(derived.is_file(), derived)
                self.assertEqual(hashlib.sha256(derived.read_bytes()).hexdigest(), item['sha256'])
            for sheet in manifest['sheets']:
                self.assertTrue((unpacked / sheet['path']).is_file(), sheet['path'])
            for scene in manifest['scenes']:
                for source in scene['band_sources']:
                    self.assertTrue((unpacked / source).is_file(), source)
            rebuilt = build_package(snapshot, unpacked, Path(second), require_final=True)
            rebuilt_root = Path(rebuilt['package'])
            self.assertEqual(validate(json.loads((rebuilt_root / 'project.json').read_text()),
                                      'preproduction', rebuilt_root), [])
            self.assertEqual(p, original)


if __name__ == '__main__':
    unittest.main()
