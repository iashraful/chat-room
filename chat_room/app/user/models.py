from pydantic import EmailStr, BaseModel


class User(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    @classmethod
    def collection_name(cls):
        return f'{cls.__name__.lower()}s'
