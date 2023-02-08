"""Unit test file for pandas_metrics.py."""
from probable_fiesta.config.builder.config_builder import ConfigBuilder

from src.pubnub_python_metrics.metrics import pandas_metrics

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestPandasMetrics(TestCase):

    def test_init(self):
        metrics = pandas_metrics.PandasMetrics(None)
        self.assertEqual(str(metrics), "{'raw': None, 'metrics': None, 'error': ''}")

    def test_load(self):
        import os
        import json
        import pandas
        metrics = None
        with open(os.path.join(os.path.dirname(__file__), "test_data", "sample_test_pandas_metrics.json"), "r") as f:
            metrics = pandas_metrics.PandasMetrics(f)
            metrics.load()

        # Metrics is now a DataFrame
        print("DataFrame: ", metrics.metrics)
        for m in metrics.metrics:
            print(m)

        # Create series from DataFrame
        ts = pandas.Series(metrics.metrics['edge'].values, index=metrics.metrics['edge'])
        print("ts: ", ts)
        print("describe: ", ts.describe())
        print("all: ", ts.all())
        print("explode: ", ts.explode())
        print("sum: ", ts.sum())
        
        #test2 = ts.resample('days').sum()
        #print("test2: ", test2)

        #test3 = ts.resample('sum').sum()
        #print("test3: ", test3)

        #total = ts.sum("total")
        #print("total: ", total)

        print(metrics.get_col_by_name("edge"))
        self.assertEqual(True, "{'raw': None, 'metrics': None}")
