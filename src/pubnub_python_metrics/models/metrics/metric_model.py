from pydantic import BaseModel, Field, constr
import pandas as pd
from enum import Enum
from pydantic.main import ModelMetaclass
from typing import List, Optional


class CsvFileType(str, Enum):
    tx_api = 0  # StrictCsvTxApi
    tx_type = 1  # StrictCsvTxType
    msg_type = 2  # StrictCsvTxName
    msg_size = 3  # StrictCsvTxName
    misc = 4  # StrictCsvTxName
    all = 5  # StrictCsvTxName


class Metric(BaseModel):
    name: constr(strict=True) = Field(..., alias="metric")  # type: ignore
    type: Optional[str] = Field(None, alias="type")
    feature: Optional[str] = Field(None, alias="feature")
    action: Optional[str] = Field(None, alias="action")
    label: Optional[str] = Field(None, alias="label")
    description: Optional[str] = Field(None, alias="description")
    total: Optional[float] = Field(None, alias="total")

    def enrich(self, csv_file_type: CsvFileType, tx: pd.DataFrame):
        tx = tx.loc[tx["metric"] == self.name]
        if not tx.empty:
            if csv_file_type == "tx_api":
                tx = validate_metric(tx)
                self.type = tx["type"].values[0]
                self.feature = tx["feature"].values[0]
                self.action = tx["action"].values[0]
                self.label = tx["label"].values[0]
                self.description = tx["description"].values[0]
                return self
            if csv_file_type == "tx_type":
                tx = validate_metric(tx)
                self.type = tx["type"].values[0]
                return self


class StrictCsvTxName(BaseModel):
    name: constr(strict=True) = Field(..., alias="metric")  # type: ignore


class StrictCsvTxType(BaseModel):
    name: constr(strict=True) = Field(..., alias="metric")  # type: ignore
    type: str = Field(..., alias="type")


class StrictCsvTxApi(BaseModel):
    name: constr(strict=True) = Field(..., alias="metric")  # type: ignore
    type: str = Field(..., alias="type")
    feature: str = Field(..., alias="feature")
    action: str = Field(..., alias="action")
    label: str = Field(..., alias="label")
    description: str = Field(..., alias="description")


class StrictPnApiMetric(BaseModel):
    days: dict = Field(..., alias="days")
    hours: dict = Field(..., alias="hours")
    peak: float = Field(..., alias="peak")
    peak_ts: int = Field(..., alias="peak_ts")
    total: float = Field(..., alias="sum")


class StrictPnMetric(Metric):
    name: str
    total: float


# Decorator
def validate_data_schema(data_schema: ModelMetaclass):
    """This decorator will validate a pandas.DataFrame against the given data_schema."""

    def Inner(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if isinstance(res, pd.DataFrame):
                # check result of the function execution against the data_schema
                df_dict = res.to_dict(orient="records")

                # Wrap the data_schema into a helper class for validation
                class ValidationWrap(BaseModel):
                    df_dict: List[data_schema]  # type: ignore

                # Do the validation
                _ = ValidationWrap(df_dict=df_dict)
            else:
                raise TypeError(
                    "Your Function is not returning an object of type pandas.DataFrame."
                )

            # return the function result
            return res

        return wrapper

    return Inner


@validate_data_schema(data_schema=Metric)
def validate_metric(df) -> pd.DataFrame:
    return df


# To use a List of Dict Validator Example:
# class DictValidator(BaseModel):
# id: int = Field(..., ge=1)
# name: str = Field(..., max_length=20)
# height: float = Field(..., ge=0, le=250, description="Height in cm.")
# class PdVal(BaseModel):
# df_dict: List[DictValidator]
