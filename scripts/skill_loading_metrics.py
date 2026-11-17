# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# How to run: import from an existing local Python environment; no installation.
"""Offline reference-token metrics; not billing or semantic compliance scores.

File metrics normalize CRLF/CR for text but fingerprint original bytes. Read
metrics count matched successful Pi text tool results, including repeated reads.
Their unique total deduplicates identical (path, returned-text) chunks, NOT
possibly overlapping spans. No file is reopened to reconstruct a tool result.
"""
from __future__ import annotations

import base64
from collections.abc import Sequence
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import tempfile
from typing import Final, Literal, Protocol, TypeAlias, TypedDict

Json: TypeAlias = str | int | float | bool | None | list['Json'] | dict[str, 'Json']
CACHE_URL: Final = 'https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken'
CACHE_SHA: Final = '446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d'
# Fixed official o200k_base pattern paired with the pinned ranks above.
O200K_PATTERN: Final = '|'.join((
    r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?",
    r"[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?",
    r'\p{N}{1,3}', r' ?[^\s\p{L}\p{N}]+[\r\n/]*',
    r'\s*[\r\n]+', r'\s+(?!\S)', r'\s+',
))


@dataclass(frozen=True, slots=True)
class MeasurementError(ValueError):
    code: str
    path: str

    def __str__(self) -> str:
        return f'{self.code}: {self.path}'


class Encoder(Protocol):
    def encode(self, text: str, *, disallowed_special: tuple[()] = ()) -> list[int]: ...


class FileMetric(TypedDict):
    path: str
    sha256: str
    characters: int
    tokens: int


class ReadMetric(TypedDict):
    path: str
    call_id: str
    returned_sha256: str
    characters: int
    tokens: int
    coverage: Literal['partial', 'full_return']


class Measurement(TypedDict):
    status: Literal['measured', 'unverified', 'blocked']
    tokenizer: str
    total_tokens: int
    unique_tokens: int
    files: list[FileMetric]
    reads: list[ReadMetric]
    issues: list[str]
    billing_tokens: None


def _empty() -> Measurement:
    return {'status': 'measured', 'tokenizer': 'o200k_base (reference, not host billing)',
            'total_tokens': 0, 'unique_tokens': 0, 'files': [], 'reads': [],
            'issues': [], 'billing_tokens': None}


def _encoder() -> Encoder:
    """Construct from one verified local snapshot; never call a fetch registry."""
    try:
        import tiktoken
    except ImportError as exc:
        raise MeasurementError('tokenizer_unavailable', 'tiktoken not installed') from exc
    cache_dir = os.environ.get('TIKTOKEN_CACHE_DIR', os.environ.get(
        'DATA_GYM_CACHE_DIR', str(Path(tempfile.gettempdir()) / 'data-gym-cache')))
    cache = Path(cache_dir) / hashlib.sha1(CACHE_URL.encode()).hexdigest()
    try:
        raw = cache.read_bytes() if cache_dir else b''
    except OSError as exc:
        raise MeasurementError('tokenizer_unavailable', str(cache)) from exc
    if hashlib.sha256(raw).hexdigest() != CACHE_SHA:
        raise MeasurementError('tokenizer_unavailable', 'verified local o200k_base cache required; no download')
    ranks = {base64.b64decode(token, validate=True): int(rank)
             for token, rank in (line.split() for line in raw.splitlines() if line)}
    return tiktoken.Encoding(name='o200k_base', pat_str=O200K_PATTERN,
        mergeable_ranks=ranks, special_tokens={'<|endoftext|>': 199999, '<|endofprompt|>': 200018})


def _path(root: Path, value: str) -> str:
    """Reject absolute and symlink escapes, including nonexistent leaf paths."""
    resolved_root = root.resolve()
    path = (resolved_root / value).resolve()
    if not path.is_relative_to(resolved_root):
        raise MeasurementError('outside_root', value)
    return path.relative_to(resolved_root).as_posix()


def _normalized(text: str) -> str:
    return text.replace('\r\n', '\n').replace('\r', '\n')


def measure_files(root: Path, relative_paths: Sequence[str]) -> Measurement:
    """Return a static file union and requested-read sum, not observed reads."""
    paths = [_path(root, value) for value in relative_paths]
    result = _empty()
    try:
        encoder = _encoder()
    except MeasurementError as exc:
        result.update(status='blocked', issues=[str(exc)])
        return result
    unique: dict[str, FileMetric] = {}
    for path in paths:
        if path not in unique:
            raw = (root / path).read_bytes()
            text = _normalized(raw.decode('utf-8'))
            row: FileMetric = {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
                               'characters': len(text), 'tokens': len(encoder.encode(text, disallowed_special=()))}
            unique[path] = row
            result['files'].append(row)
        result['total_tokens'] += unique[path]['tokens']
    result['unique_tokens'] = sum(row['tokens'] for row in unique.values())
    return result


def _text_result(value: Json) -> str | None:
    """Accept only a real returned text body, not read metadata or image data."""
    match value:
        case str():
            return value
        case {'content': list() as content}:
            parts = []
            for block in content:
                match block:
                    case {'type': 'text', 'text': str() as text}:
                        parts.append(text)
                    case _:
                        continue  # Open JSON wire boundary; other block types are not text.
            return '\n'.join(parts) if parts else None
        case _:
            return None  # Open JSON wire boundary, not a closed variant union.


def measure_read_events(events: Sequence[dict[str, Json]], root: Path) -> Measurement:
    """Measure matched Pi start/end read events; absent bodies stay unverified."""
    result = _empty()
    try:
        encoder = _encoder()
    except MeasurementError as exc:
        result.update(status='blocked', issues=[str(exc)])
        return result
    pending: dict[str, dict[str, Json]] = {}
    seen_chunks: set[tuple[str, str]] = set()
    for event in events:
        cid = str(event.get('toolCallId', ''))
        match event.get('type'):
            case 'tool_execution_start':
                if event.get('toolName') in ('read', 'functions.read', 'tools.read'):
                    pending[cid] = event
            case 'tool_execution_end':
                start = pending.pop(cid, None)
                if start is None:
                    if event.get('toolName') in ('read', 'functions.read', 'tools.read'):
                        result['issues'].append(f'{cid}: unmatched read result')
                    continue
                args = start.get('args')
                match args:
                    case {'path': str() as path}:
                        path = _path(root, path)
                    case _:
                        result['issues'].append(f'{cid}: read path unavailable')
                        continue
                text = _text_result(event.get('result'))
                if event.get('isError') or text is None:
                    result['issues'].append(f'{cid}: failed read or returned text unavailable')
                    continue
                text = _normalized(text)
                digest = hashlib.sha256(text.encode()).hexdigest()
                tokens = len(encoder.encode(text, disallowed_special=()))
                wire = event.get('result')
                partial = False
                match wire:
                    case {'details': {'truncated': True}} | {'truncated': True}:
                        partial = True
                    case _:
                        partial = 'Use offset' in text or '[Truncated' in text
                row: ReadMetric = {'call_id': cid, 'path': path, 'returned_sha256': digest,
                                   'characters': len(text), 'tokens': tokens,
                                   'coverage': 'partial' if partial else 'full_return'}
                result['reads'].append(row)
                result['total_tokens'] += tokens
                if (path, digest) not in seen_chunks:
                    result['unique_tokens'] += tokens
                    seen_chunks.add((path, digest))
                if partial:
                    result['issues'].append(f'{cid}: partial/truncated content; owner completeness unverified')
            case _:
                continue
    if pending or not result['reads']:
        result['issues'].append('unmatched reads or no measured returned text')
    if result['issues']:
        result['status'] = 'unverified'
    return result
