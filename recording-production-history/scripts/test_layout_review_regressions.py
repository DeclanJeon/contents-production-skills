"""Behavior regressions from the independent Media Studio review."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import production_history as ph  # noqa: E402
import studio_layout as sl  # noqa: E402
from storage_test_support import isolate_storage_environment  # noqa: E402
from test_production_history import run_cli  # noqa: E402


def setUpModule():
    isolate_storage_environment()


def tearDownModule():
    # pytest invokes tearDownModule but not unittest's module-cleanup stack.
    unittest.doModuleCleanups()


def directory_link(link: Path, target: Path, kind: str) -> None:
    """Use real directory links, including unprivileged Windows junctions."""
    if kind == 'junction':
        if os.name != 'nt':
            raise unittest.SkipTest('Windows junctions require Windows')
        result = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(link), str(target)],
            capture_output=True, timeout=10)
        if result.returncode:
            raise unittest.SkipTest(f'junction unavailable: {result.stderr!r}')
    else:
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            raise unittest.SkipTest(f'symlinks unavailable: {exc}') from exc


class TestEnvironmentCleanupTests(unittest.TestCase):
    def test_pytest_restores_environment_after_storage_module(self):
        # Given ambient choices which must be restored, not leaked across modules.
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            env = os.environ.copy()
            expected = {'HOME': str(base / 'home'),
                        'USERPROFILE': str(base / 'home'),
                        'XDG_CONFIG_HOME': str(base / 'config'),
                        'MEDIA_STUDIO_ROOT': str(base / 'production')}
            env.update(expected)
            # Keep the installed test runner importable under the disposable HOME.
            env['PYTHONPATH'] = os.pathsep.join(sys.path)
            probe = base / 'test_restored_environment.py'
            probe.write_text(
                'import os\n'
                'def test_restored_environment():\n'
                f'    expected = {expected!r}\n'
                '    assert {k: os.environ.get(k) for k in expected} == expected\n',
                encoding='utf-8')
            suite = Path(__file__).with_name('test_production_history.py')
            # When: pytest switches from the storage module to an unrelated module.
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                 str(suite) + '::InitTests::test_init_default_layout_creates_only_needed_dirs',
                 str(probe)], env=env, capture_output=True,
                text=True, encoding='utf-8', timeout=30)
            # Then: the unrelated module sees its original environment.
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((base / 'production').exists())


class StudioContainmentTests(unittest.TestCase):
    def test_linked_slug_never_writes_outside_selected_studio(self):
        # Given a linked slug under every supported studio selection route.
        for route in ('explicit', 'documents', 'env', 'config'):
            for kind in ('symlink', 'junction'):
                with self.subTest(route=route, kind=kind), tempfile.TemporaryDirectory() as tmp:
                    base = Path(tmp)
                    studio = base / 'Documents' / 'Media_Studio'
                    outside = base / 'outside'
                    studio.mkdir(parents=True)
                    outside.mkdir()
                    directory_link(studio / 'demo', outside, kind)
                    env = {'XDG_CONFIG_HOME': str(base / 'config')}
                    if route == 'env':
                        env['MEDIA_STUDIO_ROOT'] = str(studio)
                    if route == 'config':
                        sl.write_config({'media_studio_root': str(studio)}, env=env)
                    kwargs = ({'media_studio_root': studio} if route == 'explicit'
                              else {'documents': base / 'Documents'})
                    # When / Then: reject before any write reaches the target.
                    with patch.dict(os.environ, env), self.assertRaises(ph.UsageError):
                        ph.initialize_project('demo', **kwargs)
                    self.assertEqual(list(outside.iterdir()), [])


class ExistingProjectTests(unittest.TestCase):
    def test_reinit_ignores_unused_linked_work_directory(self):
        # Given an initialized project with a legitimate internal work link.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sl.initialize_layout(root, 'demo')
            (root / 'source').rmdir()
            (root / 'data').mkdir()
            directory_link(root / 'source', root / 'data', 'symlink')
            before = sorted(p.relative_to(root).as_posix() for p in root.rglob('*'))
            ledger = (root / 'project.json').read_bytes()
            # When
            result = sl.initialize_layout(root, 'demo', layout='full')
            # Then: preset-independent no-op, not a write through the link.
            self.assertEqual(result['created'], [])
            self.assertEqual((root / 'project.json').read_bytes(), ledger)
            self.assertEqual(sorted(p.relative_to(root).as_posix()
                                    for p in root.rglob('*')), before)

    def test_ensure_dir_rejects_missing_project_without_creating_orphan(self):
        # Given a typo/nonexistent project root.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'typo'
            # When
            code, out, err = run_cli(['ensure-dir', '--project-root', str(root),
                                      '--name', 'assets'])
            # Then
            self.assertEqual(code, 2)
            self.assertEqual(out, '')
            self.assertIn('error', json.loads(err))
            self.assertFalse(root.exists())


class InvalidEncodingTests(unittest.TestCase):
    def test_undecodable_config_falls_back_to_default_without_writes(self):
        # Given a non-UTF-8 saved configuration.
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            env = {'XDG_CONFIG_HOME': str(base / 'config'),
                   'STUDIO_DOCUMENTS_DIR': str(base / 'Documents')}
            config = sl.config_path(env=env)
            config.parent.mkdir(parents=True)
            config.write_bytes(b'\xff')
            # When
            with patch.dict(os.environ, env):
                code, out, err = run_cli(['list'])
            # Then: broken-config fallback, structured JSON, no initialization.
            self.assertEqual(code, 0, err)
            report = json.loads(out)
            self.assertEqual(Path(report['studio_root']),
                             (base / 'Documents' / 'Media_Studio').resolve())
            self.assertEqual(report['count'], 0)
            self.assertFalse((base / 'Documents').exists())
            self.assertEqual(config.read_bytes(), b'\xff')

    def test_undecodable_ledger_is_structured_preflight_failure(self):
        # Given an existing ledger with invalid UTF-8.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / 'project.json'
            ledger.write_bytes(b'\xff')
            # When
            code, out, err = run_cli(['init', '--project-root', str(root),
                                      '--project-id', 'demo'])
            # Then: preserve bytes and reject without creating work/history.
            self.assertEqual(code, 2)
            self.assertEqual(out, '')
            self.assertIn('error', json.loads(err))
            self.assertEqual(ledger.read_bytes(), b'\xff')
            self.assertEqual([p.name for p in root.iterdir()], ['project.json'])


if __name__ == '__main__':
    unittest.main()
