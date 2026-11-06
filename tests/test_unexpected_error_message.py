import contextlib
import io
import unittest
from unittest import mock

from src.analyzer import AnalysisError, main


class TestUnexpectedErrorMessage(unittest.TestCase):
    def _run(self, **patch):
        err = io.StringIO()
        with mock.patch("sys.argv", ["analyzer.py", "anything.bin"]):
            with mock.patch("src.analyzer.analyze_file", **patch):
                with contextlib.redirect_stderr(err):
                    with self.assertRaises(SystemExit) as ctx:
                        main()
        return ctx.exception.code, err.getvalue()

    def test_unexpected_error_exits_2_with_short_message(self):
        code, err = self._run(side_effect=RuntimeError("boom"))
        self.assertEqual(code, 2)
        self.assertIn("unexpected error", err)
        self.assertNotIn("Traceback", err)

    def test_unexpected_error_is_logged_with_error_type(self):
        with self.assertLogs("src.analyzer", level="ERROR") as logs:
            self._run(side_effect=RuntimeError("boom"))
        self.assertTrue(any("analyze_unhandled_error" in m for m in logs.output))
        self.assertTrue(any("RuntimeError" in m for m in logs.output))

    def test_expected_analysis_error_keeps_its_own_message(self):
        code, err = self._run(side_effect=AnalysisError("File not found: x"))
        self.assertEqual(code, 2)
        self.assertIn("File not found: x", err)
        self.assertNotIn("unexpected error", err)


if __name__ == "__main__":
    unittest.main()