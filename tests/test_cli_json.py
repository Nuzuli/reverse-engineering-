import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.analyzer import main


class TestJsonFlag(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def _run(self, *args):
        buffer = io.StringIO()
        with mock.patch("sys.argv", ["analyzer.py", *args]):
            with contextlib.redirect_stdout(buffer):
                main()
        return buffer.getvalue()

    def test_json_flag_prints_valid_json_with_sha256(self):
        path = self.tmp / "sample.bin"
        path.write_bytes(b"hello")

        data = json.loads(self._run(str(path), "--json"))

        self.assertEqual(data["sha256"], hashlib.sha256(b"hello").hexdigest())
        self.assertEqual(data["name"], "sample.bin")
        self.assertEqual(data["size_bytes"], 5)

    def test_json_flag_keeps_empty_header_empty(self):
        path = self.tmp / "empty.bin"
        path.write_bytes(b"")

        data = json.loads(self._run(str(path), "--json"))

        self.assertEqual(data["header_hex"], "")

    def test_default_output_is_not_json(self):
        path = self.tmp / "sample.bin"
        path.write_bytes(b"hello")

        output = self._run(str(path))

        self.assertIn("File Analysis Report", output)
        with self.assertRaises(ValueError):
            json.loads(output)


if __name__ == "__main__":
    unittest.main()