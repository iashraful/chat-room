from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from chat_room.core.response import BaseResponse


class LoginResponse(BaseModel):
    auth_token: str
    refresh_token: str


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    auth_token: str
    refresh_token: str
