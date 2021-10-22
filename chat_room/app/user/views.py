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


class UserView:
    @staticmethod
    async def create_user(user: UserCreateSchema, db: DBClient = Depends(get_database)):
        collection = db[settings.DB_NAME][User.collection_name()]
        user_data_dict = user.dict()
        _password = user_data_dict.pop('password', None)
        if not _password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password should be provided.')
        result = await collection.insert_one(user_data_dict)
        return SingleResponse(data={'result': result})
