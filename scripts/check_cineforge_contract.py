#!/usr/bin/env python3
"""Validate the package adapter and hashes before distributing a pack update."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from build_cineforge_inventory import ROOT, build
from install_package import CINEFORGE_INVENTORY

SCHEMA = ROOT / 'integrations/cineforge/skill_pack.schema.json'


def check(root: Path) -> list[str]:
    manifest = json.loads((root / 'manifest.json').read_bytes())
    contract = manifest.get('integrations', {}).get('cineforge')
    schema = json.loads(SCHEMA.read_bytes())
    try:
        Draft202012Validator(schema).validate(contract)
    except ValidationError as exc:
        field = '.'.join(map(str, exc.absolute_path)) or 'integrations.cineforge'
        return [f'{field}: {exc.message}']
    inventory_bytes = (root / CINEFORGE_INVENTORY).read_bytes()
    if inventory_bytes != build(root).encode('utf-8'):
        return ['stale CineForge inventory; run python scripts/build_cineforge_inventory.py']
    inventory = json.loads(inventory_bytes)
    skills = set(manifest['skills'])
    errors = []
    refs = set(contract['delivery_files']) | {f'{name}/SKILL.md' for name in skills}
    for stage, row in contract['stages'].items():
        if unknown := set(row['owners']) - skills:
            errors.append(f'{stage}: unregistered skill owners: {sorted(unknown)}')
        refs.update(row['refs'])
        if row.get('guide'):
            refs.add(row['guide'])
        for branch in row.get('when', {}).values():
            refs.update(branch['refs'])
    errors.extend(f'not in CineForge inventory: {path}' for path in sorted(refs - inventory.keys()))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        errors = check(args.root.resolve())
    except (OSError, KeyError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(error)
    if errors:
        return 1
    print('CineForge contract v1 and pack inventory OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
