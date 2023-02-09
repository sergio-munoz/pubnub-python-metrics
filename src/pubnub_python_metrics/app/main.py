import sys
import json

from probable_fiesta.config.variables import DotEnvDef as ded
from probable_fiesta.config.builder.config_builder import ConfigBuilder
from probable_fiesta.logger.builder.logger_factory import LoggerFactory
from probable_fiesta.app.builder.context_factory import ContextFactory as CF
from probable_fiesta.app.builder.app_builder import AppBuilder

from ..models.user.pubnub_user import PubNubUser
from ..metrics.pandas_metrics import PandasMetrics

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
        pu = PubNubUser()
        pu.login(email, password)
        pu.load()
    except Exception as e:
        print(e)
        return None

    if not pu.isLogin:
        print("User login failed.")
        return None 

    return pu

def main(args=None):
    if not args:
        args = sys.argv[1:]

    cB = ConfigBuilder()
    config = cB\
        .logger\
            .set_logger(LoggerFactory.new_logger_get_logger("pn_py_metrics", "DEBUG"))\
        .dotenv\
            .load_dotenv()\
            .set_vars(MyDotEnvDef())\
        .build()

    aB = AppBuilder()
    main_app = aB\
        .name\
            .set_name("main_app")\
        .arguments\
            .set_arguments(args)\
            .set_executables(["version", "all_date"])\
        .args_parser\
            .add_argument("--version", action='store_true', help="show version builder")\
            .add_argument("-start", "--date-start", type=str, help="Start date")\
            .add_argument("-end", "--date-end", type=str, help="End date")\
            .add_argument("--all-date", action="store_true", help="By date")\
            .add_argument("-email", "--pn-console-email", type=str, help="PubNub Console email")\
            .add_argument("-password", "--pn-console-password", type=str, help="PubNub Console password")\
        .context\
            .add_context(
                CF.new_context_one_new_command("version", "version", get_version, None))\
        .config\
            .set_config(config)\
        .validate()\
        .build()

    # get from arguments or dotenv
    # Note: arguments have priority over dotenv
    pu = create_pubnub_user(main_app.get_arg("PN_CONSOLE_EMAIL"), main_app.get_arg("PN_CONSOLE_PASSWORD"))
    #print("pu: ", pu)
    if not pu:
        print("PubNub user not authenticated. Trying to run anyways...")
        #return None
    else:
        # Create context with new command
        start = main_app.get_arg("date_start")
        end = main_app.get_arg("date_end")
        c1 = CF.new_context_one_new_command("all_date", "get_all_metrics_by_date", pu.get_all_metrics_by_date, start, end)
        main_app.context.add_context(c1)
    
    if main_app.args_parser.error:
        print("MAIN APP ERROR: ", main_app.args_parser.error)
        return main_app.args_parser.error

    run_context = main_app.run()
    #print("run_context: ", run_context)
    history = run_context.get_run_history()
    print(history)
    return history

def experiment():
    print()
    metrics = pu.all_metrics()
    pm = PandasMetrics()
    pm.set_raw_metrics(json.dumps(metrics[0]))
    parsed_metrics = pm.parse_raw_metrics()

    print("All parsed metrics keys")
    for metric_key in parsed_metrics.keys():
        print("metric_key: ", metric_key)
        for element in parsed_metrics[metric_key]:
            pass
            #print("element", element) 

    print("EDGE: ", parsed_metrics['edge'])
    print("REPLICATED: ", parsed_metrics['replicated'])
    print("SIGNALS: ", parsed_metrics['signals'])
    print("CHANNEL: ", parsed_metrics['channel'])
    print("EXECUTIONS: ", parsed_metrics['executions'])

    def parse_metric(my_dict):
        total_sum = 0.0
        for day, value in my_dict.items():
            print("key: ", day)
            print("value: ", value)
            total_sum += value['sum']
        return total_sum
        
    print("total_sum_edge: ", parse_metric(parsed_metrics['edge']))
    print("total_sum_edge: ", parse_metric(parsed_metrics['channel']))

    # print all columns
    print("All columns:")
    print(list(parsed_metrics.columns))

    # Get by date
    date_metrics = pu.get_all_metrics_by_date(
        "2022-10-23", "2022-12-24")
    print("\n\n->All apps date metric:")
    print(date_metrics)

    print("transactions total:", date_metrics['transactions_total'])

def get_version() -> str:
    """Get package version.

    Returns:
        str: Current package version.
    """
    return f"HELLO WORLD!"


if __name__ == "__main__":
    main()