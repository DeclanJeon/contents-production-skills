"""Actual image and safe-output behavior; synthetic pixels are not artistic QA."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from render_storyboard_sheet import render_sheet, resolve_font
from test_validate_preproduction import image_package
from validate_project import validate


class StoryboardRenderTests(unittest.TestCase):
    def font(self):
        try:
            return resolve_font()[1]
        except ValueError as exc:
            self.skipTest(str(exc))

    def test_all_panel_pixels_present_and_output_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            result = render_sheet(p, root, 'actual.png', font_path=self.font())
            with Image.open(Path(root) / 'actual.png') as im:
                colors = {color for count, color in im.convert('RGB').getcolors(im.width * im.height)}
                self.assertTrue(all((i * 40, 20, 80) in colors for i in range(5)))
            before = (Path(root) / 'actual.png').read_bytes()
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                render_sheet(p, root, 'actual.png')
            self.assertEqual((Path(root) / 'actual.png').read_bytes(), before)
            self.assertEqual(result['sha256'], hashlib.sha256(before).hexdigest())

    def test_rendered_captions_expose_panel_level_traceability(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            result = render_sheet(p, root, 'traceability.png', font_path=self.font())
            with Image.open(Path(root) / 'traceability.png') as rendered:
                metadata = rendered.info['storyboard_sheet.panel_traceability']
            self.assertEqual(json.loads(metadata), result['panel_traceability'])
            first = result['panel_traceability'][0]
            self.assertEqual(first['panel_id'], 'P01')
            self.assertEqual(first['beat_ids'], ['B01'])
            self.assertEqual(first['visible_character_ids'], ['CH01'])
            self.assertEqual(first['audio_cue_ids'], ['AU01'])
            self.assertIn('SP01', first['speech_ids'])
            self.assertTrue(any('reveals test reveal' in line for line in first['caption']))

    def test_corrupt_or_changed_input_writes_no_sheet(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            (Path(root) / 'panel0.png').write_bytes(b'corrupt actual image')
            with self.assertRaises(ValueError):
                render_sheet(p, root, 'missing.png')
            self.assertFalse((Path(root) / 'missing.png').exists())

    def test_output_confinement_before_any_write(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            with self.assertRaisesRegex(ValueError, 'escapes'):
                render_sheet(p, root, '../escape.png')

    def test_crop_source_hashes_register_as_actual_inputs(self):
        with tempfile.TemporaryDirectory() as root:
            p = image_package(root)
            canvas = Path(root) / 'input-sheet.png'
            Image.new('RGB', (40, 24), 'orange').save(canvas)
            digest = hashlib.sha256(canvas.read_bytes()).hexdigest()
            p['asset_registry'].append({'id':'CROPINPUT', 'kind':'image', 'version':'1',
                                       'path':canvas.name, 'status':'available', 'sha256':digest})
            p['storyboard']['panels'][0].update(source_sheet_asset_id='CROPINPUT',crop_box=[0,0,40,24])
            result = render_sheet(p, root, 'crop-output.png', font_path=self.font())
            sheet = next(a for a in p['asset_registry'] if a['id'] == 'SHEETIMG')
            sheet.update(path=result['relative_path'], sha256=result['sha256'],
                         panel_ids=result['panel_ids'], source_asset_ids=result['source_asset_ids'],
                         source_sha256=result['source_sha256'])
            self.assertEqual(validate(p,'preproduction',root), [])
            self.assertEqual(result['source_asset_ids'][0], 'CROPINPUT')
            self.assertEqual(result['source_sha256']['CROPINPUT'],digest)
            sheet['source_sha256']['CROPINPUT'] = '0' * 64
            self.assertTrue(any('source hashes' in e for e in validate(p,'preproduction',root)))


if __name__ == '__main__':
    unittest.main()
