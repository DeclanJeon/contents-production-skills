"""Optional checks of supplied reference records, not legal/media/provider verification.

These pure helpers never browse, upload, generate, listen, solve a camera or mutate a
project. Preserve native project enums: results are derived handoff dispositions only.
"""

ACTIONS = {'view', 'commercial_use', 'redistribute', 'generator_upload', 'ai_training'}


def camera_choice(intent):
    """Map an explicit geometric intention; ambiguous prose remains unresolved."""
    return {
        'translate_toward_subject': 'dolly',
        'tighten_without_translation': 'zoom_or_crop',
        'rotate_fixed_position': 'pan_or_tilt',
        'translate_sideways': 'truck',
        'change_focus_target': 'rack_focus',
    }.get(intent, 'unresolved')


def rights_disposition(record, action):
    """Require action-specific evidence; a statement for another action is irrelevant."""
    if action not in ACTIONS:
        raise ValueError('unknown rights action')
    row = record.get('actions', {}).get(action, {})
    if not all(isinstance(row.get(k), str) and row[k].strip()
               for k in ('evidence_locator', 'checked_at')):
        return 'unverified'
    if row.get('decision') == 'restricted':
        return 'restricted'
    return 'evidence_recorded' if row.get('decision') == 'allowed' else 'unverified'


def control_disposition(field, contract):
    """A named current transport field needs its own declared semantic and locator."""
    if not contract.get('inspected') or not contract.get('locator'):
        return 'UNVERIFIED'
    spec = contract.get('fields', {}).get(field)
    if isinstance(spec, dict) and spec.get('supported') is True and spec.get('locator'):
        return 'HARD_CONTROL'
    if field in contract.get('unsupported', []):
        return 'UNSUPPORTED'
    return 'SOFT_PROMPT' if contract.get('text_intent_supported') is True else 'UNVERIFIED'


def inspection_support(record, claim):
    """Report whether supplied evidence could support a claim; does not attest truth."""
    if claim not in {'body_text', 'sampled_appearance', 'motion', 'audio'}:
        raise ValueError('unknown inspection claim')
    evidence = record.get('evidence', {})
    mode = {'body_text': 'page_text', 'sampled_appearance': 'opened_frames',
            'motion': 'continuous_playback', 'audio': 'listening'}[claim]
    rows = evidence.get(mode, [])
    return bool(isinstance(rows, list) and rows and all(
        isinstance(r, dict) and isinstance(r.get('locator'), str) and
        r['locator'].strip() and isinstance(r.get('scope'), str) and r['scope'].strip()
        for r in rows))
