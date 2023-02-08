import csv

class PubNubMetrics:
    def __init__(self, pandas_metrics):
        self.metrics = pandas_metrics
        self.tx_api = None
        self.tx_type = None
        self.mgs_type = None
        self.misc = None

    def load_tx_api_file(self, file):
        reader = csv.DictReader(file)
        data = list(reader)
        self.tx_api = data

    def by_api(self, name):
        for m in self.tx_api:
            if m['api'] == name:
                try:
                    return self.metrics.get_sum_of_name(name)
                except Exception as e:
                    print(e)
                    return None
        print("No such api: ", name)
        return None

    def by_feature(self, name):
        l_sum = 0
        for m in self.tx_api:
            if m['feature'] == name:
                try:
                    l_sum += self.get_sum_of_name(m['api'])
                except Exception as e:
                    print(e)
                    return None
        return l_sum

    def by_type(self, name):
        l_sum = 0
        for m in self.tx_api:
            if m['type'] == name:
                try:
                    l_sum += self.get_sum_of_name(m['api'])
                except Exception as e:
                    print(e)
                    return None
        return l_sum