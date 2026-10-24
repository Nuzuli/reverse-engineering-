import tempfile
import unittest
from pathlib import Path

from src.analyzer import analyze_file


class TestAnalyzeFile(unittest.TestCase):
    def test_analyze_file_returns_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "sample.bin"
            sample.write_bytes(b"hello")

            result = analyze_file(sample)

            self.assertIsNotNone(result)

    def test_not_a_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(Exception):
                analyze_file(Path(temp_dir))


if __name__ == "__main__":
    unittest.main()