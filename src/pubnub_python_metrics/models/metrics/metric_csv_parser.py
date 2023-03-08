from enum import Enum
import pandas as pd
from .metric_model import (
    Metric,
    validate_data_schema,
    StrictCsvTxApi,
    StrictCsvTxType,
    StrictCsvTxName,
    PdVal,
)


@validate_data_schema(data_schema=Metric)
def validate_metric(df) -> pd.DataFrame:
    return df


class CsvFileTypes(str, Enum):
    tx_api = 0  # StrictCsvTxApi
    tx_type = 1  # StrictCsvTxType
    msg_type = 2  # StrictCsvTxName
    msg_size = 3  # StrictCsvTxName
    misc = 4  # StrictCsvTxName
    all = 5  # StrictCsvTxName


# List-Backed Properties Iterator Pattern
class CsvMetrics:
    _tx_api = 0
    _tx_type = 1
    _msg_type = 2
    _msg_size = 3
    _misc = 4
    _all = 5

    def __init__(self) -> None:
        # From enum
        self.csv_metrics = [None, None, None, None, None, None]

    @property
    def tx_api(self):
        return self.csv_metrics[CsvFileTypes.tx_api.value]

    @tx_api.setter
    def tx_api(self, value):
        self.csv_metrics[CsvFileTypes.tx_api.value] = value

    def get_as_metric_tx(self, csv_file_type: CsvFileTypes, tx: pd.DataFrame, spm):
        pass


def read_csv_file(csv_file) -> pd.DataFrame:
    # reader = pd.read_csv(csv_file, keep_default_na=False, na_values=[""])
    reader = pd.read_csv(csv_file)
    return reader


@validate_data_schema(data_schema=StrictCsvTxApi)
def validate_csv_tx_api(df) -> pd.DataFrame:
    return df


@validate_data_schema(data_schema=StrictCsvTxType)
def validate_csv_tx_type(df) -> pd.DataFrame:
    return df


@validate_data_schema(data_schema=StrictCsvTxName)
def validate_csv_tx_name(df) -> pd.DataFrame:
    return df


# Dict Validator Example
def pd_val(df):
    _ = PdVal(df_dict=df.to_dict(orient="records"))
    return df
