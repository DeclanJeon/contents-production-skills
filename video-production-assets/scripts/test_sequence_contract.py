"""Frame/path contracts; these tests do not judge media meaning."""
from fractions import Fraction
import hashlib
import json

import pytest

from sequence_contract import (FrameSpan, SequenceError, checked_assets, frame_at,
                               parse_fps, project_file, read_projection)


def test_half_open_span_maps_last_included_frame():
    # Given / When
    span = FrameSpan(24, 72)
    # Then
    assert (span.length, span.last) == (48, 71)


@pytest.mark.parametrize('start,end', [(True, 2), (-1, 3), (2, 2), (3, 2), (0, 1.5)])
def test_invalid_span_is_rejected(start, end):
    # Given / When / Then
    with pytest.raises(SequenceError):
        FrameSpan(start, end)


def test_fractional_fps_preserves_frame_boundaries():
    # Given
    fps = parse_fps({'num': 24000, 'den': 1001})
    # When / Then
    assert frame_at(Fraction(1001, 24000) * 1000, fps) == 1000


@pytest.mark.parametrize('fps', [True, 0, -24, float('nan'), {'num': 24, 'den': 0}])
def test_invalid_fps_is_not_a_time_basis(fps):
    # Given / When / Then
    with pytest.raises(SequenceError):
        parse_fps(fps)


def test_fractional_frame_time_is_not_silently_rounded():
    # Given / When / Then
    with pytest.raises(SequenceError):
        frame_at(0.01, Fraction(24))


def test_symlink_cannot_escape_project(tmp_path):
    # Given
    root = tmp_path / 'project'; root.mkdir()
    outside = tmp_path / 'outside'; outside.write_text('private')
    (root / 'link').symlink_to(outside)
    # When / Then
    with pytest.raises(SequenceError, match='outside_root'):
        project_file(root, 'link')


def test_asset_bytes_must_match_registered_hash(tmp_path):
    # Given
    path = tmp_path / 'a.bin'; path.write_bytes(b'changed')
    p = {'asset_registry': [{'id': 'AS1', 'version': '1', 'status': 'available',
          'path': 'a.bin', 'sha256': hashlib.sha256(b'original').hexdigest()}]}
    # When / Then
    with pytest.raises(SequenceError, match='asset_hash'):
        checked_assets(p, tmp_path, ['AS1'])


def test_duplicate_asset_identity_is_rejected(tmp_path):
    # Given
    row = {'id': 'AS1', 'version': '1', 'status': 'planned'}
    # When / Then
    with pytest.raises(SequenceError, match='duplicate'):
        checked_assets({'asset_registry': [row, row]}, tmp_path, ['AS1'])


def test_projection_parser_requires_versioned_format(tmp_path):
    # Given
    f = tmp_path / 'p.json'; f.write_text(json.dumps({'format': 'invented'}))
    # When / Then
    with pytest.raises(SequenceError, match='projection_format'):
        read_projection(f)
