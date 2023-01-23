import sys
import json

from probable_fiesta.app.main import main as main_app
from ..pubnub_console_user.pubnub_user import PubNubUser
from probable_fiesta.config.variables import DotEnvDef
from probable_fiesta.config.config_builder import ConfigBuilder
from .my_metrics.pandas_metrics import PandasMetrics

class MyDotEnvDef(DotEnvDef):
    def __init__(self):
        super().__init__()
        self.PN_CONSOLE_EMAIL = "PN_CONSOLE_EMAIL"
        self.PN_CONSOLE_PASSWORD = "PN_CONSOLE_PASSWORD"

def main(args=None):
    if not args:
        args = sys.argv[1:]

    # TODO: wrap this into app machine

    mded = MyDotEnvDef()

    cB = ConfigBuilder()
    config = cB\
        .dotenv\
            .load_dotenv()\
            .set_vars(mded)\
        .build()

    # TODO: obscure this. Add cryptolib library.
    email = config.parsed_dotenv['PN_CONSOLE_EMAIL']
    password = config.parsed_dotenv['PN_CONSOLE_PASSWORD']

    try:
        pu = PubNubUser()
        pu.login(email, password)
        pu.load()
    except Exception as e:
        print(e)
        return e

    if not pu.isLogin:
        print("User login failed.")
        return None 
    
    metrics = pu.all_metrics()
    print(metrics)

    print("Creating... Pandas metrics:")
    pm = PandasMetrics()
    print("Created... Pandas metrics:")

    print("set raw metrics:")
    pm.set_raw_metrics(json.dumps(metrics[0]))

    parsed_metrics = pm.parse_raw_metrics()
    print("Parsed metrics:")
    print(parsed_metrics)

    # print all columns
    print("All columns:")
    pm_copy = parsed_metrics
    print(list(pm_copy.columns))

    # print all rows from transactions_total
    print("Transactions total:")
    transaction_total = pm_copy['transactions_total']
    print("PRINTING TRANSACTION TOTAL:")
    print(transaction_total)

    # print all rows from transactions_total
    print("Transactions I NEED a BREAK total:")
    print(pm_copy['transactions_total'])

    # Do something
    print("Doing something:")
    print(pm_copy['transactions_total'].sum())

    print("\n.Doing pandas server magic man.\n")
    shape = parsed_metrics.shape
    print("Shape: ", shape)

    ## Find messages total
    print("->>Meddages total:")
    messages_total = pm_copy['msgs_total']
    print("PRINTING MESSAGES TOTAL:")
    for x in messages_total:
        print(x)
    print(messages_total)
    print("->> DONE PRINTING <<--")

    # print all rows from transactions_total
    print("Transactions I NEED a BREAK total:")
    print(pm_copy['transactions_total'])

    print("Explore column active keys:")
    print(pm.explore_col("active_keys"))
    print(pm.explore_col_name("active_keys"))
    print("Explored column active keys:")
    print("Explore column transactions total:")
    print(pm.explore_col("transactions_total"))
    print(pm.explore_col_name("transactions_total"))
    print("Explored column transactions total:")

    #main_app()

if __name__ == "__main__":
    main()