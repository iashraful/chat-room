from chat_room.core.response import BaseResponse


class LoginResponse(BaseResponse):
    auth_token: str
