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
    formatting = set()
    edits = json.loads((QA / 'rule-edits.json').read_text()) if (QA / 'rule-edits.json').exists() else []
    moved_lines = {edit['new_line']: edit['old_line'] for edit in edits}
    for edit in edits:
        assert edit['reason'] and set(edit['equivalence_case_ids']) <= cases
        assert edit['new_line'] in (ROOT / edit['new_path']).read_text().splitlines()
    for path in destinations:
        for line in (ROOT / REF / path).read_text().splitlines():
            line = moved_lines.get(line, line)
            # Moved self-fragment links now name their exact stage owner.
            line = re.sub(r'\]\(storyboard-(?:direction|media|delivery|schema|contract)\.md#', '](#', line)
            digest = hashlib.sha256(line.encode()).hexdigest()
            if line.startswith('```') or set(line) <= set('|-: '):
                formatting.add(digest)
            if line.strip() and not line.startswith(('#', '<a ')):
                observed[digest] += 1
    for digest, count in baseline['body_line_counts'].items():
        if digest not in formatting:
            assert observed[digest] == count, (name, digest, count, observed[digest])


def test_common_legacy_anchors_ownership_and_body_preservation():
    assert_migration('contract', [f'contract-{p}.md' for p in ('core','project','package','delivery')])


@pytest.mark.parametrize('owner', ['direction','media','delivery','schema'])
def test_board_owners_are_real_files(owner):
    assert (ROOT / REF / f'storyboard-{owner}.md').is_file()


def test_board_legacy_anchors_ownership_and_body_preservation():
    assert_migration('storyboard-contract', ['storyboard-contract.md'] + [
        f'storyboard-{name}.md' for name in ('direction','media','delivery','schema')])


def test_board_core_keeps_complete_default_and_all_technical_slots():
    core = (ROOT / REF / 'storyboard-contract.md').read_text()
    for field in ('제작용 계획을 기본값','여섯 부분','전체 샷 명세표','전체 패널 표',
                  'KEEP / FIX / 미검증','카메라','공간','VFX','발화','음향','start / action_peak / end / hold'):
        assert field in core, field
    assert 'storyboard-direction.md' in core
    assert 'render_storyboard_sheet.py' not in core
    assert 'schema_version=1.1' not in core


def routes():
    with (ROOT / 'creative-production/references/routing.csv').open(newline='') as stream:
        return {r['route_id']: r for r in csv.DictReader(stream)}


def test_narrow_lighting_uses_core_not_full_contract_or_package():
    entry = (ROOT / 'video-production-assets/SKILL.md').read_text()
    assert 'references/contract-core.md' in entry
    assert '`references/contract.md`를 읽고' not in entry
    assert '단일 조명' in entry


def test_character_appearance_is_conditional_not_route_prerequisite():
    assert 'appearance-language-catalog' not in routes()['R03']['required_read']
    assert '때만' in (ROOT / 'designing-video-character-sheets/SKILL.md').read_text()


def test_text_board_routes_only_core_and_direction_before_media_or_schema():
    paths = routes()['R10']['required_read'].split('; ')
    assert REF + 'storyboard-contract.md' in paths
    assert REF + 'storyboard-direction.md' in paths
    assert not any(p.endswith(('storyboard-media.md','storyboard-schema.md','storyboard-delivery.md')) for p in paths)
    entry = (ROOT / 'storyboarding-video/SKILL.md').read_text()
    assert 'no media, files, or spend' not in entry
    assert 'storyboard-direction.md' in entry


def test_thumbnail_checks_selected_executor_not_unused_higgsfield_account():
    entry = (ROOT / 'higgsfield-youtube-thumbnail/SKILL.md').read_text()
    assert 'Codex Imagen' in entry
    assert 'do not require Higgsfield auth' in entry
    assert 'Before any generation:\n\n1. `higgsfield`' not in entry


def test_text_only_and_no_save_are_independent_policy_constraints():
    policy = (ROOT / 'creative-production/references/policy.md').read_text()
    assert '`text_only`' in policy and '`no-save`' in policy
    assert 'explicit MD/PDF' in policy
    common = (ROOT / REF / 'contract-core.md').read_text()
    assert '텍스트만/저장 금지 요청은 반환 제안에서 끝난다' not in common


def test_sequence_docs_distinguish_saved_full_from_display_view():
    text = (ROOT / REF / 'sequence-execution.md').read_text()
    assert '--view focus' in text and '--view full' in text
    assert 'sequence-focus-view/1' in text


@pytest.mark.parametrize('skill,detail,forbidden_inline', [
    ('recording-production-history', 'cli-contract.md', '## 이벤트 파일 규칙'),
    ('higgsfield-video-replicate', 'clip-execution.md', '--mode omni_reference'),
    ('higgsfield-video-explainer', 'block-execution.md', '--items @blocks.json'),
    ('higgsfield-generate', 'model-catalog.md', 'Models that accept it'),
])
def test_execution_detail_is_linked_not_unconditionally_inlined(skill, detail, forbidden_inline):
    entry = (ROOT / skill / 'SKILL.md').read_text()
    assert (ROOT / skill / 'references' / detail).is_file()
    assert 'references/' + detail in entry
    assert forbidden_inline not in entry


def test_common_owner_boundaries():
    core, project, package, delivery = [(ROOT / REF / f'contract-{name}.md').read_text()
                                      for name in ('core','project','package','delivery')]
    assert '단독 채팅 산출물' in core and '동시 수정하지 않는다' in core
    assert 'input_versions' in project and 'timing_policy' in project
    assert '7뷰' in package and 'master_asset_ref' in package and 'required_asset_versions' in package
    assert 'ZIP' in delivery and 'relocation map' in delivery
    assert 'render_storyboard_sheet.py' not in core and 'package_production.py' not in core
