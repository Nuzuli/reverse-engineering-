import json
import unittest

from src.report import REQUIRED_KEYS, format_json

SAMPLE = {
    "name": "sample.bin",
    "size_bytes": 5,
    "sha256": "abc123",
    "header_hex": "68 65 6c 6c 6f",
}


class TestFormatJson(unittest.TestCase):
    def test_output_is_valid_json_with_all_keys(self):
        data = json.loads(format_json(SAMPLE))

        self.assertEqual(data, SAMPLE)
        self.assertEqual(tuple(data), REQUIRED_KEYS)

    def test_empty_header_stays_empty_in_json(self):
        data = json.loads(format_json(dict(SAMPLE, header_hex="")))

        self.assertEqual(data["header_hex"], "")

    def test_extra_keys_are_ignored(self):
        data = json.loads(format_json(dict(SAMPLE, extra="x")))

        self.assertNotIn("extra", data)

    def test_missing_keys_raise_value_error(self):
        for key in REQUIRED_KEYS:
            with self.subTest(missing=key):
                incomplete = {k: v for k, v in SAMPLE.items() if k != key}
                with self.assertRaises(ValueError):
                    format_json(incomplete)


if __name__ == "__main__":
    unittest.main()