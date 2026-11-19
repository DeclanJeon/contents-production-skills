"""Real ffmpeg round trips; synthetic sources are not artistic evidence."""
import copy
import hashlib
import json
import shutil
import subprocess

import pytest
from sequence_contract import SequenceError
from sequence_test_fixture import prepared_plan, check
from sequence_media import probe_media, render_sequence, inspect_sequence_frames

pytestmark = pytest.mark.skipif(not shutil.which('ffmpeg') or not shutil.which('ffprobe'), reason='installed ffmpeg/ffprobe required')


def prepared_edit(root):
    p, q = prepared_plan(root)
    q['execution_artifact_id'] = 'EDIT'
    q['include_source_audio'] = True
    q['output_spec'] = {'video_codec': 'ffv1', 'width': 64, 'height': 36}
    for i, cut in enumerate(q['cuts']):
        asset = f'VIDEO{i}'
        path = root / f'{asset}.mkv'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=64x36:r=24:d=5',
                        '-f', 'lavfi', '-i', f'sine=frequency={300 + i * 300}:sample_rate=48000:duration=5',
                        '-vf', f'hue=h={i * 90}', '-c:v', 'ffv1', '-c:a', 'pcm_s16le', str(path)], check=True)
        row = {'id': asset, 'version': '1', 'kind': 'video', 'status': 'available',
               'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        p['asset_registry'].append(row)
        q['inputs']['assets'][asset] = {'version': '1', 'sha256': row['sha256']}
        cut.update(source_asset_id=asset, source_in_frame=12 + i * 12, source_out_frame=60 + i * 12,
                   source_frame_count=120, source_fps={'num': 24, 'den': 1}, evidence='selected')
        for kind, method in [('source_range', 'continuous_playback'), ('source_audio', 'listening')]:
            record = check('cut:' + cut['cut_id'], kind, [asset], method)
            record.update({k: cut[k] for k in ('source_asset_id', 'source_in_frame', 'source_out_frame')})
            q['checks'].append(record)
    for link in q['links']:
        link['evidence'] = 'observed'
        for kind, method in [('boundary_motion', 'continuous_playback'), ('boundary_audio', 'listening')]:
            q['checks'].append(check('link:' + link['key'], kind, ['VIDEO0', 'VIDEO1'], method))
    for req in q['requirements']:
        source = next(c['source_asset_id'] for c in q['cuts'] if c['cut_id'] == req['cut_ids'][0])
        record = check('requirement:' + req['key'], 'selected_requirement', [source], 'continuous_playback')
        cut = next(c for c in q['cuts'] if c['cut_id'] == req['cut_ids'][0])
        record['event_ranges'] = [{'cut_id': cut['cut_id'], 'source_asset_id': source,
            'source_in_frame': cut['source_in_frame'] + req['final_in_frame'] - cut['final_in_frame'],
            'source_out_frame': cut['source_in_frame'] + req['final_out_frame'] - cut['final_in_frame'],
            'final_in_frame': req['final_in_frame'], 'final_out_frame': req['final_out_frame']}]
        q['checks'].append(record)
    for record in q['checks']:
        if record['kind'] in ('source_range', 'source_audio', 'boundary_motion', 'boundary_audio', 'selected_requirement'):
            record['cut_ranges'] = {c['cut_id']: {k: c[k] for k in ('source_asset_id', 'source_in_frame', 'source_out_frame', 'final_in_frame', 'final_out_frame')}
                                    for c in q['cuts'] if c['source_asset_id'] in record['observed_asset_ids']}
    return p, q


def frame_hashes(path):
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                             '-f', 'framemd5', '-'], capture_output=True, text=True, check=True)
    return [line.split(',')[-1].strip() for line in result.stdout.splitlines() if line and not line.startswith('#')]


def test_rendered_frames_match_exact_selected_sources(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    before = {a['id']: a['sha256'] for a in p['asset_registry']}
    # When
    result = render_sequence(p, q, tmp_path, 'render-v1')
    output = tmp_path / result['video_path']
    # Then
    info = probe_media(output)
    assert (info['frame_count'], info['fps']) == (96, {'num': 24, 'den': 1})
    expected = frame_hashes(tmp_path / 'VIDEO0.mkv')[12:60] + frame_hashes(tmp_path / 'VIDEO1.mkv')[24:72]
    assert frame_hashes(output) == expected
    assert all(hashlib.sha256((tmp_path / a['path']).read_bytes()).hexdigest() == before[a['id']] for a in p['asset_registry'])
    assert result['quality'] == 'unverified'
    assert (tmp_path / result['manifest_path']).is_file()


@pytest.mark.parametrize("scope", ["shot_subset", None, "extra_shot"])
def test_render_distinguishes_approved_subset_from_incomplete_film(tmp_path, scope):
    from test_validate_storyboard import panel, shot

    p, q = prepared_edit(tmp_path)
    p['target_duration_s'] = 6
    p['shots'].append(shot('SH03', 4, 6, ('B04',)))
    p['storyboard']['beats'].append({'id': 'B04', 'synopsis_locator': 'paragraph 4',
                                    'event': 'third beat', 'emotion': 'calm'})
    p['storyboard']['panels'].extend([
        panel('P06', 'SH03', 4, 'start', 'IM01', ('B04',)),
        panel('P07', 'SH03', 143 / 24, 'end', 'IM02', ('B04',)),
    ])
    approved = next(a for a in p['artifacts'] if a['id'] == 'EDIT')['execution_scope']
    if scope is not None:
        approved['deliverable'] = 'shot_subset'
    if scope == 'extra_shot':
        approved['shot_ids'].append('SH03')

    if scope == 'shot_subset':
        result = render_sequence(p, q, tmp_path, 'subset')
        assert result['probe']['frame_count'] == 96
        assert result['quality'] == 'unverified'
    else:
        with pytest.raises(SequenceError, match='shot_coverage'):
            render_sequence(p, q, tmp_path, 'subset')
        assert not (tmp_path / 'subset').exists()


def test_render_accepts_approved_supplied_footage_without_board(tmp_path):
    # Given: actual local footage and a current edit plan with no storyboard.
    p, q = prepared_edit(tmp_path)
    p.pop('storyboard')
    for shot in p['shots']:
        shot.pop('beat_ids', None)
    authority = next(row for row in p['artifacts'] if row['id'] == 'EDIT')
    authority['execution_scope']['basis'] = 'supplied_footage'
    q['requirements'] = [req for req in q['requirements'] if req['kind'] != 'beat']
    for req in q['requirements']:
        req['panel_ids'] = []
    # When: run the real local renderer.
    result = render_sequence(p, q, tmp_path, 'boardless')
    # Then: only actual selected ranges appear in the exported timeline.
    expected = frame_hashes(tmp_path / 'VIDEO0.mkv')[12:60] + frame_hashes(tmp_path / 'VIDEO1.mkv')[24:72]
    assert frame_hashes(tmp_path / result['video_path']) == expected


def test_supplied_footage_flag_cannot_erase_existing_panel_evidence(tmp_path):
    # Given: a board-driven edit with one missing panel link.
    p, q = prepared_edit(tmp_path)
    authority = next(row for row in p['artifacts'] if row['id'] == 'EDIT')
    authority['execution_scope']['basis'] = 'supplied_footage'
    q['requirements'][0]['panel_ids'] = []
    # When / Then: the explicit flag cannot bypass existing storyboard QA.
    with pytest.raises(SequenceError, match='requirement_panel'):
        render_sequence(p, q, tmp_path, 'invalid')
    assert not (tmp_path / 'invalid').exists()


def test_render_requires_export_authority_before_writing(tmp_path):
    # Given: edit authority alone.
    p, q = prepared_edit(tmp_path)
    authority = next(row for row in p['artifacts'] if row['id'] == 'EDIT')
    authority['execution_scope']['operations'] = ['edit']
    # When / Then: rendering refuses to create even an output directory.
    with pytest.raises(SequenceError, match='execution_scope'):
        render_sequence(p, q, tmp_path, 'not-authorized')
    assert not (tmp_path / 'not-authorized').exists()


def test_captioned_edit_does_not_silently_render_without_captions(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    p['captions'] = [{'id': 'CAP01', 'start_s': 0, 'end_s': 1, 'text': 'Hello'}]
    # When / Then
    with pytest.raises(SequenceError, match='unsupported_captions'):
        render_sequence(p, q, tmp_path, 'captionless')
    assert not (tmp_path / 'captionless').exists()


@pytest.mark.parametrize('mode', ['burned_in', 'sidecar'])
def test_delivery_caption_mode_blocks_render_even_without_cues(tmp_path, mode):
    # Given: only the canonical delivery specification requires captions.
    p, q = prepared_edit(tmp_path)
    p['delivery_spec']['caption_mode'] = mode
    # When / Then: the unsupported delivery cannot write an output.
    with pytest.raises(SequenceError, match='unsupported_captions'):
        render_sequence(p, q, tmp_path, 'captionless')
    assert not (tmp_path / 'captionless').exists()


def test_existing_output_is_not_overwritten(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    target = tmp_path / 'existing'; target.mkdir(); (target / 'keep').write_text('original')
    # When / Then
    with pytest.raises(SequenceError, match='output_exists'):
        render_sequence(p, q, tmp_path, 'existing')
    assert (target / 'keep').read_text() == 'original'


def test_wrong_declared_source_count_fails_before_output(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['cuts'][0]['source_frame_count'] = 121
    # When / Then
    with pytest.raises(SequenceError, match='source_probe'):
        render_sequence(p, q, tmp_path, 'wrong')
    assert not (tmp_path / 'wrong').exists()


def test_fps_change_is_not_an_implicit_speed_fix(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['cuts'][0]['source_fps']['num'] = 25
    # When / Then
    with pytest.raises(SequenceError, match='conform_required'):
        render_sequence(p, q, tmp_path, 'wrong')


def test_source_preview_can_be_created_before_perceptual_inspection(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['checks'] = []
    # When
    result = inspect_sequence_frames(p, q, tmp_path, 'unreviewed-source', 'source')
    # Then
    assert len(result['cuts']) == 2
    assert result['quality'] == 'unverified'


def test_first_source_preview_does_not_require_future_shot_media(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['focus']['shot_ids'] = ['SH01']
    q['cuts'][1]['source_asset_id'] = None
    # When
    result = inspect_sequence_frames(p, q, tmp_path, 'first-source', 'source')
    # Then
    assert [c['cut_id'] for c in result['cuts']] == ['SH01']


def test_source_previews_include_exact_out_minus_one_frames(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    # When
    result = inspect_sequence_frames(p, q, tmp_path, 'inspection-v1', 'source')
    # Then
    assert [(r['source_in_frame'], r['source_last_frame']) for r in result['cuts']] == [(12, 59), (24, 71)]
    assert all((tmp_path / row['exit_image']).is_file() for row in result['cuts'])
    assert result['quality'] == 'unverified'


def test_plan_comparison_has_real_images_and_timeline_positions(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    # When
    result = inspect_sequence_frames(p, q, tmp_path, 'plan-review-v1', 'plan')
    # Then
    assert len(result['panels']) == 5
    assert result['panels'][1]['final_frame'] == 47
    assert result['links'][0]['out_frame'] == 47
    assert result['links'][0]['in_frame'] == 48


@pytest.mark.parametrize('pin', [None, {'version': 'old', 'sha256': 'old'}])
def test_external_audio_requires_current_projection_input_pin(tmp_path, pin):
    # A separately registered audio-bearing input must appear in render lineage.
    p, q = prepared_edit(tmp_path)
    track = dict(next(a for a in p['asset_registry'] if a['id'] == 'VIDEO0'), id='TRACK')
    p['asset_registry'].append(track)
    q['audio_tracks'] = [{'asset_id': 'TRACK', 'source_in_s': 0, 'source_out_s': 1, 'final_start_s': 0}]
    if pin is not None:
        q['inputs']['assets']['TRACK'] = pin
    with pytest.raises(SequenceError, match='stale_asset'):
        render_sequence(p, q, tmp_path, 'unpinned-audio')
    assert not (tmp_path / 'unpinned-audio').exists()


def test_pinned_external_audio_is_preserved_in_render_input_manifest(tmp_path):
    p, q = prepared_edit(tmp_path)
    track = dict(next(a for a in p['asset_registry'] if a['id'] == 'VIDEO0'), id='TRACK')
    p['asset_registry'].append(track)
    q['inputs']['assets']['TRACK'] = {'version': track['version'], 'sha256': track['sha256']}
    q['audio_tracks'] = [{'asset_id': 'TRACK', 'source_in_s': 0, 'source_out_s': 1, 'final_start_s': 0}]
    result = render_sequence(p, q, tmp_path, 'pinned-audio')
    assert result['inputs']['assets']['TRACK'] == {'version': '1', 'sha256': track['sha256']}
    assert probe_media(tmp_path / result['video_path'])['has_audio']


def test_missing_heard_audio_cannot_silently_export_mute(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path); q['include_source_audio'] = False
    # When / Then
    with pytest.raises(SequenceError, match='audio_path'):
        render_sequence(p, q, tmp_path, 'mute')
