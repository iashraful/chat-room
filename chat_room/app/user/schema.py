from pydantic import BaseModel, EmailStr

from chat_room.core.response import BaseResponse


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    is_superuser: bool = False


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str

