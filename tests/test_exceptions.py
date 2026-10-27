import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.analyzer import (
    AnalysisError,
    FileNotFoundAnalysisError,
    FileReadError,
    NotARegularFileError,
    analyze_file,
    main,
)


class TestExceptionHierarchy(unittest.TestCase):
    def test_specific_errors_are_analysis_errors(self):
        for error_type in (
            FileNotFoundAnalysisError,
            NotARegularFileError,
            FileReadError,
        ):
            with self.subTest(error=error_type.__name__):
                self.assertTrue(issubclass(error_type, AnalysisError))


class TestSpecificErrors(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def test_missing_file_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundAnalysisError):
            analyze_file(self.tmp / "missing.bin")

    def test_directory_raises_not_a_regular_file_error(self):
        with self.assertRaises(NotARegularFileError):
            analyze_file(self.tmp)

    def test_read_failure_raises_file_read_error(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"data")

        with mock.patch.object(Path, "open", side_effect=OSError("boom")):
            with self.assertRaises(FileReadError) as ctx:
                analyze_file(sample)

        self.assertIsInstance(ctx.exception.__cause__, OSError)

    def test_cli_still_exits_with_code_2_for_each_error(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"data")
        cases = (self.tmp / "missing.bin", self.tmp)
        for path in cases:
            with self.subTest(path=path.name):
                with mock.patch("sys.argv", ["analyzer.py", str(path)]):
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit) as ctx:
                            main()
                self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()