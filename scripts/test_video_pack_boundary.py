"""Package boundary and installed reference tests; never mutate real skill roots."""
from pathlib import Path
import json
import re
import install_package

ROOT=Path(__file__).resolve().parents[1]
MOVED={'product-detail-page-builder','higgsfield-brandkit','higgsfield-marketplace-cards','higgsfield-product-photoshoot','higgsfield-websites'}


def test_video_manifest_preserves_direct_support_and_excludes_nonvideo():
    skills=set(json.loads((ROOT/'manifest.json').read_text())['skills'])
    assert not skills & MOVED
    assert {'creative-production','video-production-assets','camera-spatial-design',
            'camera-motion-reference-analysis','ai-camera-control','blender-previsualization',
            'designing-video-character-sheets','designing-character-personas',
            'recording-production-history','topic-demand-selection','searching-social-media'} <= skills


def test_installed_video_pack_is_self_contained_and_does_not_install_nonvideo(tmp_path):
    target=tmp_path/'installed'
    result=install_package.install(target,repo_root=ROOT,exclude_derived_support=True)
    assert {p.name for p in result.installed}.isdisjoint(MOVED)
    missing=[]
    for skill in result.installed:
        for p in skill.rglob('*.md'):
            if 'support' in p.relative_to(skill).parts:continue
            body=re.sub(r'```.*?```','',p.read_text(encoding='utf-8'),flags=re.S)
            for ref in re.findall(r'\]\(([^)]+)\)',body):
                rel=ref.split('#')[0]
                if not rel or '://' in rel or rel.startswith(('mailto:','data:')):continue
                dest=(p.parent/rel).resolve()
                if not dest.is_relative_to(target.resolve()) or not dest.is_file():missing.append((str(p),ref))
    assert not missing


def test_migration_records_preserve_every_original_file():
    migration=json.loads((ROOT/'integrations/non-video-migration.json').read_text())
    assert {m['skill'] for m in migration['moves']}==MOVED
    assert not migration['remote_operations']
    for move in migration['moves']:
        assert move['files']
        for entry in move['files']:
            assert re.fullmatch('[0-9a-f]{64}',entry['source_sha256'])
            assert re.fullmatch('[0-9a-f]{64}',entry['destination_sha256'])
            assert entry['modified'] == (entry['source_sha256'] != entry['destination_sha256'])
