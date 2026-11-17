# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# How to run: imported by sequence_view; no direct execution.
"""Display record closure, separate from executable project_index semantics."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Final
from sequence_contract import Document, Json, SequenceError, table

GLOBAL_TYPES: Final = frozenset(('storyboard', 'storyboard_sheet', 'generation_spec',
    'edit_plan', 'video_execution_plan', 'preproduction_review', 'qa_review'))


def collect_context(project: Mapping[str, Json], q: Document, included: list[Document],
             handoff: Document, requirements: list[Document], links: list[Document]) -> tuple[Document, Document, list[Document]]:
    """Close actual record consumption; compact global owners, not their maps."""
    shots, assets, artifacts = (table(project, key) for key in ('shots','asset_registry','artifacts'))
    selected_shots = {c['shot_id'] for c in included}
    storyboard = project.get('storyboard', {})
    panels = [p for p in storyboard.get('panels', []) if p['shot_id'] in selected_shots]
    wanted_assets: set[str] = set()
    wanted_artifacts: set[str] = set()
    declared_board = project.get('preproduction', {}).get('storyboard_artifact_id')
    board_ids = [aid for aid, row in artifacts.items() if row.get('type') == 'storyboard']
    if declared_board:
        wanted_artifacts.add(declared_board)
    elif len(board_ids) == 1:
        wanted_artifacts.add(board_ids[0])
    voices: set[str] = set()
    characters: set[str] = set()
    scenes: set[str] = set()
    claims: set[str] = set()
    cues: set[str] = set()
    for sid in selected_shots:
        s = shots[sid]
        scenes.add(s['scene_id']); characters.update(s.get('character_ids', []))
        claims.update(s.get('claim_ids', [])); cues.update(s.get('audio_cue_ids', []))
        wanted_assets.update(s.get('asset_ids', []))
        spatial = s.get('spatial', {})
        if spatial.get('artifact_id'):
            wanted_artifacts.add(spatial['artifact_id'])
        voices.update(speech['voice_artifact_id'] for speech in s.get('speech', []) if speech.get('voice_artifact_id'))
    for c in included:
        if c.get('source_asset_id'):
            wanted_assets.add(c['source_asset_id'])
    for p in panels:
        wanted_assets.update(p.get('asset_version_refs', {}))
        for key in ('image_asset_id','source_sheet_asset_id'):
            if p.get(key): wanted_assets.add(p[key])
    character_rows = [row for cid, row in table(project, 'characters').items() if cid in characters]
    for row in character_rows:
        if row.get('ssot_artifact_id'): wanted_artifacts.add(row['ssot_artifact_id'])
        if row.get('identity_sheet_asset_id'): wanted_assets.add(row['identity_sheet_asset_id'])
        if row.get('voice_artifact_id'): voices.add(row['voice_artifact_id'])
    if project.get('look_asset_id'): wanted_assets.add(project['look_asset_id'])
    if storyboard.get('synopsis_artifact_id'): wanted_artifacts.add(storyboard['synopsis_artifact_id'])
    for aid in (q['owner'].get('artifact_id'), q.get('execution_artifact_id')):
        if aid: wanted_artifacts.add(aid)
    for binding in handoff.get('bindings', []):
        if binding.get('reference_asset_id'): wanted_assets.add(binding['reference_asset_id'])
        if binding.get('voice_artifact_id'): voices.add(binding['voice_artifact_id'])
    adapter_id = handoff.get('adapter_artifact_id')
    if adapter_id:
        if not isinstance(adapter_id, str) or adapter_id not in artifacts:
            raise SequenceError('artifact_reference', str(adapter_id), 'unknown required adapter')
        wanted_artifacts.add(adapter_id)
        descriptor = artifacts[adapter_id].get('reference_adapter', {})
        if not isinstance(descriptor, dict):
            raise SequenceError('transport_adapter', adapter_id, 'expected native descriptor object')
        if descriptor.get('schema_asset_id'):
            wanted_assets.add(descriptor['schema_asset_id'])
    for key, value in handoff.items():
        if key.endswith('_asset_id') and value: wanted_assets.add(value)
    def overlaps(row: Document) -> bool:
        return row.get('shot_id') in selected_shots or any(
            row.get('start_s', 0) < shots[sid]['end_s'] and row.get('end_s', 0) > shots[sid]['start_s']
            for sid in selected_shots)
    audio = [r for r in table(project, 'audio_cues').values() if r['id'] in cues or overlaps(r)]
    captions = [r for r in table(project, 'captions').values() if overlaps(r)]
    for row in audio + captions:
        if row.get('asset_id'): wanted_assets.add(row['asset_id'])
    panel_ids = {p['id'] for p in panels}
    targets = {'cut:' + c['cut_id'] for c in included} | {'panel:' + pid for pid in panel_ids} | {'voice:' + vid for vid in voices}
    targets.update('link:' + link['key'] for link in links)
    targets.update('requirement:' + requirement['key'] for requirement in requirements)
    checks = [r for r in q['checks'] if r.get('target') in targets]
    for record in checks:
        wanted_assets.update(record.get('observed_asset_ids', []))
        if record.get('evidence_asset_id'): wanted_assets.add(record['evidence_asset_id'])
    wanted_artifacts.update(voices)
    # A contact sheet's contributors are coverage, not lineage to every shot.
    aggregates = {p.get('source_sheet_asset_id') for p in panels if p.get('source_sheet_asset_id')}
    aggregates.update(a['id'] for a in assets.values() if a.get('panel_ids'))
    seen_assets: set[str] = set(); seen_artifacts: set[str] = set()
    pending_assets = list(wanted_assets); pending_artifacts = list(wanted_artifacts)
    while pending_assets or pending_artifacts:
        while pending_assets:
            aid = pending_assets.pop()
            if aid in seen_assets: continue
            if aid not in assets: raise SequenceError('asset_reference', str(aid), 'unknown required asset')
            seen_assets.add(aid); row = assets[aid]
            if aid not in aggregates: pending_assets.extend(row.get('source_asset_ids', []))
            master = row.get('master_asset_ref', {})
            if master.get('asset_id'): pending_assets.append(master['asset_id'])
            for artifact in artifacts.values():
                if aid in artifact.get('asset_ids', []): pending_artifacts.append(artifact['id'])
        if pending_artifacts:
            aid = pending_artifacts.pop()
            if aid in seen_artifacts: continue
            if aid not in artifacts: raise SequenceError('artifact_reference', str(aid), 'unknown required artifact')
            seen_artifacts.add(aid); row = artifacts[aid]
            if row.get('type') not in GLOBAL_TYPES:
                pending_artifacts.extend(row.get('dependencies', []))
                pending_assets.extend(row.get('asset_ids', []))
                pending_assets.extend(row.get('required_asset_versions', {}))
    issues: list[Document] = []
    def pin_issue(aid: str, pin: Json) -> None:
        version = pin.get('version') if isinstance(pin, dict) else pin
        if version is not None and version != assets[aid].get('version'):
            issues.append({'code':'stale_pin','locator':aid,'pinned_version':version,'current_version':assets[aid].get('version')})
    asset_rows = []
    for aid in sorted(seen_assets):
        row = assets[aid]
        master = row.get('master_asset_ref', {})
        if master.get('asset_id'): pin_issue(master['asset_id'], master.get('version'))
        if row.get('status') == 'stale': issues.append({'code':'stale_asset','locator':aid})
        if aid in aggregates:
            display = {k: row[k] for k in ('id','kind','version','status','path','sha256','master_asset_ref') if k in row}
            display.update(locator=f'project#/asset_registry/{aid}', aggregate=True,
                           omitted_source_count=len(row.get('source_asset_ids', [])))
        else: display = row
        asset_rows.append(display)
    artifact_rows = []
    for aid in sorted(seen_artifacts):
        row = artifacts[aid]
        if row.get('type') in GLOBAL_TYPES:
            display = {k: row[k] for k in ('id','type','version','status','finality') if k in row}
            display.update(locator=f'project#/artifacts/{aid}', omitted_fields=[k for k in (
                'asset_ids','dependencies','dependency_versions','required_asset_versions','execution_scope') if k in row])
            if aid == adapter_id:
                descriptor = row.get('reference_adapter', {})
                display['reference_adapter'] = {'tool':descriptor.get('tool'),
                    'schema_asset_id':descriptor.get('schema_asset_id'),
                    'locator':f'project#/artifacts/{aid}/reference_adapter'}
            display['required_asset_versions'] = {asset: pin for asset, pin in row.get('required_asset_versions', {}).items() if asset in seen_assets}
            display['dependency_versions'] = {dep: pin for dep, pin in row.get('dependency_versions', {}).items() if dep in seen_artifacts}
        else: display = dict(row, locator=f'project#/artifacts/{aid}')
        artifact_rows.append(display)
    inputs = {'assets': {aid: pin for aid, pin in q['inputs'].get('assets', {}).items() if aid in seen_assets},
              'artifact_versions': {aid: pin for aid, pin in q['inputs'].get('artifact_versions', {}).items() if aid in seen_artifacts}}
    for aid, pin in inputs['assets'].items(): pin_issue(aid, pin)
    for panel in panels:
        for aid, pin in panel.get('asset_version_refs', {}).items(): pin_issue(aid, pin)
    for aid in seen_artifacts:
        row = artifacts[aid]
        for asset, pin in row.get('required_asset_versions', {}).items():
            if asset in seen_assets: pin_issue(asset, pin)
        pin = inputs['artifact_versions'].get(aid)
        if pin is not None and pin != row.get('version'):
            issues.append({'code':'stale_pin','locator':aid,'pinned_version':pin,'current_version':row.get('version')})
    beats = {b for sid in selected_shots for b in shots[sid].get('beat_ids', [])}
    context = {'shots':[shots[sid] for sid in sorted(selected_shots)],
        'scenes':[s for s in table(project,'scenes').values() if s['id'] in scenes],
        'characters':character_rows, 'asset_registry':asset_rows, 'artifacts':artifact_rows,
        'claims':[r for r in table(project,'claims').values() if r['id'] in claims or selected_shots.intersection(r.get('shot_ids', []))],
        'audio_cues':audio,'captions':captions,
        'generation_attempts':[r for r in table(project,'generation_attempts').values() if r.get('shot_id') in selected_shots],
        'storyboard':{'panels':panels,'beats':[r for r in storyboard.get('beats', []) if r['id'] in beats]},
        'checks':checks}
    return context, inputs, issues


