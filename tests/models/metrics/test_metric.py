"""Unit test file for metrics.py."""
import json
import os
import inspect

from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory

from src.pubnub_python_metrics.models.user import pubnub_user
from src.pubnub_python_metrics.models.metrics import metric_parser
from src.pubnub_python_metrics.models.metrics import metric_pandas
from src.pubnub_python_metrics.models.metrics import metric
from src.pubnub_python_metrics.models.metrics import metric_holder

from unittest import TestCase


class TestMetric(TestCase):
    def setUp(self) -> None:
        super().setUp()
        _frame = inspect.currentframe()
        test_filename = inspect.getframeinfo(_frame).filename  # type: ignore
        test_filename = os.path.basename(test_filename)
        self.log = LoggerFactory.new_logger_get_logger(test_filename, "DEBUG")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        return

    def test_metric_builder_with_csv_file(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore
        test_path = os.path.join(self.current_dir, "test_data", test_name)

        # Set raw metrics from file
        raw = None
        with open(f"{test_path}.json", "r") as f:
            raw = json.load(f)

        # Create MetricPandas
        mp = metric_pandas.MetricPandas(raw)
        res = mp.extract_total("transactions_total")
        self.assertEqual(res, 1655.0)

        # Create MetricBuilder
        csv_file = os.path.join(self.current_dir, "test_data", f"{test_name}.csv")
        mb = metric.MetricBuilder()

        # Current csv file has 82 rows
        metrics = mb.with_csv_file(csv_file, mp)
        self.assertEqual(len(metrics), 82)

        # Check totals by type
        tot = sum([x.total for x in metrics if x.type == "edg"])
        self.assertEqual(tot, 640.0)
        tot = sum([x.total for x in metrics if x.type == "rep"])
        self.assertEqual(tot, 1015.0)
        tot = sum([x.total for x in metrics if x.type == "sig"])
        self.assertEqual(tot, 0)
        tot = sum([x.total for x in metrics if x.type == "ma"])
        self.assertEqual(tot, 0)

        # Use metric holder to get easier access to metrics
        mh = metric_holder.MetricHolder(metrics)
        # print(mh.names)  # type: ignore
        # print(mh.types)  # type: ignore
        # print(mh.totals)  # type: ignore
        # print(mh.get("transactions_total"))  # type: ignore

        # Check totals by feature
        # manually
        tot = sum([x.total for x in metrics if x.feature == "publish"])
        self.assertEqual(tot, 1015.0)
        # using metric holder
        tot = mh.total_of_feature("publish")  # type: ignore
        self.assertEqual(tot, 1015.0)
        # iterate all features using metric holder
        totals = {}
        for feature in list(set(mh.features)):  # type: ignore
            tot = sum([x.total for x in metrics if x.feature == feature])
            # print(f"--TOTAL By Feature: {feature} = {tot}")
            totals[feature] = tot

        self.assertEqual(
            totals,
            {
                "files": 0,
                "presence": 23.0,
                "message actions": 0,
                "channel groups": 0,
                "fire": 0,
                "publish": 1015.0,
                "history with actions": 0,
                "funcitons": 0,
                "signal": 0,
                "push": 0,
                "objects": 0,
                "subscribe": 611.0,
                "access manager": 0,
                "history": 6.0,
                "history counts": 0,
                "functions": 0,
            },
        )

    def get_and_write_metrics(self):
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
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore

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
        test_method(first_app_id, user.token, "transaction", "2023-01-21", "2023-02-08")

        # write to file. Uncomment to write your own test data.
        with open(
            os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "w"
        ) as f:
            f.write(json.dumps(metrics.raw))

        # read from file
        expected = None
        with open(
            os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "r"
        ) as f:
            expected = json.load(f)

        self.assertEqual(metrics.raw, expected)
