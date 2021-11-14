from fastapi import APIRouter

from chat_room.app.chat.views import (
    create_group,
    create_inbox,
    get_groups,
    get_inboxes,
    websocket_endpoint,
)

chat_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)
chat_router.add_api_route("/groups", get_groups, methods=["GET"])
chat_router.add_api_route("/groups", create_group, methods=["POST"])
chat_router.add_api_route("/inboxes", get_inboxes, methods=["GET"])
chat_router.add_api_route("/inboxes", create_inbox, methods=["POST"])
chat_router.add_api_websocket_route("/ws/{client_id}", websocket_endpoint)
