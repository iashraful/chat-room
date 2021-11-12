from fastapi import APIRouter

from chat_room.app.chat.views import create_group, get_groups

chat_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)
chat_router.add_api_route("/groups", get_groups, methods=["GET"])
chat_router.add_api_route("/groups", create_group, methods=["POST"])
