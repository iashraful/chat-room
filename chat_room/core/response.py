from typing import Any, Optional
from pydantic import BaseModel, validator


class BaseResponse(BaseModel):
    msg: str
    status: int
    data: Optional[Any]

    @validator("data", always=True)
    def validate_data(value):
        if isinstance(value, dict):
            value["id"] = str(value.pop("_id", ""))
        return value
