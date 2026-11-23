"""Exercise the skill-pack gate with actual MP4s, without writing CineForge receipts."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).with_name('submit_code_motion.py')
JOB = 'video:S01C01'
pytestmark = pytest.mark.skipif(not all(shutil.which(t) for t in ('ffmpeg', 'ffprobe')), reason='FFmpeg needed')


@pytest.mark.parametrize(('size', 'seconds', 'error'), [
    ('90x160', '1', ''), ('160x90', '1', 'aspect'), ('90x160', '2', 'duration'),
    ('invalid', '1', 'ffprobe'),
])
def test_submit_gate(tmp_path: Path, size: str, seconds: str, error: str) -> None:
    clip = tmp_path / 'cut.mp4'
    if size == 'invalid':
        clip.write_text('not a video')
    else:
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', f'color=s={size}:r=30',
                        '-t', seconds, '-c:v', 'libx264', str(clip)], check=True)
    jobs = tmp_path / 'jobs'
    jobs.mkdir()
    (jobs / 'S08_video.json').write_text(json.dumps({'jobs': [{'job_id': JOB, 'provider': 'code-motion',
        'params': {'duration_s': '1', 'aspect': '9:16'}}]}))
    rows = [{'job_id': JOB, 'status': 'accepted', 'path': clip.name}]
    results = tmp_path / 'results.json'
    results.write_text(json.dumps(rows))
    marker = tmp_path / 'forwarded.json'
    receiver = tmp_path / 'cineforge'
    receiver.write_text(f'#!{sys.executable}\nfrom pathlib import Path\nimport sys\n'
                        f'Path({str(marker)!r}).write_bytes(Path(sys.argv[sys.argv.index("--file") + 1]).read_bytes())\n')
    receiver.chmod(0o755)
    run = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path), '--file', str(results),
                          '--cineforge', str(receiver)], capture_output=True, text=True)
    if error:
        assert error in run.stderr
        assert run.returncode != 0
        assert not marker.exists()
    else:
        assert run.returncode == 0, run.stderr
        assert json.loads(marker.read_text()) == rows
