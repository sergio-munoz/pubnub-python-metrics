from enum import Enum
import pandas as pd
from .metric_model import (
    validate_data_schema,
    StrictCsvTxApi,
    StrictCsvTxType,
    StrictCsvTxName,
    PdVal,
)


class CsvFileTypes(str, Enum):
    tx_api = "tx_api"  # StrictCsvTxApi
    tx_type = "tx_type"  # StrictCsvTxType
    msg_type = "msg_type"  # StrictCsvTxName
    msg_size = "msg_size"  # StrictCsvTxName
    misc = "misc"  # StrictCsvTxName
    all = "all"  # StrictCsvTxName


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
