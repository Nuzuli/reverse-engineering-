"""End-to-end tests that run the CLI as a real subprocess."""

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    """Run ``python -m src.analyzer`` from the repository root."""
    return subprocess.run(
        [sys.executable, "-m", "src.analyzer", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class TestExitCodes(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def test_existing_file_exits_0_and_reports_hash(self):
        sample = self.tmp / "sample.bin"
        data = b"hello reverse engineering"
        sample.write_bytes(data)
        result = run_cli(str(sample))
        self.assertEqual(result.returncode, 0)
        self.assertIn(hashlib.sha256(data).hexdigest(), result.stdout)
        self.assertEqual(result.stderr, "")

    def test_missing_file_exits_2_with_message(self):
        result = run_cli(str(self.tmp / "missing.bin"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("not found", result.stderr.lower())
        self.assertEqual(result.stdout, "")

    def test_directory_exits_2_with_message(self):
        result = run_cli(str(self.tmp))
        self.assertEqual(result.returncode, 2)
        self.assertIn("not a regular file", result.stderr.lower())

    def test_empty_path_argument_exits_2(self):
        result = run_cli("")
        self.assertEqual(result.returncode, 2)
        self.assertNotEqual(result.stderr, "")

    def test_missing_argument_exits_2(self):
        result = run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()