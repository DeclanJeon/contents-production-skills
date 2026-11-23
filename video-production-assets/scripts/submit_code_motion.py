#!/usr/bin/env python3
"""Check local code-motion takes against their job envelope before submitting."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


def run_media(tool: str, args: list[str]) -> str:
    result = subprocess.run([tool, *args], capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise ValueError(f'{tool}: {result.stderr.strip()[:400]}')
    return result.stdout


def check_clip(clip: Path, params: dict[str, str]) -> None:
    if not clip.is_file():
        raise ValueError(f'missing file: {clip}')
    probe = json.loads(run_media('ffprobe', ['-v', 'error', '-show_streams', '-of', 'json', str(clip)]))
    videos = [stream for stream in probe['streams'] if stream['codec_type'] == 'video'
              and not stream.get('disposition', {}).get('attached_pic')]
    if len(videos) != 1:
        raise ValueError('expected one video stream')
    video = videos[0]
    width, height = video['width'], video['height']
    sar = video.get('sample_aspect_ratio', '1:1')
    aspect = Fraction(width, height) * (Fraction(1) if sar == 'N/A' else Fraction(sar.replace(':', '/')))
    if any(int(side.get('rotation', 0)) % 180 for side in video.get('side_data_list', [])):
        aspect = 1 / aspect
    if aspect != Fraction(str(params['aspect']).split()[0].replace(':', '/')):
        raise ValueError(f'aspect: got {aspect}, expected {params["aspect"]}')
    fps = Fraction(video['avg_frame_rate'])
    duration = Fraction(video['duration'])
    expected = Fraction(params['duration_s'])
    if fps <= 0 or expected <= 0 or abs(duration - expected) > min(Fraction(1, 20), 1 / fps):
        raise ValueError(f'duration: got {float(duration):.3f}s, expected {expected}s')
    for key, actual in [('width', width), ('height', height), ('fps', fps)]:
        if key in params and Fraction(params[key]) != actual:
            raise ValueError(f'{key}: got {actual}, expected {params[key]}')
    run_media('ffmpeg', ['-nostdin', '-v', 'error', '-xerror', '-i', str(clip),
                         '-map', f'0:{video["index"]}', '-f', 'null', '-'])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--file', type=Path, required=True, help='CineForge results JSON array')
    parser.add_argument('--cineforge', default='cineforge')
    args = parser.parse_args()
    root = args.project.resolve()
    try:
        envelope = json.loads((root / 'jobs/S08_video.json').read_text(encoding='utf-8'))
        jobs = {job['job_id']: job for job in envelope['jobs']}
        payload = args.file.read_bytes()
        rows = json.loads(payload)
        if not isinstance(rows, list) or not rows:
            raise ValueError('results must be a nonempty JSON array')
        seen = set()
        for row in rows:
            job_id = row['job_id']
            if job_id in seen or jobs.get(job_id, {}).get('provider') != 'code-motion':
                raise ValueError(f'duplicate or non-code-motion job: {job_id}')
            seen.add(job_id)
            status = row['status']
            if status not in ('accepted', 'rejected', 'uncertain'):
                raise ValueError(f'{job_id}: invalid status')
            if status == 'accepted':
                path = Path(row['path'])
                if path.is_absolute() or '..' in path.parts or not (root / path).resolve().is_relative_to(root):
                    raise ValueError(f'{job_id}: expected project-relative output path')
                try:
                    check_clip(root / path, jobs[job_id]['params'])
                except (ValueError, KeyError, ZeroDivisionError) as exc:
                    raise ValueError(f'{job_id}: {exc}') from exc
        with TemporaryDirectory(prefix='code-motion-results-') as tmp:
            verified = Path(tmp) / 'results.json'
            verified.write_bytes(payload)
            return subprocess.run([args.cineforge, 'results', str(root), '--stage', 'S08_video',
                                   '--file', str(verified), '--runner', 'code-motion']).returncode
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f'code-motion submission refused: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
