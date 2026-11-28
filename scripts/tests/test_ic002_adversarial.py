"""IC-002 adversarial regression probes for authoritative feature state.

Expected-failure tests describe bypasses that the current implementation still permits.
Remove the expectedFailure decorator only after the corresponding hardening is proven.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parent.parent.parent
SPEC = "Feature: demo\n  Scenario: works\n    Given x\n    Then y\n"


class IC002AdversarialPaths(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(
            REAL_ROOT / "scripts", self.tmp / "scripts",
            ignore=shutil.ignore_patterns("tests", "__pycache__"),
        )
        shutil.copy(REAL_ROOT / "harness.env", self.tmp / "harness.env")
        (self.tmp / "features").mkdir()
        (self.tmp / "features" / "a.feature").write_text(SPEC, encoding="utf-8")
        (self.tmp / "feature_list.json").write_text(
            json.dumps({"schema_version": 2, "project": "ic002", "features": []}),
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "scripts/feature.py", *args],
            cwd=self.tmp, capture_output=True, text=True,
        )

    def board(self):
        return json.loads((self.tmp / "feature_list.json").read_text(encoding="utf-8"))

    def start_feature(self):
        self.assertEqual(self.cli("add", "alpha", "Alpha", "--spec", "features/a.feature").returncode, 0)
        self.assertEqual(self.cli("start", "alpha").returncode, 0)

    @unittest.expectedFailure
    def test_direct_sensor_recording_without_execution_is_rejected(self):
        self.start_feature()
        result = self.cli("record-sensor", "ios")
        self.assertNotEqual(
            result.returncode, 0,
            "record-sensor must not create authoritative green state without trusted execution",
        )

    @unittest.expectedFailure
    def test_gate_rejects_caller_supplied_platform_claims_without_evidence(self):
        self.start_feature()
        result = self.cli("gate", "alpha", "--sensors", "ios,android")
        self.assertNotEqual(
            result.returncode, 0,
            "Gate must derive required outcomes from trusted Evidence, not --sensors",
        )

    @unittest.expectedFailure
    def test_gate_rejects_platform_name_outside_feature_profile(self):
        self.start_feature()
        result = self.cli("gate", "alpha", "--sensors", "ios,android,ghost")
        self.assertNotEqual(result.returncode, 0, "Gate must reject unknown sensor names")

    def test_workspace_process_can_bypass_editor_only_board_protection(self):
        self.start_feature()
        code = (
            "import json; from pathlib import Path; "
            "p=Path('feature_list.json'); d=json.loads(p.read_text()); "
            "d['features'][0]['title']='written outside CLI'; "
            "p.write_text(json.dumps(d))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=self.tmp, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.board()["features"][0]["title"], "written outside CLI")

    @unittest.expectedFailure
    def test_gate_rejects_sensor_results_after_spec_snapshot_changes(self):
        self.start_feature()
        self.assertEqual(self.cli("record-sensor", "ios").returncode, 0)
        self.assertEqual(self.cli("record-sensor", "android").returncode, 0)
        spec = self.tmp / "features" / "a.feature"
        spec.write_text(SPEC + "\n  # changed after sensor recording\n", encoding="utf-8")
        result = self.cli("gate", "alpha", "--sensors", "ios,android")
        self.assertNotEqual(
            result.returncode, 0,
            "Gate must reject verification results that do not match the current source snapshot",
        )

    @unittest.expectedFailure
    def test_completion_rejects_cli_flag_without_authenticated_human_approval(self):
        self.start_feature()
        self.cli("record-sensor", "ios")
        self.cli("record-sensor", "android")
        self.assertEqual(self.cli("gate", "alpha", "--sensors", "ios,android").returncode, 0)
        result = self.cli("done", "alpha", "--human-checklist-ok")
        self.assertNotEqual(
            result.returncode, 0,
            "a caller-supplied boolean flag must not stand in for authenticated human approval",
        )


if __name__ == "__main__":
    unittest.main()
