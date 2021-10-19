from pydantic import EmailStr

from chat_room.core.base_model import ModelBase


class UserCreateSchema(ModelBase):
    name: str
    email: EmailStr
    password: str
    is_superuser: bool = False
