#!/usr/bin/env python3
"""Prepare an exact checked MCP call or audit its recorded invocation; never send it."""
from __future__ import annotations

import argparse
from collections.abc import Mapping
import copy
import hashlib
import json
from pathlib import Path

from generation_transport import pinned_document
from sequence_contract import Document, Json, SequenceError, read_document, read_projection
from validate_sequence import validate_sequence


def _digest(value: Json) -> str:
    """Canonical JSON makes key/whitespace changes irrelevant, not input changes."""
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise SequenceError('packet_json', 'arguments', 'finite JSON values required') from exc
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def prepare_request(project: Mapping[str, Json], projection: Mapping[str, Json], root: Path) -> Document:
    """Return unchanged checked native arguments with a current provenance snapshot."""
    result = validate_sequence(project, projection, 'generation', root)
    if not result['ready']:
        raise SequenceError('generation_blocked', 'generation', json.dumps(result['blockers'], ensure_ascii=False))
    request_id = projection.get('submission_asset_id')
    request = pinned_document(project, projection, root, request_id)
    tool = projection['generation_handoff']['tool']
    call = {'tool': tool, 'arguments': copy.deepcopy(request)}
    return {'format': 'sequence-generation-call/1', 'tool': tool, 'arguments': call['arguments'],
            'request_asset_id': request_id, 'request_sha256': projection['inputs']['assets'][request_id]['sha256'],
            'call_sha256': _digest(call), 'owner': copy.deepcopy(projection['owner']),
            'inputs': copy.deepcopy(projection['inputs']), 'submitted': False,
            'provider_conditioning': 'not_verified', 'quality': 'unverified',
            'limits': 'Prepared local call only. Coordinator must use this exact tool/arguments and record actual invocation; no job/upload/network occurs here.'}


def audit_call(packet: Mapping[str, Json], actual_call: Mapping[str, Json]) -> Document:
    """Compare a frozen packet with an actual-call record without resubmission."""
    if (packet.get('format') != 'sequence-generation-call/1' or not isinstance(packet.get('tool'), str)
            or not isinstance(packet.get('arguments'), dict)):
        raise SequenceError('prepared_packet', 'packet', 'versioned prepared tool/arguments required')
    expected = {'tool': packet['tool'], 'arguments': packet['arguments']}
    if packet.get('call_sha256') != _digest(expected):
        raise SequenceError('prepared_packet', 'call_sha256', 'prepared call changed after validation')
    actual = {'tool': actual_call.get('tool'), 'arguments': actual_call.get('arguments')}
    if _digest(actual) != packet['call_sha256']:
        raise SequenceError('actual_call_mismatch', 'tool/arguments', 'actual MCP invocation differs from prepared references/body/settings')
    match actual_call.get('transport_status', 'unknown'):
        case 'returned':
            response = actual_call.get('response')
            if not isinstance(response, dict):
                raise SequenceError('actual_call_record', 'response', 'returned status needs the actual native response')
            state = 'failed' if response.get('isError') is True else 'returned'
        case 'timeout' | 'unknown':
            state = 'unknown'
        case _:
            raise SequenceError('actual_call_record', 'transport_status', 'expected returned/timeout/unknown')
    return {'arguments_match': True, 'call_sha256': packet['call_sha256'],
            'submission_state': state, 'provider_conditioning': 'not_verified',
            'quality': 'unverified', 'resubmit_allowed': False,
            'limits': 'Audits the supplied client invocation record, not its authenticity, backend conditioning, generation success or perceptual quality. Unknown outcomes must be reconciled, not resubmitted.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, nargs='?')
    parser.add_argument('projection', type=Path, nargs='?')
    parser.add_argument('--prepared-packet', type=Path)
    parser.add_argument('--audit-call', type=Path)
    args = parser.parse_args()
    try:
        if args.audit_call is not None:
            if args.prepared_packet is None or args.project is not None or args.projection is not None:
                parser.error('audit needs --prepared-packet and --audit-call, without project/projection')
            result = audit_call(read_document(args.prepared_packet), read_document(args.audit_call))
        else:
            if args.project is None or args.projection is None or args.prepared_packet is not None:
                parser.error('prepare needs project.json and projection.json')
            result = prepare_request(read_document(args.project), read_projection(args.projection), args.project.resolve().parent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (SequenceError, OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc), 'submission_state': 'unknown', 'resubmit_allowed': False}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
