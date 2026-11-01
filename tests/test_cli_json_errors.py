"""Run the CLI with --json as a real subprocess and check error handling."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.report import REQUIRED_KEYS

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "src.analyzer", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class TestJsonErrors(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def test_missing_file_with_json_exits_2_and_prints_no_json(self):
        result = run_cli(str(self.tmp / "missing.bin"), "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not found", result.stderr.lower())
        self.assertEqual(result.stdout, "")

    def test_directory_with_json_exits_2(self):
        result = run_cli(str(self.tmp), "--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a regular file", result.stderr.lower())
        self.assertEqual(result.stdout, "")

    def test_success_prints_exactly_the_documented_keys(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"hello")
        result = run_cli(str(sample), "--json")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(list(json.loads(result.stdout)), list(REQUIRED_KEYS))


if __name__ == "__main__":
    unittest.main()