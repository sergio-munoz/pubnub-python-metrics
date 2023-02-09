import pandas as pd


class MetricPandas:
    def __init__(self, raw, txt_api_file=None):
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
