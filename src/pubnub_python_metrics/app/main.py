import sys

from probable_fiesta.config.variables import DotEnvDef as ded
from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory
from probable_fiesta.app.builder.context_factory import ContextFactory as CF
from probable_fiesta.app.builder.app_builder import AppBuilder

from ..models.user.pubnub_user import PubNubUser


class MyDotEnvDef(ded):
    def __init__(self):
        super().__init__()
        self.email = "PN_CONSOLE_EMAIL"
        self.password = "PN_CONSOLE_PASSWORD"

    # make the class iterable
    def __iter__(self):
        # only yield the values
        for attr, value in self.__dict__.items():
            yield value


def create_pubnub_user(email, password):
    try:
        pu = PubNubUser(email, password)
        pu.login()
        pu.load_all()
    except Exception as e:
        print(e)
        return None
    return pu


def main(args=None):
    if not args:
        args = sys.argv[1:]

    cB = ConfigBuilder()
    config = (
        cB.logger.set_logger(
            LoggerFactory.new_logger_get_logger("pn_py_metrics", "DEBUG")
        )
        .dotenv.load_dotenv()
        .set_vars(MyDotEnvDef())
        .build()
    )

    aB = AppBuilder()
    main_app = (
        aB.name.set_name("main_app")
        .arguments.set_arguments(args)
        .set_executables(
            [
                "version",
                "all_date",
                "all_pandas",
                "all_total_by_name",
                "all_total_by_attr",
                "all_total_by_attr_enriched",
            ]
        )
        .args_parser.add_argument(
            "--version", action="store_true", help="show version builder"
        )
        .add_argument("-start", "--date-start", type=str, help="Start date")
        .add_argument("-end", "--date-end", type=str, help="End date")
        .add_argument("--all-date", action="store_true", help="By date")
        .add_argument("--all-pandas", action="store_true", help="By date pandas")
        .add_argument("--all-total-by-name", action="store_true", help="By metric name")
        .add_argument("--all-total-by-attr", type=str, help="By metric attribute")
        .add_argument(
            "--all-total-by-attr-enriched",
            type=str,
            help="By metric attribute enriched",
        )
        .add_argument("-name", "--metric-name", type=str, help="Metric name")
        .add_argument(
            "-email", "--pn-console-email", type=str, help="PubNub Console email"
        )
        .add_argument(
            "-password",
            "--pn-console-password",
            type=str,
            help="PubNub Console password",
        )
        .context.add_context(
            CF.new_context_one_new_command("version", "version", get_version, None)
        )
        .config.set_config(config)
        .validate()
        .build()
    )

    # Get arguments from CLI or dotenv
    pu = create_pubnub_user(
        main_app.get_arg("PN_CONSOLE_EMAIL"), main_app.get_arg("PN_CONSOLE_PASSWORD")
    )
    # Authenticate user
    if not pu:
        print("PubNub user not authenticated")
        return

    # Add commands after passing authentication
    # all_metrics
    start = main_app.get_arg("date_start")
    end = main_app.get_arg("date_end")
    c1 = CF.new_context_one_new_command(
        "all_date",
        "get_all_metrics_by_date",
        pu.get_apps(),
        start,
        end,
    )
    main_app.context.add_context(c1)  # type: ignore

    # all_pandas
    c2 = CF.new_context_one_new_command(
        "all_pandas",
        "get_all_metrics_pandas",
        pu.all_metrics_pandas,
        start,
        end,
    )
    main_app.context.add_context(c2)  # type: ignore

    # total_by_metric
    c3 = CF.new_context_one_new_command(
        "all_total_by_name",
        "get_all_total_by_name",
        pu.all_metrics_total_by_name,
        start,
        end,
        main_app.get_arg("metric_name"),
    )
    main_app.context.add_context(c3)  # type: ignore

    # total_by_attr
    c4 = CF.new_context_one_new_command(
        "all_total_by_attr",
        "get_all_total_by_attr",
        pu.all_metrics_total_by_attr,
        start,
        end,
        main_app.get_arg("all_total_by_attr"),
        main_app.get_arg("metric_name"),
    )
    main_app.context.add_context(c4)  # type: ignore

    # total_by_attr_enriched
    c5 = CF.new_context_one_new_command(
        "all_total_by_attr_enriched",
        "get_all_total_by_attr_enriched",
        pu.all_metrics_total_by_attr_enriched,
        start,
        end,
        main_app.get_arg("all_total_by_attr_enriched"),
        main_app.get_arg("metric_name"),
    )
    main_app.context.add_context(c5)  # type: ignore

    if main_app.args_parser.error:  # type: ignore
        print("MAIN APP ERROR: ", main_app.args_parser.error)  # type: ignore
        return main_app.args_parser.error  # type: ignore

    run_context = main_app.run()
    # print("run_context: ", run_context)
    history = run_context.get_run_history()
    print(history)
    return history


def get_version() -> str:
    """Get package version.

    Returns:
        str: Current package version.
    """
    return f"HELLO WORLD!"


if __name__ == "__main__":
    main()
