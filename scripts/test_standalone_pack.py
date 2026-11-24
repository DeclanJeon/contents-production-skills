"""The installable pack contains no orchestration-consumer adapter."""

import json
from pathlib import Path

from install_package import install


ROOT = Path(__file__).resolve().parents[1]
CONSUMER = "cine" + "forge"


def check_tree(root: Path) -> None:
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        assert CONSUMER not in path.name.casefold(), relative
        if path.is_file() and path.suffix in {".md", ".py", ".mjs", ".json", ".csv", ".yml", ".yaml"}:
            assert CONSUMER not in path.read_text(encoding="utf-8").casefold(), relative


def test_active_skill_pack_has_no_consumer_coupling() -> None:
    manifest = (ROOT / "manifest.json").read_text(encoding="utf-8")
    assert CONSUMER not in manifest.casefold()
    check_tree(ROOT / "integrations")
    check_tree(ROOT / ".github")
    for skill in json.loads(manifest)["skills"]:
        check_tree(ROOT / skill)


def test_can_copy_install_standalone_pack(tmp_path: Path) -> None:
    install(tmp_path, repo_root=ROOT)
    support = tmp_path / "video-production-assets" / "support"
    assert not (support / "integrations" / CONSUMER).exists()
    assert CONSUMER not in (support / "manifest.json").read_text(encoding="utf-8").casefold()
    assert (tmp_path / "video-production-assets" / "scripts" / "render_html_motion.mjs").is_file()
