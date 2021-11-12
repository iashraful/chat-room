from fastapi.param_functions import Depends
from starlette import status
from chat_room.app.chat.models import Group
from chat_room.app.chat.schema import GroupCreateSchema
from chat_room.auth.utils import request_user

from chat_room.core.config import settings
from chat_room.core.database import DBClient, get_database
from chat_room.core.response import BaseResponse
from chat_room.core.utility import async_cursor_parser


async def get_groups(
    db: DBClient = Depends(get_database), current_user: dict = Depends(request_user)
):
    collection = db[settings.DB_NAME][Group.collection_name()]
    cursor = collection.find()
    groups = await async_cursor_parser(cursor=cursor)
    return BaseResponse(
        msg="Group fetched successfully.", status=status.HTTP_200_OK, data=groups
    )


async def create_group(
    group: GroupCreateSchema,
    db: DBClient = Depends(get_database),
    current_user: dict = Depends(request_user),
):
    collection = db[settings.DB_NAME][Group.collection_name()]
    provided_document = group.dict()
    provided_document["admin"] = current_user
    await collection.insert_one(provided_document)
    return BaseResponse(
        msg="Group created successfully.", status=status.HTTP_201_CREATED
    )
