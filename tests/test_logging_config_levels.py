import unittest
import os
import logging
from src.analyzer import resolve_log_level

class TestLoggingConfig(unittest.TestCase):

    def test_defaults_to_warning(self):
        os.environ.pop("LOG_LEVEL", None)
        self.assertEqual(resolve_log_level(), logging.WARNING)

    def test_valid_levels_accepted(self):
        os.environ["LOG_LEVEL"] = "INFO"
        self.assertEqual(resolve_log_level(), logging.INFO)

    def test_lowercase_accepted(self):
        os.environ["LOG_LEVEL"] = "debug"
        self.assertEqual(resolve_log_level(), logging.DEBUG)

    def test_invalid_fallsback(self):
        os.environ["LOG_LEVEL"] = "SALAH"
        self.assertEqual(resolve_log_level(), logging.WARNING)

if __name__ == "__main__":
    unittest.main()
