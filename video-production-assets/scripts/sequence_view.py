# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# How to run: sequence_context.py PROJECT --shot SH01 --view focus
"""Pure display selection, deliberately independent of project_index expansion.

No validation, filesystem reads, approval inference or native request rewriting.
The full execution projection remains the only input to execution consumers.
"""
from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Final

from sequence_contract import (Document, FrameSpan, Json, SequenceError,
                               check_projection, predecessor_cuts, table)
from sequence_view_records import collect_context

FORMAT: Final = 'sequence-focus-view/1'



def _document(value: Json, locator: str) -> Document:
    match value:
        case dict():
            return value
        case _:
            raise SequenceError('view_shape', locator, 'expected object')


def _rows(value: Json, locator: str) -> list[Document]:
    """Parse an open JSON record-array boundary with a located error."""
    match value:
        case list() if all(isinstance(row, dict) for row in value):
            return value
        case _:
            raise SequenceError('view_shape', locator, 'expected array of objects')


def _ids(value: Json, locator: str) -> list[str]:
    match value:
        case list() if all(isinstance(item, str) for item in value):
            return value
        case _:
            raise SequenceError('view_shape', locator, 'expected string IDs')


def _selection(project: Mapping[str, Json], q: Document, focus: set[str]) -> tuple[list[Document], dict[str, set[str]], list[Document]]:
    """Close declared history, not every historical edit predecessor."""
    cuts = q['cuts']
    by_cut: dict[str, Document] = {}
    for cut in cuts:
        cid = cut.get('cut_id')
        if not isinstance(cid, str) or cid in by_cut or cut.get('shot_id') not in table(project, 'shots'):
            raise SequenceError('cuts', str(cid), 'unique cut ID and known shot required')
        FrameSpan(cut.get('final_in_frame'), cut.get('final_out_frame'))
        by_cut[cid] = cut
    ordered = sorted(cuts, key=lambda cut: cut['final_in_frame'])
    reasons: dict[str, set[str]] = {}
    def include(cid: str, reason: str) -> None:
        if cid not in by_cut:
            raise SequenceError('cut_reference', str(cid), 'unknown cut')
        reasons.setdefault(cid, set()).add(reason)
    for i, cut in enumerate(ordered):
        if cut['shot_id'] in focus:
            include(cut['cut_id'], 'focus')
            if i:
                include(ordered[i - 1]['cut_id'], 'predecessor')
            if i + 1 < len(ordered):
                include(ordered[i + 1]['cut_id'], 'successor')
    if focus - {c['shot_id'] for c in ordered if 'focus' in reasons.get(c['cut_id'], ())}:
        raise SequenceError('focus', 'cuts', 'every focus shot needs at least one cut')
    pending = [cid for cid, why in reasons.items() if 'focus' in why]
    visited: set[str] = set()
    selected_links: dict[int, Document] = {}
    while pending:
        cid = pending.pop()
        if cid in visited:
            continue
        visited.add(cid)
        for i, link in enumerate(q['links']):
            if link.get('from_cut_id') not in by_cut or link.get('to_cut_id') not in by_cut:
                raise SequenceError('link_reference', str(i), 'known source and target cuts required')
            if link['to_cut_id'] == cid:
                # Reuse execution's history ID/target rejection semantics.
                predecessor_cuts(q, link)
                selected_links[i] = link
                for sid in _ids(link.get('history_shot_ids', []), f'links/{i}/history_shot_ids'):
                    for historical in ordered:
                        if historical['shot_id'] == sid:
                            include(historical['cut_id'], 'history')
                            pending.append(historical['cut_id'])
                if 'focus' in reasons[cid]:
                    include(link['from_cut_id'], 'referenced_dependency')
            if link['from_cut_id'] == cid and 'focus' in reasons[cid]:
                selected_links[i] = link
    return ordered, reasons, [dict(row, locator=f'projection#/links/{i}') for i, row in selected_links.items()]


def build_sequence_focus_view(project: Mapping[str, Json], shot_ids: Sequence[str],
                              projection: Mapping[str, Json] | None = None) -> Document:
    """Select display records without changing the canonical or full inputs."""
    from sequence_context import _bootstrap
    focus = set(shot_ids); shots = table(project, 'shots')
    if not focus or focus - shots.keys():
        raise SequenceError('focus','shot_ids','explicit known shot scope required')
    q = copy.deepcopy(dict(projection)) if projection is not None else _bootstrap(project)
    check_projection(q, Path('<provided>'))
    _document(q.get('focus', {}), 'focus')
    for field in ('assets', 'artifact_versions'):
        _document(q['inputs'].get(field, {}), 'inputs/' + field)
    if q.get('generation_handoff') is not None:
        _document(q['generation_handoff'], 'generation_handoff')
    ordered, reasons, links = _selection(project, q, focus)
    requirements = [r for r in q['requirements'] if r.get('shot_id') in focus]
    for req in requirements:
        for cid in req.get('cut_ids', []):
            if cid not in {c['cut_id'] for c in ordered}: raise SequenceError('cut_reference',str(cid),'unknown required cut')
            reasons.setdefault(cid,set()).add('referenced_dependency')
    original_focus = _ids(q.get('focus', {}).get('shot_ids', []), 'focus/shot_ids')
    raw_handoff = q.get('generation_handoff')
    applicability = 'absent'
    handoff: Document = {}
    if raw_handoff is not None:
        applicability = 'applicable' if set(original_focus) == focus else 'mismatch'
        handoff = {'scope_shot_ids':original_focus,'locator':'projection#/generation_handoff',
                   'submission_asset_id':q.get('submission_asset_id')}
        if applicability == 'applicable':
            handoff.update(raw_handoff)
            for binding in _rows(handoff.get('bindings', []),'generation_handoff/bindings'):
                if binding.get('source_cut_id'):
                    cid = binding['source_cut_id']
                    if cid not in {c['cut_id'] for c in ordered}: raise SequenceError('cut_reference',str(cid),'unknown binding source')
                    reasons.setdefault(cid,set()).add('referenced_dependency')
        else:
            handoff['limits'] = 'Different submission scope; no current native handoff inferred.'
    included = [c for c in ordered if c['cut_id'] in reasons]
    context, inputs, issues = collect_context(project,q,included,handoff if applicability == 'applicable' else {},requirements,links)
    checks = context.pop('checks')
    for i, record in enumerate(q['checks']):
        if record.get('target') == 'scope':
            checks.append({'target':'scope','kind':record.get('kind'),'status':record.get('status'),
                           'locator':f'projection#/checks/{i}','applicability':'not_inferred'})
    for key in ('project_id','project_version'):
        expected = project.get('version' if key == 'project_version' else key)
        if q['owner'].get(key) != expected:
            issues.append({'code':'source_mismatch','locator':f'owner/{key}'})
    if applicability == 'mismatch': issues.append({'code':'handoff_scope','locator':'projection#/focus'})
    omissions = {}
    for key, total, shown in [('cuts',len(q['cuts']),len(included)),('requirements',len(q['requirements']),len(requirements)),
        ('panels',len(project.get('storyboard', {}).get('panels', [])),len(context['storyboard']['panels'])),
        ('assets',len(project.get('asset_registry', [])),len(context['asset_registry'])),
        ('artifacts',len(project.get('artifacts', [])),len(context['artifacts']))]:
        omissions[key] = {'total':total,'shown':shown,'omitted':total-shown}
    return copy.deepcopy({'format':FORMAT,'read_only':True,'executable':False,'validation':'not_run',
        'source':{'project_id':project.get('project_id'),'project_version':project.get('version'),
                  'owner':q['owner'],'origin':'provided' if projection is not None else 'bootstrap',
                  'project_snapshot':None,'projection_snapshot':None},
        'focus':{'shot_ids':sorted(focus),'cut_ids':[c['cut_id'] for c in included if c['shot_id'] in focus],
                 'context_shot_ids':sorted({c['shot_id'] for c in included}),
                 'inclusion':[{'cut_id':c['cut_id'],'shot_id':c['shot_id'],'reasons':sorted(reasons[c['cut_id']])} for c in included]},
        'time_basis':q['time_basis'],'context':context,'cuts':included,'links':links,
        'requirements':requirements,'checks':checks,'inputs':inputs,'handoff':handoff,
        'handoff_applicability':applicability,'issues':issues,'omissions':omissions,
        'full_projection_locator':'source.projection_snapshot (unavailable in pure calls)',
        'additional_query':'Use the original full projection; select other shots with --view focus.',
        'limits':'Display only, not executable. Validation not run; snapshots do not certify media, quality or authority. Execution consumers must reread the original full projection.'})
