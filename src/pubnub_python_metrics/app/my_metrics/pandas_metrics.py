import pandas as pd

class PandasMetrics:
    def __init__(self):
        self.raw_metrics = None
        self.parsed_metrics = None

    def set_raw_metrics(self, raw_metrics):
        self.raw_metrics = raw_metrics

    def get_raw_metrics(self):
        return self.raw_metrics

    def parse_raw_metrics(self):
        if self.raw_metrics is None:
            print("No raw metrics to parse")
            return None
        self.parsed_metrics = pd.read_json(self.raw_metrics)
        return self.parsed_metrics

    def explore_col(self, column_name):
        if self.parsed_metrics is None:
            print("No parsed metrics to explore")
            return None
        return self.parsed_metrics[column_name]

    def explore_col_name(self, column_name):
        if self.parsed_metrics is None:
            print("No parsed metrics to explore")
            return None
        print("--experiment: Exploring specific column")
        matched_here = self.parsed_metrics[column_name]
        print("MATCHED_HERE: ", matched_here)
        found_here = self.parsed_metrics[column_name].name
        print("FOUND_HERE: ", found_here)

        print("TELL ME IF I SHOULD RETURN SOMETHING")
