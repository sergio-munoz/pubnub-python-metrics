"""Unit test file for metrics_pandas.py."""
import json
import os
import inspect

from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory

from src.pubnub_python_metrics.models.user import pubnub_user
from src.pubnub_python_metrics.models.metrics import metric_parser
from src.pubnub_python_metrics.models.metrics import metric_pandas

from src.pubnub_python_metrics.config.variables import LoggerDef as ld

from unittest import TestCase


class TestMetricPandas(TestCase):
    def setUp(self) -> None:
        _frame = inspect.currentframe()
        test_filename = inspect.getframeinfo(_frame).filename  # type: ignore
        test_filename = os.path.basename(test_filename).split(".")[0]
        self.log = LoggerFactory.new_logger_get_logger(
            test_filename, "DEBUG", directory=ld.DIRECTORY
        )
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        return super().setUp()

    def test_metric_pandas_validate(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore
        test_path = os.path.join(self.current_dir, "test_data", test_name)

        # Validate 1
        raw = None
        with open(f"{test_path}_1.json", "r") as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        strict_pn_metrics = mp.validate()

        self.assertEqual(len(strict_pn_metrics), 146)
        self.assertEqual(str(strict_pn_metrics[0]), "name='active_keys' total=0.0")

        # Validate 2
        raw = None
        with open(f"{test_path}_2.json", "r") as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        strict_pn_metrics = mp.validate()

        self.assertEqual(len(strict_pn_metrics), 146)
        self.assertEqual(str(strict_pn_metrics[0]), "name='active_keys' total=0.0")

        # Validate 3
        raw = None
        with open(f"{test_path}_3.json", "r") as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        strict_pn_metrics = mp.validate()

        self.assertEqual(len(strict_pn_metrics), 146)
        self.assertEqual(str(strict_pn_metrics[0]), "name='active_keys' total=0.0")

    def test_metric_pandas_init(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore

        # set raw metrics from file
        raw = None
        with open(
            os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "r"
        ) as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        print(mp.metrics.to_dict(orient="records"))
        res = mp.extract_total("transactions_total")
        self.assertEqual(res, 1655.0)

    def test_metric_pandas_init_2(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore

        # set raw metrics from file
        raw = None
        with open(
            os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "r"
        ) as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        res = mp.extract_total("transactions_total")
        self.assertEqual(res, 12.0)

    def test_metric_pandas_init_3(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore

        # set raw metrics from file
        raw = None
        with open(
            os.path.join(self.current_dir, "test_data", f"{test_name}.json"), "r"
        ) as f:
            raw = json.load(f)
        mp = metric_pandas.MetricPandas(raw)
        res = mp.extract_total("transactions_total")
        self.assertEqual(res, 0.0)

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
        test_method(first_app_id, user.token, "transaction", "2023-01-01", "2023-01-01")

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
