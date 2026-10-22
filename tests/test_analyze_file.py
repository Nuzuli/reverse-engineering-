import pytest
from pathlib import Path

from pathlib import Path
from src.analyzer import analyze_file, AnalysisError

class TestAnalyzeFile(unittest.TestCase):
    def test_analyze_file_returns_basic_information(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "sample.bin"
            sample.write_bytes(b"hello")

            # Memanggil fungsi dari src/analyzer.py
            result = analyze_file(sample)

            # Tambahkan assertion sesuai dengan output fungsi analyze_file-mu
            self.assertIsNotNone(result)

    def test_file_not_found(self):
        with self.assertRaises(AnalysisError):
            analyze_file("file_palsu.txt")

    def test_not_a_file(self, tmp_path):
        # Mengetes jika path yang diberikan adalah folder, bukan file
        with self.assertRaises(AnalysisError):
            analyze_file(tmp_path)

if __name__ == "__main__":
    unittest.main()