"""Local media adapters: actual frame extraction/rendering, not visual judgment."""
from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
import html
import json
from pathlib import Path
import shutil
import subprocess

from sequence_contract import (Document, FrameSpan, Json, SequenceError, checked_assets,
                               file_hash, frame_at, number, parse_fps, table, project_file)
from validate_sequence import validate_sequence


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Bound local processes; never execute provider output as shell commands."""
    if shutil.which(command[0]) is None:
        raise SequenceError('tool_missing', command[0], 'installed executable required')
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=300, check=False)
    except subprocess.TimeoutExpired as exc:
        raise SequenceError('process_timeout', command[0], 'operation exceeded 300 seconds') from exc
    if completed.returncode:
        raise SequenceError('media_process', command[0], completed.stderr[-1500:])
    return completed


def probe_media(path: Path) -> Document:
    """Measure actual display frames and PTS; do not infer counts from duration."""
    raw = json.loads(_run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)]).stdout)
    streams = raw.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    if video is None:
        raise SequenceError('video_stream', str(path), 'video stream missing')
    rate = Fraction(video['r_frame_rate'])
    if rate <= 0:
        raise SequenceError('video_fps', str(path), 'unknown positive frame rate')
    time_base = Fraction(video['time_base'])
    data = json.loads(_run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_frames',
                            '-show_entries', 'frame=best_effort_timestamp', '-of', 'json', str(path)]).stdout)
    frames = data.get('frames', [])
    if not frames or any('best_effort_timestamp' not in f for f in frames):
        raise SequenceError('video_pts', str(path), 'display frame PTS unavailable')
    pts = [int(f['best_effort_timestamp']) for f in frames]
    deltas = [(b - a) * time_base for a, b in zip(pts, pts[1:])]
    vfr = any(delta <= 0 or abs(delta - 1 / rate) > time_base for delta in deltas)
    return {'fps': {'num': rate.numerator, 'den': rate.denominator}, 'frame_count': len(pts),
            'width': int(video['width']), 'height': int(video['height']),
            'time_base': str(time_base), 'frame_pts': pts, 'vfr': vfr,
            'has_audio': any(s.get('codec_type') == 'audio' for s in streams),
            'duration_s': float((pts[-1] - pts[0]) * time_base + 1 / rate)}


def _new_output(root: Path, value: str) -> Path:
    path = project_file(root, value, must_exist=False)
    if path.exists():
        raise SequenceError('output_exists', value, 'use a new versioned output directory')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.mkdir()
    except FileExistsError as exc:
        raise SequenceError('output_exists', value, 'another writer reserved this output') from exc
    return path


def _save(path: Path, data: Document) -> None:
    with path.open('x', encoding='utf-8') as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
        output.write('\n')


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root.resolve()).as_posix()


def _checked_cuts(project: Mapping[str, Json], q: Mapping[str, Json], root: Path) -> tuple[dict[str, Path], dict[str, Document]]:
    cuts = q['cuts']
    ids = sorted({c['source_asset_id'] for c in cuts})
    paths = checked_assets(project, root, ids)
    registered = table(project, 'asset_registry')
    pins = q.get('inputs', {}).get('assets', {})
    for aid in ids:
        expected = {'version': registered[aid]['version'], 'sha256': registered[aid]['sha256']}
        if pins.get(aid) != expected:
            raise SequenceError('stale_asset', aid, 'candidate version/hash differs from projection')
    probes = {aid: probe_media(path) for aid, path in paths.items()}
    fps = parse_fps(q['time_basis']['fps'])
    for cut in cuts:
        probe = probes[cut['source_asset_id']]
        if probe['vfr'] or parse_fps(probe['fps']) != fps:
            raise SequenceError('conform_required', cut['cut_id'], 'supply explicitly conformed CFR asset and raw lineage; no implicit speed/FPS fix')
        if probe['frame_count'] != cut['source_frame_count'] or parse_fps(probe['fps']) != parse_fps(cut['source_fps']):
            raise SequenceError('source_probe', cut['cut_id'], 'declared frame count/FPS differs from actual source')
    return paths, probes


def _gate(project: Mapping[str, Json], q: Mapping[str, Json], phase: str, root: Path) -> None:
    result = validate_sequence(project, q, phase, root)
    if not result['ready']:
        raise SequenceError('gate_blocked', phase, json.dumps(result['blockers'], ensure_ascii=False))


def render_sequence(project: Mapping[str, Json], q: Mapping[str, Json],
                    root: Path, output: str) -> Document:
    """Render only a reviewed edit projection; retain sources and mark quality unverified."""
    root = root.resolve()
    _gate(project, q, 'edit', root)
    paths, probes = _checked_cuts(project, q, root)
    fps = parse_fps(q['time_basis']['fps'])
    cuts = q['cuts']; total = cuts[-1]['final_out_frame']; duration = Fraction(total, 1) / fps
    spec = q.get('output_spec', {})
    codec = spec.get('video_codec', 'libx264')
    if codec not in ('libx264', 'ffv1'):
        raise SequenceError('unsupported_codec', 'output_spec', 'use libx264 or ffv1')
    first = probes[cuts[0]['source_asset_id']]
    width, height = spec.get('width', first['width']), spec.get('height', first['height'])
    if any(p['width'] != width or p['height'] != height for p in probes.values()):
        raise SequenceError('conform_required', 'resolution', 'explicitly conformed equal-size sources required')
    if Fraction(width, height) != Fraction(project['aspect_ratio'].replace(':', '/')):
        raise SequenceError('aspect_ratio', 'output_spec', 'output dimensions differ from project aspect ratio')
    use_source_audio = q.get('include_source_audio', False)
    tracks = q.get('audio_tracks', [])
    if not isinstance(tracks, list) or not all(isinstance(t, dict) for t in tracks):
        raise SequenceError('audio_tracks', 'audio_tracks', 'expected audio layer objects')
    if project.get('audio_mode') != 'no_audio' and not use_source_audio and not tracks:
        raise SequenceError('audio_path', 'edit', 'explicit source audio or actual external layers required')
    if use_source_audio and any(not p['has_audio'] for p in probes.values()):
        raise SequenceError('audio_path', 'source', 'source-audio concat needs audio in every selected source')
    track_paths = checked_assets(project, root, [t['asset_id'] for t in tracks])
    registered = table(project, 'asset_registry')
    for aid in track_paths:
        expected = {'version': registered[aid]['version'], 'sha256': registered[aid]['sha256']}
        if q.get('inputs', {}).get('assets', {}).get(aid) != expected:
            raise SequenceError('stale_asset', aid, 'external audio requires a current projection version/hash pin')
    paths.update(track_paths)
    for track in tracks:
        a = number(track.get('source_in_s'), 'audio in'); b = number(track.get('source_out_s'), 'audio out')
        start = number(track.get('final_start_s'), 'audio position')
        if a < 0 or b <= a or start < 0 or start + b - a > duration:
            raise SequenceError('audio_bounds', track['asset_id'], 'invalid source/final interval')
        gain = number(track.get('gain_db', 0), 'gain')
        if not -96 <= gain <= 24:
            raise SequenceError('audio_gain', track['asset_id'], 'gain outside -96..24 dB')
        for field in ('fade_in_s', 'fade_out_s'):
            if not 0 <= number(track.get(field, 0), field) <= b - a:
                raise SequenceError('audio_fade', field, 'fade exceeds layer duration')
        audio_info = json.loads(_run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_type:format=duration', '-of', 'json', str(paths[track['asset_id']])]).stdout)
        if not audio_info.get('streams') or b > number(float(audio_info['format']['duration']), 'audio duration'):
            raise SequenceError('audio_bounds', track['asset_id'], 'layer exceeds actual audio')
    ids = list(paths); indexes = {aid: i for i, aid in enumerate(ids)}
    command = ['ffmpeg', '-v', 'error', '-nostdin']
    for aid in ids:
        command.extend(['-i', str(paths[aid])])
    filters, concat, lineage = [], [], []
    for i, cut in enumerate(cuts):
        span = FrameSpan(cut['source_in_frame'], cut['source_out_frame'])
        source = cut['source_asset_id']; index = indexes[source]
        filters.append(f'[{index}:v:0]trim=start_frame={span.start}:end_frame={span.end},setpts=PTS-STARTPTS,setsar=1[v{i}]')
        concat.append(f'[v{i}]')
        if use_source_audio:
            a, b = float(span.start / fps), float(span.end / fps)
            filters.append(f'[{index}:a:0]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a{i}]')
            concat.append(f'[a{i}]')
        probe = probes[source]
        lineage.append({'cut_id': cut['cut_id'], 'source_asset_id': source,
                        'source_in_frame': span.start, 'source_out_frame': span.end,
                        'source_in_pts': probe['frame_pts'][span.start], 'source_last_pts': probe['frame_pts'][span.last],
                        'source_time_base': probe['time_base'], 'final_in_frame': cut['final_in_frame'],
                        'final_out_frame': cut['final_out_frame']})
    filters.append(''.join(concat) + f'concat=n={len(cuts)}:v=1:a={int(use_source_audio)}[vout]' + ('[baseaudio]' if use_source_audio else ''))
    audio_labels = ['[baseaudio]'] if use_source_audio else []
    for i, track in enumerate(tracks):
        a, b, start = (float(number(track[k], k)) for k in ('source_in_s', 'source_out_s', 'final_start_s'))
        fi, fo = float(number(track.get('fade_in_s', 0), 'fade')), float(number(track.get('fade_out_s', 0), 'fade'))
        filters.append(f'[{indexes[track["asset_id"]]}:a:0]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aresample=48000,'
                       f'aformat=channel_layouts=stereo,volume={float(number(track.get("gain_db", 0), "gain"))}dB,'
                       f'afade=t=in:st=0:d={fi},afade=t=out:st={b-a-fo}:d={fo},adelay={start*1000}:all=1[track{i}]')
        audio_labels.append(f'[track{i}]')
    if audio_labels:
        filters.append(''.join(audio_labels) + f'amix=inputs={len(audio_labels)}:duration=longest:normalize=0,'
                       f'apad=whole_dur={float(duration)},atrim=duration={float(duration)}[aout]')
    folder = _new_output(root, output)
    video = folder / ('sequence.mkv' if codec == 'ffv1' else 'sequence.mp4')
    _save(folder / 'RUNNING.json', {'status': 'incomplete', 'quality': 'unverified'})
    command.extend(['-filter_complex', ';'.join(filters), '-map', '[vout]', '-r', str(fps), '-fps_mode', 'cfr',
                    '-frames:v', str(total), '-c:v', codec, '-pix_fmt', 'yuv420p'])
    if audio_labels:
        command.extend(['-map', '[aout]', '-c:a', 'pcm_s16le' if codec == 'ffv1' else 'aac', '-ar', '48000'])
    else:
        command.append('-an')
    command.extend(['-n', str(video)])
    _run(command)
    actual = probe_media(video)
    if actual['frame_count'] != total or parse_fps(actual['fps']) != fps or actual['vfr']:
        raise SequenceError('output_probe', str(video), 'rendered FPS/frame count/PTS do not match edit')
    _run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-'])
    checked_assets(project, root, ids)
    result = {'status': 'rendered', 'quality': 'unverified', 'video_path': _relative(root, video),
              'manifest_path': _relative(root, folder / 'manifest.json'), 'sha256': file_hash(video),
              'probe': actual, 'cuts': lineage, 'owner': q['owner'], 'inputs': q['inputs'],
              'limits': 'Technical render only; actual boundary/whole playback and listening still required.'}
    _save(folder / 'manifest.json', result)
    (folder / 'RUNNING.json').unlink()
    return result


def _extract(path: Path, frame: int, destination: Path) -> None:
    _run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(path), '-vf', f'select=eq(n\\,{frame})',
          '-frames:v', '1', '-fps_mode', 'passthrough', '-n', str(destination)])
    if not destination.is_file():
        raise SequenceError('frame_missing', str(path), f'frame {frame} not decoded')


def inspect_sequence_frames(project: Mapping[str, Json], q: Mapping[str, Json], root: Path,
                            output: str, mode: str = 'plan') -> Document:
    """Build concrete comparison evidence; observing it remains the agent's job."""
    root = root.resolve()
    if mode not in ('plan', 'source', 'export'):
        raise SequenceError('inspection_mode', mode, 'expected plan/source/export')
    panels = project.get('storyboard', {}).get('panels', [])
    paths, probes = {}, {}
    inspected_cuts = q['cuts']
    if mode == 'plan':
        ids = [p.get('image_asset_id') or p.get('source_sheet_asset_id') for p in panels]
        paths = checked_assets(project, root, ids)
    elif mode == 'source':
        # Inspection precedes perceptual acceptance. Only decode the requested
        # actual candidates, never require unproduced future takes for a preview.
        focus = q.get('focus', {}).get('shot_ids', [])
        inspected_cuts = [c for c in q['cuts'] if c['shot_id'] in focus] if focus else q['cuts']
        if not inspected_cuts or any(not isinstance(c.get('source_asset_id'), str) for c in inspected_cuts):
            raise SequenceError('source_selection', 'inspection', 'explicit actual candidate sources required')
        paths, probes = _checked_cuts(project, dict(q, cuts=inspected_cuts), root)
    else:
        output_id = q.get('output_asset_id')
        if not isinstance(output_id, str):
            raise SequenceError('output_asset', mode, 'register the actual output before inspection')
        paths = checked_assets(project, root, [output_id])
        probes[output_id] = probe_media(paths[output_id])
        expected = q['cuts'][-1]['final_out_frame']
        if probes[output_id]['frame_count'] != expected or parse_fps(probes[output_id]['fps']) != parse_fps(q['time_basis']['fps']):
            raise SequenceError('output_probe', output_id, 'actual output differs from declared timeline')
    folder = _new_output(root, output)
    fps = parse_fps(q['time_basis']['fps'])
    result = {'mode': mode, 'quality': 'unverified', 'panels': [], 'cuts': [], 'links': [],
              'manifest_path': _relative(root, folder / 'comparisons.json')}
    figures = []
    if mode == 'plan':
        from PIL import Image
        for index, panel in enumerate(panels):
            source = panel.get('image_asset_id') or panel.get('source_sheet_asset_id')
            target = folder / f'panel-{index:04d}.png'
            with Image.open(paths[source]) as image:
                if not panel.get('image_asset_id') and panel.get('crop_box'):
                    image = image.crop(panel['crop_box'])
                image.save(target)
            frame = frame_at(panel['frame_time_s'], fps)
            result['panels'].append({'panel_id': panel['id'], 'shot_id': panel['shot_id'], 'final_frame': frame,
                                     'asset_id': source, 'image': _relative(root, target)})
            figures.append(f'<figure><img src="{target.name}"><figcaption>{html.escape(panel["id"])} — final f{frame}</figcaption></figure>')
    else:
        for i, cut in enumerate(inspected_cuts):
            source = q['output_asset_id'] if mode == 'export' else cut['source_asset_id']
            a = cut['final_in_frame'] if mode == 'export' else cut['source_in_frame']
            b = cut['final_out_frame'] if mode == 'export' else cut['source_out_frame']
            if b > probes[source]['frame_count']:
                raise SequenceError('source_bounds', cut['cut_id'], 'inspection exceeds decoded frames')
            entry, exit_image, preview = (folder / f'cut-{i:04d}-{suffix}' for suffix in ('entry.png', 'exit.png', 'motion.mp4'))
            _extract(paths[source], a, entry); _extract(paths[source], b - 1, exit_image)
            info = probes[source]
            command = ['ffmpeg', '-v', 'error', '-nostdin', '-i', str(paths[source]),
                       '-vf', f'trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS',
                       '-r', str(fps), '-frames:v', str(b-a), '-c:v', 'libx264', '-pix_fmt', 'yuv420p']
            if info['has_audio']:
                command.extend(['-af', f'atrim=start={float(a/fps)}:end={float(b/fps)},asetpts=PTS-STARTPTS', '-c:a', 'aac'])
            else:
                command.append('-an')
            _run(command + ['-n', str(preview)])
            result['cuts'].append({'cut_id': cut['cut_id'], 'source_asset_id': source,
                'source_in_frame': a, 'source_last_frame': b-1, 'source_in_pts': info['frame_pts'][a],
                'source_last_pts': info['frame_pts'][b-1], 'time_base': info['time_base'],
                'entry_image': _relative(root, entry), 'exit_image': _relative(root, exit_image),
                'motion_preview': _relative(root, preview)})
            figures.append(f'<figure><img src="{entry.name}"><img src="{exit_image.name}"><video controls src="{preview.name}"></video>'
                           f'<figcaption>{html.escape(cut["cut_id"])}: {a} → {b-1}</figcaption></figure>')
    by_cut = {c['cut_id']: c for c in q['cuts']}
    for link in q['links']:
        a, b = by_cut[link['from_cut_id']], by_cut[link['to_cut_id']]
        result['links'].append({'key': link['key'], 'out_frame': a['final_out_frame']-1,
                                'in_frame': b['final_in_frame'], 'state_out': link.get('state_out'),
                                'state_in': link.get('state_in'), 'relation': link.get('relation'),
                                'quality': 'unverified'})
    (folder / 'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Sequence comparison</title>'
        '<h1>Actual comparison material — not inspection acceptance</h1><style>img,video{max-width:45%;height:auto}figure{border-bottom:1px solid #888;padding:1em}</style>'
        + ''.join(figures), encoding='utf-8')
    checked_assets(project, root, list(paths))
    registered = table(project, 'asset_registry')
    result['owner'] = q['owner']
    result['inputs'] = q['inputs']
    result['observed_assets'] = {aid: {'version': registered[aid]['version'], 'sha256': registered[aid]['sha256']} for aid in paths}
    _save(folder / 'comparisons.json', result)
    return result
