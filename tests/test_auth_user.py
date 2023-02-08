"""Unit test file for auth_user.py."""
from probable_fiesta.config.builder.config_builder import ConfigBuilder

from src.pubnub_python_metrics.authorization import auth_user

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestAuthUser(TestCase):

    def test_init(self):
        user = auth_user.AuthUser()
        self.assertEqual(user.email, None)
        self.assertEqual(user.password, None)
        self.assertEqual(user.user, None)
        self.assertEqual(user.token, None)
        self.assertEqual(str(user), "{'email': None, 'password': None, 'user': None, 'token': None}")

    def test_login(self):
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
        user = auth_user.AuthUser(email, password)
        user.login()
        self.assertIsNotNone(user.token)
        self.assertIsNotNone(user.user)

