import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parent.parent.parent


class ScanSecrets(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REAL_ROOT / "scripts", self.tmp / "scripts", ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def scan(self):
        return subprocess.run([sys.executable, "scripts/scan-secrets.py"], cwd=self.tmp, capture_output=True, text=True)

    def write(self, rel, text):
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_clean_tree_passes(self):
        self.write("README.md", "hello\n")
        self.assertEqual(self.scan().returncode, 0)

    def test_private_key_detected(self):
        self.write("a.txt", "-----BEGIN " + "RSA PRIVATE KEY-----\n")
        self.assertEqual(self.scan().returncode, 1)

    def test_aws_key_detected(self):
        self.write("a.kt", 'val k = "' + "AKIA" + "ABCDEFGHIJKLMNOP" + '"\n')
        self.assertEqual(self.scan().returncode, 1)

    def test_hardcoded_credential_detected(self):
        self.write("a.swift", 'let password = "' + "hunter2hunter2hunter2" + '"\n')
        self.assertEqual(self.scan().returncode, 1)

    def test_inline_allow_marker(self):
        self.write("a.swift", 'let password = "' + "hunter2hunter2hunter2" + '" // secrets:allow\n')
        self.assertEqual(self.scan().returncode, 0)

    def test_forbidden_file_detected_but_example_allowed(self):
        self.write(".env.example", "KEY=\n")
        self.assertEqual(self.scan().returncode, 0)
        self.write("android/app/google-services.json", "{}")
        self.assertEqual(self.scan().returncode, 1)

    def test_allowlist_glob(self):
        self.write("fixtures/key.pem", "x")
        self.write(".secrets-allowlist", "fixtures/*\n")
        self.assertEqual(self.scan().returncode, 0)


if __name__ == "__main__":
    unittest.main()
