import unittest
from pathlib import Path

from src.analyzer import (AnalysisError, InvalidPathError, analyze_file,
                          validate_path)


class TestValidatePath(unittest.TestCase):
    def test_empty_string_is_rejected(self):
        with self.assertRaises(InvalidPathError) as ctx:
            validate_path("")
        self.assertIn("empty", str(ctx.exception).lower())

    def test_whitespace_only_string_is_rejected(self):
        with self.assertRaises(InvalidPathError):
            validate_path("   ")

    def test_null_byte_is_rejected(self):
        with self.assertRaises(InvalidPathError) as ctx:
            validate_path("bad\0name")
        self.assertIn("null", str(ctx.exception).lower())

    def test_invalid_path_error_is_an_analysis_error(self):
        self.assertTrue(issubclass(InvalidPathError, AnalysisError))

    def test_valid_string_becomes_a_path(self):
        self.assertEqual(validate_path("some/file.bin"), Path("some/file.bin"))

    def test_path_object_is_accepted(self):
        path = Path("some/file.bin")
        self.assertEqual(validate_path(path), path)


class TestAnalyzeFileUsesValidation(unittest.TestCase):
    def test_empty_string_raises_invalid_path_error(self):
        with self.assertRaises(InvalidPathError):
            analyze_file("")

    def test_null_byte_raises_invalid_path_error(self):
        with self.assertRaises(InvalidPathError):
            analyze_file("bad\0name")


if __name__ == "__main__":
    unittest.main()