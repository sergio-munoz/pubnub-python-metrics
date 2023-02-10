from .metric import MetricBuilder


class MetricHolder:
    def __init__(self, metrics=[]):
        self._metrics = metrics

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        self._metrics = metrics

    @metrics.deleter
    def metrics(self):
        del self._metrics

    def add(self, metric):
        self._metrics.append(metric)

    def remove(self, metric):
        self._metrics.remove(metric)

    @property
    def names(self):
        return [x.name for x in self._metrics]

    @property
    def types(self):
        return [x.type for x in self._metrics]

    @property
    def features(self):
        return [x.feature for x in self._metrics]

    @property
    def totals(self):
        return [x.total for x in self._metrics]

    def get_by_name(self, name):
        for metric in self.metrics:
            if metric.name == name:
                return metric
        return None

    def total_of_name(self, name):
        if isinstance(name, str):
            metric = self.get_by_name(name)
            if metric:
                return metric.total
        if isinstance(name, list):
            return sum([x.total for x in self.metrics if x.name in name])

    def total_of_type(self, type):
        return sum([x.total for x in self.metrics if x.type == type])

    def total_of_feature(self, feature):
        return sum([x.total for x in self.metrics if x.feature == feature])
