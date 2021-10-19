from fastapi import HTTPException
from starlette import status

from chat_room.app.user.models import User
from chat_room.app.user.schema import UserCreateSchema
from chat_room.core.config import settings
from chat_room.core.database import DBClient


async def create_user(db: DBClient, user: UserCreateSchema):
    collection = db[settings.DB_NAME][User.collection_name()]
    user_data_dict = user.dict()
    _password = user_data_dict.pop('password', None)
    if not _password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password should be provided.')
    result = collection.insert_one(user_data_dict)
    print(result)
    return {'data': result}
