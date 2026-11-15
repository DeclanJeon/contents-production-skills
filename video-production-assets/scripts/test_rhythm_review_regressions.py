"""Regression evidence for the independent rhythm review (F1--F3)."""
import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from measure_cut_rhythm import cuts_from_media, main, read_cuts_csv, media_duration
from test_validate_storyboard import board


def invoke(tmp_path, detected, duration):
    project = tmp_path / 'project.json'
    project.write_text(json.dumps(board()))
    output = tmp_path / 'report.json'
    with patch('measure_cut_rhythm.detect_cuts', return_value=detected), \
         patch('measure_cut_rhythm.media_duration', return_value=duration, create=True):
        code = main(['--project', str(project), '--media', 'fixture.mp4', '--out', str(output)])
    return code, json.loads(output.read_text())


def test_f1_media_unmatched_is_partial(tmp_path):
    code, report = invoke(tmp_path, [1.0, 3.0], 4.0)
    assert code == 0
    assert report['status'] == 'partial'
    assert report['curve_check']['unmatched_detected']


def test_f2_media_tail_is_counted(tmp_path):
    code, report = invoke(tmp_path, [2.0], 4.0)
    assert code == 0
    assert report['status'] == 'measured'
    assert [c['duration_s'] for c in report['cuts']] == [2.0, 2.0]
    assert report['stats']['total_s'] == 4.0
    assert report['curve_check']['planned_total_s'] == 4.0


def test_f2_no_transition_is_one_complete_cut(tmp_path):
    _, report = invoke(tmp_path, [], 4.0)
    assert len(report['cuts']) == 1
    assert report['cuts'][0]['end_s'] == 4.0
    assert report['status'] == 'partial'  # SH02 has no detected boundary.


def test_f2_missing_duration_is_not_measured(tmp_path):
    project = tmp_path / 'project.json'
    project.write_text(json.dumps(board()))
    out = tmp_path / 'report.json'
    with patch('measure_cut_rhythm.detect_cuts', return_value=[2.0]), \
         patch('measure_cut_rhythm.media_duration', side_effect=ValueError('media_duration_unavailable'), create=True):
        assert main(['--project', str(project), '--media', 'x.mp4', '--out', str(out)]) == 3
    assert json.loads(out.read_text())['status'] == 'unverified'


@pytest.mark.parametrize('value', ['nan', 'inf', '-inf'])
def test_f3_nonfinite_csv_is_rejected(tmp_path, value):
    csv = tmp_path / 'cuts.csv'
    csv.write_text(f'cut_id,start_s,end_s\nM01,{value},2\n')
    with pytest.raises(ValueError, match='non-finite'):
        read_cuts_csv(csv, board(), 0.5)


def test_f2_csv_gap_is_reported(tmp_path):
    project = tmp_path / 'project.json'
    project.write_text(json.dumps(board()))
    csv = tmp_path / 'cuts.csv'
    csv.write_text('cut_id,start_s,end_s,shot_id\nM01,0,2,SH01\nM02,2.5,4,SH02\n')
    out = tmp_path / 'report.json'
    assert main(['--project', str(project), '--cuts', str(csv), '--out', str(out)]) == 0
    report = json.loads(out.read_text())
    assert report['status'] == 'partial'
    assert report['curve_check']['coverage_gaps'] == [{'start_s': 2.0, 'end_s': 2.5}]


def test_f2_probe_duration_from_actual_video(tmp_path):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        pytest.skip('requires existing ffmpeg and ffprobe')
    media = tmp_path / 'three-cuts.mp4'
    argv = [shutil.which('ffmpeg'), '-v', 'error', '-y']
    for color in ('red', 'blue', 'white'):
        argv += ['-f', 'lavfi', '-i', f'color=c={color}:s=160x90:d=2:r=24']
    argv += ['-filter_complex', '[0:v][1:v][2:v]concat=n=3:v=1:a=0',
             '-pix_fmt', 'yuv420p', str(media)]
    subprocess.run(argv, check=True, capture_output=True)
    project = board()
    project['shots'].append(dict(project['shots'][-1], id='SH03', start_s=4, end_s=6))
    cuts, meta = cuts_from_media(media, project, 0.3, 0.4, 0.5)
    assert media_duration(media) == pytest.approx(6.0, abs=1 / 24)
    assert [c['shot_id'] for c in cuts] == ['SH01', 'SH02', 'SH03']
    assert sum(c['duration_s'] for c in cuts) == pytest.approx(6.0, abs=1 / 24)
    assert not meta['unmatched_planned']
