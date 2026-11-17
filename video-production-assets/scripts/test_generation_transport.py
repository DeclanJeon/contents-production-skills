"""Native adapter and explicit-schema transport cases; no external calls."""
import json
import pytest
from av_handoff_test_fixture import prepared_handoff, rewrite_document
from generation_transport import inspect_transport
from sequence_contract import SequenceError, file_hash


def prepared_explicit(root):
    p, q = prepared_handoff(root)
    h = q['generation_handoff']; h.update(adapter='explicit', tool='mcp__example__generate', adapter_artifact_id='ADAPTER')
    path = root / 'explicit-schema.json'
    path.write_text(json.dumps({'input_schema': {'type': 'object', 'properties': {
        'medias': {'type': 'array', 'items': {'properties': {'value': {'type': 'string'},
                    'role': {'type': 'string', 'enum': ['reference', 'voice_timbre', 'first_frame']}}}},
        'model': {'type': 'string'}, 'prompt': {'type': 'string'},
        'audio_policy': {'type': 'string', 'enum': ['prompt_only', 'no_audio']}}}}))
    p['asset_registry'].append({'id': 'SCHEMA', 'version': '1', 'kind': 'document', 'status': 'available', 'path': path.name, 'sha256': file_hash(path)})
    q['inputs']['assets']['SCHEMA'] = {'version': '1', 'sha256': file_hash(path)}
    descriptor = {'tool': h['tool'], 'schema_asset_id': 'SCHEMA', 'schema_root_pointer': '/input_schema',
        'request_root_pointer': '/params', 'selection_field': 'medias', 'value_field': 'value', 'role_field': 'role',
        'prompt_pointer': '/prompt', 'model_pointer': '/model', 'model': 'fixture-model',
        'audio_policy_pointer': '/audio_policy', 'audio_policy_values': {'audio': 'prompt_only', 'no_audio': 'no_audio'},
        'readiness_tool': 'mcp__example__list_media', 'readiness_items_pointer': '/result/structuredContent/items',
        'readiness_id_field': 'id', 'readiness_asset_field': 'asset_id',
        'readiness_state_field': 'state', 'readiness_ready_value': 'ready'}
    p['artifacts'].append({'id': 'ADAPTER', 'type': 'generation_spec', 'version': '1', 'status': 'verified',
        'asset_ids': ['SCHEMA'], 'evidence': 'synthetic current descriptor', 'dependencies': [], 'dependency_versions': {},
        'reference_adapter': descriptor})
    q['inputs']['artifact_versions']['ADAPTER'] = '1'
    request = {'params': {'medias': [{'value': b['native_reference_id'], 'role': b['role']} for b in h['bindings']],
        'model': 'fixture-model', 'audio_policy': 'prompt_only',
        'prompt': 'synthetic required direction\n' + '\n'.join(b['request_clause'] for b in h['bindings'])}}
    rewrite_document(p, q, root, 'REQUEST', lambda d: (d.clear(), d.update(request)))
    rewrite_document(p, q, root, 'REFS', lambda d: d.update(tool=descriptor['readiness_tool']))
    return p, q, request


def test_explicit_adapter_consumes_actual_array_values_and_roles(tmp_path):
    # Given
    p, q, request = prepared_explicit(tmp_path)
    # When
    bound = inspect_transport(p, q, request, tmp_path)
    # Then
    assert [b.native_reference_id for b in bound] == [r['value'] for r in request['params']['medias']]


@pytest.mark.parametrize('field,value,code', [
    ('prompt', 'missing binding instructions', 'reference_clause'),
    ('model', 'another-model', 'transport_model'),
    ('audio_policy', 'no_audio', 'audio_policy'),
    ('medias', [], 'reference_selection'),
])
def test_explicit_payload_cannot_change_verified_intent(tmp_path, field, value, code):
    # Given
    p, q, request = prepared_explicit(tmp_path); request['params'][field] = value
    # When / Then
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == code


def test_readiness_snapshot_must_come_from_declared_native_tool(tmp_path):
    # Given
    p, q, request = prepared_explicit(tmp_path)
    rewrite_document(p, q, tmp_path, 'REFS', lambda d: d.update(tool='mcp__other__list'))
    # When / Then
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'native_snapshot'


def test_archived_native_media_cannot_pass_generic_readiness(tmp_path):
    # Given
    p, q, request = prepared_explicit(tmp_path)
    rewrite_document(p, q, tmp_path, 'REFS', lambda d: d['result']['structuredContent']['items'][0].update(asset_archived=True))
    # When / Then
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'reference_readiness'


@pytest.mark.parametrize('field', [
    'readiness_id_field', 'readiness_asset_field', 'readiness_state_field',
    'readiness_ready_value',
])
@pytest.mark.parametrize('value', [None, ''])
def test_explicit_adapter_requires_complete_readiness_contract(tmp_path, field, value):
    # Given: omission must not turn row.get(None) == None into readiness.
    p, q, request = prepared_explicit(tmp_path)
    descriptor = next(a for a in p['artifacts'] if a['id'] == 'ADAPTER')['reference_adapter']
    descriptor[field] = value
    # When / Then
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'transport_adapter'


def test_missing_readiness_configuration_cannot_accept_pending_media(tmp_path):
    p, q, request = prepared_explicit(tmp_path)
    descriptor = next(a for a in p['artifacts'] if a['id'] == 'ADAPTER')['reference_adapter']
    descriptor.pop('readiness_state_field')
    descriptor.pop('readiness_ready_value')
    rewrite_document(p, q, tmp_path, 'REFS', lambda d: d['result']['structuredContent']['items'][0].update(state='pending'))
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'transport_adapter'


@pytest.mark.parametrize('field,value', [('state', 'pending'), ('asset_id', 'wrong-upload')])
def test_explicit_readiness_requires_ready_state_and_matching_uploaded_asset(tmp_path, field, value):
    p, q, request = prepared_explicit(tmp_path)
    rewrite_document(p, q, tmp_path, 'REFS', lambda d: d['result']['structuredContent']['items'][0].update({field: value}))
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'reference_readiness'


def test_unverified_adapter_is_not_an_execution_shortcut(tmp_path):
    # Given
    p, q, request = prepared_explicit(tmp_path)
    next(a for a in p['artifacts'] if a['id'] == 'ADAPTER')['status'] = 'draft'
    # When / Then
    with pytest.raises(SequenceError) as error:
        inspect_transport(p, q, request, tmp_path)
    assert error.value.code == 'transport_adapter'
