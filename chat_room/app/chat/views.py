from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from starlette.websockets import WebSocket

from chat_room.app.chat.connection import socket_mgr
from chat_room.app.chat.models import Group, Inbox
from chat_room.app.chat.schema import GroupCreateSchema, InboxCreateSchema
from chat_room.app.chat.utility import encode_access_key
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


async def create_inbox(
    inbox: InboxCreateSchema,
    db: DBClient = Depends(get_database),
    current_user: dict = Depends(request_user),
):
    if len(inbox.subscribers) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inbox need at least two participants.",
        )
    collection = db[settings.DB_NAME][Inbox.collection_name()]
    provided_document = inbox.dict()

    provided_document["access_key"] = encode_access_key(inbox.subscribers)
    await collection.insert_one(provided_document)
    return BaseResponse(
        msg="Index created successfully.", status=status.HTTP_201_CREATED
    )


async def get_inboxes(
    db: DBClient = Depends(get_database), current_user: dict = Depends(request_user)
):
    collection = db[settings.DB_NAME][Inbox.collection_name()]
    cursor = collection.find()
    inboxes = await async_cursor_parser(cursor=cursor)
    return BaseResponse(
        msg="Inbox fetched successfully.", status=status.HTTP_200_OK, data=inboxes
    )


async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await socket_mgr.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await socket_mgr.broadcast(f"Client {client_id}: {data}")
