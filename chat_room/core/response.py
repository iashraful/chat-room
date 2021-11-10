from typing import Any, List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    msg: str
    status: int


class SingleResponse(BaseResponse):
    data: dict


class ListResponse(BaseResponse):
    data: List[dict]
