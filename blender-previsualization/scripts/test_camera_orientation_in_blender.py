import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

BLENDER = os.environ.get("BLENDER_EXECUTABLE") or shutil.which("blender")


@unittest.skipUnless(BLENDER, "set BLENDER_EXECUTABLE or put blender on PATH")
class CameraOrientationTests(unittest.TestCase):
    def test_camera_points_at_subjects_in_rendered_scene(self):
        repository = Path(__file__).resolve().parents[2]
        spec = repository / "camera-spatial-design" / "assets" / "camera-spec-example.json"
        builder = Path(__file__).with_name("build_previs.py")

        with tempfile.TemporaryDirectory(prefix="camera-orientation-") as temporary:
            output = Path(temporary) / "render"
            subprocess.run(
                [
                    BLENDER,
                    "--background",
                    "--factory-startup",
                    "--python",
                    str(builder),
                    "--",
                    "--spec",
                    str(spec),
                    "--output",
                    str(output),
                    "--mode",
                    "smoke",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            inspection = json.loads((output / "blender-inspection.json").read_text(encoding="utf-8"))
            checks = inspection["shots"][0]["checks"]
            invisible = [
                f"frame {check['frame']} {check['subject_id']} {check['point']}"
                for check in checks
                if not check["proxy_point_visible"]
            ]
            self.assertEqual(invisible, [], f"camera does not frame proxy points: {invisible}")


if __name__ == "__main__":
    unittest.main()
