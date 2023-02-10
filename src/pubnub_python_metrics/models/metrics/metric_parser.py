from ...api.pubnub import internal_rest_api as api


class MetricParser:
    def __init__(self):
        self.raw = None

    def __str__(self):
        return f"{self.__dict__}"

    def get_app_based_usage(self, app_id, token, metric_type, start_date, end_date):
        self.raw = api.get_app_based_usage(
            app_id, token, metric_type, start_date, end_date
        )
        return self.raw

    def get_key_based_usage(self, key_id, token, metric_type, start_date, end_date):
        self.raw = api.get_key_based_usage(
            key_id, token, metric_type, start_date, end_date
        )
        return self.raw
