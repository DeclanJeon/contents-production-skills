"""Isolated, non-generative Brandkit smoke; no installs or provider submissions."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
WORK = OUT / 'synthetic-brand'
WORK.mkdir(exist_ok=True)
CLI = ROOT / 'higgsfield-brandkit/scripts/brandkit.py'
records = []

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def run(*args):
    cmd = [sys.executable, str(CLI), *map(str, args)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=150)
    row = {'command': cmd, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    records.append(row)
    dump(OUT / 'commands.json', records)
    print(json.dumps(row, ensure_ascii=False))
    return p

logo = WORK / 'fixture-symbol.svg'
logo.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path fill="#101820" d="M20 80V20H40V60H80V80Z"/></svg>', encoding='utf-8')
fonts = {'display': {'family': 'Georgia', 'source': 'C:/Windows/Fonts/georgiab.ttf', 'weight': 700, 'style': 'normal'}, 'body': {'family': 'Arial', 'source': 'C:/Windows/Fonts/arial.ttf', 'weight': 400, 'style': 'normal'}}
colors = [{'hex': '#F7F7F5', 'name': 'Paper', 'role': 'background'}, {'hex': '#101820', 'name': 'Ink', 'role': 'text'}, {'hex': '#00AEEF', 'name': 'Signal', 'role': 'accent'}]
state = WORK / 'state.json'
run('state', '--state-file', state, '--action', 'get_status')
inspection = run('logo-inspect', '--source', logo)
fingerprint = json.loads(inspection.stdout)['geometry_fingerprint']
for slot, value in [('palette', {'colors': colors, 'gradients': []}), ('logo', {'name': 'Synthetic Corner symbol', 'asset': {'path': str(logo)}, 'geometry_fingerprint': fingerprint}), ('typography', {**fonts, 'font_links': []})]:
    payload = WORK / f'official-{slot}.json'
    dump(payload, {'source_summary': 'Synthetic QA fixture supplied by this smoke, not a user brand approval.', slot: value})
    run('state', '--state-file', state, '--action', f'lock_authoritative_{slot}', '--input', payload)
run('state', '--state-file', state, '--action', 'get_essential_kit')
review = {'stage': 'essential', 'name': 'Synthetic Corner', 'premise': 'An angular corner mark with quiet supporting typography.', 'keywords': ['angular', 'clear'], 'palette': colors, 'logo_ideas': [], 'logo_svg': str(logo), 'display_font': fonts['display'], 'body_font': fonts['body'], 'headline': 'Synthetic Corner', 'body': 'Local fixture. No products, claims, or customer approvals.', 'background_color': '#F7F7F5', 'text_color': '#101820'}
dump(WORK / 'reviews.json', {'reviews': [review]})
preview = run('preview', '--input', WORK / 'reviews.json', '--output-dir', WORK / 'reviews')
dump(WORK / 'export.json', {'name': 'synthetic-corner', 'logo_svg': str(logo), 'delivery': 'user', 'replacements': [], 'include_monochrome': False})
run('logo-export', '--input', WORK / 'export.json', '--output-dir', WORK / 'export')
dump(WORK / 'brandbook.json', {'brand_name': 'Synthetic Corner', 'concept_summary': 'An angular corner mark with quiet supporting typography.', 'palette_summary': 'Paper and Ink support reading; Signal is the accent.', 'secondary_logo_url': '', 'mockups': [], 'revision': 1})
run('brandbook-build', '--state-file', state, '--input', WORK / 'brandbook.json', '--output-dir', WORK / 'brandbook')
dump(WORK / 'bad-reviews.json', {'reviews': []})
run('preview', '--input', WORK / 'bad-reviews.json', '--output-dir', WORK / 'bad-reviews')

from playwright.sync_api import sync_playwright
visual = {}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1100}, device_scale_factor=1)
    if preview.returncode == 0:
        board = Path(json.loads(preview.stdout)['files'][0]['file'])
        page.goto(board.as_uri())
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(OUT / 'essential-preview.png'), full_page=True)
        visual['board'] = page.evaluate("""() => ({title: document.title, text: document.body.innerText, width: document.documentElement.scrollWidth, viewport: innerWidth, fonts: [...document.fonts].map(f => ({family:f.family,status:f.status,weight:f.weight}))})""")
    page.goto(logo.as_uri())
    page.screenshot(path=str(OUT / 'source-symbol.png'))
    browser.close()
dump(OUT / 'visual-inspection.json', visual)

source_paths = [Path('E:/Book/06_Book/originals/마케팅/md/Strategic Brand Management (Kevin Lane Keller, Vanitha Swaminathan) (z-library.sk, 1lib.sk, z-lib.sk).md')]
identities = []
for path in source_paths:
    data = path.read_bytes()
    identities.append({'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'read_state': 'READ-PARTIAL', 'locator': 'L309-L315, L333-L337; printed pp154-157,166-168'})
for url, scope in [('https://www.adobe.com/express/learn/blog/best-logos-for-brand.md', 'Tips for choosing logo fonts; Text-only logo fonts; Text and icon logo fonts; Monogram logo fonts'), ('https://www.adobe.com/express/learn/blog/10-ways-to-pair-fonts-for-maximum-impact.md', '1. Event flyers; 2. Social media ads; 5. Resumes'), ('https://www.adobe.com/express/learn/blog/how-to-design-a-logo.md', 'What are the different types of logos?; Core components; Steps 1,3,5,7,8; Logo design best practices / Own one thing')]:
    try:
        data = urlopen(url, timeout=30).read()
        identities.append({'url': url, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'read_state': 'READ-PARTIAL', 'locator': scope})
    except Exception as e:
        identities.append({'url': url, 'error': str(e)})
dump(OUT / 'source-identities.json', identities)
dump(OUT / 'artifact-identities.json', [{'path': str(f.relative_to(ROOT)), 'bytes': f.stat().st_size, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()} for f in WORK.rglob('*') if f.is_file()])
