import os
import stat
import tempfile
import unittest
from pathlib import Path

from src.analyzer import (AnalysisError, FileNotFoundAnalysisError,
                          FileReadError, analyze_file)


class TestPathEdgeCases(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are not supported")
    def test_symlink_loop_is_reported_as_not_found(self):
        first = self.tmp / "first"
        second = self.tmp / "second"
        first.symlink_to(second)
        second.symlink_to(first)
        with self.assertRaises(FileNotFoundAnalysisError):
            analyze_file(first)

    @unittest.skipUnless(hasattr(os, "geteuid"), "needs POSIX permissions")
    def test_unreadable_file_raises_file_read_error(self):
        if os.geteuid() == 0:
            self.skipTest("root can read any file")
        locked = self.tmp / "locked.bin"
        locked.write_bytes(b"secret")
        locked.chmod(0)
        self.addCleanup(locked.chmod, stat.S_IRUSR | stat.S_IWUSR)
        with self.assertRaises(FileReadError) as ctx:
            analyze_file(locked)
        self.assertIn("Unable to read", str(ctx.exception))
        self.assertIsInstance(ctx.exception, AnalysisError)


if __name__ == "__main__":
    unittest.main()