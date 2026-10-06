"""Completeness checks for full preproduction packages and sheet-derived output.

Shared project validation owns record schemas and registered-file hashes; this
validator joins current sheets and split manifests to canonical panels, scenes
and their registered extracted files. It makes no artistic, identity-similarity,
rights or user-approval attestation. Standalone plans without a full package do
not use this gate.
"""
import re
from pathlib import Path


def validate_preproduction(project, base_dir=None, *, image_backed_required=False, panels_per_sheet=8):
    errors = []
    if not isinstance(project, dict):
        return ['preproduction: project must be an object']
    package = project.get('preproduction')
    if not isinstance(package, dict):
        return ['preproduction: full-package declaration required']
    mode = package.get('mode')
    if mode not in ('text', 'image_backed'):
        errors.append('preproduction.mode: text or image_backed required')
    images = mode == 'image_backed'
    if image_backed_required and not images:
        errors.append('preproduction: image-backed review/execution cannot use text mode')
    base = Path(base_dir).resolve() if base_dir is not None else None
    if base is None:
        errors.append('preproduction: saved-package completeness requires --base-dir')

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def table(name):
        rows = project.get(name)
        return {row['id']: row for row in rows if isinstance(row, dict) and text(row.get('id'))} if isinstance(rows, list) else {}

    artifacts = table('artifacts')
    assets = table('asset_registry')
    characters = table('characters')
    shots = table('shots')
    decoded = set()

    def artifact(aid, kind, label):
        row = artifacts.get(aid) if isinstance(aid, str) else None
        if row is None or row.get('type') != kind:
            errors.append(f'preproduction {label}: {kind} artifact required')
            return None
        if row.get('status') == 'stale':
            errors.append(f'preproduction {label}: stale artifact {aid}')
        return row

    def dependency(row, aid, label):
        if row is None or not isinstance(aid, str) or aid not in artifacts:
            return
        deps, versions = row.get('dependencies'), row.get('dependency_versions')
        if not isinstance(deps, list) or aid not in deps:
            errors.append(f'preproduction {label}: missing dependency {aid}')
        elif not isinstance(versions, dict) or versions.get(aid) != artifacts[aid].get('version'):
            errors.append(f'preproduction {label}: stale dependency version {aid}')

    def file_asset(aid, label, *, kind=None, image=False, markdown=False):
        row = assets.get(aid) if isinstance(aid, str) else None
        if row is None:
            errors.append(f'preproduction {label}: registered asset required')
            return None
        if kind is not None and row.get('kind') != kind:
            errors.append(f'preproduction {label}: asset kind must be {kind}')
        if row.get('status') not in ('available', 'verified'):
            errors.append(f'preproduction {label}: actual available/verified asset required')
        digest = row.get('sha256')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            errors.append(f'preproduction {label}: actual asset SHA-256 required')
        path = row.get('path')
        if not text(path):
            errors.append(f'preproduction {label}: actual file path required')
            return row
        if base is None:
            return row
        try:
            raw = Path(path)
            if raw.is_absolute() or '..' in raw.parts:
                errors.append(f'preproduction {label}: unsafe project-relative path')
                return row
            candidate = base
            for part in raw.parts:
                candidate = candidate / part
                if candidate.is_symlink() or (hasattr(candidate, 'is_junction') and candidate.is_junction()):
                    errors.append(f'preproduction {label}: symbolic link in managed path')
                    return row
            resolved = candidate.resolve()
            if not resolved.is_relative_to(base) or not resolved.is_file():
                errors.append(f'preproduction {label}: file missing or outside project root')
                return row
            if markdown:
                if resolved.suffix.lower() != '.md' or not resolved.read_text(encoding='utf-8').strip():
                    errors.append(f'preproduction {label}: nonempty Markdown file required')
            if image and resolved not in decoded:
                from PIL import Image
                with Image.open(resolved) as source:
                    source.load()
                decoded.add(resolved)
        except (OSError, ValueError, ImportError) as exc:
            errors.append(f'preproduction {label}: cannot read actual file: {exc}')
        return row

    def document(row, label):
        if row is None:
            return
        ids = row.get('asset_ids')
        if not isinstance(ids, list) or len(ids) != 1:
            errors.append(f'preproduction {label}: exactly one Markdown asset required')
            return
        file_asset(ids[0], label, markdown=True)

    synopsis_id = package.get('synopsis_artifact_id')
    synopsis = artifact(synopsis_id, 'synopsis', 'synopsis')
    document(synopsis, 'synopsis')
    board_id = package.get('storyboard_artifact_id')
    board = artifact(board_id, 'storyboard', 'storyboard')
    document(board, 'storyboard')
    dependency(board, synopsis_id, 'storyboard')
    sb = project.get('storyboard')
    if not isinstance(sb, dict) or sb.get('synopsis_artifact_id') != synopsis_id:
        errors.append('preproduction: storyboard must use the package synopsis')
    from validate_storyboard import validate_storyboard
    errors.extend(validate_storyboard(project, base_dir, images, check_project=False,
                                      panels_per_sheet=panels_per_sheet))

    for cid, character in characters.items():
        persona = character.get('persona')
        if not isinstance(persona, dict) or not all(text(persona.get(key)) for key in ('role', 'personality', 'observable_behavior', 'speech')):
            errors.append(f'preproduction {cid}: persona role/personality/observable_behavior/speech required')
        ssot_id = character.get('ssot_artifact_id')
        ssot = artifact(ssot_id, 'character_sheet', cid)
        document(ssot, f'{cid} SSOT')
        dependency(ssot, synopsis_id, f'{cid} SSOT')
        dependency(board, ssot_id, 'storyboard')
        if images:
            aid = character.get('identity_sheet_asset_id')
            sheet = file_asset(aid, f'{cid} identity sheet', kind='character_identity_sheet', image=True)
            ssot_assets = ssot.get('asset_ids') if isinstance(ssot, dict) else None
            source_ids = sheet.get('source_asset_ids') if isinstance(sheet, dict) else None
            if not isinstance(ssot_assets, list) or len(ssot_assets) != 1 \
                    or not isinstance(source_ids, list) or ssot_assets[0] not in source_ids:
                expected = ssot_assets[0] if isinstance(ssot_assets, list) and len(ssot_assets) == 1 else '?'
                errors.append(
                    f'preproduction {cid}: identity sheet must include SSOT source asset {expected}')
            if sheet is not None and (sheet.get('entity_type') != 'character' or sheet.get('entity_id') != cid):
                errors.append(f'preproduction {cid}: identity sheet must belong to the same character')
            for sid, shot in shots.items():
                ids = shot.get('character_ids')
                if isinstance(ids, list) and cid in ids:
                    refs = shot.get('asset_ids')
                    if not isinstance(refs, list) or aid not in refs:
                        errors.append(f'preproduction {sid}: missing character identity reference {cid}')

    required_review_inputs = [synopsis_id, board_id]
    if images:
        sheet_ids = package.get('storyboard_sheet_artifact_ids')
        if not isinstance(sheet_ids, list) or not sheet_ids \
                or any(not isinstance(sheet_id, str) for sheet_id in sheet_ids):
            errors.append('preproduction combined storyboard sheets: ordered sheet artifact ids required')
        else:
            required_review_inputs.extend(sheet_ids)
            for sheet_id in sheet_ids:
                label = f'combined storyboard sheet {sheet_id}'
                sheet_artifact = artifact(sheet_id, 'storyboard_sheet', label)
                dependency(sheet_artifact, board_id, label)
        from asset_gate import validate_storyboard_extractions
        errors.extend(validate_storyboard_extractions(project, base))

    # Review may consume these through the sheet/board dependency chain.
    for rid, row in artifacts.items():
        if row.get('type') != 'preproduction_review' or row.get('status') not in ('reviewed', 'approved'):
            continue
        pending = list(row.get('dependencies', [])) if isinstance(row.get('dependencies'), list) else []
        seen = set()
        while pending:
            aid = pending.pop()
            if not isinstance(aid, str) or aid in seen or aid not in artifacts:
                continue
            seen.add(aid)
            deps = artifacts[aid].get('dependencies')
            if isinstance(deps, list):
                pending.extend(deps)
        for aid in required_review_inputs:
            if isinstance(aid, str) and aid not in seen:
                errors.append(f'preproduction {rid}: review does not consume package artifact {aid}')
    for issue in table('issues').values():
        if issue.get('severity') == 'blocker' and issue.get('status') != 'resolved':
            errors.append(f'preproduction: unresolved blocker {issue["id"]}')
    return errors
