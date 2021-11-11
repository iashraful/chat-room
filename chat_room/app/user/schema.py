from typing import List
from pydantic import BaseModel, EmailStr

from chat_room.core.response import BaseResponse, ListResponse


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    is_superuser: bool = False


class UserListSchema(BaseModel):
    id: str
    name: str
    email: str
    is_superuser: bool


class UserListResponse(ListResponse):
    data: List[UserListSchema]
