import tempfile
import unittest
from pathlib import Path

from scripts.analyze_file import AnalysisError, analyze_file


class TestAnalyzeFile(unittest.TestCase):
    def test_analyze_file_returns_basic_information(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "sample.bin"
            sample.write_bytes(b"hello")

            result = analyze_file(sample)

            self.assertEqual(result["name"], "sample.bin")
            self.assertEqual(result["size_bytes"], 5)
            self.assertEqual(
                result["sha256"],
                "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            )
            self.assertEqual(result["header_hex"], "68 65 6c 6c 6f")

    def test_missing_file_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing.bin"

            with self.assertRaises(AnalysisError):
                analyze_file(missing)

    def test_directory_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(AnalysisError):
                analyze_file(Path(temp_dir))


if __name__ == "__main__":
    unittest.main()