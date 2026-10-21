"""Replay new normal/boundary smoke scenarios; never count them among the frozen 61."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import run_cases as runner


def case_for(scenario, manifest):
    prompt = scenario['prompt']
    return {'id':'M-NORMAL-'+scenario['id'],'prompt':prompt,
        'prompt_sha256':hashlib.sha256(prompt.encode('utf-8')).hexdigest(),
        'supplemental_required_reads':scenario['required_reads'],
        'assertion':{'path':str(manifest),'line':None,
            'text':f"| supplemental | {scenario['owner']} | Explicit owner, not a frozen case |"}}

def select_scenarios(scenarios, requested_ids):
    if requested_ids is None:
        return scenarios
    ids = [scenario['id'] for scenario in scenarios]
    if len(requested_ids) != len(set(requested_ids)):
        raise ValueError('Requested supplemental IDs must be unique')
    unknown = set(requested_ids) - set(ids)
    if unknown:
        raise ValueError(f'Unknown supplemental IDs: {sorted(unknown)}')
    selected = set(requested_ids)
    return [scenario for scenario in scenarios if scenario['id'] in selected]


def parse_max_time(value):
    try:
        seconds = int(value)
    except ValueError as exc:
        raise ValueError('Maximum time must be a positive integer') from exc
    if seconds <= 0:
        raise ValueError('Maximum time must be a positive integer')
    return seconds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--shard', type=int, choices=range(3), required=True)
    parser.add_argument('--only', nargs='+', help='run only these scenario IDs; bypass shard selection')
    parser.add_argument('--max-time', type=parse_max_time, default=300,
        help='maximum seconds per case (default: 300)')
    args = parser.parse_args()
    payload = json.loads(args.manifest.read_text(encoding='utf-8'))
    scenarios = payload['scenarios']
    ids = [case['id'] for case in scenarios]
    if len(ids) != len(set(ids)):
        raise ValueError('Supplemental IDs must be unique')
    scenarios = select_scenarios(scenarios, args.only)
    executable = shutil.which('omp')
    if not executable:
        raise RuntimeError('omp executable not found')
    version = subprocess.run([executable, '--version'], capture_output=True, check=True).stdout.decode().strip()
    profile = {'series':'supplemental-normal-v1', 'model':runner.MODEL,
        'executable':executable,'version':version,'max_time':args.max_time,
        'tools':['read','grep','glob'],'no_lsp':True,'no_extensions':True,'no_skills':True,
        'output_mode':'json','context_policy':'explicit-checkout-owner; same read-only safety as formal, new user scenarios',
        'runner_sha256':runner.sha(Path(runner.__file__).read_bytes()),
        'parser_sha256':runner.sha(runner.PARSER_PATH.read_bytes()),
        'supplemental_runner_sha256':runner.sha(Path(__file__).read_bytes()),
        'supplemental_manifest_sha256':runner.sha(args.manifest.read_bytes()),
        'environment':{key:value for key,value in os.environ.items() if key in {'OMP_PROFILE','PI_CODING_AGENT_DIR','PI_PACKAGE_DIR'}}}
    tree = runner.tree_fingerprint(runner.ROOT)
    args.run_dir.mkdir(parents=True,exist_ok=True)
    metadata = {'tree':tree,'profile':profile,'shard':args.shard,
        'scope':'Supplemental only. No frozen-case denominator or automatic PASS.',
        'side_effect_policy':'read/grep/glob only; no paid creation/upload/train/deploy/publish'}
    metadata_path = args.run_dir/'metadata.json'
    if metadata_path.exists() and json.loads(metadata_path.read_text(encoding='utf-8')) != metadata:
        raise ValueError('Supplemental identity changed; use a new run directory')
    runner.save(metadata_path,metadata)
    failures = 0
    for index, scenario in enumerate(scenarios):
        if args.only is None and index % 3 != args.shard:
            continue
        if runner.tree_fingerprint(runner.ROOT) != tree:
            raise RuntimeError('Tree changed; stop and start a new supplemental series')
        case = case_for(scenario, args.manifest)
        attempt = runner.execute(case,runner.ROOT,args.run_dir,profile,tree)
        seen = {item.get('local_path') for item in attempt['tool_reads']
                if item.get('success') and item.get('source_confirmed')}
        missing = sorted(set(scenario['required_reads'])-seen)
        status = attempt['status'] if attempt['status'] != 'completed' else 'checkout-read-missing' if missing else 'completed'
        result = {'scenario':scenario,'attempt':attempt,'missing_supplemental_reads':missing,
            'execution_status':status,'verdict':'UNREVIEWED' if status=='completed' else 'ERROR'}
        runner.save(args.run_dir/case['id']/'supplemental-result.json',result)
        print(f"{scenario['id']}: {status}; {result['verdict']}",flush=True)
        failures += status != 'completed'
        if status == 'tree-mutated':
            break
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
