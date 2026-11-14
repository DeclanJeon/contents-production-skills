"""studio_layout: path/naming/Documents/layout helpers shared with the CLI.

These tests exercise observable behavior (returned paths, created folders,
rejected names), not internal helpers.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_layout as sl  # noqa: E402
from storage_test_support import isolate_storage_environment  # noqa: E402


def setUpModule():
    isolate_storage_environment()


def tearDownModule():
    # pytest invokes tearDownModule but not unittest's module-cleanup stack.
    unittest.doModuleCleanups()


class TestEnvironmentIsolationTests(unittest.TestCase):
    def test_storage_suite_ignores_ambient_studio_choices(self):
        # Given a saved/overridden production root outside the inner test fixture.
        for choice in ('config', 'env'):
            with self.subTest(choice=choice), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                outside = base / 'production'
                outside.mkdir()
                config = base / 'config' / 'media-studio' / 'config.json'
                config.parent.mkdir(parents=True)
                config.write_text(json.dumps({'media_studio_root': str(outside)}),
                                  encoding='utf-8')
                env = os.environ.copy()
                env.pop('MEDIA_STUDIO_ROOT', None)
                env.update(XDG_CONFIG_HOME=str(base / 'config'),
                           HOME=str(base / 'home'), USERPROFILE=str(base / 'home'))
                if choice == 'env':
                    env['MEDIA_STUDIO_ROOT'] = str(outside)
                # When: run a real existing storage test, including module setup.
                result = subprocess.run(
                    [sys.executable, '-m', 'unittest',
                     'test_production_history.InitTests.test_init_default_layout_creates_only_needed_dirs'],
                    cwd=Path(__file__).resolve().parent, env=env,
                    capture_output=True, text=True, encoding='utf-8', timeout=30)
                # Then: neither ambient choice may receive test artifacts.
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(list(outside.iterdir()), [])


class SlugTests(unittest.TestCase):
    def test_casefolds_and_strips_separators(self):
        self.assertEqual(sl.slugify('Demo Film', 'project_id'), 'demo-film')
        self.assertEqual(sl.slugify('DemoFilm', 'project_id'),
                         sl.slugify('demofilm', 'project_id'))

    def test_rejects_traversal_and_reserved(self):
        for bad in ('..', 'a/b', 'a\\b', 'CON', '.'):
            with self.assertRaises(sl.UsageError):
                sl.slugify(bad, 'project_id')


class DocumentsTests(unittest.TestCase):
    def test_linux_uses_xdg_when_configured(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cfg = home / '.config'
            cfg.mkdir()
            (cfg / 'user-dirs.dirs').write_text(
                'XDG_DOCUMENTS_DIR="$HOME/Eigene Dokumente"\n', encoding='utf-8')
            self.assertEqual(
                sl.detect_documents(platform='linux', env={}, home=home),
                home / 'Eigene Dokumente')

    def test_darwin_and_fallback_use_home_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(
                sl.detect_documents(platform='darwin', env={}, home=home),
                home / 'Documents')

    def test_env_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Elsewhere')}
            self.assertEqual(
                sl.detect_documents(platform='linux', env=env,
                                    home=Path('/nonexistent-home')),
                (Path(tmp) / 'Elsewhere').resolve())


class DetectionPrecedenceTests(unittest.TestCase):
    def test_explicit_env_beats_platform_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Chosen')}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                (Path(tmp) / 'Chosen').resolve())

    def test_relative_env_override_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': 'relative/path'}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                Path(tmp) / 'Documents')


class StudioRootTests(unittest.TestCase):
    def test_relative_studio_env_is_rejected(self):
        # Given an invalid root, resolving against cwd would save to the wrong place.
        with tempfile.TemporaryDirectory() as tmp:
            # When / Then: explicit studio choices must be absolute.
            with self.assertRaises(sl.UsageError):
                sl.detect_studio_root(env={'MEDIA_STUDIO_ROOT': 'relative'},
                                      home=Path(tmp))

    def test_relative_cached_root_is_ignored(self):
        # Given a malformed saved choice, use the real default, not cwd.
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            sl.write_config({'media_studio_root': 'relative'}, env={}, home=home)
            # When
            root, explicit = sl.detect_studio_root(
                documents=home / 'Docs', env={}, home=home)
            # Then
            self.assertEqual(root, (home / 'Docs' / 'Media_Studio').resolve())
            self.assertIsNone(explicit)

    def test_media_studio_root_env_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'Docs'
            env = {'MEDIA_STUDIO_ROOT': str(Path(tmp) / 'Mine')}
            root, explicit = sl.detect_studio_root(
                documents=docs, env=env, home=Path(tmp))
            self.assertEqual(root, (Path(tmp) / 'Mine').resolve())
            self.assertIsNotNone(explicit)

    def test_default_is_documents_media_studio(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / 'Docs'
            root, explicit = sl.detect_studio_root(
                documents=docs, env={}, home=Path(tmp))
            self.assertEqual(root, (docs / 'Media_Studio').resolve())
            self.assertIsNone(explicit)

    def test_config_cache_is_read_when_no_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {'XDG_CONFIG_HOME': str(home / '.config')}
            sl.write_config(
                {'media_studio_root': str(home / 'Cached')}, env=env, home=home)
            root, explicit = sl.detect_studio_root(
                documents=home / 'Docs', env=env, home=home)
            self.assertEqual(root, (home / 'Cached').resolve())
            self.assertIsNotNone(explicit)

    def test_ensure_studio_root_does_not_recreate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'Media_Studio'
            self.assertTrue(sl.ensure_studio_root(root))
            self.assertTrue(root.is_dir())
            (root / 'keep.txt').write_text('keep')
            self.assertFalse(sl.ensure_studio_root(root))
            self.assertEqual((root / 'keep.txt').read_text(), 'keep')


class InitializeLayoutTests(unittest.TestCase):
    def test_non_object_ledger_is_rejected_without_writes(self):
        # Given valid JSON that is not a project ledger.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'project.json').write_text('[]', encoding='utf-8')
            # When / Then
            with self.assertRaises(sl.UsageError):
                sl.initialize_layout(root, 'Demo')
            self.assertEqual([p.name for p in root.iterdir()], ['project.json'])

    def test_unsafe_history_is_rejected_before_creating_work_dirs(self):
        # Given an external audit symlink, a rejected init must be read-only.
        with tempfile.TemporaryDirectory() as tmp:
            root, outside = Path(tmp) / 'proj', Path(tmp) / 'outside'
            root.mkdir()
            outside.mkdir()
            try:
                (root / '.history').symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f'symlinks unavailable: {exc}')
            # When / Then
            with self.assertRaises(sl.UsageError):
                sl.initialize_layout(root, 'Demo', layout='full')
            self.assertFalse((root / 'source').exists())
            self.assertEqual(list(outside.iterdir()), [])

    def test_text_layout_creates_only_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            result = sl.initialize_layout(root, 'Demo Film')
            self.assertTrue((root / 'source').is_dir())
            self.assertTrue((root / 'project.json').is_file())
            self.assertTrue((root / '.history' / 'events').is_dir())
            for absent in ('bible', 'assets', 'final', 'audio', 'edit', 'qa'):
                self.assertFalse((root / absent).exists(), absent)
            self.assertEqual(result['layout'], 'text')
            self.assertFalse(result['existing'])

    def test_image_preset_creates_expected_dirs_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo', layout='image')
            for present in ('source', 'bible', 'storyboards', 'assets', 'qa'):
                self.assertTrue((root / present).is_dir(), present)
            for absent in ('audio', 'edit', 'final'):
                self.assertFalse((root / absent).exists(), absent)

    def test_reinit_on_existing_project_is_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo', layout='full')
            ledger_bytes = (root / 'project.json').read_bytes()
            result = sl.initialize_layout(root, 'Demo', layout='full')
            self.assertTrue(result['existing'])
            self.assertEqual(result['created'], [])
            self.assertEqual((root / 'project.json').read_bytes(), ledger_bytes)
            self.assertTrue((root / 'source').is_dir())

    def test_reinit_refuses_foreign_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Alpha')
            import json as _json
            (root / 'project.json').write_text(
                _json.dumps({'project_id': 'beta'}), encoding='utf-8')
            with self.assertRaises(sl.UsageError):
                sl.initialize_layout(root, 'Alpha')

    def test_ensure_work_dir_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            sl.initialize_layout(root, 'Demo')
            first = sl.ensure_work_dir(root, 'assets')
            self.assertTrue(first.is_dir())
            self.assertEqual(sl.ensure_work_dir(root, 'assets'), first)
            with self.assertRaises(sl.UsageError):
                sl.ensure_work_dir(root, '../escape')
            with self.assertRaises(sl.UsageError):
                sl.ensure_work_dir(root, 'not_a_work_dir')


class PathSafetyTests(unittest.TestCase):
    def test_assert_managed_path_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            with self.assertRaises(sl.UsageError):
                sl.assert_managed_path(root, root.parent / 'outside.txt')

    def test_resolve_inside_keeps_relative_under_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            self.assertEqual(
                sl.resolve_inside(root, 'assets/x.png', 'output'),
                (root / 'assets/x.png').resolve())

    def test_resolve_inside_rejects_absolute_outside(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'proj'
            root.mkdir()
            with self.assertRaises(sl.UsageError):
                sl.resolve_inside(root, str(Path(tmp) / 'elsewhere.png'),
                                  'output')


if __name__ == '__main__':
    unittest.main()
