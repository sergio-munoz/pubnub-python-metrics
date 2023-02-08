"""Metrics parser."""

from ..pubnub import internal_rest_api as api

class MyMetric:
    def __init__(self):
        self.raw = None

    def __str__(self):
        return f"{self.__dict__}"

    def get_app_based_usage(self, app_id, token, metric_type, start_date, end_date):
        self.raw = api.get_app_based_usage(app_id, token, metric_type, start_date, end_date)
        return self.raw

    def get_key_based_usage(self, key_id, token, metric_type, start_date, end_date):
        self.raw = api.get_key_based_usage(key_id, token, metric_type, start_date, end_date)
        return self.raw

class Metric:

    def __init__(self, token=None):
        self.token = token
        self.app_id = None
        self.metric_type = None
        self.start_date = None
        self.end_date = None
        self.raw_metrics = None

    def set_metric_params(self, app_id, metric_type, start_date, end_date):
        self.app_id = app_id
        self.metric_type = metric_type # transaction
        self.start_date = start_date # 2022-12-01
        self.end_date = end_date # 2022-12-02

    def perform_metric(self):
        self.raw_metrics = api.get_app_based_usage(self.app_id, self.token, self.metric_type, self.start_date, self.start_date)

    def get_raw_metric(self):
        return self.raw_metrics

class MetricBuilder():
    def __init__(self, metric=None, token=None):
        if metric is None:
            self.metric = Metric(token)
        else:
            self.metric = metric

    @property
    def parse(self):
        return ParseMetric(self.metric)

    def build(self):
        return self.metric

class ParseMetric(MetricBuilder):
    def __init__(self, metric=None, token=None):
        super().__init__(metric, token)

    def parse_metric(self, app_id, metric_type, start_date, end_date):
        self.metric.set_metric_params(app_id, metric_type, start_date, end_date)
        self.metric.perform_metric()
        return self.metric.get_raw_metric()

    def set_token(self, token):
        self.metric.token = token
        return self

    def set_date(self, start, end):
        self.metric.start_date = start
        self.metric.end_date = end
        return self

class MetricParser(Metric):

    def __init__(self, token=None):
        metric = super().__init__(token)
        self.metric = metric
        self.all_metrics = []

    def parse_metric(self, app_id, metric_type, start_date, end_date):
        self.set_metric_params(app_id, metric_type, start_date, end_date)
        self.metric.perform_metric()
        return self.metric.get_raw_metrics()

    def all_metrics(self):
        try:
            for _, app_ids in self.apps.items():
                for app_id in app_ids:
                    self.all_metrics.metrics.append(
                        api.get_app_based_usage(app_id, self.token, "transaction", "2022-12-01", "2022-12-02")
                        )
        except Exception as error:
            print(error)
            self.all_metrics = None

    def get_all_metrics(self):
        return self.all_metrics

    def set_date(self, start, end):
        self.metric.start_date = start
        self.metric.end_date = end
        return self