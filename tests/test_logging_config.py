import io
import json
import logging
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.logging_config import (DEFAULT_LEVEL, JsonFormatter,
                                configure_logging, resolve_level)

REPO_ROOT = Path(__file__).resolve().parents[1]


def make_record(level=logging.INFO, exc_info=None):
    return logging.LogRecord(
        "src.test", level, __file__, 1, "hello %s", ("world",), exc_info
    )


class TestJsonFormatter(unittest.TestCase):
    def test_output_is_valid_json_with_expected_keys(self):
        data = json.loads(JsonFormatter().format(make_record()))
        self.assertEqual(
            set(data), {"timestamp", "level", "logger", "message"}
        )
        self.assertEqual(data["level"], "INFO")
        self.assertEqual(data["logger"], "src.test")
        self.assertEqual(data["message"], "hello world")

    def test_exception_text_is_included(self):
        try:
            raise ValueError("boom")
        except ValueError:
            record = make_record(logging.ERROR, sys.exc_info())
        data = json.loads(JsonFormatter().format(record))
        self.assertIn("ValueError: boom", data["exception"])


class TestResolveLevel(unittest.TestCase):
    def test_missing_value_uses_default(self):
        self.assertEqual(resolve_level(None), DEFAULT_LEVEL)
        self.assertEqual(resolve_level(""), DEFAULT_LEVEL)

    def test_names_are_case_and_space_insensitive(self):
        self.assertEqual(resolve_level("debug"), logging.DEBUG)
        self.assertEqual(resolve_level(" Info "), logging.INFO)

    def test_unknown_name_falls_back_to_default(self):
        self.assertEqual(resolve_level("loud"), DEFAULT_LEVEL)


class TestConfigureLogging(unittest.TestCase):
    def setUp(self):
        self.root = logging.getLogger()
        self.saved_level = self.root.level
        self.handlers = []
        self.addCleanup(self._restore)

    def _restore(self):
        for handler in self.handlers:
            self.root.removeHandler(handler)
        self.root.setLevel(self.saved_level)

    def _configure(self, *args, **kwargs):
        handler = configure_logging(*args, **kwargs)
        self.handlers.append(handler)
        return handler

    def test_writes_json_lines_to_the_given_stream(self):
        buffer = io.StringIO()
        self._configure(logging.INFO, stream=buffer)
        logging.getLogger("src.demo").info("done size=%d", 3)
        data = json.loads(buffer.getvalue().strip())
        self.assertEqual(data["message"], "done size=3")
        self.assertEqual(data["logger"], "src.demo")

    def test_level_filters_lower_severity_records(self):
        buffer = io.StringIO()
        self._configure(logging.WARNING, stream=buffer)
        logging.getLogger("src.demo").info("hidden")
        self.assertEqual(buffer.getvalue(), "")

    def test_calling_twice_replaces_the_handler(self):
        first = self._configure(logging.DEBUG, stream=io.StringIO())
        second = self._configure(logging.INFO, stream=io.StringIO())
        self.assertNotIn(first, self.root.handlers)
        self.assertIn(second, self.root.handlers)
        self.assertEqual(self.root.level, logging.INFO)


class TestLogLevelEnvironmentVariable(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.sample = Path(self._tmp.name) / "sample.bin"
        self.sample.write_bytes(b"hello")

    def _run(self, **env):
        environment = {
            key: value for key, value in os.environ.items()
            if key != "LOG_LEVEL"
        }
        environment.update(env)
        return subprocess.run(
            [sys.executable, "-m", "src.analyzer", str(self.sample)],
            cwd=REPO_ROOT, env=environment,
            capture_output=True, text=True, check=False,
        )

    def test_log_level_enables_json_logs_on_stderr(self):
        result = self._run(LOG_LEVEL="INFO")
        self.assertEqual(result.returncode, 0)
        lines = [line for line in result.stderr.splitlines() if line]
        messages = [json.loads(line)["message"] for line in lines]
        self.assertTrue(any(m.startswith("analyze_done") for m in messages))
        self.assertIn("SHA-256", result.stdout)

    def test_without_log_level_stderr_stays_empty(self):
        result = self._run()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()