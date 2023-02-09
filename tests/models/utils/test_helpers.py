"""Unit test file for helpers.py."""
import os

from src.pubnub_python_metrics.utils import helpers

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestMetricsParser(TestCase):

    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        return super().setUp()

    def test_get_os_dir(self):
        res = helpers.get_os_dir()
        self.assertEqual(res, self.current_dir)
    
    def test_get_file_dir(self):
        res = helpers.get_file_dir()
        print(res)
        self.assertEqual(res, self.current_dir)
    