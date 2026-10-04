#!/usr/bin/env python3
"""Split storyboard panels into ordered clean cut files and a derived manifest.

Reads each panel's registered source sheet crop or existing clean image,
preflights every ID/path/crop/overwrite before writing, and emits
000N_PANELID.png plus split-manifest.json. The manifest is a derived
registration report, not a new ledger; the project is never mutated.
Pillow is required; no network access or media generation happens here.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - environment check
    raise RuntimeError(
        'split_storyboard requires Pillow (pip install Pillow)'
    )

ID_PATTERN = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]*')
VALID_SOURCE_STATUS = ('available', 'verified')


def _sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def _confined(base, relative, label, errors):
    """Resolve a project-relative asset path inside base_dir."""
    if not isinstance(relative, str) or not relative.strip():
        errors.append(f'{label}: nonempty relative path required')
        return None
    if Path(relative).is_absolute() or re.match(r'^[A-Za-z]:', relative):
        errors.append(f'{label}: path must stay inside the project base')
        return None
    resolved = (base / relative).resolve()
    if resolved != base and base not in resolved.parents:
        errors.append(f'{label}: path escapes the project base')
        return None
    return resolved


def _asset(assets, asset_id):
    return assets.get(asset_id) if isinstance(asset_id, str) else None


def _check_source(panel_id, panel, assets, base, errors):
    """Return (kind, asset, box) for a panel source, or None on errors."""
    sheet_id = panel.get('source_sheet_asset_id')
    image_id = panel.get('image_asset_id')
    box = panel.get('crop_box')
    has_sheet = sheet_id is not None
    has_box = box is not None
    if has_sheet != has_box:
        errors.append(f'{panel_id}: source_sheet_asset_id and crop_box must appear together')
    if has_sheet or has_box:
        if not has_sheet:
            errors.append(f'{panel_id}: crop_box without source_sheet_asset_id')
            return None
        asset = _asset(assets, sheet_id)
        if asset is None:
            errors.append(f'{panel_id}: unknown source_sheet_asset_id {sheet_id}')
            return None
        if asset.get('status') not in VALID_SOURCE_STATUS:
            errors.append(f'{panel_id}: source sheet {sheet_id} must be available or verified')
        path = _confined(base, asset.get('path'), f'{panel_id}: source sheet {sheet_id}', errors)
        if path is not None and not path.is_file():
            errors.append(f'{panel_id}: source sheet file missing for {sheet_id}')
            path = None
        if box is None or not isinstance(box, list) or len(box) != 4:
            errors.append(f'{panel_id}: crop_box must be [left,top,right,bottom]')
            return ('sheet', asset, path, None)
        bad = any(not isinstance(v, int) or isinstance(v, bool) for v in box)
        if bad:
            errors.append(f'{panel_id}: crop_box values must be integers')
            return ('sheet', asset, path, None)
        left, top, right, bottom = box
        if right <= left or bottom <= top:
            errors.append(f'{panel_id}: crop_box must be nonempty')
            return ('sheet', asset, path, None)
        return ('sheet', asset, path, tuple(box))
    # Clean image source: image_asset_id alone.
    if image_id is None:
        errors.append(f'{panel_id}: image_asset_id or source_sheet_asset_id+crop_box required')
        return None
    asset = _asset(assets, image_id)
    if asset is None:
        errors.append(f'{panel_id}: unknown image_asset_id {image_id}')
        return None
    if asset.get('status') not in VALID_SOURCE_STATUS:
        errors.append(f'{panel_id}: clean image {image_id} must be available or verified')
    path = _confined(base, asset.get('path'), f'{panel_id}: image {image_id}', errors)
    if path is not None and not path.is_file():
        errors.append(f'{panel_id}: clean image file missing for {image_id}')
        path = None
    return ('clean', asset, path, None)


def _overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def split_storyboard(project, base_dir, output_dir):
    """Extract panel cuts; returns the manifest dict. Raises ValueError on preflight failure."""
    base = Path(base_dir).resolve()
    out = Path(output_dir).resolve()
    if out != base and base not in out.parents:
        raise ValueError('output directory must be inside the project base')
    if out.exists():
        raise ValueError(f'output directory already exists: {out}')
    if not isinstance(project, dict):
        raise ValueError('project must be an object')
    storyboard = project.get('storyboard')
    if not isinstance(storyboard, dict) or not isinstance(storyboard.get('panels'), list):
        raise ValueError('project.storyboard.panels array required')
    panels = storyboard['panels']
    if not panels:
        raise ValueError('storyboard.panels is empty; nothing to split')
    def ids(table):
        rows = project.get(table)
        if not isinstance(rows, list):
            return {}
        return {row.get('id'): row for row in rows
                if isinstance(row, dict) and isinstance(row.get('id'), str)}
    shots = ids('shots')
    assets = ids('asset_registry')
    scenes = set(ids('scenes'))
    characters = set(ids('characters'))
    audio_cues = set(ids('audio_cues'))
    beat_rows = storyboard.get('beats')
    beats = {row.get('id') for row in (beat_rows if isinstance(beat_rows, list) else [])
             if isinstance(row, dict) and isinstance(row.get('id'), str)}

    errors = []
    jobs = []          # (index, panel, kind, asset, source_path, box)
    boxes_by_sheet = {}
    seen_panel_ids = set()
    for index, panel in enumerate(panels, 1):
        label = f'panels[{index - 1}]'
        if not isinstance(panel, dict):
            errors.append(f'{label}: panel must be an object')
            continue
        panel_id = panel.get('id')
        if not isinstance(panel_id, str) or not ID_PATTERN.fullmatch(panel_id):
            errors.append(f'{label}: unsafe panel id {panel_id!r}')
            continue
        key = panel_id.lower()
        if key in seen_panel_ids:
            errors.append(f'{panel_id}: duplicate panel id')
        seen_panel_ids.add(key)
        filename = f'{index:04d}_{panel_id}.png'
        shot_id = panel.get('shot_id')
        shot = shots.get(shot_id) if isinstance(shot_id, str) else None
        if shot is None:
            errors.append(f'{panel_id}: unknown shot_id {shot_id}')
        else:
            scene_ref = shot.get('scene_id')
            if not isinstance(scene_ref, str) or scene_ref not in scenes:
                errors.append(f'{panel_id}: shot {shot_id} unknown scene_id {scene_ref!r}')
            for field, table in (('beat_ids', beats), ('character_ids', characters),
                                 ('audio_cue_ids', audio_cues)):
                values = shot.get(field, [])
                if not isinstance(values, list):
                    errors.append(f'{panel_id}: shot {shot_id} {field} must be an array')
                    continue
                for value in values:
                    if not isinstance(value, str) or value not in table:
                        errors.append(f'{panel_id}: shot {shot_id} unknown {field} {value!r}')
        source = _check_source(panel_id, panel, assets, base, errors)
        if source is None:
            continue
        kind, asset, path, box = source
        if kind == 'sheet' and box is not None:
            boxes_by_sheet.setdefault(id(asset), (asset, []))[1].append((panel_id, box))
        jobs.append((index, panel, panel_id, filename, kind, asset, path, box))

    # Open each source sheet once: decode validity plus crop bounds.
    sheet_sizes = {}
    for asset, pairs in boxes_by_sheet.values():
        path = _confined(base, asset.get('path'), 'source sheet', errors)
        if path is None or not path.is_file():
            continue
        try:
            with Image.open(path) as im:
                im.load()
                sheet_sizes[id(asset)] = im.size
        except Exception as e:
            errors.append(f'source sheet {asset.get("id")}: unreadable image ({e})')
            continue
        w, h = sheet_sizes[id(asset)]
        for panel_id, box in pairs:
            left, top, right, bottom = box
            if left < 0 or top < 0 or right > w or bottom > h:
                errors.append(f'{panel_id}: crop_box {box} outside image {w}x{h}')
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                if _overlap(pairs[i][1], pairs[j][1]):
                    errors.append(
                        f'{pairs[i][0]}: crop overlaps panel {pairs[j][0]} on sheet {asset.get("id")}')
    # Clean images must decode too.
    for index, panel, panel_id, filename, kind, asset, path, box in jobs:
        if kind != 'clean' or path is None or not path.is_file():
            continue
        try:
            with Image.open(path) as im:
                im.load()
        except Exception as e:
            errors.append(f'{panel_id}: clean image unreadable ({e})')
    if errors:
        raise ValueError('split preflight failed: ' + '; '.join(errors))

    out.mkdir(parents=True)
    entries = []
    try:
        for index, panel, panel_id, filename, kind, asset, path, box in jobs:
            dest = out / filename
            with Image.open(path) as im:
                if kind == 'sheet':
                    im.crop(box).save(dest, format='PNG')
                else:
                    keep = im.convert('RGBA') if 'A' in im.getbands() else im.convert('RGB')
                    keep.save(dest, format='PNG')
            shot = shots.get(panel.get('shot_id'), {})
            entries.append({
                'file': filename,
                'sha256': _sha256(dest),
                'panel_id': panel_id,
                'shot_id': panel.get('shot_id'),
                'scene_id': shot.get('scene_id'),
                'beat_ids': list(shot.get('beat_ids') or []),
                'character_ids': list(shot.get('character_ids') or []),
                'audio_cue_ids': list(shot.get('audio_cue_ids') or []),
                'source_asset_id': asset.get('id'),
                'crop_box': list(box) if box else None,
            })
    except Exception:
        shutil.rmtree(out, ignore_errors=True)
        raise
    manifest = {
        'kind': 'split-manifest',
        'derived': True,
        'project_id': project.get('project_id'),
        'entries': entries,
    }
    (out / 'split-manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project')
    parser.add_argument('--base-dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        project = json.loads(Path(args.project).read_text(encoding='utf-8'))
        manifest = split_storyboard(project, args.base_dir, args.output)
    except (OSError, ValueError, RuntimeError) as e:
        print(json.dumps({'ok': False, 'errors': [str(e)]}, ensure_ascii=False))
        return 2
    print(json.dumps({'ok': True, 'files': len(manifest['entries']),
                      'manifest': str(Path(args.output) / 'split-manifest.json')},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
