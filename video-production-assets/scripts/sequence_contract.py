"""Shared boundary types for non-canonical sequence execution projections."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Final, Mapping, TypeAlias

Json: TypeAlias = str | int | float | bool | None | list['Json'] | dict[str, 'Json']
Document: TypeAlias = dict[str, Json]
FORMAT: Final = 'sequence-execution/1'
PHASES: Final = ('plan', 'generation', 'edit', 'export')


@dataclass(eq=False)
class SequenceError(ValueError):
    """Actionable error with a stable machine code and evidence location."""
    code: str
    locator: str
    detail: str

    def __str__(self) -> str:
        return f'{self.code}: {self.locator}: {self.detail}'


@dataclass(frozen=True, slots=True)
class FrameSpan:
    """Zero-based, start-inclusive/end-exclusive display-frame interval."""
    start: int
    end: int

    def __post_init__(self) -> None:
        if type(self.start) is not int or type(self.end) is not int or self.start < 0 or self.end <= self.start:
            raise SequenceError('frame_span', 'frames', 'expected nonnegative integer [in,out)')

    @property
    def length(self) -> int:
        return self.end - self.start

    @property
    def last(self) -> int:
        return self.end - 1


def number(value: Json | Fraction, locator: str) -> Fraction:
    """Parse a finite number without admitting bool or numeric strings."""
    if isinstance(value, Fraction):
        return value
    if type(value) not in (int, float) or not math.isfinite(value):
        raise SequenceError('number', locator, 'expected finite number, not bool/string')
    return Fraction(str(value))


def parse_fps(value: Json) -> Fraction:
    """Preserve rational FPS; never conflate 24, 25 and 24000/1001."""
    if isinstance(value, dict):
        n, d = value.get('num'), value.get('den')
        if type(n) is not int or type(d) is not int or n <= 0 or d <= 0:
            raise SequenceError('fps', 'time_basis', 'num/den must be positive integers')
        return Fraction(n, d)
    fps = number(value, 'fps').limit_denominator(1_000_000)
    if fps <= 0:
        raise SequenceError('fps', 'time_basis', 'FPS must be positive')
    return fps


def frame_at(seconds: Json | Fraction, fps: Fraction) -> int:
    """Convert only frame-aligned seconds, allowing serialized float noise."""
    frames = number(seconds, 'seconds') * fps
    nearest = round(frames)
    if frames < 0 or abs(frames - nearest) > Fraction(1, 100000):
        raise SequenceError('frame_alignment', 'seconds', 'time is not a nonnegative frame boundary')
    return nearest


def table(project: Mapping[str, Json], key: str) -> dict[str, Document]:
    """Index canonical rows once and reject duplicate/malformed identities."""
    rows = project.get(key, [])
    if not isinstance(rows, list):
        raise SequenceError('table', key, 'expected array')
    result = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip():
            raise SequenceError('identity', key, 'each row needs a nonempty id')
        if row['id'] in result:
            raise SequenceError('duplicate', key, row['id'])
        result[row['id']] = row
    return result


def predecessor_cuts(projection: Mapping[str, Json], link: Mapping[str, Json], *, for_generation: bool = False) -> list[Document]:
    """Resolve the adjacent and historical sources, with a narrow generation exception."""
    cuts = projection['cuts']
    by_cut = {cut['cut_id']: cut for cut in cuts}
    primary = by_cut.get(link.get('from_cut_id'))
    target = by_cut.get(link.get('to_cut_id'))
    if primary is None or target is None:
        raise SequenceError('predecessor_selection', str(link.get('key')), 'known source and target cuts required')
    history = link.get('history_shot_ids', [])
    if not isinstance(history, list) or not all(isinstance(sid, str) for sid in history):
        raise SequenceError('history_reference', str(link.get('key')), 'historical shot IDs required')
    independence = link.get('generation_independence')
    if for_generation and independence is not None:
        if (not isinstance(independence, dict)
                or not all(isinstance(independence.get(k), str) and independence[k].strip()
                           for k in ('reason', 'source_locator'))
                or link.get('relation') not in ('cross_cut', 'intentional_discontinuity')
                or link.get('state_out') != {} or link.get('state_in') != {}):
            raise SequenceError('generation_independence', str(link.get('key')),
                                'requires sourced independence, a cross-cut/discontinuity and no shared boundary state')
        result: dict[str, Document] = {}
    else:
        result = {primary['cut_id']: primary}
    for sid in history:
        matches = [cut for cut in cuts if cut['shot_id'] == sid]
        if not matches or sid == target['shot_id']:
            raise SequenceError('history_reference', sid, 'history must resolve to another selected narrative source, not the current shot')
        for cut in matches:
            result[cut['cut_id']] = cut
    return list(result.values())


def project_file(root: Path, value: str, *, must_exist: bool = True) -> Path:
    """Resolve paths, including symlinks, inside the explicit project root."""
    if not isinstance(value, str) or not value.strip():
        raise SequenceError('path', 'file', 'expected nonempty path')
    base = root.resolve()
    path = (base / value).resolve()
    if not path.is_relative_to(base):
        raise SequenceError('outside_root', value, 'path escapes project root')
    if must_exist and not path.is_file():
        raise SequenceError('file_missing', value, 'expected readable regular file')
    return path


def file_hash(path: Path) -> str:
    """Hash without loading a potentially large video into memory."""
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def checked_assets(project: Mapping[str, Json], root: Path, ids: list[str]) -> dict[str, Path]:
    """Require actual registered bytes; neither planned paths nor URLs qualify."""
    assets = table(project, 'asset_registry')
    result = {}
    for aid in ids:
        row = assets.get(aid)
        if row is None or row.get('status') not in ('available', 'verified'):
            raise SequenceError('asset_unavailable', aid, 'actual available/verified asset required')
        path = project_file(root, row.get('path'))
        expected = row.get('sha256')
        if not isinstance(expected, str) or file_hash(path) != expected:
            raise SequenceError('asset_hash', aid, 'registered SHA256 does not match actual bytes')
        result[aid] = path
    return result


def _parse_document(raw: bytes, path: Path) -> Document:
    """Parse one UTF-8 snapshot with the existing finite JSON semantics."""
    def invalid_constant(token: str) -> None:
        raise SequenceError('json_number', str(path), f'invalid constant {token}')
    def finite_float(token: str) -> float:
        value = float(token)
        if not math.isfinite(value):
            raise SequenceError('json_number', str(path), 'floating-point overflow')
        return value
    value = json.loads(raw.decode('utf-8'), parse_constant=invalid_constant, parse_float=finite_float)
    if not isinstance(value, dict):
        raise SequenceError('json_object', str(path), 'expected JSON object')
    return value


def check_projection(value: Document, path: Path) -> Document:
    """Recognize the derived format, including for in-memory display callers."""
    if value.get('format') != FORMAT or value.get('phase') not in PHASES:
        raise SequenceError('projection_format', str(path), f'expected {FORMAT} and known phase')
    for key in ('owner', 'inputs', 'time_basis'):
        if not isinstance(value.get(key), dict):
            raise SequenceError('projection_shape', key, 'expected object')
    for key in ('requirements', 'links', 'cuts', 'checks'):
        if not isinstance(value.get(key), list) or not all(isinstance(row, dict) for row in value[key]):
            raise SequenceError('projection_shape', key, 'expected array of objects')
    return value


def read_snapshot(path: Path, *, projection: bool = False) -> tuple[Document, Document]:
    """Bind the parsed document and SHA256 to exactly the same raw read."""
    raw = path.read_bytes()
    value = _parse_document(raw, path)
    if projection:
        check_projection(value, path)
    return value, {'path': str(path.resolve()), 'sha256': hashlib.sha256(raw).hexdigest()}


def read_document(path: Path) -> Document:
    """Parse a JSON object and reject nonstandard NaN/Infinity tokens."""
    return read_snapshot(path)[0]


def read_projection(path: Path) -> Document:
    """Read only a full execution projection, never a display view."""
    return read_snapshot(path, projection=True)[0]
