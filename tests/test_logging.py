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

    def _messages(self, captured):
        return [record.getMessage() for record in captured.records]

    def test_successful_analysis_logs_start_and_done_fields(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"hello")

        with self.assertLogs(LOGGER_NAME, level="INFO") as captured:
            analyze_file(sample)

        messages = self._messages(captured)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], f"analyze_start path={sample}")
        self.assertEqual(messages[1], "analyze_done name=sample.bin size_bytes=5")

    def test_missing_file_logs_reason_field(self):
        missing = self.tmp / "missing.bin"

        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
            with self.assertRaises(AnalysisError):
                analyze_file(missing)

        self.assertIn(
            f"analyze_rejected path={missing} reason=file_not_found",
            self._messages(captured),
        )

    def test_directory_logs_reason_field(self):
        with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
            with self.assertRaises(AnalysisError):
                analyze_file(self.tmp)

        self.assertIn(
            f"analyze_rejected path={self.tmp} reason=not_a_regular_file",
            self._messages(captured),
        )

    def test_read_failure_logs_error_field(self):
        sample = self.tmp / "sample.bin"
        sample.write_bytes(b"data")

        with mock.patch.object(Path, "open", side_effect=OSError("boom")):
            with self.assertLogs(LOGGER_NAME, level="DEBUG") as captured:
                with self.assertRaises(AnalysisError):
                    analyze_file(sample)

        self.assertIn(
            f"analyze_failed path={sample} error=boom",
            self._messages(captured),
        )


if __name__ == "__main__":
    unittest.main()