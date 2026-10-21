"""Frozen 61-case evaluator. Execution success is never an automatic PASS."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path('qa/2026-10-16-corpus-audit')
EXPECTED = ({f'M-{n:02}' for n in range(1, 25)} |
            {f'V-{n:02}' for n in range(1, 29)} |
            {'VC-1', 'VC-2', 'VC-3', 'VP-1', 'VP-2', 'VS-1', 'VO-1', 'S1a', 'S1b'})
SERIES = 'omp-readonly-local-owner-v3'
MODEL = 'openai-codex/gpt-6.1-sol'
PARSER_PATH = Path(__file__).with_name('event_trace.py')


def parse_trace(wire_stdout, root):
    spec = importlib.util.spec_from_file_location('event_trace', PARSER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_trace(wire_stdout, root)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents overwriting previous attempts or metadata.
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def frozen_sources(root):
    records = []
    for line in (root / AUDIT / 'prompts.sha256').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([^\t]+)\t(\d+)B\tsha256=([0-9a-f]{64})', line)
        if not match:
            continue
        name, size, digest = match.groups()
        path = AUDIT / name
        data = (root / path).read_bytes()
        if len(data) != int(size) or sha(data) != digest:
            raise ValueError(f'Frozen source mismatch: {path}')
        records.append({'path': path.as_posix(), 'bytes': len(data), 'sha256': digest})
    if len(records) != 4:
        raise ValueError('Expected exactly four frozen source hashes')
    return records


def build_manifest(root):
    sources = frozen_sources(root)
    assertions = {}
    for name in ('baseline-matrix.md', 'baseline-matrix-vpa.md'):
        path = AUDIT / name
        for number, line in enumerate((root / path).read_text(encoding='utf-8').splitlines(), 1):
            match = re.match(r'\| ((?:M|V)-\d+|VC-\d+|VP-\d+|VS-\d+|VO-\d+) \|', line)
            if match:
                assertions[match[1]] = {'path': path.as_posix(), 'line': number, 'text': line}
    supplementary = AUDIT / 'baseline-prompts.md'
    for identifier, number in [('S1a', 32), ('S1b', 33)]:
        assertions[identifier] = {'path': supplementary.as_posix(), 'line': number,
                                 'text': (root / supplementary).read_text(encoding='utf-8').splitlines()[number - 1]}
    cases = []
    for name in ('baseline-prompts-exact.md', 'baseline-prompts.md'):
        path = AUDIT / name
        # bytes + keepends preserve CRLF and the newline immediately before closing fence.
        lines = (root / path).read_bytes().splitlines(keepends=True)
        identifier = None
        index = 0
        while index < len(lines):
            heading = re.match(rb'## ((?:M|V)-\d+|VC-\d+|VP-\d+|VS-\d+|VO-\d+|S1[ab])(?:[, ]|\r?$)', lines[index])
            if lines[index].startswith(b'## '):
                identifier = heading[1].decode() if heading else None
            if lines[index].rstrip(b'\r\n') == b'```text':
                start = index + 1
                end = start
                while end < len(lines) and lines[end].rstrip(b'\r\n') != b'```':
                    end += 1
                if end == len(lines) or identifier is None:
                    raise ValueError(f'Unaddressable text fence in {path}:{index + 1}')
                prompt = b''.join(lines[start:end])
                cases.append({'id': identifier, 'prompt': prompt.decode('utf-8'),
                              'prompt_sha256': sha(prompt), 'prompt_bytes': len(prompt),
                              'source': {'path': path.as_posix(), 'start_line': start + 1, 'end_line': end},
                              'assertion': assertions[identifier], 'evaluator': None})
                index = end
            index += 1
    result = {'schema': 1, 'series': SERIES, 'sources': sources, 'cases': cases}
    validate_manifest(result)
    return result


def validate_manifest(manifest):
    cases = manifest['cases']
    ids = [case['id'] for case in cases]
    if len(ids) != len(set(ids)) or set(ids) != EXPECTED:
        raise ValueError('Manifest must contain exactly the 61 unique frozen IDs; no Scoring')
    for case in cases:
        data = case['prompt'].encode('utf-8')
        if not data.strip() or sha(data) != case['prompt_sha256'] or len(data) != case['prompt_bytes']:
            raise ValueError(f'Invalid prompt bytes: {case["id"]}')
        if not case.get('assertion', {}).get('line'):
            raise ValueError(f'Missing assertion location: {case["id"]}')


def tree_fingerprint(root):
    """Fingerprint instruction/code inputs and skill assets, not archival doc images."""
    excluded = {'.git', 'qa', '__pycache__', '.pytest_cache', 'node_modules'}
    entries = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excluded)
        for name in sorted(files):
            path = Path(directory) / name
            relative = path.relative_to(root)
            if relative.parts[0] == 'docs' and path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
                continue  # Historical screenshots are not inputs to these text-only cases.
            if path.suffix in {'.pyc', '.pyo'}:
                continue
            entries.append((path.relative_to(root).as_posix(), sha(path.read_bytes())))
    return sha(json.dumps(entries, separators=(',', ':')).encode())


def identity(case, tree, profile):
    return sha(json.dumps({'prompt': case['prompt_sha256'], 'tree': tree,
                           'context': case_context(case), 'required_reads': required_reads(case),
                           'output_mode': 'json', 'parser_sha256': sha(PARSER_PATH.read_bytes()),
                           'profile': profile}, sort_keys=True).encode())


def classify(stdout, stderr, code, timed_out=False):
    text = stderr.lower()
    if timed_out:
        return 'timeout'
    for label, needles in [
        ('file-read-failure', ('readfail', 'cannot read', 'could not read', 'unable to read', 'enoent', 'file not found')),
        ('helper-error', ('helper_unknown_error', 'no model selected')),
        ('account-error', ('usage limit', 'quota exceeded', 'unauthorized', 'authentication failed')),
        ('transport-error', ('network error', 'mcp transport', 'connection refused')),
        ('permission-error', ('permission denied', 'access denied')),
        ('timeout', ('session timed out', 'maximum time exceeded', 'max-time exceeded')),
    ]:
        if any(needle in text for needle in needles):
            return label
    if code != 0:
        return 'nonzero-exit'
    if not stdout.strip():
        return 'blank-output'
    return 'completed'


def reusable(attempt, key):
    trace = attempt.get('structured_evidence', {})
    required = attempt.get('required_reads', [])
    observed = {read.get('local_path') for read in trace.get('reads', [])
                if read.get('success') and read.get('source_confirmed')}
    return (attempt.get('identity') == key and attempt.get('status') == 'completed'
            and attempt.get('exit_code') == 0 and bool(attempt.get('stdout', '').strip())
            and attempt.get('output_mode') == 'json' and bool(required)
            and trace.get('agent_completed') is True
            and not trace.get('tool_errors') and not trace.get('protocol_errors')
            and set(required) <= observed
            and trace.get('final_text') == attempt['stdout']
            and classify(attempt['stdout'], attempt.get('stderr', ''), 0) == 'completed')


def required_reads(case):
    if case.get('supplemental_required_reads'):
        return case['supplemental_required_reads']
    base = 'video-production-assets/references/'
    if case['id'] in {'S1a', 'M-03'}:
        names = ['16-concept-emotion-retention.md', '12-qa.md']
        if case['id'] == 'M-03':
            names += ['10-evidence.md', '17-genre-comedy.md']
        return [base + name for name in names]
    if case['id'] == 'S1b':
        return [base + '16-concept-emotion-retention.md']
    owner = case['assertion']['text'].split('|')[2].strip().strip('`')
    return [f'{owner}/SKILL.md' if case['id'].startswith('M-') else base + owner]



def case_context(case):
    """Load the checkout owner, not an unrelated globally installed skill."""
    common = (
        "Repository QA harness. Apply the frozen corpus common rules: one turn; "
        "read-only; hypothetical provider actions only; no generation, spending, "
        "upload, training, deployment or publication. Every craft claim needs "
        "an exact package file and section locator. The user request is replayed "
        "verbatim. Read the local checkout files rather than substituting global "
        "skills with similar names. "
    )
    if case.get('supplemental_required_reads'):
        paths = ', '.join(case['supplemental_required_reads'])
        return common + "Read only the checkout files expressly listed in the user request: " + paths + "."
    case_id = case['id']
    if case_id in {'S1a', 'M-03'}:
        return common + "Read only the package files expressly requested by the user; do not load another skill."
    if case_id == 'S1b':
        return common + "Start with video-production-assets/references/16-concept-emotion-retention.md and follow applicable package references."
    owner = case['assertion']['text'].split('|')[2].strip().strip('`')
    if case_id.startswith('M-'):
        target = f'{owner}/SKILL.md'
    else:
        target = f'video-production-assets/references/{owner}'
    return common + f"Before answering, read the exact assigned checkout file {target}, including when missing input requires an early stop; a blocker response does not waive that read. Then respond to the user's request. Read only additional references needed within the user's scope."


def execute(case, root, run_dir, profile, tree):
    key = identity(case, tree, profile)
    directory = run_dir / case['id']
    directory.mkdir(parents=True, exist_ok=True)
    for path in sorted(directory.glob('attempt-*.json')):
        previous = json.loads(path.read_text(encoding='utf-8'))
        if reusable(previous, key):
            return previous
    command = [profile['executable'], '--mode', 'json', '--model', profile['model'], '--tools', 'read,grep,glob',
               '--no-lsp', '--no-extensions', '--no-skills', '--no-session', '--max-time', str(profile['max_time']),
               '--append-system-prompt', case_context(case), '-p', case['prompt']]
    start = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = process.communicate(timeout=profile['max_time'] + 15)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            else:
                process.kill()
            out, err = process.communicate()
        code = process.returncode
    except OSError as error:
        out, err, code = b'', str(error).encode(), None
    wire_stdout, stderr = out.decode('utf-8', errors='replace'), err.decode('utf-8', errors='replace')
    trace = parse_trace(wire_stdout, root)
    stdout = trace['final_text']
    required = required_reads(case)
    observed = {read.get('local_path') for read in trace['reads']
                if read.get('success') and read.get('source_confirmed')}
    missing = sorted(set(required) - observed)
    after = tree_fingerprint(root)
    status = classify(stdout, stderr, code, timed_out)
    if status in {'completed', 'blank-output'}:
        if trace['tool_errors']:
            status = 'tool-error'
        elif trace['protocol_errors'] or not trace['agent_completed']:
            status = 'protocol-error'
        elif missing:
            status = 'checkout-read-missing'
    if after != tree:
        status = 'tree-mutated'
    number = 1
    while (directory / f'attempt-{number:04}.json').exists():
        number += 1
    # Raw bytes survive decoding errors; never silently normalize original output.
    stem = directory / f'attempt-{number:04}'
    with stem.with_suffix('.stdout').open('xb') as handle:
        handle.write(out)
    with stem.with_suffix('.stderr').open('xb') as handle:
        handle.write(err)
    record = {'case_id': case['id'], 'identity': key, 'prompt': case['prompt'],
              'prompt_sha256': case['prompt_sha256'], 'tree_before': tree, 'tree_after': after,
              'profile': profile, 'command': command, 'stdout': stdout, 'stderr': stderr,
              'output_mode': 'json', 'structured_evidence': trace,
              'tool_reads': trace['reads'], 'tool_errors': trace['tool_errors'],
              'protocol_errors': trace['protocol_errors'], 'external_reads': trace['external_reads'],
              'required_reads': required, 'missing_required_reads': missing,
              'exit_code': code, 'duration_seconds': time.monotonic() - start,
              'started_at': started_at,
              'status': status, 'verdict': 'UNREVIEWED' if status == 'completed' else 'ERROR',
              'assertion': case['assertion'], 'evaluator': None, 'evidence': [],
              'recorded_at': datetime.now(timezone.utc).isoformat()}
    save(stem.with_suffix('.json'), record)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path)
    parser.add_argument('--case', choices=sorted(EXPECTED))
    parser.add_argument('--build-manifest', action='store_true')
    parser.add_argument('--model', default=MODEL)
    args = parser.parse_args(argv)
    if args.build_manifest:
        save(args.manifest, build_manifest(ROOT))
        print('Frozen hashes verified; wrote 61 unique cases (59 + S1a/S1b).')
        return 0
    if args.run_dir is None:
        parser.error('--run-dir is required for execution')
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    validate_manifest(manifest)
    if manifest != build_manifest(ROOT):
        raise ValueError('Manifest does not match frozen source extraction')
    executable = shutil.which('omp')
    if not executable:
        raise RuntimeError('omp executable not found')
    version = subprocess.run([executable, '--version'], capture_output=True, check=True).stdout.decode().strip()
    profile = {'series': SERIES, 'model': args.model, 'executable': executable, 'version': version,
               'tools': ['read', 'grep', 'glob'], 'max_time': 180, 'concurrency': 1,
               'no_lsp': True, 'no_extensions': True, 'no_skills': True,
               'context_policy': 'frozen-common-rules+explicit-checkout-owner-v3',
               'tree_policy': 'code+instructions+skill-assets; excludes QA/cache and archival docs images',
               'runner_sha256': sha(Path(__file__).read_bytes()),
               'parser_sha256': sha(PARSER_PATH.read_bytes()), 'output_mode': 'json',
               'environment': {key: value for key, value in os.environ.items()
                               if key in {'OMP_PROFILE', 'PI_CODING_AGENT_DIR', 'PI_PACKAGE_DIR'}}}
    tree = tree_fingerprint(ROOT)
    metadata = {'tree': tree, 'profile': profile, 'manifest_sha256': sha(args.manifest.read_bytes()),
                'side_effect_policy': 'read/grep/glob only; no provider actions; no automatic PASS'}
    args.run_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = args.run_dir / 'metadata.json'
    if metadata_path.exists():
        if json.loads(metadata_path.read_text(encoding='utf-8')) != metadata:
            raise ValueError('Run identity changed: use a new run directory')
    else:
        save(metadata_path, metadata)
    errors = 0
    for case in manifest['cases']:
        if args.case and case['id'] != args.case:
            continue
        if tree_fingerprint(ROOT) != tree:
            raise RuntimeError('Tree changed; stop and start a new series directory')
        result = execute(case, ROOT, args.run_dir, profile, tree)
        print(f'{case["id"]}: {result["status"]}; {result["verdict"]}', flush=True)
        errors += result['status'] != 'completed'
        if result['status'] == 'tree-mutated':
            break
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
