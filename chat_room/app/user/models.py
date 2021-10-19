from pydantic import EmailStr

from chat_room.core.base_model import ModelBase


class User(ModelBase):
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    @classmethod
    def collection_name(cls):
        return f'{cls.__name__.lower()}s'
