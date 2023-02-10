"""Unit test file for metrics_parser.py."""
import json
import os
import inspect

from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory

from src.pubnub_python_metrics.models.user import pubnub_user
from src.pubnub_python_metrics.models.metrics import metric_parser

from unittest import TestCase


class TestMetricParser(TestCase):
    def setUp(self) -> None:
        class MyDotEnvDef:
            def __init__(self):
                self.email = "PN_CONSOLE_EMAIL"
                self.password = "PN_CONSOLE_PASSWORD"

            def __iter__(self):
                for attr, value in self.__dict__.items():
                    yield value

        cB = ConfigBuilder()
        config = cB.dotenv.load_dotenv().set_vars(MyDotEnvDef()).build()
        self.config = config
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        super().setUp()
        _frame = inspect.currentframe()
        test_filename = inspect.getframeinfo(_frame).filename  # type: ignore
        test_filename = os.path.basename(test_filename)
        self.log = LoggerFactory.new_logger_get_logger(test_filename, "DEBUG")
        return

    def test_init(self):
        metrics = metric_parser.MetricParser()
        self.assertEqual(str(metrics), "{'raw': None}")

    def test_get_app_based_usage(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore
        test_path = os.path.join(self.current_dir, "test_data", test_name)

        # Set test method
        metrics = metric_parser.MetricParser()
        test_method = metrics.get_app_based_usage

        # Set from dotenv. Override with your own
        email = self.config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = self.config.parsed_dotenv["PN_CONSOLE_PASSWORD"]

        # Log in and get first app_id
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()
        first_app_id = user.apps[user.accounts[0]][0]  # type: ignore
        print("first app_id: ", first_app_id)

        # test method
        test_method(first_app_id, user.token, "transaction", "2023-01-01", "2023-01-01")

        # write to file. Uncomment to write your own test data.
        # with open(os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "w") as f:
        # f.write(json.dumps(metrics.raw))

        # read from file
        expected = None
        with open(f"{test_path}.json", "r") as f:
            expected = json.load(f)

        self.assertEqual(metrics.raw, expected)

    def test_get_key_based_usage(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore
        test_path = os.path.join(self.current_dir, "test_data", test_name)

        # Set test method
        metrics = metric_parser.MetricParser()
        test_method = metrics.get_key_based_usage

        # Set from dotenv. Override with your own
        email = self.config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = self.config.parsed_dotenv["PN_CONSOLE_PASSWORD"]

        # Log in and get first app_id
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()
        first_app_id = user.apps[user.accounts[0]][0]  # type: ignore

        # get first key_id
        keys = user.get_keys(first_app_id)
        first_key_id = keys[0]

        # test method
        test_method(first_key_id, user.token, "transaction", "2023-01-01", "2023-01-01")

        # write to file
        # with open(os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "w") as f:
        # f.write(json.dumps(metrics.raw))

        # read from file
        expected = None
        with open(f"{test_path}.json", "r") as f:
            expected = json.load(f)

        self.assertEqual(metrics.raw, expected)
