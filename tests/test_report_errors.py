import json
import unittest

from src.report import REQUIRED_KEYS, format_json, format_report

SAMPLE = {
    "name": "sample.bin",
    "size_bytes": 5,
    "sha256": "abc123",
    "header_hex": "68 65 6c 6c 6f",
}


class TestFormatJsonErrors(unittest.TestCase):
    def test_missing_key_raises_value_error_naming_the_key(self):
        for key in REQUIRED_KEYS:
            with self.subTest(missing=key):
                incomplete = {k: v for k, v in SAMPLE.items() if k != key}
                with self.assertRaises(ValueError) as ctx:
                    format_json(incomplete)
                self.assertIn(key, str(ctx.exception))

    def test_empty_mapping_lists_every_missing_key(self):
        with self.assertRaises(ValueError) as ctx:
            format_json({})
        for key in REQUIRED_KEYS:
            self.assertIn(key, str(ctx.exception))

    def test_error_message_lists_all_missing_keys_at_once(self):
        with self.assertRaises(ValueError) as ctx:
            format_report({"name": "only-name"})
        message = str(ctx.exception)
        for key in ("size_bytes", "sha256", "header_hex"):
            self.assertIn(key, message)


class TestFormatJsonShape(unittest.TestCase):
    def test_extra_keys_are_ignored(self):
        data = json.loads(format_json(dict(SAMPLE, extra="ignored")))
        self.assertEqual(sorted(data), sorted(REQUIRED_KEYS))

    def test_keys_keep_the_documented_order(self):
        data = json.loads(format_json(SAMPLE))
        self.assertEqual(list(data), list(REQUIRED_KEYS))

    def test_empty_header_stays_an_empty_string(self):
        data = json.loads(format_json(dict(SAMPLE, header_hex="")))
        self.assertEqual(data["header_hex"], "")


if __name__ == "__main__":
    unittest.main()