# /// script
# requires-python = ">=3.11"
# dependencies = ["tiktoken"]
# ///
# How to run: python3 audit_metrics.py --repo <repository> --output <directory>
"""Measure local skill text; o200k_base is a reference, not the host model tokenizer.

This is an audit evidence script, not a production-skill behavior validator.
Markdown reachability means links exist, not that a task must load all targets.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

import tiktoken


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--include-unlisted', action='store_true')
    args = parser.parse_args()
    root = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((root / 'manifest.json').read_text())
    encoder = tiktoken.get_encoding('o200k_base')

    def count(text: str) -> int:
        return len(encoder.encode(text, disallowed_special=()))

    skills = list(manifest['skills'])
    if args.include_unlisted:
        skills.extend(sorted(path.parent.name for path in root.glob('*/SKILL.md')
                             if path.parent.name not in skills))
    files: dict[str, str] = {}
    for skill in skills:
        for path in (root / skill).rglob('*.md'):
            rel = path.relative_to(root)
            if 'support' not in rel.parts:
                files[rel.as_posix()] = path.read_text()
    links: list[dict[str, str | bool | int]] = []
    rows: list[dict[str, str | int]] = []
    graph: dict[str, set[str]] = defaultdict(set)
    duplicates: dict[str, list[dict[str, str | int]]] = defaultdict(list)
    for relative, text in files.items():
        for match in re.finditer(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            href = match[1]
            if href.startswith(('https:', 'http:', 'mailto:', '#', 'data:')):
                continue
            raw = unquote(href.split('#', 1)[0])
            target = (root / relative).parent / raw
            target = target.resolve()
            target_rel = target.relative_to(root).as_posix() if target.is_relative_to(root) else str(target)
            links.append({'source': relative, 'line': text.count('\n', 0, match.start()) + 1,
                          'href': href, 'target': target_rel, 'exists': target.exists()})
            if target_rel in files:
                graph[relative].add(target_rel)
        for paragraph in re.split(r'\n\s*\n', text):
            normalized = re.sub(r'\s+', ' ', paragraph).strip()
            if len(normalized) >= 140 and not normalized.startswith(('```', '|', '---')):
                duplicates[normalized].append({'path': relative,
                    'line': text[:text.find(paragraph)].count('\n') + 1})
        paragraphs = re.split(r'\n\s*\n', text)
        front = text.split('---', 2)[1] if text.startswith('---\n') else ''
        rows.append({'path': relative, 'skill': relative.split('/')[0], 'lines': len(text.splitlines()),
                     'chars': len(text), 'bytes': (root / relative).stat().st_size, 'tokens': count(text),
                     'frontmatter_tokens': count(front), 'max_paragraph_tokens': max(map(count, paragraphs)),
                     'mandatory_markers': len(re.findall(r'\b(?:MUST|REQUIRED|MANDATORY)\b|필수|반드시|항상', text)),
                     'local_links': sum(1 for item in links if item['source'] == relative),
                     'sha256': hashlib.sha256((root / relative).read_bytes()).hexdigest(),
                     'normalized_text_sha256': hashlib.sha256(text.encode()).hexdigest()})
    file_metrics = {row['path']: row for row in rows}
    skill_rows = []
    for skill in skills:
        body = file_metrics[skill + '/SKILL.md']
        owned = [row for row in rows if row['skill'] == skill]
        seen: set[str] = set()
        pending = [skill + '/SKILL.md']
        while pending:
            path = pending.pop()
            if path in seen:
                continue
            seen.add(path)
            pending.extend(graph.get(path, set()) - seen)
        skill_rows.append({**body, 'manifest_listed': skill in manifest['skills'], 'markdown_files': len(owned),
            'all_markdown_tokens': sum(row['tokens'] for row in owned),
            'all_link_reachable_markdown_files': len(seen),
            'all_link_reachable_tokens': sum(file_metrics[path]['tokens'] for path in seen)})
    frontier = ['creative-production/SKILL.md', 'creative-production/references/routing.csv',
                'creative-production/references/routing-disambiguation.csv', 'creative-production/references/policy.md']
    route_rows = []
    for route in csv.DictReader(io.StringIO((root / frontier[1]).read_text())):
        paths = list(dict.fromkeys(frontier + [route['owner'] + '/SKILL.md'] +
                     [path.strip() for path in route['required_read'].split(';') if path.strip()]))
        route_rows.append({**route, 'explicit_first_read_paths': paths,
                           'explicit_first_read_tokens': sum(count((root / path).read_text()) for path in paths)})
    repeat_rows = [{'tokens': count(paragraph), 'occurrences': locations,
                    'avoidable_duplicate_tokens_if_shared': count(paragraph) * (len(locations) - 1),
                    'text': paragraph} for paragraph, locations in duplicates.items()
                   if len({str(item['path']) for item in locations}) > 1]
    result = {'reference_encoding': encoder.name, 'head': subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
        'scope': 'Manifest skills plus unlisted root skills when requested; Markdown excludes generated support payloads; live working tree',
        'manifest_skill_count': len(manifest['skills']),
        'caveats': ['Reference-encoding counts use universal-newline decoded text, not measured runtime/model cost or latency.',
                    'Explicit route first-read union excludes conditional/transitive references and project data.',
                    'All-link reachability is a structural upper envelope, not mandatory read volume.',
                    'Exact paragraph duplication misses paraphrases and may include useful local safety reminders.'],
        'skills': sorted(skill_rows, key=lambda row: int(row['tokens']), reverse=True),
        'files': sorted(rows, key=lambda row: int(row['tokens']), reverse=True),
        'links': links, 'missing_link_targets': [link for link in links if not link['exists']],
        'routes': sorted(route_rows, key=lambda row: int(row['explicit_first_read_tokens']), reverse=True),
        'exact_duplicate_paragraphs': sorted(repeat_rows,
            key=lambda row: int(row['avoidable_duplicate_tokens_if_shared']), reverse=True)}
    (output / 'metrics.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (output / 'skills.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(skill_rows[0]))
        writer.writeheader(); writer.writerows(result['skills'])
    print(json.dumps({'skills': len(skill_rows), 'markdown_files': len(rows),
        'skill_entry_tokens': sum(int(row['tokens']) for row in skill_rows),
        'markdown_tokens': sum(int(row['tokens']) for row in rows),
        'explicit_local_links': len(links), 'missing_link_targets': len(result['missing_link_targets']),
        'exact_repeated_paragraphs': len(repeat_rows), 'output': str(output)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
