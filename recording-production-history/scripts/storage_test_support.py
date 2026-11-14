"""Isolate storage test modules from the operator's saved production paths."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def isolate_storage_environment() -> None:
    """Install module-scoped temporary settings for pytest and unittest runs."""
    temporary = tempfile.TemporaryDirectory(prefix='storage-test-env-')
    unittest.addModuleCleanup(temporary.cleanup)
    base = Path(temporary.name)
    home = base / 'home'
    home.mkdir()
    environment = os.environ.copy()
    environment.pop('MEDIA_STUDIO_ROOT', None)
    environment.update(HOME=str(home), USERPROFILE=str(home),
                       XDG_CONFIG_HOME=str(base / 'config'),
                       STUDIO_DOCUMENTS_DIR=str(base / 'Documents'))
    override = patch.dict(os.environ, environment, clear=True)
    override.start()
    unittest.addModuleCleanup(override.stop)
