"""Prepare/audit are local operations: these tests never submit an MCP job."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest
from av_handoff_test_fixture import prepared_handoff
from sequence_contract import SequenceError, file_hash
from prepare_generation_request import prepare_request, audit_call


def test_prepare_returns_exact_checked_arguments_without_submission(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    before = {a['id']: file_hash(tmp_path / a['path']) for a in p['asset_registry']}
    # When
    packet = prepare_request(p, q, tmp_path)
    # Then
    assert packet['tool'] == 'mcp__Ludyte__send_message'
    assert packet['arguments'] == json.loads((tmp_path / 'request.json').read_text())
    assert packet['submitted'] is False
    assert packet['provider_conditioning'] == 'not_verified'
    assert all(file_hash(tmp_path / a['path']) == before[a['id']] for a in p['asset_registry'])


def test_incomplete_reference_selection_has_no_dispatch_packet(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); q['generation_handoff']['bindings'].pop(0)
    # When / Then
    with pytest.raises(SequenceError) as error:
        prepare_request(p, q, tmp_path)
    assert error.value.code == 'generation_blocked'


@pytest.mark.parametrize('change', [
    lambda call: call['arguments']['message'].update(reference_ids=[]),
    lambda call: call['arguments']['message'].update(text='different body'),
    lambda call: call.update(tool='mcp__other__generate'),
    lambda call: call['arguments'].update(expected_revision=7.0),
])
def test_audit_detects_changed_actual_inputs(tmp_path, change):
    # Given
    p, q = prepared_handoff(tmp_path); packet = prepare_request(p, q, tmp_path)
    call = {'tool': packet['tool'], 'arguments': copy.deepcopy(packet['arguments']),
            'transport_status': 'returned', 'response': {'isError': False}}
    change(call)
    # When / Then
    with pytest.raises(SequenceError) as error:
        audit_call(packet, call)
    assert error.value.code == 'actual_call_mismatch'


@pytest.mark.parametrize('status,state', [('returned', 'returned'), ('timeout', 'unknown'), ('unknown', 'unknown')])
def test_audit_separates_transport_from_generation_success(tmp_path, status, state):
    # Given
    p, q = prepared_handoff(tmp_path); packet = prepare_request(p, q, tmp_path)
    call = {'tool': packet['tool'], 'arguments': packet['arguments'], 'transport_status': status,
            'response': {'isError': False, 'structuredContent': {'status': 'running'}}}
    # When
    result = audit_call(packet, call)
    # Then
    assert result['arguments_match'] is True
    assert result['submission_state'] == state
    assert result['provider_conditioning'] == 'not_verified'
    assert result['resubmit_allowed'] is False


def test_prepared_packet_cannot_be_changed_to_match_a_different_call(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); packet = prepare_request(p, q, tmp_path)
    packet['arguments']['message']['reference_ids'] = []
    call = {'tool': packet['tool'], 'arguments': packet['arguments']}
    # When / Then
    with pytest.raises(SequenceError) as error:
        audit_call(packet, call)
    assert error.value.code == 'prepared_packet'


def test_actual_native_error_is_not_a_successful_submission(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path); packet = prepare_request(p, q, tmp_path)
    call = {'tool': packet['tool'], 'arguments': packet['arguments'], 'transport_status': 'returned',
            'response': {'isError': True}}
    # When
    result = audit_call(packet, call)
    # Then
    assert result['submission_state'] == 'failed'
    assert result['resubmit_allowed'] is False


def test_cli_prepare_and_audit_round_trip(tmp_path):
    # Given
    p, q = prepared_handoff(tmp_path)
    project = tmp_path / 'project.json'; project.write_text(json.dumps(p))
    projection = tmp_path / 'sequence.json'; projection.write_text(json.dumps(q))
    script = Path(__file__).with_name('prepare_generation_request.py')
    # When
    prepared = subprocess.run([sys.executable, str(script), str(project), str(projection)], capture_output=True, text=True, check=False)
    # Then
    assert prepared.returncode == 0, prepared.stdout + prepared.stderr
    packet = json.loads(prepared.stdout)
    packet_file = tmp_path / 'packet.json'; packet_file.write_text(prepared.stdout)
    call = tmp_path / 'call.json'; call.write_text(json.dumps({'tool': packet['tool'], 'arguments': packet['arguments'],
        'transport_status': 'timeout'}))
    audited = subprocess.run([sys.executable, str(script), '--prepared-packet', str(packet_file), '--audit-call', str(call)], capture_output=True, text=True, check=False)
    assert audited.returncode == 0, audited.stdout + audited.stderr
    assert json.loads(audited.stdout)['submission_state'] == 'unknown'
