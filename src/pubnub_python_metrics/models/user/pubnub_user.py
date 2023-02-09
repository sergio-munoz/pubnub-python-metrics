"""SRP PubNub User to interact with PubNub Web Console."""
from .auth_user import AuthUser
from ...api.pubnub import internal_rest_api as api
from ...metrics.metrics_parser import MetricBuilder


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
        for _, app_ids in self.apps.items():
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

    def all_metrics(self):
        metrics = []

        mB = MetricBuilder().parse.set_token(self.token)

        try:
            for app_id in self:
                metric = mB.parse_metric(
                    app_id, "transaction", "2022-12-01", "2022-12-02"
                )
                metrics.append(metric)
        except Exception as error:
            print(error)
            return None
        return metrics

    def get_all_metrics_by_date(self, start, end):
        mB = MetricBuilder().parse.set_token(self.token).set_date(start, end)
        try:
            for app_id in self:
                metric = mB.parse_metric(app_id, "transaction", start, end)
                return metric
        except Exception as error:
            print(error)
            return None
