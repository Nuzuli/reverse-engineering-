import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.analyzer import AnalysisError, analyze_file

LOGGER_NAME = "src.analyzer"


class TestAnalyzerLogging(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def test_successful_analysis_logs_start_and_finish(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"hello")

        with self.assertLogs(LOGGER_NAME, level="INFO") as captured:
            analyze_file(sample)

        messages = [record.getMessage() for record in captured.records]
        self.assertEqual(len(messages), 2)
        self.assertIn("Analyzing", messages[0])
        self.assertIn("Finished sample.bin (5 bytes)", messages[1])

    def test_missing_file_is_logged_before_error(self):
        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
            with self.assertRaises(AnalysisError):
                analyze_file(self.tmp / "missing.bin")

        self.assertTrue(
            any("file not found" in line for line in captured.output)
        )

    def test_directory_is_logged_before_error(self):
        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
            with self.assertRaises(AnalysisError):
                analyze_file(self.tmp)

        self.assertTrue(
            any("not a regular file" in line for line in captured.output)
        )

    def test_read_failure_is_logged_before_error(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"data")

        with mock.patch.object(Path, "open", side_effect=OSError("boom")):
            with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
                with self.assertRaises(AnalysisError):
                    analyze_file(sample)

        self.assertTrue(any("Read failed" in line for line in captured.output))


if __name__ == "__main__":
    unittest.main()