from fastapi import APIRouter

from .views import create_user

user_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)

user_router.add_api_route("/", create_user, methods=["POST"])
