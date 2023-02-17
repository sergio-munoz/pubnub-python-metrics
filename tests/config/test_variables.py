"""Unit test file for variables.py."""
import os
import inspect

from probable_fiesta.logger.builder.logger_factory import LoggerFactory

from src.pubnub_python_metrics.config import variables

from unittest import TestCase


class TestVariables(TestCase):
    def setUp(self) -> None:
        _frame = inspect.currentframe()
        test_filename = inspect.getframeinfo(_frame).filename  # type: ignore
        test_filename = os.path.basename(test_filename)
        self.log = LoggerFactory.new_logger_get_logger(test_filename, "DEBUG")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        return super().setUp()

    def test_init(self):
        ld = variables.LoggerDef
        self.assertEquals(ld.ROOT_DIR.split("/")[-1], "pubnub-python-metrics")
        self.assertEquals(ld.LEVEL, 20)
        self.assertEquals(
            "/".join(ld.DIRECTORY.split("/")[-2:]), "pubnub-python-metrics/logs"
        )
        self.assertEquals(ld.FORMAT, "simple")
        self.assertEquals(ld.NAME, "main_log")
        self.assertEquals(ld.TYPE, "default")
