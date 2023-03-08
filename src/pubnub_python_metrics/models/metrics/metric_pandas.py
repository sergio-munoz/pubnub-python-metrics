import pandas as pd
from enum import Enum
from .metric_model import validate_data_schema, StrictPnMetric, StrictPnApiMetric


class MetricPandas:
    def __init__(self, raw):
        self.metrics = self.load_raw(raw)

    @staticmethod
    def load_raw(raw):
        # Json
        try:
            return pd.read_json(raw)
        except Exception as e:
            print("Exception:", e)
            pass
        # Dict
        try:
            return pd.DataFrame.from_dict(raw)
        except Exception as e:
            print("Exception:", e)
        raise TypeError

    def validate(self) -> list:
        "Get a list of class StrictPnMetric"
        d = self.metrics.to_dict()
        stdout = []
        for name, _ in d.items():
            # print("name: ", name, "c ", _)
            # print("name: ", name)
            res = self.metrics[name]  # type: ignore
            df = pd.DataFrame(res.to_list())
            df = validate_pn_metric(df)
            # print("---")
            # print("df: ", df)
            m = StrictPnMetric(name=name, total=df["sum"].sum())  # type:ignore
            stdout.append(m)
        return stdout

    def extract_total(self, name):
        try:
            # dtype=object
            res = self.metrics[name]  # type: ignore
            df = pd.DataFrame(res.to_list())
            return df["sum"].sum()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def read_csv(csv_file):
        try:
            df = pd.read_csv(csv_file)
            return df
        except Exception as e:
            print(e)
            return None


class MetricAttrEnum(Enum):
    metric_name = "name"
    metric_type = "type"
    metric_feature = "feature"
    metric_action = "action"
    metric_label = "label"
    metric_tx_type = "tx_type"


@staticmethod
@validate_data_schema(data_schema=StrictPnApiMetric)
def validate_pn_metric(df) -> pd.DataFrame:
    return df
