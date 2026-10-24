import hashlib
import tempfile
import unittest
from pathlib import Path

from src.analyzer import AnalysisError, analyze_file


class TestAnalyzeFile(unittest.TestCase):
    def _make_file(self, temp_dir, data):
        path = Path(temp_dir) / "sample.bin"
        path.write_bytes(data)
        return path

    def test_returns_expected_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyze_file(self._make_file(temp_dir, b"hello"))

            self.assertEqual(
                set(result.keys()),
                {"name", "size_bytes", "sha256", "header_hex"},
            )
            self.assertEqual(result["name"], "sample.bin")
            self.assertEqual(result["size_bytes"], 5)
            self.assertEqual(result["sha256"], hashlib.sha256(b"hello").hexdigest())

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyze_file(self._make_file(temp_dir, b""))

            self.assertEqual(result["size_bytes"], 0)
            self.assertEqual(result["header_hex"], "(empty file)")

    def test_large_file_uses_chunked_read(self):
        data = b"A" * 20000
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyze_file(self._make_file(temp_dir, data))

            self.assertEqual(result["size_bytes"], 20000)
            self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())

    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(AnalysisError):
                analyze_file(Path(temp_dir) / "tidak_ada.bin")

    def test_directory_raises(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(AnalysisError):
                analyze_file(Path(temp_dir))


if __name__ == "__main__":
    unittest.main()