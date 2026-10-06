"""Behavioral tests for production_history: storage layout, event
chronology, interruption/resume honesty, and path safety. Assertions
check what the user and orchestrator can observe (files, JSON output,
recorded prompts), not internal helpers."""
import hashlib
import os
import io
import json
import sys
import tempfile
import subprocess
import time
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import production_history as ph  # noqa: E402


def run_cli(argv):
    """Invoke the CLI exactly like a subprocess would; return (code, out)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = ph.main(argv)
    return code, out.getvalue(), err.getvalue()


def event_files(root):
    return sorted((Path(root) / '.history' / 'events').iterdir())


def event_names(root):
    return [p.name for p in event_files(root)]


class SlugTests(unittest.TestCase):
    def test_traversal_and_separator_inputs_rejected(self):
        for bad in ('../escape', 'a/b', 'a\\b', '..', '', '   ', '.'):
            with self.assertRaises(ph.UsageError, msg=bad):
                ph.slugify(bad, 'project_id')

    def test_reserved_windows_device_names_rejected(self):
        for bad in ('CON', 'con', 'PRN', 'aux', 'NUL', 'COM1', 'LPT9',
                    'nul.txt'):
            with self.assertRaises(ph.UsageError, msg=bad):
                ph.slugify(bad, 'project_id')

    def test_reasonable_ids_become_slugged(self):
        self.assertEqual(ph.slugify('My Project v1', 'project_id'),
                         'my-project-v1')
        self.assertEqual(ph.slugify('CH01_master', 'operation_id'),
                         'ch01_master')

    def test_unicode_project_names_kept_and_casefolded(self):
        self.assertEqual(ph.slugify('프로젝트 시연', 'project_id'),
                         '프로젝트-시연')
        self.assertEqual(ph.slugify('demo_프로젝트', 'project_id'),
                         'demo_프로젝트')
        # Casefold prevents case-only collisions on case-insensitive FS.
        self.assertEqual(ph.slugify('DemoFilm', 'project_id'),
                         ph.slugify('demofilm', 'project_id'))


class DocumentsTests(unittest.TestCase):
    def test_linux_uses_xdg_when_configured(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg = home / '.config'
            cfg.mkdir()
            (cfg / 'user-dirs.dirs').write_text(
                'XDG_DOCUMENTS_DIR="$HOME/Eigene Dokumente"\n',
                encoding='utf-8')
            got = ph.detect_documents(platform='linux', env={}, home=home)
            self.assertEqual(got, home / 'Eigene Dokumente')

    def test_linux_falls_back_to_home_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            got = ph.detect_documents(platform='linux', env={}, home=home)
            self.assertEqual(got, home / 'Documents')

    def test_darwin_uses_home_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(
                ph.detect_documents(platform='darwin', env={}, home=home),
                home / 'Documents')

    def test_win32_falls_back_without_known_folder_api(self):
        # On non-Windows CI, neither windll nor winreg resolve: honest
        # fallback is ~/Documents rather than a fabricated path.
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            if sys.platform != 'win32':
                got = ph.detect_documents(platform='win32', env={}, home=home)
                self.assertEqual(got, home / 'Documents')

    def test_env_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Elsewhere')}
            got = ph.detect_documents(platform='linux', env=env,
                                      home=Path('/nonexistent-home'))
            self.assertEqual(got, Path(tmp) / 'Elsewhere')


class InitTests(unittest.TestCase):
    def test_init_creates_full_v51_layout_and_reports_absolute_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = ph.initialize_project('Demo Film', documents=tmp)
            root = Path(result['project_root'])
            self.assertTrue(root.is_absolute())
            self.assertEqual(root, Path(tmp) / 'studio_production' / 'demo-film')
            for rel in ph.PACKAGE_DIRS:
                self.assertTrue((root / rel).is_dir(), rel)
            self.assertTrue((root / '.history' / 'events').is_dir())
            self.assertTrue((root / '.history' / 'prompts').is_dir())
            self.assertTrue((root / 'project.json').is_file())
            ledger = json.loads((root / 'project.json').read_text('utf-8'))
            self.assertEqual(ledger['project_id'], 'demo-film')
            for value in (result['project_root'], result['history_dir']):
                self.assertTrue(Path(value).is_absolute())

    def test_init_is_idempotent_and_preserves_existing_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = ph.initialize_project('demo', documents=tmp)
            root = Path(first['project_root'])
            (root / 'project.json').write_text(
                json.dumps({'project_id': 'demo', 'version': 'v007',
                            'scenes': [{'id': 'S01'}]}), encoding='utf-8')
            (root / '02_BIBLE' / 'style_world_bible.md').write_text('# bible')
            second = ph.initialize_project('demo', documents=tmp)
            ledger = json.loads((root / 'project.json').read_text('utf-8'))
            self.assertEqual(ledger['version'], 'v007')
            self.assertEqual(ledger['scenes'], [{'id': 'S01'}])
            self.assertIn('project.json', second['kept'])
            self.assertTrue((root / '02_BIBLE' / 'style_world_bible.md')
                            .read_text().startswith('# bible'))

    def test_init_refuses_root_owned_by_other_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Simulate reuse of a root whose ledger belongs to a different
            # project: same slug target, foreign project_id inside.
            first = ph.initialize_project('beta', documents=tmp)
            root = Path(first['project_root'])
            (root / 'project.json').write_text(
                json.dumps({'project_id': 'alpha'}), encoding='utf-8')
            with self.assertRaises(ph.UsageError):
                ph.initialize_project('beta', documents=tmp)
            # The foreign ledger is untouched.
            self.assertEqual(json.loads(
                (root / 'project.json').read_text('utf-8'))['project_id'],
                'alpha')


    def test_explicit_project_root_is_used_without_nested_default_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            selected = Path(tmp) / 'picked'
            selected.mkdir()
            original = selected / 'keep.txt'
            original.write_text('preserve')
            result = ph.initialize_project('chosen', project_root=selected)
            self.assertEqual(Path(result['project_root']), selected)
            self.assertTrue((selected / 'project.json').is_file())
            self.assertFalse((selected / 'studio_production').exists())
            self.assertEqual(original.read_text(), 'preserve')
            with self.assertRaises(ph.UsageError):
                ph.initialize_project('chosen', documents=tmp, project_root=selected)
            code, out, err = run_cli([
                'init', '--project-id', 'chosen', '--project-root', str(selected)])
            self.assertEqual(code, 0, err)
            self.assertEqual(Path(json.loads(out)['project_root']), selected)
            self.assertFalse((selected / 'studio_production').exists())
            ledger_bytes = (selected / 'project.json').read_bytes()
            code, _, err = run_cli([
                'init', '--project-id', 'chosen', '--project-root', str(selected),
                '--documents', tmp])
            self.assertEqual(code, 2)
            self.assertEqual((selected / 'project.json').read_bytes(), ledger_bytes)
            foreign = Path(tmp) / 'foreign'
            foreign.mkdir()
            foreign_ledger = foreign / 'project.json'
            foreign_bytes = b'{"project_id":"other"}'
            foreign_ledger.write_bytes(foreign_bytes)
            with self.assertRaises(ph.UsageError):
                ph.initialize_project('chosen', project_root=foreign)
            self.assertEqual(foreign_ledger.read_bytes(), foreign_bytes)

    def test_killed_init_before_atomic_publish_leaves_no_partial_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'selected'
            root.mkdir()
            ready = Path(tmp) / 'staged'
            script = (
                'import os, time\n'
                'from pathlib import Path\n'
                'import production_history as ph\n'
                'original_link = ph.os.link\n'
                'def pause_after_stage(source, destination):\n'
                '    if Path(destination).name == "project.json":\n'
                '        Path(os.environ["READY"]).write_text("ready")\n'
                '        while True: time.sleep(0.05)\n'
                '    return original_link(source, destination)\n'
                'ph.os.link = pause_after_stage\n'
                'ph.initialize_project("demo", project_root=os.environ["ROOT"])\n')
            env = os.environ.copy()
            env.update(ROOT=str(root), READY=str(ready),
                       PYTHONPATH=str(Path(__file__).resolve().parent))
            process = subprocess.Popen(
                [sys.executable, '-c', script],
                cwd=Path(__file__).resolve().parent, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            deadline = time.monotonic() + 10
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            if not ready.exists():
                process.kill()
                stdout, stderr = process.communicate(timeout=5)
                self.fail(f'child did not stage project.json: {stdout!r} {stderr!r}')
            process.kill()
            process.wait(timeout=5)
            self.assertFalse((root / 'project.json').exists())
            result = ph.initialize_project('demo', project_root=root)
            self.assertTrue((root / 'project.json').is_file())
            self.assertEqual(result['project_id'], 'demo')
    def test_traversal_project_id_never_escapes_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ph.UsageError):
                ph.initialize_project('../../outside', documents=tmp)
            self.assertFalse((Path(tmp).parent / 'outside').exists())


class ReadOnlyStatusTests(unittest.TestCase):
    def test_status_on_initialized_project_without_history_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'frozen-project'
            root.mkdir()
            (root / 'project.json').write_text(
                json.dumps({'schema_version': '1.1', 'project_id': 'frozen'}),
                encoding='utf-8')
            before = sorted(path.relative_to(root).as_posix()
                            for path in root.rglob('*'))
            code, out, err = run_cli(['status', '--project-root', str(root)])
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)['event_count'], 0)
            after = sorted(path.relative_to(root).as_posix()
                           for path in root.rglob('*'))
            self.assertEqual(after, before)


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        result = ph.initialize_project('demo', documents=self.tmp.name)
        self.root = Path(result['project_root'])
        self.prompt = Path(self.tmp.name) / 'prompt.txt'
        self.prompt.write_text(
            'Master shot of CH01 entering LOC02, rain, api_key=sekret123 '
            'sk-ABCDEFGH1234 keep this exact creative wording.',
            encoding='utf-8')

    def _record(self, status, op_id='op-shot01', extra=()):
        argv = ['record', '--project-root', str(self.root),
                '--operation', 'generate master shot SH01',
                '--prompt-file', str(self.prompt), '--status', status,
                '--operation-id', op_id, '--tool', 'imagen', '--model', 'm-4']
        argv += list(extra)
        code, out, err = run_cli(argv)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def test_record_writes_chronological_unique_events_with_full_prompt(self):
        first = self._record('started')
        out_path = self.root / '04_STORYBOARDS' / 'SHEET_001.png'
        out_path.write_bytes(b'png')  # real produced file
        second = self._record('completed',
                              extra=['--output', '04_STORYBOARDS/SHEET_001.png'])
        names = event_names(self.root)
        self.assertEqual(len(names), 2)
        self.assertEqual(sorted(names), names)  # filesystem order == time order
        self.assertTrue(names[0].startswith('000001-'))
        self.assertTrue(names[1].startswith('000002-'))
        self.assertIn('op-shot01-started.md', names[0])
        self.assertIn('op-shot01-completed.md', names[1])
        text = (Path(first['event']).read_text(encoding='utf-8'))
        # Actual creative prompt survives redaction.
        self.assertIn('keep this exact creative wording.', text)
        self.assertIn('Master shot of CH01 entering LOC02, rain', text)
        self.assertIn('[REDACTED]', text)
        self.assertNotIn('sk-ABCDEFGH1234', text)
        self.assertNotIn('sekret123', text)
        self.assertIn(hashlib.sha256(
            self.prompt.read_text('utf-8').encode('utf-8')).hexdigest(), text)
        self.assertIn('imagen', text)
        done = Path(second['event']).read_text(encoding='utf-8')
        self.assertIn('exists: true', done)
        # Output path is recorded JSON-escaped in front matter and raw in
        # the JSON result; assert the JSON result carries the real path.
        self.assertEqual(second['outputs'][0]['path'],
                         str(out_path.resolve()))
        self.assertIn(json.dumps(second['outputs'][0]['path']), done)
        # Recorded snapshot of the prompt is stored under .history/prompts.
        snaps = list((self.root / '.history' / 'prompts').iterdir())
        self.assertEqual(len(snaps), 2)
        self.assertIn('[REDACTED]', snaps[0].read_text(encoding='utf-8'))
        # The user's original prompt file is never modified.
        self.assertIn('sk-ABCDEFGH1234',
                      self.prompt.read_text(encoding='utf-8'))

    def test_output_traversal_rejected_relative_and_absolute(self):
        self._record('started')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-shot01',
            '--output', '../../outside/file.png'])
        self.assertEqual(code, 2)
        self.assertIn('escapes the project root', err)
        outside = Path(self.tmp.name) / 'elsewhere.txt'
        outside.write_text('x')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-shot01',
            '--output', str(outside)])
        self.assertEqual(code, 2)
        self.assertIn('escapes the project root', err)

    def test_completed_requires_declared_outputs_to_exist(self):
        self._record('started')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-shot01',
            '--output', '04_STORYBOARDS/missing.png'])
        self.assertEqual(code, 2)
        self.assertIn('do not exist', err)
        # Nothing was written; op is still in flight.
        self.assertEqual(len(event_files(self.root)), 1)

    def test_failed_may_record_missing_output(self):
        self._record('started')
        result = self._record('failed',
                              extra=['--output', '09_QA/missing.mp4'])
        self.assertEqual(result['status'], 'failed')
        text = Path(result['event']).read_text(encoding='utf-8')
        self.assertIn('exists: false', text)

    def test_terminal_without_started_is_rejected(self):
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-never'])
        self.assertEqual(code, 2)
        self.assertEqual(event_files(self.root), [])
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'failed',
            '--operation-id', 'op-never'])
        self.assertEqual(code, 2)
        self.assertEqual(len(event_files(self.root)), 0)

    def test_duplicate_started_while_in_flight_rejected(self):
        self._record('started')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.prompt), '--status', 'started',
            '--operation-id', 'op-shot01'])
        self.assertEqual(code, 2)
        self.assertIn('already in flight', err)
        self.assertEqual(len(event_files(self.root)), 1)

    def test_record_requires_initialized_project_and_real_prompt(self):
        with tempfile.TemporaryDirectory() as bare:
            code, out, err = run_cli([
                'record', '--project-root', bare, '--operation', 'x',
                '--prompt-file', str(self.prompt), '--status', 'started'])
            self.assertEqual(code, 2)
            self.assertIn('run init first', err)
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--prompt-file', str(self.root / 'missing.txt'),
            '--status', 'started'])
        self.assertEqual(code, 2)
        self.assertIn('does not exist', err)
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'x',
            '--status', 'started'])
        self.assertEqual(code, 2)
        self.assertIn('--prompt-file is required', err)

    def test_attempts_increment_on_restart_of_same_operation(self):
        first = self._record('started')
        self._record('failed')
        second = self._record('started')
        self.assertEqual(first['attempt'], 1)
        self.assertEqual(second['attempt'], 2)

    def test_project_lifecycle_start_does_not_consume_operation_attempt_number(self):
        self._record('started')
        self._record('failed')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'lifecycle', '--status', 'started',
            '--operation-id', 'op-shot01'])
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)['attempt'], 1)
        second = self._record('started')
        self.assertEqual(second['attempt'], 2)
        state = ph._status(self.root)
        self.assertEqual(state['operations']['op-shot01']['attempts'], 2)
        self.assertEqual(state['operations']['op-shot01']['current_attempt'], 2)
        self.assertTrue(any(row['operation'] == 'lifecycle' for row in state['lifecycle']))

    def test_original_prompt_bytes_hash_and_spaced_secret_redaction(self):
        for index, newline in enumerate((b'\n', b'\r\n')):
            raw = b'{"password": "my fake secret with spaces", "scene": "rainy alley"}' + newline
            self.prompt.write_bytes(raw)
            started = self._record('started', op_id=f'op-prompt{index}',
                                   extra=['--attempt', '7'])
            text = Path(started['event']).read_bytes().decode('utf-8')
            snapshot = max((self.root / '.history' / 'prompts').glob('*'),
                           key=lambda path: path.stat().st_mtime_ns)
            stored = snapshot.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            self.assertIn(f'prompt_sha256: "{digest}"', text)
            self.assertIn('[REDACTED]', text)
            self.assertNotIn('my fake secret', text)
            self.assertIn('rainy alley', text)
            self.assertIn(b'[REDACTED]', stored)
            self.assertNotIn(b'my fake secret', stored)
            self.assertIn(b'rainy alley', stored)
            self.assertEqual(self.prompt.read_bytes(), raw)

    def test_history_prompt_junction_is_rejected_before_external_write(self):
        with tempfile.TemporaryDirectory() as outside:
            prompts = self.root / '.history' / 'prompts'
            prompts.rmdir()
            sentinel = Path(outside) / 'sentinel.txt'
            sentinel.write_text('unchanged')
            try:
                os.symlink(outside, prompts, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"directory symlink unavailable: {exc}")
            code, _, err = run_cli([
                'record', '--project-root', str(self.root), '--operation', 'test',
                '--prompt-file', str(self.prompt), '--status', 'started',
                '--operation-id', 'op-path'])
            self.assertEqual(code, 2)
            self.assertIn('symlink or junction', err)
            self.assertEqual(sentinel.read_text(), 'unchanged')
            self.assertEqual(list(Path(outside).iterdir()), [sentinel])

    def test_history_root_events_and_lock_junctions_are_rejected(self):
        for target_name in ('history', 'events', 'lock'):
            with self.subTest(target=target_name), tempfile.TemporaryDirectory() as outside, \
                    tempfile.TemporaryDirectory() as project_docs:
                root = Path(ph.initialize_project(
                    'boundary', documents=project_docs)['project_root'])
                history = root / '.history'
                sentinel = Path(outside) / 'sentinel.txt'
                sentinel.write_text('unchanged', encoding='utf-8')
                is_directory = target_name != 'lock'
                if target_name == 'history':
                    (history / 'events').rmdir()
                    (history / 'prompts').rmdir()
                    history.rmdir()
                    destination = history
                elif target_name == 'events':
                    destination = history / 'events'
                    destination.rmdir()
                else:
                    destination = history / ph.LOCK_NAME
                try:
                    os.symlink(outside if is_directory else sentinel, destination,
                               target_is_directory=is_directory)
                except (OSError, NotImplementedError) as exc:
                    self.skipTest(f"directory symlink unavailable: {exc}")
                code, _, err = run_cli([
                    'record', '--project-root', str(root), '--operation', 'boundary',
                    '--prompt-file', str(self.prompt), '--status', 'started'])
                self.assertNotEqual(code, 0, err)
                self.assertIn('symlink or junction', err)
                self.assertEqual(sentinel.read_text(encoding='utf-8'), 'unchanged')
                self.assertEqual(list(Path(outside).iterdir()), [sentinel])
    def test_operation_description_and_explicit_attempt_survive_resume(self):
        operation = 'render "SH01"\nwith exact wording'
        argv = ['record', '--project-root', str(self.root), '--operation', operation,
                '--prompt-file', str(self.prompt), '--status', 'started',
                '--operation-id', 'op-roundtrip', '--attempt', '7']
        code, out, err = run_cli(argv)
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)['attempt'], 7)
        code, _, err = run_cli(['resume', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        code, out, err = run_cli(['status', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        row = json.loads(out)['operations']['op-roundtrip']
        self.assertEqual(row['operation'], operation)
        self.assertEqual(row['current_attempt'], 7)

    def test_default_terminal_uses_explicit_started_attempt(self):
        started = self._record('started', extra=['--attempt', '7'])
        completed = self._record('completed')
        self.assertEqual((started['attempt'], completed['attempt']), (7, 7))
        code, out, err = run_cli(['status', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        state = json.loads(out)['operations']['op-shot01']
        self.assertEqual(state['state'], 'completed')
        self.assertEqual(state['current_attempt'], 7)
        self.assertEqual(state['attempts'], 1)

    def test_late_terminal_from_old_attempt_cannot_close_new_attempt(self):
        first = self._record('started')
        self._record('failed')
        current = self._record('started')
        self.assertEqual((first['attempt'], current['attempt']), (1, 2))
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'late',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-shot01', '--attempt', '1'])
        self.assertEqual(code, 2)
        self.assertIn('does not match', err)
        state = ph._status(self.root)['operations']['op-shot01']
        self.assertEqual(state['state'], 'started')
        self.assertEqual(state['current_attempt'], 2)
    def test_automatic_retry_uses_unused_id_after_explicit_attempt(self):
        first = self._record('started', extra=['--attempt', '2'])
        self._record('failed')
        current = self._record('started')
        self.assertEqual((first['attempt'], current['attempt']), (2, 3))
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--operation', 'late',
            '--prompt-file', str(self.prompt), '--status', 'completed',
            '--operation-id', 'op-shot01', '--attempt', '2'])
        self.assertEqual(code, 2)
        self.assertIn('does not match', err)
        state = ph._status(self.root)['operations']['op-shot01']
        self.assertEqual(state['state'], 'started')
        self.assertEqual(state['current_attempt'], 3)

    def test_escaped_quote_inside_secret_does_not_leak_suffix(self):
        # A quote escaped inside a quoted credential is part of the
        # value, not its delimiter; the suffix must be redacted too.
        for index, raw in enumerate((
                b'{"password":"prefix\\"suffix_secret","scene":"blue rain"}',
                b"{'password':'pre\\'sfx_secret','scene':'blue rain'}")):
            with self.subTest(raw=raw):
                self.prompt.write_bytes(raw)
                started = self._record('started', op_id=f'op-esc{index}')
                text = Path(started['event']).read_text(encoding='utf-8')
                snaps = sorted(
                    (self.root / '.history' / 'prompts').iterdir())
                stored = snaps[-1].read_text(encoding='utf-8')
                self.assertNotIn('secret', text)
                self.assertNotIn('secret', stored)
                self.assertIn('[REDACTED]', text)
                # Creative fields survive; original bytes and hash intact.
                self.assertIn('blue rain', text)
                self.assertIn('blue rain', stored)
                digest = hashlib.sha256(raw).hexdigest()
                self.assertIn(f'prompt_sha256: "{digest}"', text)
                self.assertEqual(self.prompt.read_bytes(), raw)



class LifecycleTests(unittest.TestCase):
    """Abrupt-death detection and honest resume semantics."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        result = ph.initialize_project('demo', documents=self.tmp.name)
        self.root = Path(result['project_root'])
        self.prompt = Path(self.tmp.name) / 'p.txt'
        self.prompt.write_text('actual prompt body', encoding='utf-8')

    def _record(self, status, op_id, extra=()):
        argv = ['record', '--project-root', str(self.root),
                '--operation', f'operation {op_id}',
                '--prompt-file', str(self.prompt), '--status', status,
                '--operation-id', op_id]
        argv += list(extra)
        code, out, err = run_cli(argv)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def _status(self):
        code, out, err = run_cli(['status', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def test_started_without_terminal_is_in_flight_completed_is_not(self):
        self._record('started', 'op-a')
        self._record('started', 'op-b')
        self._record('completed', 'op-b')
        self._record('started', 'op-c')
        self._record('failed', 'op-c')
        state = self._status()
        self.assertEqual(state['in_flight'], ['op-a'])
        self.assertEqual(state['operations']['op-b']['state'], 'completed')
        self.assertEqual(state['operations']['op-c']['state'], 'failed')

    def test_resume_marks_interruption_not_completion(self):
        self._record('started', 'op-a')
        self._record('started', 'op-b')
        self._record('completed', 'op-b')
        code, out, err = run_cli(['resume', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(result['marked_interrupted'], ['op-a'])
        self.assertEqual(len(result['events_written']), 2)
        state = self._status()
        self.assertEqual(state['in_flight'], [])  # stale starts are closed
        self.assertEqual(state['operations']['op-a']['state'], 'interrupted')
        self.assertEqual(state['operations']['op-b']['state'], 'completed')
        self.assertTrue(any(e['type'] == 'resumed'
                            for e in state['lifecycle']))
        # The interruption is explicit in the recorded event text.
        interrupted = [n for n in event_names(self.root)
                       if 'op-a-interrupted' in n]
        self.assertEqual(len(interrupted), 1)
        text = (self.root / '.history' / 'events' / interrupted[0]).read_text(
            encoding='utf-8')
        self.assertIn('interrupted', text)
        self.assertNotIn('completed', text.split('outputs:')[0])

    def test_project_completion_blocked_while_operations_in_flight(self):
        self._record('started', 'op-a')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('in flight', err)
        # The guard wrote nothing.
        self.assertEqual(len(event_files(self.root)), 1)
        self._record('completed', 'op-a')
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 0, err)

    def test_project_completion_blocked_by_missing_declared_output(self):
        # An interrupted operation that declared an output it never
        # produced must block project completion — interruption is not
        # a bypass for unresolved deliverables.
        self._record('started', 'op-a',
                     extra=['--output', '10_DELIVERY/final.mp4'])
        run_cli(['resume', '--project-root', str(self.root)])
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope',
            'project', '--operation', 'package finalized',
            '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('unresolved', err)
        # Creating an output cannot turn an interrupted attempt into success.
        produced = self.root / '10_DELIVERY' / 'final.mp4'
        produced.write_bytes(b'mp4')
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope',
            'project', '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('interrupted attempt unresolved', err)
        self._record('started', 'op-a')
        self._record('completed', 'op-a', extra=['--output', '10_DELIVERY/final.mp4'])
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope',
            'project', '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 0, err)


    def test_project_completion_rechecks_outputs_from_completed_attempt(self):
        output = self.root / '10_DELIVERY' / 'final.mp4'
        self._record('started', 'op-a', extra=['--output', '10_DELIVERY/final.mp4'])
        output.write_bytes(b'mp4')
        self._record('completed', 'op-a', extra=['--output', '10_DELIVERY/final.mp4'])
        output.unlink()
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('output', err.lower())
        output.write_bytes(b'mp4')
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 0, err)

    def test_current_failed_attempt_blocks_project_completion(self):
        self._record('started', 'op-failed')
        self._record('failed', 'op-failed')
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('unresolved', err.lower())

    def test_lower_attempt_started_later_is_the_current_attempt(self):
        # An explicit lower-numbered attempt started after a failed higher
        # one is chronologically the latest; ITS declared outputs are
        # enforced, and the dead attempt's outputs are not resurrected.
        self._record('started', 'op-chrono', extra=['--attempt', '7'])
        self._record('failed', 'op-chrono')
        self._record('started', 'op-chrono',
                     extra=['--attempt', '3',
                            '--output', '10_DELIVERY/current3.txt'])
        current = self.root / '10_DELIVERY' / 'current3.txt'
        current.write_bytes(b'real')
        self._record('completed', 'op-chrono',
                     extra=['--output', '10_DELIVERY/current3.txt'])
        state = self._status()['operations']['op-chrono']
        self.assertEqual(state['current_attempt'], 3)
        self.assertEqual(state['attempts'], 2)
        current.unlink()
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 2)
        self.assertIn('output', err.lower())

    def test_stale_high_attempt_output_does_not_shadow_newer_low(self):
        # Reverse control: a completed attempt7 output that was deleted
        # must not block completion once a newer attempt3 completed
        # cleanly with a live declared output.
        self._record('started', 'op-chrono',
                     extra=['--attempt', '7',
                            '--output', '10_DELIVERY/old7.txt'])
        old = self.root / '10_DELIVERY' / 'old7.txt'
        old.write_bytes(b'old')
        self._record('completed', 'op-chrono',
                     extra=['--output', '10_DELIVERY/old7.txt'])
        old.unlink()
        self._record('started', 'op-chrono',
                     extra=['--attempt', '3',
                            '--output', '10_DELIVERY/new3.txt'])
        new = self.root / '10_DELIVERY' / 'new3.txt'
        new.write_bytes(b'new')
        self._record('completed', 'op-chrono',
                     extra=['--output', '10_DELIVERY/new3.txt'])
        code, _, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed'])
        self.assertEqual(code, 0, err)
    def test_provider_death_leaves_unresolved_operation_honest(self):
        # A provider call that dies mid-generation leaves a dangling
        # started event. Resume must expose it as interrupted, never
        # completed, and a rerun must be a new attempt.
        self._record('started', 'op-video01')
        state = self._status()
        self.assertEqual(state['in_flight'], ['op-video01'])
        run_cli(['resume', '--project-root', str(self.root)])
        state = self._status()
        self.assertEqual(state['operations']['op-video01']['state'],
                         'interrupted')
        # No event may claim this operation completed.
        types = [e['type']
                 for e in state['operations']['op-video01']['events']]
        self.assertNotIn('completed', types)
        rerun = self._record('started', 'op-video01')
        self.assertEqual(rerun['attempt'], 2)
        self._record('failed', 'op-video01',
                     extra=['--details', 'provider timeout'])
        state = self._status()
        self.assertEqual(state['operations']['op-video01']['state'], 'failed')
        self.assertEqual(state['in_flight'], [])

    def test_resumed_operation_can_be_rerun_and_then_complete(self):
        self._record('started', 'op-a')
        run_cli(['resume', '--project-root', str(self.root)])
        rerun = self._record('started', 'op-a')
        self.assertEqual(rerun['attempt'], 2)
        self._record('completed', 'op-a')
        state = self._status()
        self.assertEqual(state['operations']['op-a']['state'], 'completed')
        # Both the interruption and the resumption stay on record.
        types = [e['type'] for e in state['operations']['op-a']['events']]
        self.assertEqual(types, ['started', 'interrupted', 'started',
                                 'completed'])

    def test_resume_rejects_operations_not_in_flight(self):
        self._record('started', 'op-a')
        self._record('completed', 'op-a')
        code, out, err = run_cli([
            'resume', '--project-root', str(self.root),
            '--operation-id', 'op-a'])
        self.assertEqual(code, 2)
        self.assertIn('not in flight', err)
        code, out, err = run_cli([
            'resume', '--project-root', str(self.root),
            '--operation-id', 'op-missing'])
        self.assertEqual(code, 2)
        self.assertIn('unknown operation id', err)

    def test_second_resume_after_clean_state_marks_nothing(self):
        self._record('started', 'op-a')
        self._record('completed', 'op-a')
        code, out, err = run_cli(['resume', '--project-root', str(self.root)])
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(result['marked_interrupted'], [])
        self.assertEqual(len(result['events_written']), 1)  # just 'resumed'

    def test_project_scope_event_is_lifecycle_not_operation(self):
        code, out, err = run_cli([
            'record', '--project-root', str(self.root), '--scope', 'project',
            '--operation', 'package finalized', '--status', 'completed',
            '--details', 'all shots delivered'])
        self.assertEqual(code, 0, err)
        state = self._status()
        self.assertEqual(state['operations'], {})
        self.assertTrue(any(e['type'] == 'completed'
                            for e in state['lifecycle']))


class CliSmokeTests(unittest.TestCase):
    def test_init_cli_reports_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, err = run_cli(
                ['init', '--project-id', 'Smoke Test', '--documents', tmp])
            self.assertEqual(code, 0, err)
            result = json.loads(out)
            self.assertEqual(Path(result['project_root']),
                             Path(tmp) / 'studio_production' / 'smoke-test')

    def test_end_to_end_cli_sequence(self):
        """init → started → abrupt death → status sees in_flight → resume →
        rerun → completed → project completion; all via real argv."""
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_cli(
                ['init', '--project-id', 'E2E Film', '--documents', tmp])
            self.assertEqual(code, 0)
            root = json.loads(out)['project_root']
            prompt = Path(tmp) / 'p.txt'
            prompt.write_text('SH001 generation prompt', encoding='utf-8')
            record = ['record', '--project-root', root, '--prompt-file',
                      str(prompt)]
            code, out, _ = run_cli(
                record + ['--operation', 'render SH001', '--status', 'started',
                          '--operation-id', 'op-sh001'])
            self.assertEqual(code, 0)
            # Simulated death: no terminal event.
            code, out, _ = run_cli(['status', '--project-root', root])
            self.assertEqual(json.loads(out)['in_flight'], ['op-sh001'])
            code, out, _ = run_cli(['resume', '--project-root', root])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)['marked_interrupted'],
                             ['op-sh001'])
            code, out, _ = run_cli(
                record + ['--operation', 'render SH001 retry',
                          '--status', 'started',
                          '--operation-id', 'op-sh001'])
            self.assertEqual(json.loads(out)['attempt'], 2)
            produced = Path(root) / '06_GENERATION_SPECS' / 'SH001_out.mp4'
            produced.write_bytes(b'mp4')  # real file before completed
            code, out, _ = run_cli(
                record + ['--operation', 'render SH001 retry',
                          '--status', 'completed',
                          '--operation-id', 'op-sh001', '--output',
                          '06_GENERATION_SPECS/SH001_out.mp4'])
            self.assertEqual(code, 0)
            code, out, _ = run_cli(
                record + ['--operation', 'package delivered',
                          '--status', 'completed', '--scope', 'project'])
            self.assertEqual(code, 0)
            code, out, _ = run_cli(['status', '--project-root', root])
            state = json.loads(out)
            self.assertEqual(state['in_flight'], [])
            self.assertEqual(
                [e['type'] for e in
                 state['operations']['op-sh001']['events']],
                ['started', 'interrupted', 'started', 'completed'])
            self.assertTrue(any(e['type'] == 'resumed'
                                for e in state['lifecycle']))
            self.assertTrue(any(e['type'] == 'completed'
                                for e in state['lifecycle']))


if __name__ == '__main__':
    unittest.main()
