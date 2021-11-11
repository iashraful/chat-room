from typing import Any, List
from pydantic import BaseModel, validator


class BaseResponse(BaseModel):
    msg: str
    status: int


class SingleResponse(BaseResponse):
    data: dict

    @validator("data", always=True)
    def validate_data(value):
        if isinstance(value, dict):
            value["id"] = str(value.pop("_id", ""))
        return value


class ListResponse(BaseResponse):
    data: List[dict]
