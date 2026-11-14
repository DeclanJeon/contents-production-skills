"""studio_layout: path/naming/Documents/layout helpers shared with the CLI.

These tests exercise observable behavior (returned paths, created folders,
rejected names), not internal helpers.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import studio_layout as sl  # noqa: E402


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
                Path(tmp) / 'Elsewhere')


class DetectionPrecedenceTests(unittest.TestCase):
    def test_explicit_env_beats_platform_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': str(Path(tmp) / 'Chosen')}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                Path(tmp) / 'Chosen')

    def test_relative_env_override_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = {'STUDIO_DOCUMENTS_DIR': 'relative/path'}
            self.assertEqual(
                sl.detect_documents(platform='darwin', env=env, home=Path(tmp)),
                Path(tmp) / 'Documents')


class StudioRootTests(unittest.TestCase):
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
