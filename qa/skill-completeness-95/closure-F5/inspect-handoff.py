"""Inspect new QA handoff formats; not behavior or source-text testing."""
import csv
import json
from pathlib import Path
root=Path(__file__).resolve().parent
prompts=json.loads((root/'smoke-prompts.json').read_text(encoding='utf-8'))
rows=list(csv.reader((root/'claims.tsv').read_text(encoding='utf-8').splitlines(),delimiter='\t'))
assert all(len(row)==16 for row in rows)
assert len({row[0] for row in rows[1:]})==len(rows)-1
assert all(row[0].startswith('F5-') for row in rows[1:])
assert len({p['id'] for p in prompts})==len(prompts)
repo=root.parents[2]
for p in prompts:
    assert set(p)=={'id','owner','prompt','required_reads','checks'}
    for file in p['required_reads']:
        assert (repo/file).is_file(),file
out={'supplemental_scenarios':len(prompts),'claim_rows':len(rows)-1,'claim_columns':16,'files':{p.name:len(p.read_text(encoding='utf-8').splitlines()) for p in root.iterdir() if p.is_file() and p.suffix in {'.md','.json','.py','.tsv'}}}
ssot=(root/'character-ssot.md').read_text(encoding='utf-8')
out['ssot_sections']=[line for line in ssot.splitlines() if line.startswith('## ') and line[3:4].isdigit()]
out['prompt_word_counts']={}
for number, end in [(28,29),(29,30)]:
    block=ssot.split(f'## {number}.',1)[1].split(f'## {end}.',1)[0]
    paragraph=next(line for line in block.splitlines() if line.startswith('P '))
    out['prompt_word_counts'][str(number)]=len(paragraph.split(': ',1)[1].split())
(root/'handoff-inspection.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
