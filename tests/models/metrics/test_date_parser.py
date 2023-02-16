"""Unit test file for date_parser.py."""
from unittest import TestCase
from src.pubnub_python_metrics.models.metrics import date_parser
import datetime


class TestDateParser(TestCase):
    def setUp(self) -> None:
        self.now = datetime.datetime(year=2018, month=8, day=4)
        self.now_str = self.now.strftime("%Y-%m-%d")
        return super().setUp()

    def test_init(self):
        dp = date_parser.DateParser(self.now)
        parsed = dp.parse()

        self.assertEqual(parsed.strftime("%Y-%m-%d"), self.now_str)  # type: ignore

    def test_to_string(self):
        dp = date_parser.DateParser(self.now_str)
        parsed = dp.parse()

        self.assertEqual(date_parser.DateParser.dt_to_string(parsed), self.now_str)
