"""Unit test file for metric_holder.py."""
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


class TestMetricHolder(TestCase):
    def setUp(self) -> None:
        super().setUp()
        _frame = inspect.currentframe()
        test_filename = inspect.getframeinfo(_frame).filename  # type: ignore
        test_filename = os.path.basename(test_filename)
        self.log = LoggerFactory.new_logger_get_logger(test_filename, "DEBUG")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        return

    def test_metric_holder(self):
        # Set test
        _frame = inspect.currentframe()
        test_name = inspect.getframeinfo(_frame).function  # type: ignore
        test_path = os.path.join(self.current_dir, "test_data", test_name)

        # Set raw metrics from file
        raw = None
        with open(f"{test_path}.json") as f:
            raw = json.load(f)

        # Create MetricPandas
        mp = metric_pandas.MetricPandas(raw)
        # Create MetricBuilder
        csv_file = os.path.join(self.current_dir, "test_data", f"{test_name}.csv")
        mb = metric.MetricBuilder()
        # Current csv file
        metrics = mb.with_csv_file(csv_file, mp)

        mh = metric_holder.MetricHolder(metrics)
        features_totals = {}
        for feature in list(set(mh.features)):  # type: ignore
            tot = sum([x.total for x in metrics if x.feature == feature])
            # print(f"--TOTAL By Feature: {feature} = {tot}")
            features_totals[feature] = tot

        types_totals = {}
        for type in list(set(mh.types)):
            tot = sum([x.total for x in metrics if x.type == type])
            # print(f"--TOTAL By Type: {type} = {tot}")
            types_totals[type] = tot

        names_totals = {}
        for name in mh.names:
            tot = sum([x.total for x in metrics if x.name == name])
            # print(f"--TOTAL By Name: {name} = {tot}")
            names_totals[name] = tot

        self.assertEqual(
            types_totals, {"fre": 0, "edg": 640.0, "rep": 1015.0, "ma": 0, "sig": 0}
        )
        self.assertEqual(
            names_totals,
            {
                "transaction_accessmanager_audits": 0,
                "transaction_accessmanager_clienterrors": 0,
                "transaction_apns_sent": 0,
                "transaction_fcm_sent": 0,
                "transaction_files_clienterrors": 0,
                "transaction_files_delete_file": 0,
                "transaction_files_generate_url": 0,
                "transaction_files_get_all_files": 0,
                "transaction_files_get_file": 0,
                "transaction_files_unauthorized": 0,
                "transaction_history": 6.0,
                "transaction_history_clienterrors": 0,
                "transaction_history_messages_count": 0,
                "transaction_history_with_actions": 0,
                "transaction_history_with_actions_clienterrors": 0,
                "transaction_history_with_actions_unauthorized": 0,
                "transaction_kv_read": 0,
                "transaction_message_actions_clienterrors": 0,
                "transaction_message_actions_get": 0,
                "transaction_objects_clienterrors": 0,
                "transaction_objects_get_all_spaces": 0,
                "transaction_objects_get_all_users": 0,
                "transaction_objects_get_space": 0,
                "transaction_objects_get_space_user_memberships": 0,
                "transaction_objects_get_user": 0,
                "transaction_objects_get_user_space_memberships": 0,
                "transaction_objects_reads": 0,
                "transaction_objects_unauthorized": 0,
                "transaction_presence_clienterrors": 0,
                "transaction_presence_getuserstate": 0,
                "transaction_presence_heartbeats": 0,
                "transaction_presence_herenow": 6.0,
                "transaction_presence_herenow_global": 0,
                "transaction_presence_leave": 17.0,
                "transaction_presence_wherenow": 0,
                "transaction_publish_clienterrors": 0,
                "transaction_publish_unauthorized": 0,
                "transaction_push_device_clienterrors": 0,
                "transaction_push_device_reads": 0,
                "transaction_streamcontroller_clienterrors": 0,
                "transaction_streamcontroller_reads": 0,
                "transaction_subscribe": 425.0,
                "transaction_subscribe_clientclosedconnection": 35.0,
                "transaction_subscribe_clienterrors": 0,
                "transaction_subscribe_files": 0,
                "transaction_subscribe_heartbeats": 34.0,
                "transaction_subscribe_objects": 0,
                "transaction_subscribe_streaming": 0,
                "transaction_subscribe_timeouts": 117.0,
                "transaction_subscribe_unauthorized": 0,
                "transaction_fire": 0,
                "transaction_fire_client": 0,
                "transaction_fire_eh": 0,
                "transaction_message_actions_add": 0,
                "transaction_message_actions_remove": 0,
                "transaction_message_actions_subscribe": 0,
                "transaction_message_actions_unauthorized": 0,
                "transaction_accessmanager_grants": 0,
                "transaction_apns_removed": 0,
                "transaction_fcm_removed": 0,
                "transaction_files_publish": 0,
                "transaction_internal_publish_objects": 0,
                "transaction_kv_write": 0,
                "transaction_misfire_client": 0,
                "transaction_misfire_eh": 0,
                "transaction_objects_create_space": 0,
                "transaction_objects_create_user": 0,
                "transaction_objects_delete_space": 0,
                "transaction_objects_delete_user": 0,
                "transaction_objects_update_space": 0,
                "transaction_objects_update_space_user_memberships": 0,
                "transaction_objects_update_user": 0,
                "transaction_objects_update_user_space_memberships": 0,
                "transaction_objects_writes": 0,
                "transaction_presence_setuserstate": 0,
                "transaction_publish": 1015.0,
                "transaction_push_device_writes": 0,
                "transaction_streamcontroller_writes": 0,
                "transaction_signal": 0,
                "transaction_signal_clienterrors": 0,
                "transaction_signal_unauthorized": 0,
                "transaction_subscribe_signal": 0,
            },
        )
        self.assertEqual(
            features_totals,
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
