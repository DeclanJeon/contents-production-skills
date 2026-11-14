"""Pure layout/path/naming helpers for the production history tool.

This module owns everything about *where* production files live: slug
rules, managed-path guards, cross-platform Documents detection, the
``Media_Studio`` studio root, and the lazy project layout. It performs no
event recording; the event store and CLI stay in ``production_history.py``.

Nothing here writes production data except the explicit
``initialize_layout`` / ``ensure_work_dir`` / ``ensure_studio_root`` /
``write_config`` calls, and each of those is idempotent.
"""
from __future__ import annotations

import os
import re
import sys
import json
from pathlib import Path


class UsageError(ValueError):
    """A user-correctable project or command preflight failure."""


# ---------------------------------------------------------------------------
# Naming / path safety
# ---------------------------------------------------------------------------
_SLUG_BAD = re.compile(r"[^\w.-]+")
_SLUG_RUNS = re.compile(r"-{2,}")
_WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
}


def slugify(value: str, field: str) -> str:
    """Return a filesystem-safe slug; reject anything that can traverse.

    Unicode letters/numbers/underscore/hyphen/dot are kept so Korean and
    other non-ASCII project names work on Windows, macOS and Linux. The
    slug is casefolded so case-insensitive filesystems cannot create two
    projects that differ only in case.
    """
    if not isinstance(value, str) or not value.strip():
        raise UsageError(f"{field} must be a non-empty string")
    if "/" in value or "\\" in value:
        raise UsageError(f"{field} must not contain path separators: {value!r}")
    slug = _SLUG_BAD.sub("-", value.strip())
    slug = _SLUG_RUNS.sub("-", slug).strip("-_.").casefold()
    if not slug or slug in (".", "..") or ".." in slug:
        raise UsageError(
            f"{field} has no usable filename-safe characters: {value!r}")
    basename = slug.split(".", 1)[0]
    if basename in _WINDOWS_RESERVED:
        raise UsageError(
            f"{field} resolves to a reserved Windows device name: {value!r}")
    return slug


def resolve_inside(root: Path, raw: str, field: str) -> Path:
    """Resolve any output path; production outputs must stay under root."""
    candidate = Path(raw).expanduser()
    resolved = (candidate if candidate.is_absolute()
                else root / candidate).resolve()
    if resolved == root or root not in resolved.parents:
        raise UsageError(f"{field} escapes the project root: {raw!r}")
    return resolved


def assert_managed_path(root: Path, target: Path) -> None:
    """Reject symlink/junction components and resolved paths outside root."""
    root = root.absolute()
    target = target.absolute()
    try:
        relative = target.relative_to(root)
    except ValueError as exc:
        raise UsageError(f"managed path escapes project root: {target}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise UsageError(f"managed path traverses a symlink or junction: {current}")
    resolved_root = root.resolve()
    resolved_target = target.resolve()
    if resolved_target != resolved_root and resolved_root not in resolved_target.parents:
        raise UsageError(f"managed path resolves outside project root: {target}")


# ---------------------------------------------------------------------------
# Documents directory (cross-platform)
# ---------------------------------------------------------------------------
def _windows_documents(env, home) -> Path | None:
    """Real Windows Documents folder, honoring shell redirection/OneDrive."""
    try:
        import ctypes
        from ctypes import wintypes

        class _GUID(ctypes.Structure):
            _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                        ("Data3", wintypes.WORD), ("Data4", ctypes.c_byte * 8)]

        # FOLDERID_Documents = FDD39AD0-238F-46AF-ADB4-6C85480369C7
        guid = _GUID(0xFDD39AD0, 0x238F, 0x46AF,
                     (ctypes.c_byte * 8)(0xAD, 0xB4, 0x6C, 0x85,
                                         0x48, 0x03, 0x69, 0xC7))
        buf = ctypes.c_wchar_p()
        hr = ctypes.windll.shell32.SHGetKnownFolderPath(  # type: ignore[attr-defined]
            ctypes.byref(guid), 0, None, ctypes.byref(buf))
        if hr == 0 and buf.value:
            path = Path(buf.value)
            ctypes.windll.ole32.CoTaskMemFree(buf)  # type: ignore[attr-defined]
            return path
    except (OSError, AttributeError, ImportError):
        pass
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        try:
            raw, _ = winreg.QueryValueEx(key, "Personal")
        finally:
            winreg.CloseKey(key)
        expanded = os.path.expandvars(str(raw))
        if expanded and Path(expanded).is_absolute():
            return Path(expanded)
    except (OSError, ImportError):
        pass
    return None


def _linux_documents(env, home: Path) -> Path | None:
    """XDG user-dirs Documents when configured, else ~/Documents."""
    config_home = env.get("XDG_CONFIG_HOME")
    config_dir = Path(config_home) if config_home else home / ".config"
    try:
        text = (config_dir / "user-dirs.dirs").read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r'(?m)^\s*XDG_DOCUMENTS_DIR\s*=\s*"(.*)"\s*$', text)
    if not match:
        return None
    candidate = Path(match.group(1).replace("$HOME", str(home)))
    return candidate if candidate.is_absolute() else None


def detect_documents(platform: str | None = None, env=None, home=None) -> Path:
    """Resolve the actual user Documents directory for the current OS.

    Precedence: an absolute ``STUDIO_DOCUMENTS_DIR`` override, then the
    OS default (Windows known folder/registry, macOS ``~/Documents``,
    Linux XDG user-dirs), then ``~/Documents``. A relative override is
    ignored in favour of real detection rather than resolved against the
    process cwd.
    """
    platform = platform or sys.platform
    env = os.environ if env is None else env
    home = Path(home) if home is not None else Path.home()
    override = env.get("STUDIO_DOCUMENTS_DIR")
    if override:
        # Only an absolute override counts; a relative value is ignored in
        # favour of real detection rather than resolved against the cwd.
        candidate = Path(override).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()
    detected = None
    if platform == "win32":
        detected = _windows_documents(env, home)
    elif platform == "darwin":
        detected = home / "Documents"
    elif platform.startswith(("linux", "freebsd", "openbsd")):
        detected = _linux_documents(env, home)
    if detected is not None:
        return detected
    return home / "Documents"


# ---------------------------------------------------------------------------
# Studio root
# ---------------------------------------------------------------------------
MEDIA_STUDIO_DIRNAME = "Media_Studio"


def config_path(env=None, home=None) -> Path:
    """User config file for the saved studio root (XDG-aware)."""
    env = os.environ if env is None else env
    home = Path(home) if home is not None else Path.home()
    base = env.get("XDG_CONFIG_HOME")
    config_dir = Path(base) if base else home / ".config"
    return config_dir / "media-studio" / "config.json"


def read_config(env=None, home=None) -> dict:
    """Read the saved config; a missing or broken file is just empty."""
    try:
        data = json.loads(config_path(env, home).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def write_config(data: dict, env=None, home=None) -> Path:
    """Atomically write the config, creating its parent directory."""
    path = config_path(env, home)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage = path.with_name(
        f".config.json.stage-{os.getpid()}-{os.urandom(4).hex()}")
    try:
        with open(stage, "x", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)
    return path


def detect_studio_root(documents=None, env=None, home=None):
    """Resolve the studio root and whether it was explicitly chosen.

    Precedence: ``MEDIA_STUDIO_ROOT`` -> saved config (``set-root``) ->
    ``<Documents>/Media_Studio``. The second value is a short label when
    the user already chose a root (so the coordinator need not ask again)
    and ``None`` on the plain default.
    """
    env = os.environ if env is None else env
    override = env.get("MEDIA_STUDIO_ROOT")
    if override:
        candidate = Path(override).expanduser()
        if not candidate.is_absolute():
            raise UsageError("MEDIA_STUDIO_ROOT must be an absolute path")
        return candidate.resolve(), f"MEDIA_STUDIO_ROOT={override}"
    cached = read_config(env, home).get("media_studio_root")
    if isinstance(cached, str) and cached.strip():
        candidate = Path(cached).expanduser()
        if candidate.is_absolute():
            return candidate.resolve(), "saved studio root"
    base = (Path(documents).expanduser() if documents
            else detect_documents(env=env, home=home))
    return (base / MEDIA_STUDIO_DIRNAME).resolve(), None


def ensure_studio_root(root: Path) -> bool:
    """Create the studio root only if absent; True if it was created."""
    if root.is_dir():
        return False
    root.mkdir(parents=True, exist_ok=True)
    return True


# ---------------------------------------------------------------------------
# Project root / initialization
# ---------------------------------------------------------------------------
STUDIO_DIRNAME = MEDIA_STUDIO_DIRNAME

HISTORY_DIRNAME = ".history"
EVENTS_DIRNAME = "events"
PROMPTS_DIRNAME = "prompts"
PROJECT_JSON = "project.json"
WORK_DIRS = ("source", "bible", "storyboards", "assets", "audio", "edit",
             "qa", "final")
LAYOUT_PRESETS = {
    "text": ("source",),
    "image": ("source", "bible", "storyboards", "assets", "qa"),
    "full": WORK_DIRS,
}


def _skeleton(project_id: str) -> dict:
    return {"schema_version": "1.1", "project_id": project_id, "version": "v001",
            "target_duration_s": None, "fps": None, "aspect_ratio": None,
            "scenes": [], "characters": [], "shots": [], "claims": [],
            "artifacts": [], "asset_registry": []}


def _write_skeleton_exclusive(root: Path, project_id: str) -> None:
    """Publish a fresh project.json only if none exists (atomic link)."""
    project_file = root / PROJECT_JSON
    stage = root / f".project.json.stage-{os.getpid()}-{os.urandom(4).hex()}"
    try:
        with open(stage, "x", encoding="utf-8") as handle:
            json.dump(_skeleton(project_id), handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.link(stage, project_file)
    except FileExistsError:
        raise UsageError(
            f"project.json appeared during initialization; preserved: {project_file}")
    finally:
        stage.unlink(missing_ok=True)


def resolve_project_root(project_id: str,
                         documents: str | os.PathLike | None = None,
                         env=None, home=None) -> Path:
    """Absolute default root: <Documents>/Media_Studio/<slug>."""
    slug = slugify(project_id, "project_id")
    root, _ = detect_studio_root(documents=documents, env=env, home=home)
    return project_root_in_studio(root, slug)


def project_root_in_studio(studio: Path, project_id: str) -> Path:
    """Resolve a slug child only after validating the selected studio boundary."""
    studio = studio.expanduser().resolve()
    child = studio / slugify(project_id, "project_id")
    assert_managed_path(studio, child)
    return child.resolve()


def initialize_layout(root: Path, project_id: str, layout: str = "text") -> dict:
    """Create an idempotent project layout, only the dirs a task needs.

    An existing project.json means this is a reuse: no preset directory is
    created (the project is preserved), only missing ``.history`` folders
    are completed. Unknown layout presets are rejected.
    """
    if layout not in LAYOUT_PRESETS:
        raise UsageError(
            f"unknown layout {layout!r} (expected one of "
            f"{tuple(LAYOUT_PRESETS)})")
    slug = slugify(project_id, "project_id")
    root = root.absolute()
    project_file = root / PROJECT_JSON
    for target in (project_file, root / HISTORY_DIRNAME / EVENTS_DIRNAME,
                   root / HISTORY_DIRNAME / PROMPTS_DIRNAME):
        assert_managed_path(root, target)

    existing = project_file.exists()
    if existing:
        try:
            ledger = json.loads(project_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise UsageError(
                f"existing project.json is unreadable; refusing to reuse "
                f"root {root}: {exc}")
        if not isinstance(ledger, dict):
            raise UsageError(f"existing project.json must contain an object: {project_file}")
        other = ledger.get("project_id")
        if other and slugify(str(other), "project_id") != slug:
            raise UsageError(
                f"project.json at {project_file} belongs to project {other!r}")

    if not existing:
        for name in LAYOUT_PRESETS[layout]:
            assert_managed_path(root, root / name)
    root.mkdir(parents=True, exist_ok=True)
    created, kept = [], []
    if existing:
        kept.append(PROJECT_JSON)
    else:
        for rel in LAYOUT_PRESETS[layout]:
            target = root / rel
            assert_managed_path(root, target)
            if target.is_dir():
                kept.append(rel)
            else:
                target.mkdir(parents=False)
                created.append(rel)

    history = root / HISTORY_DIRNAME
    for rel in (EVENTS_DIRNAME, PROMPTS_DIRNAME):
        target = history / rel
        assert_managed_path(root, target)
        target.mkdir(parents=True, exist_ok=True)

    if not existing:
        _write_skeleton_exclusive(root, slug)
        created.append(PROJECT_JSON)

    return {"project_root": str(root), "studio_root": str(root.parent),
            "project_id": slug, "layout": layout,
            "created": created, "kept": kept,
            "history_dir": str(history), "existing": existing}


def ensure_work_dir(root: Path, name: str) -> Path:
    """Create one allowed work dir on demand; return its absolute path."""
    slug = slugify(name, "work dir")
    if slug not in WORK_DIRS:
        raise UsageError(
            f"unknown work dir: {name!r} (expected one of {WORK_DIRS})")
    target = root.absolute() / slug
    assert_managed_path(root.absolute(), target)
    target.mkdir(parents=True, exist_ok=True)
    return target


def list_projects(root: Path) -> list[dict]:
    """Read-only inventory of projects under a studio root."""
    if not root.is_dir():
        return []
    rows = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or not (child / PROJECT_JSON).is_file():
            continue
        rows.append({
            "project_id": child.name,
            "project_root": str(child),
            "layout": [d for d in WORK_DIRS if (child / d).is_dir()],
            "files": sum(1 for p in child.rglob('*') if p.is_file()),
        })
    return rows
