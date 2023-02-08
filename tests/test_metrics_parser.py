"""Unit test file for metrics_parser.py."""
import json

from probable_fiesta.config.builder.config_builder import ConfigBuilder

from src.pubnub_python_metrics.pubnub import pubnub_user
from src.pubnub_python_metrics.pubnub import pubnub_user
from src.pubnub_python_metrics.metrics import pandas_metrics
from src.pubnub_python_metrics.metrics import metrics_parser
from src.pubnub_python_metrics.metrics import pubnub_metrics

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestMetricsParser(TestCase):

    def test_init(self):
        metrics = metrics_parser.MyMetric()
        self.assertEqual(str(metrics), "{'raw': None}")

    def test_get_app_based_usage(self):
        metrics = metrics_parser.MyMetric()
        class MyDotEnvDef():
            def __init__(self):
                self.email = "PN_CONSOLE_EMAIL"
                self.password = "PN_CONSOLE_PASSWORD"
            def __iter__(self):
                for attr, value in self.__dict__.items():
                    yield value
        cB = ConfigBuilder()
        config = cB.dotenv.load_dotenv().set_vars(MyDotEnvDef()).build()
        email = config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = config.parsed_dotenv["PN_CONSOLE_PASSWORD"]
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()
        print("user apps: ", user.apps)

        first_app_id = user.apps[user.accounts[0]][0]
        
        print("first app_id: ", first_app_id)
        
        # get key usage for first_key
        start = "2023-01-29"
        end = "2023-02-06"
        metrics.get_app_based_usage(first_app_id, user.token, "transaction", start, end)
        #print(type(metrics.raw))
        loaded = json.loads(metrics.raw)
        #print("\n--app based usage--\n", (loaded))

        pm = pandas_metrics.PandasMetrics((loaded)) # get from active_keys
        pm.load()
        #print("PM Loaded: \n", pm.metrics)
        print("Describe: ", pm.metrics.describe())
        #print("HEAD: ", pm.metrics.head())
        tx_pub = pm.get_col_by_name("transaction_publish")
        print("tx_pub :", tx_pub)
        z = 0
        for i in tx_pub:
            print("day in tx_pub: ", i)
            z += i['sum']
        print("sum of tx_pub: ", z)
        self.assertEqual(z, pm.get_sum_of_name("transaction_publish"))

    def test_get_all_app_based_usage(self):
        metrics = metrics_parser.MyMetric()
        class MyDotEnvDef():
            def __init__(self):
                self.email = "PN_CONSOLE_EMAIL"
                self.password = "PN_CONSOLE_PASSWORD"
            def __iter__(self):
                for attr, value in self.__dict__.items():
                    yield value
        cB = ConfigBuilder()
        config = cB.dotenv.load_dotenv().set_vars(MyDotEnvDef()).build()
        email = config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = config.parsed_dotenv["PN_CONSOLE_PASSWORD"]
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()

        # get key usage for first_key
        first_app_id = user.apps[user.accounts[0]][0]
        start = "2023-01-29"
        end = "2023-02-06"
        metrics.get_app_based_usage(first_app_id, user.token, "transaction", start, end)

        loaded = json.loads(metrics.raw)
        pm = pandas_metrics.PandasMetrics(loaded)
        pm.load()
        for m in pm.raw:
            print(f"Total of {m}: {pm.get_sum_of_name(m)}")


        # Open the CSV file
        pnm = pubnub_metrics.PubNubMetrics(pm)
        import os
        with open(os.path.join(os.path.dirname(__file__), "test_data", "tx_api.csv"), "r") as file:
            pnm.load_tx_api_file(file)
        # Access the data as a dictionary
        obj = pnm.tx_api
        print(obj)
        a = pnm.by_api("transaction_publish")
        print("THIS RES: ", a)
        self.assertEqual(1655.0, pm.get_sum_of_name("transaction_publish"))
        self.assertEqual(True, False)

    def test_get_app_key_based_usage(self):
        metrics = metrics_parser.MyMetric()
        class MyDotEnvDef():
            def __init__(self):
                self.email = "PN_CONSOLE_EMAIL"
                self.password = "PN_CONSOLE_PASSWORD"
            def __iter__(self):
                for attr, value in self.__dict__.items():
                    yield value
        cB = ConfigBuilder()
        config = cB.dotenv.load_dotenv().set_vars(MyDotEnvDef()).build()
        email = config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = config.parsed_dotenv["PN_CONSOLE_PASSWORD"]
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()
        print("user apps: ", user.apps)

        first_app_id = user.apps[user.accounts[0]][0]
        keys = user.get_keys(first_app_id, 2, 1)
        first_key = None
        for result in keys:
            for app in keys[result]:
                print(app.keys())
                print("app id: ", app['id'])
                first_key = app['id']
                print(first_key)
            break
        
        print("first key: ", first_key)
        
        # get key usage for first_key
        start = "2023-01-30"
        end = "2023-02-06"
        metrics.get_key_based_usage(first_key, user.token, "transaction", start, end)
        #print("\n--key_based_usage--\n", metrics.raw)
        #print(metrics.raw)
        #for m in metrics.raw:
            #print("metrics m: ", m)
        #print(metrics.raw[0])
        loaded_metrics = json.loads(metrics.raw)
        print("Loaded: \n", loaded_metrics)
        pm = pandas_metrics.PandasMetrics(loaded_metrics) # get from active_keys
        pm.load()
        print("PM Loaded: \n", pm)
        print("Describe: ", pm.metrics.describe())
        tx_pub = pm.get_col_by_name("transaction_publish")
        print(tx_pub.to_numpy())
        #print()
        #tx_total = pm.metrics['transaction_publish']
        #pm2 = pandas_metrics.PandasMetrics(tx_total)
        #print(pm2)
        #print(pm2.metrics.describe())




        #ts = pandas.Series(metrics.metrics['edge'].values, index=metrics.metrics['edge'])
        #print("ts: ", ts)
        #print("describe: ", ts.describe())
        #print("all: ", ts.all())
        #print("explode: ", ts.explode())
        #print("sum: ", ts.sum())
        
        # get first app_id for app based usage
        #metrics.get_app_based_usage(first_app_id, user.token, "transaction", start, end)
        #print(metrics.raw)
        import os
        # write to file
        #with open(os.path.join(os.path.dirname(__file__), "test_data", "sample_test_pandas_metrics.json"), "w") as f:
            #f.write(json.dumps(metrics.raw))
        # read from file
        expected = None
        with open(os.path.join(os.path.dirname(__file__), "test_data", "sample_test_get_metric.json"), "r") as f:
            expected = json.load(f)
        self.assertEqual(True, False)