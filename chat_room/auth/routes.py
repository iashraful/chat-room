from fastapi import APIRouter

from .views import auth_token, refresh_token

auth_router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)


auth_router.add_api_route("/auth-token", auth_token, methods=["POST"])
auth_router.add_api_route("/refresh-token", refresh_token, methods=["POST"])
