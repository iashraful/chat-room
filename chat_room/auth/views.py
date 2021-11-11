from http.client import HTTPException

from fastapi.param_functions import Depends
from starlette import status

from chat_room.auth.schema import (
    AuthLoginSchema,
    RefreshTokenResponse,
    RefreshTokenSchema,
)
from chat_room.auth.schema import LoginResponse
from chat_room.auth.utils import (
    create_access_token,
    authenticate,
    create_from_refresh_token,
    create_refresh_token,
)
from chat_room.core.database import DBClient, get_database
from chat_room.core.response import BaseResponse


async def auth_token(login: AuthLoginSchema, db: DBClient = Depends(get_database)):
    user = await authenticate(email=login.email, password=login.password, db=db)
    if user:
        token = create_access_token(sub=user.get("email"))
        refresh_token = create_refresh_token(sub=user.get("email"))
        data = LoginResponse(
            auth_token=token,
            refresh_token=refresh_token,
        )
        return BaseResponse(
            msg="Login successful.", status=status.HTTP_200_OK, data=data
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to login due to credentials.",
    )


async def refresh_token(
    token: RefreshTokenSchema, db: DBClient = Depends(get_database)
):
    auth_token, new_refresh_token = create_from_refresh_token(token=token.refresh_token)

    data = RefreshTokenResponse(
        auth_token=auth_token,
        refresh_token=new_refresh_token,
    )
    return BaseResponse(
        msg="Refresh token created successfully.", status=status.HTTP_200_OK, data=data
    )
