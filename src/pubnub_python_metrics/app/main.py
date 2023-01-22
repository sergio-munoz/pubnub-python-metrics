import sys

from probable_fiesta.app.main import main as main_app
from ..pubnub_console_user.pubnub_user import PubNubUser
from probable_fiesta.config.variables import DotEnvDef
from probable_fiesta.config.config_builder import ConfigBuilder

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

    #main_app()

if __name__ == "__main__":
    main()