"""Inspect native wire reference selection, not provider conditioning or consent."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from collections.abc import Mapping
from pathlib import Path
from typing import Final, assert_never
from uuid import UUID

from sequence_contract import Document, Json, SequenceError, checked_assets, read_document, table


class Modality(StrEnum):
    VIDEO = 'video'
    AUDIO = 'audio'
    IMAGE = 'image'


@dataclass(frozen=True, slots=True)
class BoundReference:
    key: str
    reference_asset_id: str
    modality: Modality
    purpose: str
    native_reference_id: str
    native_asset_id: str
    role: str
    source_cut_id: str | None
    voice_artifact_id: str | None
    imports: tuple[str, ...]
    excludes: tuple[str, ...]
    request_clause: str


LUDYTE_ROLES: Final = frozenset(('reference', 'identity', 'costume', 'prop', 'scene', 'color_look',
    'motion', 'camera', 'edit_source', 'first_frame', 'last_frame', 'typography',
    'voice_timbre', 'audio_reuse', 'background_music', 'storyboard'))


def pinned_document(project: Mapping[str, Json], q: Mapping[str, Json], root: Path,
                    asset_id: str) -> Document:
    """Use only a current registered file in the explicit project root."""
    if not isinstance(asset_id, str):
        raise SequenceError('handoff_evidence', 'asset_id', 'registered snapshot required')
    assets = table(project, 'asset_registry')
    pin = q.get('inputs', {}).get('assets', {}).get(asset_id)
    row = assets.get(asset_id)
    if not isinstance(pin, dict) or row is None or pin.get('version') != row.get('version') or pin.get('sha256') != row.get('sha256'):
        raise SequenceError('handoff_evidence', asset_id, 'current version/hash pin required')
    return read_document(checked_assets(project, root, [asset_id])[asset_id])


def _binding(row: Document) -> BoundReference:
    strings = ('key', 'reference_asset_id', 'modality', 'purpose', 'native_reference_id', 'native_asset_id', 'role', 'request_clause')
    if any(not isinstance(row.get(k), str) or not row[k] for k in strings):
        raise SequenceError('reference_shape', 'bindings', 'nonempty identity/role/modality fields required')
    try:
        modality = Modality(row['modality'])
    except ValueError as exc:
        raise SequenceError('reference_shape', row['key'], 'unknown modality') from exc
    for name in ('imports', 'excludes'):
        if not isinstance(row.get(name), list) or not row[name] or not all(isinstance(s, str) and s for s in row[name]):
            raise SequenceError('reference_attributes', row['key'], 'attribute imports/excludes required')
    for name in ('source_cut_id', 'voice_artifact_id'):
        if row.get(name) is not None and not isinstance(row[name], str):
            raise SequenceError('reference_shape', row['key'], 'optional identifiers must be strings')
    return BoundReference(*(row[k] for k in ('key', 'reference_asset_id')), modality,
        *(row[k] for k in ('purpose', 'native_reference_id', 'native_asset_id', 'role')),
        row.get('source_cut_id'), row.get('voice_artifact_id'), tuple(row['imports']), tuple(row['excludes']), row['request_clause'])


def _uuid(value: str) -> None:
    try:
        UUID(value)
    except (ValueError, AttributeError) as exc:
        raise SequenceError('native_id', str(value), 'Ludyte uses UUID reference/asset identifiers') from exc


def _body(value: Document) -> Document:
    if value.get('isError'):
        raise SequenceError('native_snapshot', 'result', 'snapshot records a native error')
    result = value.get('structuredContent', value)
    if not isinstance(result, dict):
        raise SequenceError('native_snapshot', 'result', 'expected structured response')
    return result


def _uploads(project, q, root, h: Document, bindings: tuple[BoundReference, ...]) -> None:
    evidence = pinned_document(project, q, root, h.get('uploads_asset_id'))
    rows = evidence.get('records')
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise SequenceError('upload_binding', 'uploads', 'actual local/native correlation records required')
    assets = table(project, 'asset_registry')
    for b in bindings:
        asset = assets.get(b.reference_asset_id)
        if asset is None:
            raise SequenceError('upload_binding', b.key, 'unknown local input')
        checked_assets(project, root, [b.reference_asset_id])
        pin = q['inputs']['assets'].get(b.reference_asset_id)
        if not isinstance(pin, dict) or pin.get('version') != asset['version'] or pin.get('sha256') != asset['sha256']:
            raise SequenceError('upload_binding', b.key, 'local reference is not pinned')
        matches = [r for r in rows if r.get('reference_asset_id') == b.reference_asset_id
                   and r.get('native_reference_id') == b.native_reference_id]
        if len(matches) != 1:
            raise SequenceError('upload_binding', b.key, 'one exact upload receipt is required')
        r = matches[0]
        status = r.get('put_status')
        if (r.get('sha256') != asset['sha256'] or r.get('native_asset_id') != b.native_asset_id or
                r.get('status') != 'confirmed' or type(status) is not int or not 200 <= status < 300):
            raise SequenceError('upload_binding', b.key, 'confirmed local bytes do not match native input')


def _ludyte(project, q, request: Document, root, h: Document,
            bindings: tuple[BoundReference, ...]) -> None:
    if h.get('tool') != 'mcp__Ludyte__send_message':
        raise SequenceError('transport_tool', 'tool', 'wrong native sender')
    capability = _body(pinned_document(project, q, root, h.get('contract_asset_id')))
    props = capability.get('message_input_schema', {}).get('properties', {})
    ref_schema = props.get('reference_ids', {})
    if capability.get('capability_id') != 'ludyte.task-agent' or capability.get('contract_version') != '1.14.0' or ref_schema.get('type') != 'array':
        raise SequenceError('transport_contract', 'contract', 'verified supported Ludyte grammar required')
    message = request.get('message')
    if not isinstance(message, dict):
        raise SequenceError('reference_selection', 'message', 'native message object required')
    text = message.get('text')
    if not isinstance(text, str) or any(b.request_clause not in text for b in bindings):
        raise SequenceError('reference_clause', 'message.text', 'reference attributes must reach actual prompt text')
    selected = message.get('reference_ids')
    expected = [b.native_reference_id for b in bindings]
    if not isinstance(selected, list) or not selected or selected != expected or len(set(selected)) != len(selected):
        raise SequenceError('reference_selection', 'message.reference_ids', 'explicit ordered Task reference ids required; no inherited/empty selection')
    if len(selected) > ref_schema.get('maxItems', 12):
        raise SequenceError('reference_capacity', 'reference_ids', 'native reference limit exceeded')
    if message.get('video_model_selection') not in props.get('video_model_selection', {}).get('enum', []):
        raise SequenceError('transport_model', 'video_model_selection', 'model not in inspected contract')
    expected_audio = 'no_audio' if project.get('audio_mode') == 'no_audio' else 'prompt_only'
    if message.get('audio_policy') != expected_audio:
        raise SequenceError('audio_policy', 'message.audio_policy', 'explicit audio mode required')
    session = pinned_document(project, q, root, h.get('session_snapshot_asset_id'))
    refs = pinned_document(project, q, root, h.get('references_snapshot_asset_id'))
    sid = request.get('session_id')
    if not isinstance(sid, str):
        raise SequenceError('session_binding', 'session_id', 'native session required')
    _uuid(sid)
    for snapshot, tool in ((session, 'mcp__Ludyte__get_session'), (refs, 'mcp__Ludyte__get_session_assets')):
        if snapshot.get('tool') != tool or snapshot.get('arguments', {}).get('session_id') != sid:
            raise SequenceError('session_binding', tool, 'snapshot belongs to a different call/session')
    current = _body(session.get('result', {}))
    if current.get('session_id') != sid:
        raise SequenceError('session_binding', 'session response', 'wrong native session')
    revision = current.get('revision')
    if type(revision) is not int or type(request.get('expected_revision')) is not int or request['expected_revision'] != revision:
        raise SequenceError('session_revision', 'expected_revision', 'refresh current session after attachments')
    listed = _body(refs.get('result', {}))
    if listed.get('next_cursor'):
        raise SequenceError('reference_pagination', 'get_session_assets', 'resolve remaining pages before preparing')
    items = listed.get('items')
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        raise SequenceError('reference_readiness', 'items', 'actual native references required')
    for b in bindings:
        _uuid(b.native_reference_id); _uuid(b.native_asset_id)
        matches = [r for r in items if r.get('id') == b.native_reference_id]
        if len(matches) != 1:
            raise SequenceError('reference_readiness', b.key, 'selected Task reference absent/ambiguous')
        row = matches[0]
        if row.get('asset_id') != b.native_asset_id or row.get('state') != 'ready' or row.get('asset_archived') or row.get('model_requirement') != 'required':
            raise SequenceError('reference_readiness', b.key, 'reference must be ready, non-archived and required')
        if b.role not in LUDYTE_ROLES or row.get('role') != b.role or row.get('kind') != b.modality.value:
            raise SequenceError('reference_role', b.key, 'native role/modality differs from planned binding')


def pointer(value: Json, path: str) -> Json:
    """Resolve JSONPointer without eval, fallback search, or matching text IDs."""
    if not isinstance(path, str) or path and not path.startswith('/'):
        raise SequenceError('adapter_pointer', str(path), 'expected JSONPointer')
    for token in path.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict) and token in value:
            value = value[token]
        elif isinstance(value, list) and token.isdecimal() and int(token) < len(value):
            value = value[int(token)]
        else:
            raise SequenceError('adapter_pointer', path, 'native field absent')
    return value


def _explicit(project, q, request: Document, root, h: Document,
              bindings: tuple[BoundReference, ...]) -> None:
    aid = h.get('adapter_artifact_id')
    artifact = table(project, 'artifacts').get(aid) if isinstance(aid, str) else None
    if (artifact is None or artifact.get('status') not in ('verified', 'approved') or
            q['inputs']['artifact_versions'].get(aid) != artifact['version'] or not artifact.get('evidence', artifact.get('approval'))):
        raise SequenceError('transport_adapter', 'adapter_artifact_id', 'verified current native adapter artifact required')
    d = artifact.get('reference_adapter')
    if not isinstance(d, dict) or not d.get('tool') or h.get('tool') != d['tool']:
        raise SequenceError('transport_adapter', str(aid), 'native descriptor/tool mismatch')
    required_readiness = ('readiness_tool', 'readiness_items_pointer', 'readiness_id_field',
                          'readiness_asset_field', 'readiness_state_field', 'readiness_ready_value')
    if any(not isinstance(d.get(key), str) or not d[key] for key in required_readiness):
        raise SequenceError('transport_adapter', str(aid), 'complete nonempty native readiness and asset correlation fields required')
    contract = pinned_document(project, q, root, d.get('schema_asset_id'))
    schema = pointer(contract, d.get('schema_root_pointer'))
    body = pointer(request, d.get('request_root_pointer'))
    if not isinstance(schema, dict) or not isinstance(body, dict):
        raise SequenceError('transport_contract', str(aid), 'native request/schema object required')
    field, value_field, role_field = (d.get(k) for k in ('selection_field', 'value_field', 'role_field'))
    if not all(isinstance(k, str) for k in (field, value_field, role_field)):
        raise SequenceError('transport_contract', str(aid), 'declared native selection fields required')
    selection_schema = schema.get('properties', {}).get(field, {})
    items_schema = selection_schema.get('items', {}).get('properties', {})
    roles = items_schema.get(role_field, {}).get('enum')
    if selection_schema.get('type') != 'array' or items_schema.get(value_field, {}).get('type') != 'string' or not isinstance(roles, list):
        raise SequenceError('transport_contract', field, 'inspected native array/id/role grammar required')
    prompt = pointer(body, d.get('prompt_pointer'))
    if not isinstance(prompt, str) or any(b.request_clause not in prompt for b in bindings):
        raise SequenceError('reference_clause', str(aid), 'reference instructions absent from native prompt')
    if not isinstance(d.get('model'), str) or pointer(body, d.get('model_pointer')) != d['model']:
        raise SequenceError('transport_model', str(aid), 'native request differs from verified adapter model')
    values = d.get('audio_policy_values')
    mode = 'no_audio' if project.get('audio_mode') == 'no_audio' else 'audio'
    if not isinstance(values, dict) or mode not in values:
        raise SequenceError('audio_policy', str(aid), 'verified explicit native audio behavior required')
    actual_audio = pointer(body, d.get('audio_policy_pointer'))
    if type(actual_audio) is not type(values[mode]) or actual_audio != values[mode]:
        raise SequenceError('audio_policy', str(aid), 'native audio mode differs from project')
    selected = body.get(field)
    expected = [{value_field: b.native_reference_id, role_field: b.role} for b in bindings]
    if not isinstance(selected, list) or not selected or selected != expected or any(b.role not in roles for b in bindings):
        raise SequenceError('reference_selection', field, 'actual native selected values/roles differ')
    ready = pinned_document(project, q, root, h.get('references_snapshot_asset_id'))
    if not isinstance(d.get('readiness_tool'), str) or ready.get('tool') != d['readiness_tool']:
        raise SequenceError('native_snapshot', str(aid), 'readiness must come from declared native tool')
    _body(ready.get('result', {}))
    rows = pointer(ready, d.get('readiness_items_pointer'))
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise SequenceError('reference_readiness', field, 'native readiness array required')
    for b in bindings:
        found = [r for r in rows if r.get(d.get('readiness_id_field')) == b.native_reference_id]
        if len(found) != 1 or found[0].get(d.get('readiness_state_field')) != d.get('readiness_ready_value'):
            raise SequenceError('reference_readiness', b.key, 'native media not confirmed ready')
        if found[0].get('asset_archived') or found[0].get('model_requirement', 'required') != 'required':
            raise SequenceError('reference_readiness', b.key, 'archived or candidate media cannot condition production')
        asset_field = d.get('readiness_asset_field')
        if found[0].get(asset_field) != b.native_asset_id:
            raise SequenceError('reference_readiness', b.key, 'wrong native uploaded asset')


def inspect_transport(project: Mapping[str, Json], q: Mapping[str, Json], request: Document,
                      root: Path) -> tuple[BoundReference, ...]:
    """Require a concrete supported sender and verified actual input bindings."""
    h = q.get('generation_handoff')
    if not isinstance(h, dict):
        raise SequenceError('generation_handoff', 'generation_handoff', 'actual AV reference package required')
    rows = h.get('bindings')
    if not isinstance(rows, list) or not rows or not all(isinstance(b, dict) for b in rows):
        raise SequenceError('reference_shape', 'bindings', 'explicit reference bindings required')
    bindings = tuple(_binding(row) for row in rows)
    if len({b.key for b in bindings}) != len(bindings):
        raise SequenceError('reference_shape', 'bindings', 'duplicate binding key')
    _uploads(project, q, root, h, bindings)
    match h.get('adapter'):
        case 'ludyte':
            _ludyte(project, q, request, root, h, bindings)
        case 'explicit':
            _explicit(project, q, request, root, h, bindings)
        case _:
            raise SequenceError('transport_adapter', 'adapter', 'unknown transport must not silently submit')
    return bindings
