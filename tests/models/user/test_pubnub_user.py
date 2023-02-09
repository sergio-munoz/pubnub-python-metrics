"""Unit test file for pubnub_user.py."""
from probable_fiesta.config.builder.config_builder import ConfigBuilder

from src.pubnub_python_metrics.models.user import pubnub_user

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestPubNubUser(TestCase):

    def test_init(self):
        user = pubnub_user.PubNubUser()
        self.assertEqual(user.email, None)
        self.assertEqual(user.password, None)
        self.assertEqual(user.user, None)
        self.assertEqual(user.token, None)
        self.assertEqual(str(user), "{'email': None, 'password': None, 'user': None, 'token': None, 'accounts': None, 'apps': None, 'error': ''}")

    def test_load_all(self):
        class MyDotEnvDef():
            def __init__(self):
                self.email = "PN_CONSOLE_EMAIL"
                self.password = "PN_CONSOLE_PASSWORD"
            def __iter__(self):
                for attr, value in self.__dict__.items():
                    yield value
        cB = ConfigBuilder()
        config = cB.dotenv.load_dotenv().set_vars(MyDotEnvDef()).build()
        email = config.parsed_dotenv["PN_CONSOLE_EMAIL"]
        password = config.parsed_dotenv["PN_CONSOLE_PASSWORD"]
        user = pubnub_user.PubNubUser(email, password)
        user.login()
        user.load_all()
        self.assertIsNotNone(user.accounts)
        self.assertIsNotNone(user.apps)