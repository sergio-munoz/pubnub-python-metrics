"""SRP PubNub User to interact with PubNub Web Console."""
from .auth_user import AuthUser
from ...api.pubnub import internal_rest_api as api
from ...models.metrics.metric_parser import MetricParser
from ...models.metrics.metric_pandas import MetricPandas


class PubNubUser(AuthUser):
    """PubNub User Class"""

    def __init__(self, email=None, password=None, user=None, token=None):
        """Initialize PubNubUser class."""
        super().__init__(email, password, user, token)
        self.accounts = None
        self.apps = None
        self.error = ""

    def __str__(self):
        return f"{self.__dict__}"

    def load_all(self):
        """Load user accounts and apps."""
        try:
            self.apps = {}
            accounts = api.get_accounts(self.user, self.token)
            self.accounts = api.get_accounts_ids(accounts)

            for account in self.accounts:
                apps = api.get_apps(account, self.token)
                self.apps.update({account: api.get_apps_ids(apps)})
        except Exception as error:
            self.error = error
        return self

    def __iter__(self):
        for _, app_ids in self.apps.items():  # type: ignore
            for app_id in app_ids:
                yield app_id

    def get_apps(self):
        return self.apps

    def get_keys(self, app_id, page=1, limit=100):
        ret = []
        keys = api.get_keys(app_id, self.token, page, limit)
        for result in keys["result"]:
            ret.append(result["id"])
        return ret

    def all_metrics(self, start, end):
        metrics = []
        mp = MetricParser()

        try:
            for app_id in self:
                metric = mp.get_app_based_usage(
                    app_id, self.token, "transaction", start, end
                )
                metrics.append(metric)
        except Exception as error:
            print(error)
            return None
        return metrics

    def all_metrics_pandas(self, start, end):
        _all_metrics = self.all_metrics(start, end)
        metrics = []
        try:
            for m in _all_metrics:  # type: ignore
                # Pandas metrics validation
                pandas = MetricPandas(m)
                metrics.append(pandas.validate())
        except Exception as error:
            print(error)
            return None
        return metrics

    def all_metrics_total_by_name(self, start, end, name):
        _pandas_metrics = self.all_metrics_pandas(start, end)
        metrics = []
        try:
            for m in _pandas_metrics:  # type: ignore
                metrics.append([x for x in m if x.name == name])
        except Exception as error:
            print(error)
            return None
        return metrics
