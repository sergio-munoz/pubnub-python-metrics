"""Metrics parser."""

from . import pubnub_internal_rest_api as api


class Metrics:

    pass


class MetricsParser:

    def __init__(self) -> None:
        pass

    def get_range(self, start, end):
        pass

    def all_metrics(self):
        metrics = []
        try:
            for _, app_ids in self.apps.items():
                for app_id in app_ids:
                    metrics.append(
                        api.get_app_based_usage(app_id, self.token, "transaction", "2022-12-01", "2022-12-02")
                        )
        except Exception as error:
            print(error)
            return None
        return metrics
