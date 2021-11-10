from http.client import HTTPException

from fastapi.param_functions import Depends
from starlette import status

from chat_room.app.user.schema import AuthLoginSchema
from chat_room.auth.schema import LoginResponse
from chat_room.auth.utils import create_access_token, authenticate
from chat_room.core.database import DBClient, get_database


async def auth_token(login: AuthLoginSchema, db: DBClient = Depends(get_database)):
    user = await authenticate(email=login.email, password=login.password, db=db)
    if user:
        token = create_access_token(sub=user.get("email"))
        return LoginResponse(
            msg="Login successful.", status=status.HTTP_200_OK, auth_token=token
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to login due to credentials.",
    )
