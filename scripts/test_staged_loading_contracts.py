"""Structural migration checks, not LLM behavior or media-quality acceptance."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'qa/staged-loading'
REF = 'video-production-assets/references/'


def slug(title: str) -> str:
    return ''.join(c for c in title.lower() if c.isalnum() or c in '_- ').replace(' ', '-')


def fragments(text: str) -> set[str]:
    result = set(re.findall(r'<a id="([^"]+)"', text))
    seen = Counter()
    for heading in re.findall(r'^#{1,6} (.+)$', text, re.M):
        name = slug(heading); n = seen[name]; seen[name] += 1
        result.add(name + (f'-{n}' if n else ''))
    return result


def source(name: str):
    return next(s for s in json.loads((QA / 'legacy-anchors.json').read_text())['sources']
                if s['path'] == REF + name + '.md')


def ownership(name: str):
    with (QA / 'rule-ownership.csv').open(newline='') as stream:
        return [r for r in csv.DictReader(stream) if r['old_path'] == REF + name + '.md']


@pytest.mark.parametrize('owner', ['core', 'project', 'package', 'delivery'])
def test_common_owners_are_real_files(owner):
    assert (ROOT / REF / f'contract-{owner}.md').is_file()


def assert_migration(name: str, destinations: list[str]) -> None:
    baseline = source(name)
    old_text = (ROOT / baseline['path']).read_text()
    assert {h['fragment'] for h in baseline['headings']} <= fragments(old_text)
    cases = {c['id'] for c in json.loads((QA / 'cases.json').read_text())['cases']}
    rows = ownership(name)
    assert len({r['rule_id'] for r in rows}) == len(rows)
    assert {r['old_anchor'] for r in rows} >= {h['fragment'] for h in baseline['headings']}
    for row in rows:
        assert row['source_sha256'] == baseline['sha256']
        assert row['applies_when'] and 'planned stage owner' not in row['applies_when']
        assert set(row['equivalence_case_ids'].split(';')) <= cases
        target = ROOT / row['new_path']
        assert target.is_file(), row
        assert row['new_anchor'] in fragments(target.read_text()), row
        if row['new_path'] != row['old_path']:
            assert f"{Path(row['new_path']).name}#{row['new_anchor']}" in old_text, row
    # Every original substantive line is retained verbatim in one stage owner.
    # The frozen baseline captures original multiplicity; new links aren't evidence.
    observed = Counter()
    for path in destinations:
        for line in (ROOT / REF / path).read_text().splitlines():
            if line.strip() and not line.startswith(('#', '<a ')):
                observed[hashlib.sha256(line.encode()).hexdigest()] += 1
    for digest, count in baseline['body_line_counts'].items():
        assert observed[digest] == count, (name, digest, count, observed[digest])


def test_common_legacy_anchors_ownership_and_body_preservation():
    assert_migration('contract', [f'contract-{p}.md' for p in ('core','project','package','delivery')])


def test_common_owner_boundaries():
    core, project, package, delivery = [(ROOT / REF / f'contract-{name}.md').read_text()
                                      for name in ('core','project','package','delivery')]
    assert '단독 채팅 산출물' in core and '동시 수정하지 않는다' in core
    assert 'input_versions' in project and 'timing_policy' in project
    assert '7뷰' in package and 'master_asset_ref' in package and 'required_asset_versions' in package
    assert 'ZIP' in delivery and 'relocation map' in delivery
    assert 'render_storyboard_sheet.py' not in core and 'package_production.py' not in core
