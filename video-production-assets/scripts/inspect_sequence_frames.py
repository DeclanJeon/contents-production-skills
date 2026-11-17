#!/usr/bin/env python3
"""Extract real plan/source/export comparison material without judging it."""
import argparse
import json
from pathlib import Path
from sequence_contract import SequenceError, read_document, read_projection
from sequence_media import inspect_sequence_frames


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('projection', type=Path)
    parser.add_argument('--output', required=True, help='new directory inside project root')
    parser.add_argument('--mode', choices=('plan', 'source', 'export'), default='plan')
    args = parser.parse_args()
    try:
        result = inspect_sequence_frames(read_document(args.project), read_projection(args.projection),
                                   args.project.resolve().parent, args.output, args.mode)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (SequenceError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'failed', 'quality': 'unverified', 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
