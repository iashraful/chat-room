from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    is_superuser: bool = False
