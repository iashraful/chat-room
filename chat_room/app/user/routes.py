from fastapi import APIRouter

from .views import create_user, get_user, get_users

user_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)

user_router.add_api_route("/users/{email}", get_user, methods=["GET"])
user_router.add_api_route("/users", create_user, methods=["POST"])
user_router.add_api_route("/users", get_users, methods=["GET"])
