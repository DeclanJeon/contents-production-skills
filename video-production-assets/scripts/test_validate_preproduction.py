"""Consumer-visible completeness gates, not artwork quality assertions."""
import unittest
import json
import copy
import hashlib
import tempfile
import subprocess
import sys
from pathlib import Path
from PIL import Image
from test_validate_storyboard import board
from project_index import build_index
from update_project import prepare_update
from test_validate_project import project
from validate_project import validate

def run_preproduction_cli(project_data, base_dir):
    base = Path(base_dir)
    project_path = base / 'project.json'
    project_path.write_text(json.dumps(project_data), encoding='utf-8')
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name('validate_project.py')),
         str(project_path), '--profile', 'preproduction', '--base-dir', str(base)],
        cwd=Path(__file__).parent, capture_output=True, text=True, encoding='utf-8',
        check=False)
    return result, json.loads(result.stdout)


def image_package(root):
    """Synthetic files exercise contracts, not rendered-character quality."""
    root = Path(root)
    p = board()
    p['scenes'].append({'id': 'S02', 'purpose': 'second synthetic scene'})
    p['shots'][1]['scene_id'] = 'S02'
    def asset(aid, path, kind='document', **extra):
        row = {'id': aid, 'kind': kind, 'version': '1', 'status': 'available',
               'path': path, 'sha256': hashlib.sha256((root / path).read_bytes()).hexdigest(), **extra}
        p['asset_registry'].append(row)
        return row
    def doc(aid, path):
        (root / path).write_text('# Synthetic contract fixture\n', encoding='utf-8')
        asset(aid, path)
    def artifact(aid, kind, deps, assets):
        p['artifacts'].append({'id': aid, 'type': kind, 'version': '1', 'status': 'reviewed',
                               'dependencies': deps, 'dependency_versions': {d: '1' for d in deps},
                               'asset_ids': assets})
    doc('SYNMD', 'synopsis.md')
    next(a for a in p['artifacts'] if a['id'] == 'SYN')['asset_ids'] = ['SYNMD']
    for i, row in enumerate(p['asset_registry'][:5]):
        path = f'panel{i}.png'
        Image.new('RGB', (40, 24), (i * 40, 20, 80)).save(root / path)
        row.update(status='available', path=path, sha256=hashlib.sha256((root / path).read_bytes()).hexdigest())
    doc('CHARMD', 'character.md')
    artifact('CHAR', 'character_sheet', ['SYN'], ['CHARMD'])
    Image.new('RGB', (64, 64), 'gray').save(root / 'identity.png')
    asset('IDENTITY', 'identity.png', 'character_identity_sheet', entity_type='character',
          entity_id='CH01', source_asset_ids=['CHARMD'])
    p['characters'][0].update(persona={'role': 'protagonist', 'personality': 'cautious',
                                      'observable_behavior': 'checks before speaking', 'speech': 'measured'},
                               ssot_artifact_id='CHAR', identity_sheet_asset_id='IDENTITY')
    p['shots'][0]['asset_ids'] = ['IDENTITY']
    doc('BOARDMD', 'storyboard.md')
    artifact('BOARD', 'storyboard', ['SYN', 'CHAR'], ['BOARDMD'])
    panels = p['storyboard']['panels']
    shots = {row['id']: row for row in p['shots']}
    source_rows = {row['id']: row for row in p['asset_registry']}
    boxes = [[10, 20, 50, 44], [55, 20, 95, 44],
             [110, 20, 150, 44], [160, 20, 200, 44], [210, 20, 250, 44]]
    sheet = Image.new('RGB', (270, 70), 'white')
    panel_bounds, traceability, sources, source_hashes = [], [], [], {}
    for panel, bounds in zip(panels, boxes):
        source_id = panel.get('source_sheet_asset_id') or panel['image_asset_id']
        source = source_rows[source_id]
        with Image.open(root / source['path']) as image:
            sheet.paste(image, (bounds[0], bounds[1]))
        source_hashes[source_id] = source['sha256']
        sources.append(source_id)
        scene_id = shots[panel['shot_id']]['scene_id']
        panel_bounds.append({'panel_id': panel['id'], 'bounds': bounds})
        traceability.append({
            'panel_id': panel['id'], 'shot_id': panel['shot_id'], 'scene_id': scene_id,
            'source_asset_id': source_id, 'source_asset_version': source['version'],
            'source_sha256': source['sha256'],
            'asset_version_refs': panel.get('asset_version_refs', {})})
    from PIL import PngImagePlugin
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text('storyboard_sheet.panel_ids', ','.join(row['id'] for row in panels))
    metadata.add_text('storyboard_sheet.panel_bounds', json.dumps(panel_bounds))
    metadata.add_text('storyboard_sheet.scene_bounds', json.dumps([
        {'scene_id': 'S01', 'bounds': [5, 10, 100, 55]},
        {'scene_id': 'S02', 'bounds': [105, 10, 260, 55]}]))
    metadata.add_text('storyboard_sheet.panel_traceability', json.dumps(traceability))
    metadata.add_text('storyboard_sheet.source_sha256', json.dumps(source_hashes))
    metadata.add_text('storyboard_sheet.sheet_index', '1')
    metadata.add_text('storyboard_sheet.sheet_count', '1')
    sheet.save(root / 'sheet.png', pnginfo=metadata)
    asset('SHEETIMG', 'sheet.png', 'storyboard_sheet', panel_ids=[x['id'] for x in panels],
          source_asset_ids=sources, source_sha256=source_hashes, sheet_index=1, sheet_count=1)
    artifact('SHEET', 'storyboard_sheet', ['BOARD'], ['SHEETIMG'])
    p['preproduction'] = {'mode': 'image_backed', 'synopsis_artifact_id': 'SYN',
                          'storyboard_artifact_id': 'BOARD', 'storyboard_sheet_artifact_ids': ['SHEET']}
    from split_storyboard import split_storyboard
    output = root / '04_STORYBOARDS' / 'extracts'
    split_storyboard(p, root, output, ['sheet.png'])
    for index, path in enumerate(sorted(output.rglob('*'))):
        if not path.is_file():
            continue
        is_manifest = path.name == 'split-manifest.json'
        aid = 'SPLIT' if is_manifest else f'EXTRACT{index}'
        relative = path.relative_to(root).as_posix()
        asset(aid, relative, 'storyboard_split_manifest' if is_manifest else 'image')
    p['preproduction']['storyboard_split_asset_id'] = 'SPLIT'
    return p


class PreproductionGateTests(unittest.TestCase):
    def test_reviewed_package_without_deliverables_is_not_ready(self):
        p = project()
        p['artifacts'].append({'id': 'REVIEW', 'type': 'preproduction_review',
                               'version': '1', 'status': 'reviewed',
                               'dependencies': [], 'dependency_versions': {}})
        errors = validate(p)
        self.assertTrue(any('preproduction' in e for e in errors), errors)

    def test_complete_package_and_review_are_structurally_valid(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            self.assertEqual(validate(p, 'preproduction', root), [])
            p['artifacts'].append({'id': 'REVIEW', 'type': 'preproduction_review', 'version': '1',
                                   'status': 'reviewed', 'dependencies': ['SHEET'],
                                   'dependency_versions': {'SHEET': '1'}})

            self.assertEqual(validate(p, base_dir=root), [])

    def test_missing_wrong_stale_or_incomplete_deliverables_block_review(self):
        cases = [
            ('persona', lambda p: p['characters'][0].pop('persona')),
            ('character_sheet', lambda p: p['characters'][0].update(ssot_artifact_id='VO01')),
            ('same character', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'IDENTITY').update(entity_id='CH02')),
            ('SSOT source', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'IDENTITY').update(source_asset_ids=[])),
            ('SSOT source', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'IDENTITY').update(source_asset_ids=['SYNMD'])),
            ('identity reference', lambda p: p['shots'][0].update(asset_ids=[])),
            ('Markdown', lambda p: next(a for a in p['artifacts'] if a['id'] == 'CHAR').update(asset_ids=['IDENTITY'])),
            ('panel order registration', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')['panel_ids'].reverse()),
            ('source mapping', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG').update(source_asset_ids=['IM01'])),
            ('registered source hash mutation', lambda p: next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG').update(source_sha256={})),
            ('stale', lambda p: next(a for a in p['artifacts'] if a['id'] == 'CHAR').update(status='stale')),
            ('dependency', lambda p: next(a for a in p['artifacts'] if a['id'] == 'BOARD').update(dependencies=['SYN'], dependency_versions={'SYN':'1'})),
            ('synopsis', lambda p: p['preproduction'].update(synopsis_artifact_id='VO01')),
            ('combined storyboard sheet', lambda p: p['preproduction'].pop('storyboard_sheet_artifact_ids')),
            ('blocker', lambda p: p['issues'].append({'id':'Q01','severity':'blocker','status':'open'})),
        ]
        with tempfile.TemporaryDirectory() as root:
            original = image_package(root)
            valid_result, valid_data = run_preproduction_cli(original, root)
            self.assertEqual(valid_result.returncode, 0, valid_result.stderr)
            self.assertTrue(valid_data['valid'], valid_data)
            for label, change in cases:
                with self.subTest(case=label):
                    p = copy.deepcopy(original)
                    change(p)
                    result, data = run_preproduction_cli(p, root)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertFalse(data['valid'], data)

    def test_actual_files_not_metadata_or_empty_documents_satisfy_package(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            (Path(root) / 'identity.png').write_bytes(b'not an image')
            self.assertTrue(any('cannot read actual file' in e for e in validate(p, 'preproduction', root)))
            (Path(root) / 'character.md').write_text('', encoding='utf-8')
            self.assertTrue(any('nonempty Markdown' in e for e in validate(p, 'preproduction', root)))

    def test_text_and_characterless_packages_keep_narrow_image_scope(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            p['preproduction']['mode'] = 'text'
            p['preproduction'].pop('storyboard_sheet_artifact_ids')
            p['characters'][0].pop('identity_sheet_asset_id')
            p['shots'][0]['asset_ids'] = []
            self.assertEqual(validate(p, 'preproduction', root), [])
            p['characters'] = []
            p['shots'][0]['character_ids'] = []
            p['asset_registry'] = [a for a in p['asset_registry'] if a['id'] != 'IDENTITY']
            p['shots'][0]['speech'][0].update(kind='narration',character_id=None,lip_sync='not_applicable')
            for pn in p['storyboard']['panels']:
                pn['visible_character_ids'] = []
            self.assertEqual(validate(p, 'preproduction', root), [])
            self.assertEqual(validate(project()), [])

    def test_image_backed_review_cannot_switch_to_text_to_skip_sheet(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            p['preproduction']['mode'] = 'text'
            p['artifacts'].append({'id': 'REVIEW', 'type': 'preproduction_review', 'version':'1',
                                   'status':'reviewed','dependencies':['SHEET'],'dependency_versions':{'SHEET':'1'}})
            self.assertTrue(any('cannot use text mode' in e for e in validate(p, base_dir=root)))

    def test_image_readiness_requires_split_pointer_and_registered_scene_panel_outputs(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            p['preproduction'].pop('storyboard_split_asset_id')
            self.assertTrue(any('storyboard split manifest' in error
                                for error in validate(p, 'preproduction', root)))
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            manifest = json.loads((Path(root) / split['path']).read_text(encoding='utf-8'))
            scene_path = manifest['scenes'][0]['file']
            p['asset_registry'] = [a for a in p['asset_registry'] if a.get('path') !=
                                   f"04_STORYBOARDS/extracts/{scene_path}"]
            self.assertTrue(any('split scene' in error and 'registration/hash' in error
                                for error in validate(p, 'preproduction', root)))
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            manifest = json.loads((Path(root) / split['path']).read_text(encoding='utf-8'))
            panel_path = Path(root) / '04_STORYBOARDS/extracts' / manifest['entries'][0]['file']
            panel_path.unlink()
            self.assertTrue(any('file missing' in error
                                for error in validate(p, 'preproduction', root)))

    def test_stale_storyboard_sheet_hash_blocks_readiness(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            sheet = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
            Image.new('RGB', (271, 70), 'black').save(Path(root) / sheet['path'])
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('hash' in error.lower() for error in errors), errors)


    def test_split_entry_sheet_path_must_match_current_registered_sheet(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            manifest['entries'][0]['sheet_path'] = 'panel0.png'
            contents = json.dumps(manifest, indent=2).encode('utf-8')
            split_path.write_bytes(contents)
            split['sha256'] = hashlib.sha256(contents).hexdigest()
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('sheet_path' in error and 'current' in error for error in errors), errors)

    def test_split_manifest_bytes_must_match_registered_sha(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            split_path.write_bytes(split_path.read_bytes() + b'\n')
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('split manifest' in error and 'SHA-256' in error
                                for error in errors), errors)
    def test_replaced_registered_sheet_invalidates_existing_split(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            sheet = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
            replacement = Path(root) / 'replacement-sheet.png'
            Image.new('RGB', (270, 70), 'navy').save(replacement)
            sheet.update(path='replacement-sheet.png',
                         sha256=hashlib.sha256(replacement.read_bytes()).hexdigest())
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('current ordered storyboard sheets' in error for error in errors), errors)

    def test_split_panel_outputs_cannot_alias_another_panel(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            manifest['entries'][1]['file'] = manifest['entries'][0]['file']
            manifest['entries'][1]['sha256'] = manifest['entries'][0]['sha256']
            contents = json.dumps(manifest, indent=2).encode('utf-8')
            split_path.write_bytes(contents)
            split['sha256'] = hashlib.sha256(contents).hexdigest()
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('distinct' in error and 'panel' in error for error in errors), errors)

    def test_split_panel_pixels_must_match_current_sheet_crop(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            first = split_path.parent / manifest['entries'][0]['file']
            second = split_path.parent / manifest['entries'][1]['file']
            second.write_bytes(first.read_bytes())
            digest = hashlib.sha256(second.read_bytes()).hexdigest()
            manifest['entries'][1]['sha256'] = digest
            second_asset = next(a for a in p['asset_registry']
                                if a.get('path') == second.relative_to(root).as_posix())
            second_asset['sha256'] = digest
            contents = json.dumps(manifest, indent=2).encode('utf-8')
            split_path.write_bytes(contents)
            split['sha256'] = hashlib.sha256(contents).hexdigest()
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('pixels do not match source sheet' in error for error in errors), errors)

    def test_transparent_panel_output_does_not_match_opaque_sheet_crop(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            output = split_path.parent / manifest['entries'][1]['file']
            with Image.open(output) as image:
                transparent = image.convert('RGBA')
            transparent.putalpha(0)
            transparent.save(output)
            transparent.close()
            digest = hashlib.sha256(output.read_bytes()).hexdigest()
            manifest['entries'][1]['sha256'] = digest
            output_asset = next(a for a in p['asset_registry']
                                if a.get('path') == output.relative_to(root).as_posix())
            output_asset['sha256'] = digest
            contents = json.dumps(manifest, indent=2).encode('utf-8')
            split_path.write_bytes(contents)
            split['sha256'] = hashlib.sha256(contents).hexdigest()
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('pixels do not match source sheet' in error for error in errors), errors)

    def test_transparent_scene_output_does_not_match_opaque_sheet_bands(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
            split_path = Path(root) / split['path']
            manifest = json.loads(split_path.read_text(encoding='utf-8'))
            output = split_path.parent / manifest['scenes'][0]['file']
            with Image.open(output) as image:
                transparent = image.convert('RGBA')
            transparent.putalpha(0)
            transparent.save(output)
            transparent.close()
            digest = hashlib.sha256(output.read_bytes()).hexdigest()
            manifest['scenes'][0]['sha256'] = digest
            output_asset = next(a for a in p['asset_registry']
                                if a.get('path') == output.relative_to(root).as_posix())
            output_asset['sha256'] = digest
            contents = json.dumps(manifest, indent=2).encode('utf-8')
            split_path.write_bytes(contents)
            split['sha256'] = hashlib.sha256(contents).hexdigest()
            errors = validate(p, 'preproduction', root)
            self.assertTrue(any('scene pixels do not match source bands' in error
                                for error in errors), errors)

    def test_overlapping_produced_sheet_bounds_are_rejected(self):
        from PIL import PngImagePlugin
        for key, expected in (('panel_bounds', 'panel bounds overlap'),
                              ('scene_bounds', 'scene bounds overlap')):
            with self.subTest(metadata=key), tempfile.TemporaryDirectory() as root:
                p = image_package(root)
                sheet = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
                sheet_path = Path(root) / sheet['path']
                with Image.open(sheet_path) as image:
                    metadata = dict(image.info)
                    rows = json.loads(metadata[f'storyboard_sheet.{key}'])
                    rows[1]['bounds'] = rows[0]['bounds']
                    metadata[f'storyboard_sheet.{key}'] = json.dumps(rows)
                    pnginfo = PngImagePlugin.PngInfo()
                    for name, value in image.info.items():
                        if name != f'storyboard_sheet.{key}' and isinstance(value, str):
                            pnginfo.add_text(name, value)
                    pnginfo.add_text(f'storyboard_sheet.{key}', metadata[f'storyboard_sheet.{key}'])
                    changed = image.copy()
                changed.save(sheet_path, pnginfo=pnginfo)
                changed.close()
                sheet['sha256'] = hashlib.sha256(sheet_path.read_bytes()).hexdigest()
                split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
                split_path = Path(root) / split['path']
                manifest = json.loads(split_path.read_text(encoding='utf-8'))
                manifest['sheets'][0]['sha256'] = sheet['sha256']
                contents = json.dumps(manifest, indent=2).encode('utf-8')
                split_path.write_bytes(contents)
                split['sha256'] = hashlib.sha256(contents).hexdigest()
                errors = validate(p, 'preproduction', root)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_reviewed_and_approved_review_cannot_bypass_missing_split_output(self):
        for review_status in ('reviewed', 'approved'):
            with self.subTest(status=review_status), tempfile.TemporaryDirectory() as root:
                p = image_package(root)
                split = next(a for a in p['asset_registry'] if a['id'] == 'SPLIT')
                manifest = json.loads((Path(root) / split['path']).read_text(encoding='utf-8'))
                scene_path = manifest['scenes'][0]['file']
                scene_asset_path = f"04_STORYBOARDS/extracts/{scene_path}"
                p['asset_registry'] = [a for a in p['asset_registry']
                                       if a.get('path') != scene_asset_path]
                review = {'id': 'REVIEW', 'type': 'preproduction_review', 'version': '1',
                          'status': review_status, 'dependencies': ['SHEET'],
                          'dependency_versions': {'SHEET': '1'}}
                p['artifacts'].append(review)
                if review_status == 'approved':
                    approval = {'by': 'fixture', 'at': '2026-10-06',
                                'evidence': 'synthetic review fixture'}
                    review['approval'] = approval
                    p['artifacts'].append({
                        'id': 'EXEC', 'type': 'video_execution_plan', 'version': '1',
                        'status': 'approved', 'approval': approval,
                        'dependencies': ['REVIEW'], 'dependency_versions': {'REVIEW': '1'}})
                errors = validate(p, base_dir=root)
                self.assertTrue(any('split scene' in error and 'registration/hash' in error
                                    for error in errors), errors)

    def test_focused_shot_handoff_includes_persona_ssot_and_actual_identity_source(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            packet = build_index(p, ['SH01'])
            self.assertEqual(packet['characters'][0]['persona'], p['characters'][0]['persona'])
            self.assertEqual(packet['input_versions']['CHAR'], '1')
            self.assertIn('IDENTITY', {a['id'] for a in packet['asset_registry']})

    def test_package_header_updates_need_content_owner_and_invalidate_dependents(self):
        p = project()
        p['artifacts'].append({'id':'DEPENDENT','type':'review','version':'1','status':'reviewed',
                               'dependencies':['A01'],'dependency_versions':{'A01':'1'}})
        change = {'project_id':p['project_id'],'base_version':'1','version':'2',
                  'preproduction':{'mode':'text','synopsis_artifact_id':'A01'}, 'changes':{}}
        with self.assertRaisesRegex(ValueError, 'owner_artifact_ids'):
            prepare_update(p, change)
        change.update(owner_artifact_ids=['A01'],changes={'artifacts':[{'id':'A01','version':'2'}]})
        updated, _, stale = prepare_update(p, change)
        self.assertEqual(updated['preproduction'], change['preproduction'])
        self.assertEqual(stale, ['DEPENDENT'])


if __name__ == '__main__':
    unittest.main()
