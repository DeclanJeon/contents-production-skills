"""Drive actual public CLIs, including a real synthetic media render."""
import json
from pathlib import Path
import subprocess
import sys

from sequence_contract import read_projection
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


def test_shipped_shape_example_is_explicitly_unassigned():
    # Given
    example = SCRIPTS.parent / 'assets' / 'sequence-execution-example.json'
    # When
    projection = read_projection(example)
    # Then
    assert projection['owner']['artifact_id'] is None
    assert projection['cuts'][0]['source_asset_id'] is None
    assert projection['checks'] == []
