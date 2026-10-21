"""Budget-zero local alpha observation; not Blender or model replay evidence."""
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
background = Image.new('RGBA', (96, 64), (20, 40, 80, 255))
foreground = Image.new('RGBA', background.size, (0, 0, 0, 0))
for y in range(16, 48):
    for x in range(24, 72):
        foreground.putpixel((x, y), (240, 220, 180, 128))
composite = Image.alpha_composite(background, foreground)
composite.save(out / 'alpha-composite.png')
prompts = json.loads((out / 'smoke-prompts.json').read_text(encoding='utf-8'))
missing = [p for case in prompts for p in case['required_reads'] if not (root / p).is_file()]
result = {
    'executor': 'Pillow.Image.alpha_composite',
    'scope': 'Synthetic straight-alpha foreground over opaque background; no Blender execution, paid provider, or fresh-model invocation.',
    'size': list(composite.size),
    'background_pixel': list(composite.getpixel((0, 0))),
    'overlay_pixel': list(composite.getpixel((48, 32))),
    'expected_overlay_pixel': [130, 130, 130, 255],
    'overlay_matches_expected': composite.getpixel((48, 32)) == (130, 130, 130, 255),
    'scenario_count': len(prompts),
    'stable_ids_complete': [c['id'] for c in prompts] == [f'F1-{i:02d}' for i in range(1, 29)],
    'missing_required_paths': missing,
    'behavior_replay_status': 'NOT_RUN_PARENT_FINAL_FREEZE_REQUIRED',
}
(out / 'local-observations.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
