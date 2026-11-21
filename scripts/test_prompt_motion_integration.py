from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTION = ROOT / 'video-production-assets/references'
OPEN = ROOT / 'open-3d-production'


def test_code_motion_contract_is_reachable_from_motion_owner():
    assert '(08b-code-motion-production.md)' in (MOTION / '08-animation.md').read_text()
    text = (MOTION / '08b-code-motion-production.md').read_text()
    for scenario in ('라이브 데모', '제공한 비식별 자료', 'BPM', '실제 출력본', '최대 2회'):
        assert scenario in text


def test_realtime_does_not_claim_web_qa_is_spatial_validation():
    assert '(references/realtime-motion-direction.md)' in (OPEN / 'SKILL.md').read_text()
    text = (OPEN / 'references/realtime-motion-direction.md').read_text()
    for requirement in ('대표 샷', 'reduced motion', 'Blender', '선형 영상'):
        assert requirement in text
