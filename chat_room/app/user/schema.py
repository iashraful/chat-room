from pydantic import EmailStr, BaseModel


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_superuser: bool = False
