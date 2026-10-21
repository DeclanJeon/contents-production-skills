"""Parse observed OMP JSONL without promoting prose or requested paths to evidence."""
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re


def _local_path(value: str, root: Path):
    """Resolve reported paths only; preserve URIs and foreign Windows paths outside root."""
    if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', value) and not re.match(r'^[A-Za-z]:[\\/]', value):
        return None
    if PureWindowsPath(value).is_absolute() and not PureWindowsPath(str(root)).is_absolute():
        return None
    try:
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError, RuntimeError):
        return None


def parse_trace(wire_stdout: str, root: Path) -> dict:
    """Return evidence plus protocol errors; callers must reject any protocol errors.

    Result hashes use UTF-8 JSON with sorted keys, compact separators and unescaped
    Unicode. No filesystem content is read and no requested path certifies a source.
    """
    trace = {'final_text': '', 'reads': [], 'tool_errors': [],
             'protocol_errors': [], 'external_reads': [], 'agent_completed': False}
    errors = trace['protocol_errors']
    pending = {}
    seen_calls = set()
    final_seen = False
    for number, line in enumerate(wire_stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
        except (ValueError, RecursionError):
            errors.append(f'line {number}: malformed JSON')
            continue
        if not isinstance(event, dict) or not isinstance(event.get('type'), str):
            errors.append(f'line {number}: invalid event shape')
            continue
        kind = event['type']
        if trace['agent_completed']:
            if kind in ('tool_execution_start', 'tool_execution_end', 'message_end', 'agent_end'):
                errors.append(f'line {number}: {kind} after agent_end')
            continue
        if kind == 'agent_end':
            trace['agent_completed'] = True
        elif kind == 'tool_execution_start':
            call_id, name, args = event.get('toolCallId'), event.get('toolName'), event.get('args')
            if not isinstance(call_id, str) or not call_id or not isinstance(name, str) or not isinstance(args, dict):
                errors.append(f'line {number}: invalid tool start')
                continue
            if call_id in seen_calls:
                errors.append(f'line {number}: duplicate tool call {call_id}')
                continue
            seen_calls.add(call_id)
            pending[call_id] = (name, args)
        elif kind == 'tool_execution_end':
            call_id = event.get('toolCallId')
            if not isinstance(call_id, str):
                errors.append(f'line {number}: invalid tool end id')
                continue
            start = pending.pop(call_id, None)
            name = event.get('toolName')
            result = event.get('result')
            is_error = event.get('isError')
            if start is None:
                errors.append(f'line {number}: tool end without start {call_id}')
            if not isinstance(name, str) or not isinstance(result, dict) or not isinstance(is_error, bool):
                errors.append(f'line {number}: invalid tool end {call_id}')
                continue
            if start and start[0] != name:
                errors.append(f'line {number}: tool name mismatch {call_id}')
            if is_error:
                trace['tool_errors'].append({'tool_call_id': call_id, 'tool_name': name,
                                             'message': json.dumps(result, ensure_ascii=False, sort_keys=True)})
            if name != 'read':
                continue
            args = start[1] if start else {}
            requested = args.get('path')
            if not isinstance(requested, str):
                errors.append(f'line {number}: read missing requested path {call_id}')
                requested = None
            details = result.get('details')
            meta = details.get('meta') if isinstance(details, dict) else None
            source = meta.get('source') if isinstance(meta, dict) else None
            resolved = source.get('value') if isinstance(source, dict) else None
            confirmed = isinstance(resolved, str) and bool(resolved) and isinstance(source.get('type'), str)
            resolved = resolved if confirmed else None
            local = _local_path(resolved, root) if confirmed else None
            canonical = json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
            record = {'tool_call_id': call_id, 'requested_path': requested,
                      'resolved_path': resolved, 'local_path': local,
                      'success': not is_error, 'source_confirmed': confirmed,
                      'result_sha256': hashlib.sha256(canonical.encode('utf-8')).hexdigest()}
            trace['reads'].append(record)
            if record['success'] and confirmed and local is None:
                trace['external_reads'].append(record.copy())
        elif kind == 'message_end':
            message = event.get('message')
            if not isinstance(message, dict):
                errors.append(f'line {number}: invalid message_end')
                continue
            if message.get('role') != 'assistant':
                continue
            content = message.get('content')
            if not isinstance(content, list) or any(not isinstance(item, dict) for item in content):
                errors.append(f'line {number}: invalid assistant content')
                continue
            if message.get('stopReason') != 'stop' or any(item.get('type') in ('toolCall', 'toolUse', 'tool_use') for item in content):
                continue
            text = [item.get('text') for item in content if item.get('type') == 'text']
            if any(not isinstance(part, str) for part in text):
                errors.append(f'line {number}: invalid assistant text')
                continue
            answer = '\n'.join(text)
            if answer.strip():
                trace['final_text'] = answer
                final_seen = True
        # Session, turn, progress and delta events do not supply evidence.
    if pending:
        errors.append('unfinished tool calls: ' + ', '.join(sorted(pending)))
    if not trace['agent_completed']:
        errors.append('missing agent_end')
    if not final_seen:
        errors.append('missing completed assistant final text')
    return trace
