"""Drive actual public CLIs, including a real synthetic media render."""
import json
from pathlib import Path
import subprocess
import sys

from sequence_contract import read_projection
import pytest
import hashlib
from sequence_test_fixture import prepared_plan
from test_sequence_media import prepared_edit

SCRIPTS = Path(__file__).resolve().parent


def cli(name, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True, check=False, timeout=30)


def test_context_and_plan_gate_cli_round_trip(tmp_path):
    # Given
    p, q = prepared_plan(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'sequence.json'; projection.write_text(json.dumps(q))
    # When
    context = cli('sequence_context.py', project, '--shot', 'SH02', '--projection', projection)
    gate = cli('validate_sequence.py', project, projection, '--phase', 'plan')
    # Then
    assert context.returncode == 0, context.stderr
    assert json.loads(context.stdout)['focus']['shot_ids'] == ['SH02']
    assert gate.returncode == 0, gate.stdout
    assert json.loads(gate.stdout)['execution_authorized'] is False


def test_renderer_cli_outputs_real_manifest_then_rejects_overwrite(tmp_path):
    # Given
    p, q = prepared_edit(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'edit.json'; projection.write_text(json.dumps(q))
    # When
    result = cli('render_sequence.py', project, projection, '--output', 'output-v1')
    refused = cli('render_sequence.py', project, projection, '--output', 'output-v1')
    # Then
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report['probe']['frame_count'] == 96
    assert (tmp_path / report['manifest_path']).is_file()
    assert refused.returncode == 2
    assert json.loads(refused.stdout)['status'] == 'failed'


def test_focus_cli_uses_same_snapshot_and_preserves_full_default(tmp_path):
    p, q = prepared_plan(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'sequence.json'; projection.write_text(json.dumps(q))
    default = cli('sequence_context.py', project, '--shot', 'SH02', '--projection', projection)
    explicit = cli('sequence_context.py', project, '--shot', 'SH02', '--projection', projection, '--view', 'full')
    focused = cli('sequence_context.py', project, '--shot', 'SH02', '--projection', projection, '--view', 'focus')
    assert default.returncode == explicit.returncode == focused.returncode == 0
    assert json.loads(default.stdout) == json.loads(explicit.stdout)
    result = json.loads(focused.stdout)
    assert result['format'] == 'sequence-focus-view/1'
    assert result['source']['project_snapshot']['sha256'] == hashlib.sha256(project.read_bytes()).hexdigest()
    assert result['source']['projection_snapshot']['sha256'] == hashlib.sha256(projection.read_bytes()).hexdigest()


@pytest.mark.parametrize('flags', [[], ['--all'], ['--all', '--shot', 'SH02']])
def test_focus_cli_requires_explicit_shot_and_rejects_all(tmp_path, flags):
    p, _ = prepared_plan(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    result = cli('sequence_context.py', project, '--view', 'focus', *flags)
    assert result.returncode == 2


@pytest.mark.parametrize('script,flags', [
    ('prepare_generation_request.py', []),
    ('validate_sequence.py', ['--phase', 'generation']),
    ('render_sequence.py', ['--output', 'must-not-exist']),
    ('inspect_sequence_frames.py', ['--output', 'must-not-exist']),
])
def test_execution_consumers_reject_focus_view(tmp_path, script, flags):
    from sequence_view import build_sequence_focus_view
    p, _ = prepared_plan(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'display.json'; projection.write_text(json.dumps(build_sequence_focus_view(p, ['SH02'])))
    result = cli(script, project, projection, *flags)
    assert result.returncode != 0
    assert 'projection_format' in result.stdout, result.stderr
    assert not (tmp_path / 'must-not-exist').exists()


def test_focus_cli_malformed_stored_scope_returns_json_not_traceback(tmp_path):
    p, q = prepared_plan(tmp_path)
    q['focus']['shot_ids'] = None; q['generation_handoff'] = {'bindings':[]}
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'sequence.json'; projection.write_text(json.dumps(q))
    result = cli('sequence_context.py', project, '--shot', 'SH02', '--projection', projection, '--view', 'focus')
    assert result.returncode == 2
    assert 'focus/shot_ids' in json.loads(result.stdout)['error']
    assert 'Traceback' not in result.stderr


def test_shipped_shape_example_is_explicitly_unassigned():
    # Given
    example = SCRIPTS.parent / 'assets' / 'sequence-execution-example.json'
    # When
    projection = read_projection(example)
    # Then
    assert projection['owner']['artifact_id'] is None
    assert projection['cuts'][0]['source_asset_id'] is None
    assert projection['checks'] == []
