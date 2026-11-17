"""Measure actual returned content, never infer consumption from a path."""
from pathlib import Path
import hashlib

import pytest


def metrics():
    import skill_loading_metrics
    return skill_loading_metrics


def events(path: str, text: str | None, *, error: bool = False, truncated: bool = False):
    result = {} if text is None else {'content': [{'type': 'text', 'text': text}]}
    result['details'] = {'truncated': truncated}
    return [
        {'type': 'tool_execution_start', 'toolCallId': 'R1', 'toolName': 'read', 'args': {'path': path}},
        {'type': 'tool_execution_end', 'toolCallId': 'R1', 'toolName': 'read', 'isError': error, 'result': result},
    ]


def test_repeated_file_read_is_not_hidden_by_unique_total(tmp_path: Path):
    # Given
    (tmp_path / 'guide.md').write_text('hello world')
    # When
    result = metrics().measure_files(tmp_path, ['guide.md', 'guide.md'])
    # Then
    assert result['status'] == 'measured'
    assert result['total_tokens'] == 4
    assert result['unique_tokens'] == 2


def test_raw_hash_and_normalized_text_are_distinguished(tmp_path: Path):
    # Given
    raw = b'hello\r\nworld\r\n'; (tmp_path / 'guide.md').write_bytes(raw)
    # When
    result = metrics().measure_files(tmp_path, ['guide.md'])
    # Then
    assert result['files'][0]['sha256'] == hashlib.sha256(raw).hexdigest()
    assert result['files'][0]['characters'] == len('hello\nworld\n')


def test_actual_returned_excerpt_is_measured_not_current_file(tmp_path: Path):
    # Given
    (tmp_path / 'guide.md').write_text('a different file, much longer than the returned excerpt')
    # When
    result = metrics().measure_read_events(events('guide.md', 'hello world'), tmp_path)
    # Then
    assert result['total_tokens'] == 2
    assert result['reads'][0]['coverage'] == 'full_return'


@pytest.mark.parametrize('error,truncated,text', [(True, False, 'hello'), (False, False, None),
                                                (False, True, 'hello')])
def test_missing_failed_or_truncated_read_does_not_certify_consumption(tmp_path: Path, error, truncated, text):
    # Given
    wire = events('guide.md', text, error=error, truncated=truncated)
    # When
    result = metrics().measure_read_events(wire, tmp_path)
    # Then
    assert result['status'] == 'unverified'
    assert result['issues']


def test_unmatched_tool_end_is_not_a_successful_read(tmp_path: Path):
    # Given / When
    result = metrics().measure_read_events(events('guide.md', 'hello')[1:], tmp_path)
    # Then
    assert result['status'] == 'unverified'
    assert result['total_tokens'] == 0


def test_repeated_returned_chunk_has_separate_total_and_unique_counts(tmp_path: Path):
    # Given
    first = events('guide.md', 'hello world'); second = events('guide.md', 'hello world')
    for row in second:
        row['toolCallId'] = 'R2'
    # When
    result = metrics().measure_read_events(first + second, tmp_path)
    # Then
    assert result['total_tokens'] == 4
    assert result['unique_tokens'] == 2
    assert len(result['reads']) == 2


@pytest.mark.parametrize('from_events', [False, True])
def test_outside_root_is_rejected(tmp_path: Path, from_events: bool):
    # Given
    module = metrics()
    # When / Then
    with pytest.raises(module.MeasurementError, match='outside_root'):
        if from_events:
            module.measure_read_events(events('../private.md', 'secret'), tmp_path)
        else:
            module.measure_files(tmp_path, ['../private.md'])


def test_unavailable_tokenizer_returns_blocker_without_download(tmp_path: Path, monkeypatch):
    # Given
    module = metrics(); (tmp_path / 'guide.md').write_text('hello')
    monkeypatch.setenv('TIKTOKEN_CACHE_DIR', str(tmp_path / 'absent-cache'))
    # When
    result = module.measure_files(tmp_path, ['guide.md'])
    # Then
    assert result['status'] == 'blocked'
    assert not (tmp_path / 'absent-cache').exists()
