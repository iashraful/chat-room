from fastapi import Depends, HTTPException
from fastapi.param_functions import Security
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic.networks import EmailStr
from starlette import status

from chat_room.app.user.models import User
from chat_room.app.user.schema import UserCreateSchema, UserListResponse
from chat_room.auth.utils import get_password_hash, request_user, security
from chat_room.core.config import settings
from chat_room.core.database import DBClient, get_database
from chat_room.core.response import BaseResponse
from chat_room.core.utility import async_cursor_parser


async def create_user(user: UserCreateSchema, db: DBClient = Depends(get_database)):
    collection = db[settings.DB_NAME][User.collection_name()]
    _user = await collection.find_one({"email": user.email})
    if _user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An user already exist with this email.",
        )
    user_data_dict = user.dict()
    _password = user_data_dict.pop("password", "")
    _confirm_password = user_data_dict.pop("confirm_password", "")
    if _password != _confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password mismatch.",
        )
    hashed_password = get_password_hash(password=_password)
    user_data_dict.update(password=hashed_password)
    result = await collection.insert_one(user_data_dict)
    return BaseResponse(status=status.HTTP_200_OK, msg="User created successfully.")


async def get_user(
    email: EmailStr,
    db: DBClient = Depends(get_database),
    request_user: dict = Depends(request_user),
):
    collection = db[settings.DB_NAME][User.collection_name()]
    _user = await collection.find_one({"email": email})
    if _user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user exist with this email.",
        )
    if "password" in _user:
        _user.pop("password")
    return BaseResponse(
        status=status.HTTP_200_OK, msg="User fetched successfully.", data=_user
    )


async def get_users(
    db: DBClient = Depends(get_database),
    request_user: dict = Depends(request_user),
):
    collection = db[settings.DB_NAME][User.collection_name()]
    cursor = collection.find()
    _users = await async_cursor_parser(cursor=cursor)
    return UserListResponse(
        status=status.HTTP_200_OK, msg="User fetched successfully.", data=_users
    )
