import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parent.parent.parent
SPEC = "Feature: demo\n  Scenario: works\n    Given x\n    Then y\n"


class FeatureCli(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REAL_ROOT / "scripts", self.tmp / "scripts", ignore=shutil.ignore_patterns("tests", "__pycache__"))
        shutil.copy(REAL_ROOT / "harness.env", self.tmp / "harness.env")
        (self.tmp / "features").mkdir()
        for name in ("a", "b"):
            (self.tmp / "features" / f"{name}.feature").write_text(SPEC, encoding="utf-8")
        (self.tmp / "feature_list.json").write_text(
            json.dumps({"schema_version": 2, "project": "t", "features": []}), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "scripts/feature.py", *args], cwd=self.tmp,
                              capture_output=True, text=True)

    def board(self):
        return json.loads((self.tmp / "feature_list.json").read_text(encoding="utf-8"))

    def add_and_start(self, fid="alpha", spec="features/a.feature"):
        self.assertEqual(self.run_cli("add", fid, "Alpha", "--spec", spec).returncode, 0)
        self.assertEqual(self.run_cli("start", fid).returncode, 0)

    def test_add_requires_existing_spec(self):
        r = self.run_cli("add", "x", "X", "--spec", "features/missing.feature")
        self.assertNotEqual(r.returncode, 0)

    def test_template_marker_is_rejected(self):
        (self.tmp / "features" / "t.feature").write_text("# @template-placeholder\n" + SPEC, encoding="utf-8")
        self.assertNotEqual(self.run_cli("add", "t", "T", "--spec", "features/t.feature").returncode, 0)

    def test_only_one_in_progress(self):
        self.add_and_start()
        self.run_cli("add", "beta", "Beta", "--spec", "features/b.feature")
        self.assertNotEqual(self.run_cli("start", "beta").returncode, 0)

    def test_sensor_green_cannot_be_set_by_hand(self):
        self.add_and_start()
        r = self.run_cli("platform", "alpha", "ios", "sensor_green")
        self.assertEqual(r.returncode, 2)

    def test_done_requires_human_flag(self):
        self.add_and_start()
        self.assertEqual(self.run_cli("done", "alpha").returncode, 2)

    def test_done_requires_gate_and_green_sensors(self):
        self.add_and_start()
        self.assertNotEqual(self.run_cli("done", "alpha", "--human-checklist-ok").returncode, 0)

    def test_full_happy_path(self):
        self.add_and_start()
        self.assertEqual(self.run_cli("record-sensor", "ios").returncode, 0)
        self.assertEqual(self.run_cli("record-sensor", "android").returncode, 0)
        self.assertEqual(self.run_cli("gate", "alpha", "--sensors", "ios,android").returncode, 0)
        self.assertEqual(self.run_cli("done", "alpha", "--human-checklist-ok").returncode, 0)
        feat = self.board()["features"][0]
        self.assertEqual(feat["status"], "done")
        self.assertTrue(feat["verified"])
        self.assertEqual(self.run_cli("validate").returncode, 0)

    def test_gate_incomplete_when_a_platform_missing(self):
        self.add_and_start()
        self.run_cli("record-sensor", "ios")
        self.assertEqual(self.run_cli("gate", "alpha", "--sensors", "ios").returncode, 3)

    def test_red_sensor_invalidates_gate(self):
        self.add_and_start()
        self.run_cli("record-sensor", "ios")
        self.run_cli("record-sensor", "android")
        self.run_cli("gate", "alpha", "--sensors", "ios,android")
        self.run_cli("record-sensor", "ios", "--fail")
        feat = self.board()["features"][0]
        self.assertIsNone(feat["gate"])
        self.assertEqual(feat["platforms"]["ios"], "in_progress")
        self.assertNotEqual(self.run_cli("done", "alpha", "--human-checklist-ok").returncode, 0)

    def test_validator_catches_hand_edited_done(self):
        self.add_and_start()
        data = self.board()
        feat = data["features"][0]
        feat["status"], feat["verified"] = "done", True
        feat["platforms"] = {"ios": "done", "android": "done"}
        (self.tmp / "feature_list.json").write_text(json.dumps(data), encoding="utf-8")
        self.assertNotEqual(self.run_cli("validate").returncode, 0)

    def test_single_platform_feature(self):
        self.assertEqual(self.run_cli("add", "solo", "Solo", "--spec", "features/a.feature", "--platforms", "android").returncode, 0)
        self.run_cli("start", "solo")
        self.run_cli("record-sensor", "android")
        self.assertEqual(self.run_cli("gate", "solo", "--sensors", "android").returncode, 0)
        self.assertEqual(self.run_cli("done", "solo", "--human-checklist-ok").returncode, 0)

    def test_import_legacy_array_board(self):
        legacy = [{"id": "plant-list", "title": "List", "status": "done", "platforms": ["ios", "android"],
                   "priority": 2, "spec": "features/a.feature"}]
        path = self.tmp / "legacy.json"
        path.write_text(json.dumps(legacy), encoding="utf-8")
        self.assertEqual(self.run_cli("import-legacy", str(path)).returncode, 0)
        self.assertEqual(self.run_cli("validate").returncode, 0)


if __name__ == "__main__":
    unittest.main()
