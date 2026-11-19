"""Pre-generation AV continuity requirements, grounded in selected source ranges."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from fractions import Fraction
from pathlib import Path
from typing import TypeAlias, assert_never

from generation_transport import BoundReference, Modality, _binding, inspect_transport, pinned_document
from sequence_contract import (Document, FrameSpan, Json, SequenceError, checked_assets,
                               parse_fps, table, predecessor_cuts)
from sequence_media import probe_media, _run
import json

Inspection: TypeAlias = Callable[[str, str, str, list[str], Document | None], Document | None]


def _audio_info(path: Path) -> tuple[Fraction, int]:
    info = json.loads(_run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
        'stream=duration,duration_ts,time_base,sample_rate:format=duration', '-of', 'json', str(path)]).stdout)
    rows = info.get('streams', [])
    if not rows:
        raise SequenceError('reference_audio', str(path), 'actual audio stream missing')
    stream = rows[0]
    duration = (Fraction(stream['duration_ts']) * Fraction(stream['time_base'])
                if 'duration_ts' in stream and 'time_base' in stream else Fraction(str(info.get('format', {}).get('duration', 0))))
    sample_rate = int(stream.get('sample_rate', 0))
    if duration <= 0 or sample_rate <= 0:
        raise SequenceError('reference_audio', str(path), 'measurable audio samples required')
    return duration, sample_rate


def _reference_range(project: Mapping[str, Json], q: Mapping[str, Json], root: Path,
                     binding: BoundReference, cut: Document) -> None:
    assets = table(project, 'asset_registry')
    ref = assets[binding.reference_asset_id]
    parent_id = cut.get('source_asset_id')
    if not isinstance(parent_id, str):
        raise SequenceError('predecessor_selection', cut['cut_id'], 'actual selected source required')
    selected = FrameSpan(cut.get('source_in_frame'), cut.get('source_out_frame'))
    parent = assets[parent_id]
    fps = parse_fps(cut.get('source_fps'))
    if binding.reference_asset_id == parent_id:
        if selected.start != 0 or selected.end != cut.get('source_frame_count'):
            raise SequenceError('reference_range', binding.key, 'whole raw file includes unadopted frames; extract selected range')
        extent = selected
    else:
        lineage = ref.get('sequence_slice')
        if (not isinstance(lineage, dict) or lineage.get('source_asset_id') != parent_id or
                lineage.get('source_asset_version') != parent['version'] or lineage.get('source_sha256') != parent['sha256'] or
                parent_id not in ref.get('source_asset_ids', [])):
            raise SequenceError('reference_range', binding.key, 'registered parent/range provenance required')
        extent = FrameSpan(lineage.get('source_in_frame'), lineage.get('source_out_frame'))
        if parse_fps(lineage.get('source_fps')) != fps:
            raise SequenceError('reference_range', binding.key, 'source FPS differs')
        if extent.start < selected.start or extent.end != selected.end:
            raise SequenceError('reference_range', binding.key, 'reference must end at actual adopted exit, not failed/raw tail')
    path = checked_assets(project, root, [binding.reference_asset_id])[binding.reference_asset_id]
    match binding.modality:
        case Modality.IMAGE:
            if extent.start != selected.last or extent.end != selected.end:
                raise SequenceError('reference_range', binding.key, 'image alternative must be last included frame')
        case Modality.VIDEO:
            media = probe_media(path)
            if media['frame_count'] != extent.length or media['vfr'] or parse_fps(media['fps']) != fps:
                raise SequenceError('reference_range', binding.key, 'actual reference video does not cover declared frames')
        case Modality.AUDIO:
            duration, rate = _audio_info(path)
            if abs(duration - extent.length / fps) > Fraction(1, rate):
                raise SequenceError('reference_range', binding.key, 'actual audio duration differs from selected context')
        case unreachable:
            assert_never(unreachable)


def validate_generation_handoff(project: Mapping[str, Json], q: Mapping[str, Json], root: Path | None,
                                inspected: Inspection) -> list[Document]:
    """Apply the same AV obligations regardless of MCP; unsupported adapters block."""
    failures = []
    def fail(code: str, locator: str, detail: str) -> None:
        failures.append({'code': code, 'locator': locator, 'detail': detail})
    cuts = {c['cut_id']: c for c in q['cuts']}
    shots, artifacts = table(project, 'shots'), table(project, 'artifacts')
    focus = q.get('focus', {}).get('shot_ids', [])
    incoming = [l for l in q['links'] if l.get('to_cut_id') in cuts and cuts[l['to_cut_id']]['shot_id'] in focus]
    sources = []
    related = []
    for link in incoming:
        try:
            related.extend((link, cut) for cut in predecessor_cuts(q, link, for_generation=True))
        except SequenceError as exc:
            fail(exc.code, exc.locator, exc.detail)
    for link, cut in related:
        source = cut.get('source_asset_id')
        if not isinstance(source, str) or source not in q['inputs']['assets']:
            fail('predecessor_selection', cut['cut_id'], 'actual predecessor cannot be waived by a flag'); continue
        has_audio = project.get('audio_mode') != 'no_audio'
        if has_audio and root is not None:
            try:
                native = probe_media(checked_assets(project, root, [source])[source])
                has_audio = native['has_audio']
                if has_audio:
                    if inspected('cut:' + cut['cut_id'], 'source_audio', 'listening', [source], cut) is None:
                        fail('predecessor_audio', cut['cut_id'], 'hear the adopted audio before preparing next generation')
                else:
                    n_a = [r for r in q['checks'] if r.get('target') == 'cut:' + cut['cut_id'] and r.get('kind') == 'source_audio'
                           and r.get('status') == 'not_applicable' and r.get('reason') and
                           all(r.get(k) == cut.get(k) for k in ('source_asset_id', 'source_in_frame', 'source_out_frame'))]
                    if not n_a:
                        fail('predecessor_audio', cut['cut_id'], 'source really has no audio; record scoped N/A with reason')
            except SequenceError as exc:
                fail(exc.code, exc.locator, exc.detail)
        sources.append((link, cut, has_audio))
    h = q.get('generation_handoff')
    if not isinstance(h, dict):
        fail('generation_handoff', 'generation_handoff', 'actual video/audio native bindings required')
        return failures
    raw = h.get('bindings')
    if not isinstance(raw, list) or not all(isinstance(b, dict) for b in raw):
        fail('reference_shape', 'bindings', 'binding objects required'); return failures
    try:
        bindings = tuple(_binding(b) for b in raw)
    except SequenceError as exc:
        fail(exc.code, exc.locator, exc.detail); return failures
    assets = table(project, 'asset_registry')
    for sid in focus:
        panel_ids = {p.get('image_asset_id') or p.get('source_sheet_asset_id')
                     for p in project.get('storyboard', {}).get('panels', []) if p['shot_id'] == sid and p.get('role') in ('start', 'hold', 'action_peak')}
        if not any(b.purpose == 'current_composition' and b.reference_asset_id in panel_ids for b in bindings):
            fail('composition_reference', sid, 'current approved composition must be an actual selected input')
    for link, cut, has_audio in sources:
        for purpose, modality, code in (('visual_state', None, 'visual_reference'),
                                       ('audio_context', Modality.AUDIO, 'audio_reference')):
            if purpose == 'audio_context' and not has_audio:
                continue
            matching = [b for b in bindings if b.purpose == purpose and b.source_cut_id == cut['cut_id']
                        and (modality is None and b.modality in (Modality.VIDEO, Modality.IMAGE) or b.modality == modality)]
            if not matching:
                fail(code, cut['cut_id'], 'actual prior context must reach the selected native inputs')
            for b in matching:
                if b.reference_asset_id not in assets:
                    fail('reference_range', b.key, 'unknown reference asset'); continue
                if link.get('relation') != 'continuous_action' and b.purpose == 'visual_state' and b.role in ('first_frame', 'last_frame'):
                    fail('angle_reference', b.key, 'previous framing must not override a new approved angle')
                if root is not None:
                    try:
                        _reference_range(project, q, root, b, cut)
                    except SequenceError as exc:
                        fail(exc.code, exc.locator, exc.detail)
    if project.get('audio_mode') == 'no_audio' and any(b.modality == Modality.AUDIO for b in bindings):
        fail('audio_policy', 'bindings', 'silent deliverable cannot condition/reuse audio')
    elif project.get('audio_mode') != 'no_audio':
        ordered = sorted(q['cuts'], key=lambda c: c['final_in_frame'])
        heard_profiles = set()
        for cut in ordered:
            sid = cut['shot_id']
            profiles = {s['voice_artifact_id'] for s in shots[sid].get('speech', [])}
            if sid in focus:
                for vid in profiles & heard_profiles:
                    anchors = [b for b in bindings if b.purpose == 'voice_identity' and b.voice_artifact_id == vid and b.modality == Modality.AUDIO]
                    profile = artifacts.get(vid, {})
                    if not anchors or profile.get('status') not in ('verified', 'approved') or q['inputs']['artifact_versions'].get(vid) != profile.get('version'):
                        fail('voice_anchor', vid, 'reuse the actual verified/approved recurring voice anchor')
                    for b in anchors:
                        if b.reference_asset_id not in profile.get('asset_ids', []):
                            fail('voice_anchor', vid, 'sample differs from locked voice profile')
                        else:
                            inspected('voice:' + vid, 'voice_anchor', 'listening', [b.reference_asset_id], None)
            heard_profiles.update(profiles)
    if h.get('audio_delivery', 'native_reference') != 'native_reference':
        fail('audio_delivery', 'audio_delivery', 'alternate audio route needs explicit approved implementation; do not silently skip native handoff')
    if root is not None:
        try:
            request = pinned_document(project, q, root, q.get('submission_asset_id'))
            inspect_transport(project, q, request, root)
        except SequenceError as exc:
            fail(exc.code, exc.locator, exc.detail)
    return failures
