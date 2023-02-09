from ...api.pubnub import internal_rest_api as api

class AuthUser:
    def __init__(self, email=None, password=None, user=None, token=None):
        self.email = email
        self.password = password
        self.user = user
        self.token = token

    def __str__(self):
        return f"{self.__dict__}"

    def login(self):
        try:
            self.user, self.token = api.authenticate(self.email, self.password)
        except Exception as error:
            print(error)
        return self

    def get_token(self):
        if not self.token:
            self.login()
        return self.token

class PubNubUser(AuthUser):
    def __init__(self):
        super().__init__()
        self.accounts = None
        self.apps = None
        self.error = ''

class PubNubUserBuilder:
    def __init__(self, pubnub_user=None):
        if pubnub_user is None:
            self.pubnub_user = PubNubUser()
        else:
            self.pubnub_user = pubnub_user

    @property
    def auth(self):
        return PubNubUserBuilderAuth(self.pubnub_user)

    @property
    def account(self):
        return PubNubUserBuilderAccounts(self.pubnub_user)

    @property
    def app(self):
        return PubNubUserBuilderApp(self.pubnub_user)

    def build(self):
        return self.pubnub_user

class PubNubUserBuilderAccounts(PubNubUserBuilder):
    def __init__(self, pubnub_user):
        super().__init__(self, pubnub_user)
        self.accounts = []
    
    def load(self):
        if not self.pubnub_user.user:
            print("User not set")
            self.pubnub_user.error += "User not set\n"
        if not self.pubnub_user.token:
            print("Token not set")
            self.pubnub_user.error += "Token not set\n"
        try:
            accounts = api.get_accounts(self.pubnub_user.user, self.pubnub_user.token)
            self.accounts = api.get_accounts_ids(accounts)
        except Exception as error:
            print(error)
            self.pubnub_user.error += f"{error}\n"
        return self
    
class PubNubUserBuilderApp(PubNubUserBuilder):
    def __init__(self, pubnub_user):
        super().__init__(self, pubnub_user)
        self.apps = {}
    
    def load(self):
        try:
            for account in self.pubnub_user.accounts:
                apps = api.get_apps(account, self.pubnub_user.token)
                self.apps.update({account: api.get_apps_ids(apps)})
        except Exception as error:
            print(error)
            self.pubnub_user.error += f"{error}\n"
        return self
    
class PubNubUserBuilderAuth(PubNubUserBuilder):
    def __init__(self, pubnub_user):
        super().__init__(self, pubnub_user)
    
    def set_token(self, token):
        self.pubnub_user.token = token
        return self

    def login(self, email, password):
        self.pubnub_user.email = email
        self.pubnub_user.password = password
        try:
            self.pubnub_user.user, self.pubnub_user.token = api.authenticate(self.pubnub_user.email, self.pubnub_user.password)
        except Exception as error:
            print(error)
            self.pubnub_user.error += f"{error}\n"
            return False
        return True