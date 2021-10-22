from fastapi import APIRouter

from .views import UserView

user_router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

user_router.add_api_route("/", UserView.create_user, methods=["POST"])
