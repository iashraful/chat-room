from typing import List

from chat_room.app.user.models import User
from chat_room.app.user.schema import UserCreateSchema
from chat_room.auth.utils import get_password_hash
from chat_room.core.config import settings
from chat_room.core.database import DBClient, get_database
from fastapi import Depends, HTTPException
from starlette import status

from chat_room.core.response import BaseResponse


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
