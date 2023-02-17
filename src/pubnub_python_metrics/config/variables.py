from logging import INFO
from .. import __about__
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


# from probable_fiesta.config.variables.LoggerDef
class LoggerDef:
    """Default values for the logger config."""

    ROOT_DIR = f"{get_project_root()}"
    LEVEL = INFO
    DIRECTORY = f"{ROOT_DIR}/logs"
    FORMAT = "simple"
    NAME = "main_log"
    TYPE = "default"


class PackageDef:
    """Default values for the package config."""

    NAME = "pubnub_python_metrics"


class VariablesDef:
    """Default values for the variables config."""

    VERSION = __about__.__version__


class DotEnvDef:
    """Default values for the dotenv config."""

    # This has precedence over the PackageDefaults
    def __init__(self):
        self.PACKAGE_NAME = "pubnub_python_metrics"
        self.PACKAGE_VERSION = "0.0.1"
        # Add more variables here

    def __iter__(self):
        return iter(self.__dict__)
