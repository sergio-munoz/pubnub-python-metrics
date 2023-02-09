import pandas as pd


class MetricPandas:
    def __init__(self, raw):
        self.metrics = self.load_raw(raw)

    @staticmethod
    def load_raw(raw):
        try:
            return pd.read_json(raw)
        except Exception as e:
            print(e)
            pass
        try:
            print("trying get from dict")
            return pd.DataFrame.from_dict(raw)
        except Exception as e:
            print(e)
        return None

    def extract_total(self, name):
        try:
            # dtype=object
            res = self.metrics[name]  # type: ignore
            df = pd.DataFrame(res.to_list())
            return df["sum"].sum()
        except Exception as e:
            print(e)
            return None

    def read_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            return df
        except Exception as e:
            print(e)
            return None
