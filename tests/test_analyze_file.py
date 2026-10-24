import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.analyzer import AnalysisError, analyze_file, main


class TestAnalyzeFile(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def _make_file(self, data, name="sample.bin"):
        path = self.tmp / name
        path.write_bytes(data)
        return path

    def test_returns_expected_fields(self):
        result = analyze_file(self._make_file(b"hello"))

        self.assertEqual(
            set(result.keys()),
            {"name", "size_bytes", "sha256", "header_hex"},
        )
        self.assertEqual(result["name"], "sample.bin")
        self.assertEqual(result["size_bytes"], 5)
        self.assertEqual(result["sha256"], hashlib.sha256(b"hello").hexdigest())
        self.assertEqual(result["header_hex"], "68 65 6c 6c 6f")

    def test_accepts_string_path(self):
        path = self._make_file(b"abc")
        result = analyze_file(str(path))
        self.assertEqual(result["size_bytes"], 3)

    def test_header_is_limited_to_16_bytes(self):
        data = bytes(range(32))
        result = analyze_file(self._make_file(data))

        expected = " ".join(f"{b:02x}" for b in range(16))
        self.assertEqual(result["header_hex"], expected)
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())

    def test_empty_file(self):
        result = analyze_file(self._make_file(b""))

        self.assertEqual(result["size_bytes"], 0)
        self.assertEqual(result["header_hex"], "")
        self.assertEqual(result["sha256"], hashlib.sha256(b"").hexdigest())

    def test_large_file_uses_chunked_read(self):
        data = b"A" * 20000
        result = analyze_file(self._make_file(data))

        self.assertEqual(result["size_bytes"], 20000)
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())

    def test_missing_file_raises(self):
        with self.assertRaises(AnalysisError):
            analyze_file(self.tmp / "tidak_ada.bin")

    def test_directory_raises(self):
        with self.assertRaises(AnalysisError):
            analyze_file(self.tmp)

    def test_unreadable_file_raises(self):
        path = self._make_file(b"data")
        with mock.patch.object(Path, "open", side_effect=OSError("boom")):
            with self.assertRaises(AnalysisError):
                analyze_file(path)


class TestMain(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def _run_main(self, path):
        buffer = io.StringIO()
        with mock.patch("sys.argv", ["analyzer.py", str(path)]):
            with contextlib.redirect_stdout(buffer):
                main()
        return buffer.getvalue()

    def test_main_prints_report(self):
        path = self.tmp / "sample.bin"
        path.write_bytes(b"hello")

        output = self._run_main(path)

        self.assertIn("File Analysis Report", output)
        self.assertIn("sample.bin", output)
        self.assertIn("5 bytes", output)
        self.assertIn(hashlib.sha256(b"hello").hexdigest(), output)

    def test_main_reports_empty_file(self):
        path = self.tmp / "empty.bin"
        path.write_bytes(b"")

        output = self._run_main(path)

        self.assertIn("(empty file)", output)

    def test_main_exits_with_error_for_missing_file(self):
        with mock.patch("sys.argv", ["analyzer.py", str(self.tmp / "none.bin")]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as ctx:
                    main()
        self.assertEqual(ctx.exception.code, 2)