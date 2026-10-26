import unittest

from src.report import REQUIRED_KEYS, format_report

SAMPLE = {
    "name": "sample.bin",
    "size_bytes": 5,
    "sha256": "abc123",
    "header_hex": "68 65 6c 6c 6f",
}


class TestFormatReport(unittest.TestCase):
    def test_contains_all_fields(self):
        report = format_report(SAMPLE)

        self.assertIn("=== File Analysis Report ===", report)
        self.assertIn("File name : sample.bin", report)
        self.assertIn("Size      : 5 bytes", report)
        self.assertIn("SHA-256   : abc123", report)
        self.assertIn("Header    : 68 65 6c 6c 6f", report)

    def test_report_has_one_line_per_field_plus_title(self):
        self.assertEqual(len(format_report(SAMPLE).splitlines()), 5)

    def test_empty_file_header_placeholder(self):
        result = dict(SAMPLE, size_bytes=0, header_hex="")

        self.assertIn("Header    : (empty file)", format_report(result))

    def test_missing_keys_raise_value_error(self):
        for key in REQUIRED_KEYS:
            with self.subTest(missing=key):
                incomplete = {k: v for k, v in SAMPLE.items() if k != key}
                with self.assertRaises(ValueError) as ctx:
                    format_report(incomplete)
                self.assertIn(key, str(ctx.exception))

    def test_empty_mapping_raises_value_error(self):
        with self.assertRaises(ValueError):
            format_report({})


if __name__ == "__main__":
    unittest.main()