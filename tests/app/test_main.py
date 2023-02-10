"""Unit test file for main_app.py."""
from probable_fiesta.app.builder.app_builder import AppBuilder
from probable_fiesta.command.builder import command
from probable_fiesta.app.builder.context_factory import ContextFactory

from src.pubnub_python_metrics.app import main as main_app

from unittest import TestCase

# Create a logger if needed for testing cases
#LOG_TEST = LoggerFactory.new_logger_get_logger("test_main_app", "DEBUG")

class TestMainApp(TestCase):

    # Health-check function test - get current version
    def test_function_get_version(self):
        #LOG_TEST.info("Test function get_version()")
        # This should never fail :)
        expected = f"HELLO WORLD!"
        self.assertEqual(main_app.get_version(), expected)

    def test_create_command_function_version(self):
        c = command.Command("version test", main_app.get_version, None)
        co = ContextFactory.new_context_one_command("version test", c)
        app = AppBuilder().context.add_context(co).build()
        app.run("version test")
        stdout = app.get_run_history()
        expected = f"HELLO WORLD!"
        #LOG.debug(stdout)
        self.assertEqual(stdout, expected)

    def test_argument(self):
        arg = "--version"
        expected = f"HELLO WORLD!"
        self.assertEqual(main_app.main([arg]), expected)

    def test_argument_invalid(self):
        arg = "--invalid"
        expected = f"unrecognized arguments: {arg}"
        self.assertEqual(main_app.main([arg]), expected)

    def test_f_string(self):
        # user_id (int)
        user_id = 22317
        # 'somewhere' user_id gets converted to utf-8
        user_id_utf8 = "圭"
        # convert utf-8 to int by using ord()
        self.assertEqual(user_id, ord(user_id_utf8))
    
    