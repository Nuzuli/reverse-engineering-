import unittest
import subprocess
import sys

class TestUnexpectedErrors(unittest.TestCase):

    def test_nonexistent_file_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.analyzer", "file_tidak_ada.txt"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 2)

    def test_invalid_path_rejected(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.analyzer", "test\x00file.txt"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 2)

if __name__ == "__main__":
    unittest.main()
