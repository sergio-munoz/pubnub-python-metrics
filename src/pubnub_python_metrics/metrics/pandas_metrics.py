import pandas as pd

class PandasMetrics:
    def __init__(self, raw=None):
        self.raw = raw
        self.metrics = None
        self.error = ''

    def set_metrics(self, metrics):
        self.metrics = metrics

    def __str__(self):
        return f"{self.__dict__}"

    def load(self):
        try:
            self.metrics = pd.read_json(self.raw)
            return self.metrics
        except Exception as e:
            print(e)
            pass
        try:
            print("trying get from dict")
            self.metrics = pd.DataFrame.from_dict(self.raw)
            return self.metrics
        except Exception as e:
            print(e)
        return None 
    
    def get_col_by_name(self, name):
        return self.metrics.loc[:, name]

    def get_sum_of_name(self, name):
        try:
            metrics = self.get_col_by_name(name)
            l_sum = 0
            for m in metrics:
                l_sum += m['sum']
            return l_sum
        except Exception as e:
            print(e)
            return None