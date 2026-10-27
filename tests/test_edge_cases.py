import os
import tempfile
import unittest
from pathlib import Path

from src.analyzer import AnalysisError, analyze_file


class TestPathEdgeCases(unittest.TestCase):
    def test_empty_path_is_rejected(self):
        with self.assertRaises(AnalysisError):
            analyze_file("")

    def test_path_with_null_byte_is_rejected(self):
        with self.assertRaises(AnalysisError):
            analyze_file("bad\0name")


@unittest.skipUnless(hasattr(os, "symlink"), "symlinks are not supported")
class TestSymlinks(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def _link(self, name, target):
        link = self.tmp / name
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("cannot create symlinks here")
        return link

    def test_broken_symlink_is_rejected(self):
        link = self._link("broken", self.tmp / "missing.bin")

        with self.assertRaises(AnalysisError):
            analyze_file(link)

    def test_symlink_to_directory_is_rejected(self):
        link = self._link("dirlink", self.tmp)

        with self.assertRaises(AnalysisError):
            analyze_file(link)

    def test_symlink_to_file_is_analyzed(self):
        target = self.tmp / "target.bin"
        target.write_bytes(b"abc")
        link = self._link("alias.bin", target)

        result = analyze_file(link)

        self.assertEqual(result["name"], "alias.bin")
        self.assertEqual(result["size_bytes"], 3)


if __name__ == "__main__":
    unittest.main()