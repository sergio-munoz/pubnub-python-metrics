from pydantic import BaseModel, Field, constr, ValidationError
import pandas as pd
from pydantic.main import ModelMetaclass
from typing import List, Optional


class Metric(BaseModel):
    name: constr(strict=True) = Field(..., alias="metric")  # type: ignore
    type: Optional[str] = Field(None, alias="type")
    feature: Optional[str] = Field(None, alias="feature")
    action: Optional[str] = Field(None, alias="action")
    label: Optional[str] = Field(None, alias="label")
    description: Optional[str] = Field(None, alias="description")
    total: Optional[int] = Field(None, alias="total")


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


# Dict Validator Example
class DictValidator(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=20)
    height: float = Field(..., ge=0, le=250, description="Height in cm.")


class PdVal(BaseModel):
    df_dict: List[DictValidator]


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
