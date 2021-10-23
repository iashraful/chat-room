from typing import List

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from chat_room.app.user.models import User
from chat_room.app.user.schema import UserCreateSchema
from chat_room.core.config import settings
from chat_room.core.database import DBClient, get_database


class SingleResponse(BaseModel):
    data: dict


class ListResponse(BaseModel):
    data: List[dict]


async def create_user(user: UserCreateSchema, db: DBClient = Depends(get_database)):
    collection = db[settings.DB_NAME][User.collection_name()]

    _user = await collection.find_one({'email': user.email}, {'_id': 0})
    if user and user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='An user already exist with this email.')
    user_data_dict = user.dict()
    _password = user_data_dict.pop('password', None)
    result = await collection.insert_one(user_data_dict)
    return SingleResponse(data=_user)
