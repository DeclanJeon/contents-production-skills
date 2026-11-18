# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest", "pillow"]
# ///
# How to run: python3 benchmark_validation.py --repo <repo> --output <results.json>
"""Instrument real local validation of synthetic clips; never call a provider.

Wrappers count actual file hashing and ffprobe commands without replacing results.
Small synthetic fixtures do not predict production-video speed or model costs.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo.resolve() / 'video-production-assets/scripts'))
    import generation_handoff
    import sequence_contract
    import sequence_media
    from av_handoff_test_fixture import (prepared_handoff, prepared_history_handoff,
                                         add_history_bindings)
    from validate_sequence import validate_sequence

    rows = []
    for history in (False, True):
        with tempfile.TemporaryDirectory(prefix='skills-audit-', dir=Path.home() / '.cache') as temp:
            root = Path(temp)
            if history:
                project, projection = prepared_history_handoff(root)
                add_history_bindings(project, projection, root)
            else:
                project, projection = prepared_handoff(root)
            runs = []
            for _ in range(3):
                probes: list[str] = []
                probe_commands: list[tuple[str, ...]] = []
                hashes: list[str] = []
                real_run = sequence_media._run
                real_hash = sequence_contract.file_hash

                def observe_run(command: list[str]):
                    if command[0] == 'ffprobe':
                        probes.append(command[-1])
                        probe_commands.append(tuple(command))
                    return real_run(command)

                def observe_hash(path: Path) -> str:
                    hashes.append(str(path))
                    return real_hash(path)

                started = time.perf_counter()
                with patch.object(sequence_media, '_run', observe_run), \
                     patch.object(generation_handoff, '_run', observe_run), \
                     patch.object(sequence_contract, 'file_hash', observe_hash):
                    result = validate_sequence(project, projection, 'generation', root)
                elapsed = time.perf_counter() - started
                if not result['ready']:
                    raise RuntimeError(json.dumps(result['blockers']))
                runs.append({'elapsed_s': round(elapsed, 6), 'ffprobe_calls': len(probes),
                    'ffprobe_distinct_paths': len(set(probes)),
                    'ffprobe_distinct_commands': len(set(probe_commands)),
                    'ffprobe_duplicate_calls': len(probe_commands) - len(set(probe_commands)),
                    'hash_calls': len(hashes), 'hash_distinct_paths': len(set(hashes)),
                    'bytes_hashed': sum(Path(path).stat().st_size for path in hashes),
                    'distinct_bytes_hashed': sum(Path(path).stat().st_size for path in set(hashes))})
            rows.append({'fixture': 'return_after_insert' if history else 'adjacent_predecessor',
                         'runs': runs, 'median_elapsed_s': statistics.median(run['elapsed_s'] for run in runs)})
    payload = {'scope': 'real local validation, three repeats each, synthetic 24fps clips; no provider calls',
               'python': sys.version, 'results': rows}
    args.output.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
