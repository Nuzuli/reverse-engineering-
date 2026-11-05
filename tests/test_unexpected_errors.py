import contextlib
import io
import unittest
from unittest import mock

from src.analyzer import AnalysisError, main


class TestUnexpectedErrors(unittest.TestCase):
    def _jalankan(self, **patch):
        err = io.StringIO()
        with mock.patch("sys.argv", ["analyzer.py", "apa-saja.bin"]):
            with mock.patch("src.analyzer.analyze_file", **patch):
                with contextlib.redirect_stderr(err):
                    with self.assertRaises(SystemExit) as ctx:
                        main()
        return ctx.exception.code, err.getvalue()

    def test_kesalahan_tak_terduga_keluar_kode_2_dengan_pesan(self):
        kode, err = self._jalankan(side_effect=RuntimeError("boom"))
        self.assertEqual(kode, 2)
        self.assertIn("kesalahan tak terduga", err)
        self.assertNotIn("Traceback", err)

    def test_kesalahan_tak_terduga_dicatat_di_log(self):
        with self.assertLogs("src.analyzer", level="ERROR") as logs:
            self._jalankan(side_effect=RuntimeError("boom"))
        self.assertTrue(any("analyze_unhandled_error" in m for m in logs.output))
        self.assertTrue(any("RuntimeError" in m for m in logs.output))

    def test_kesalahan_analisis_biasa_tetap_pesan_lama(self):
        kode, err = self._jalankan(side_effect=AnalysisError("File not found: x"))
        self.assertEqual(kode, 2)
        self.assertIn("File not found: x", err)
        self.assertNotIn("kesalahan tak terduga", err)


if __name__ == "__main__":
    unittest.main()