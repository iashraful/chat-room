from datetime import datetime, timedelta
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status

from chat_room.app.user.models import User
from chat_room.core.config import settings
from chat_room.core.database import DBClient, get_database

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


async def authenticate(
    *, email: EmailStr, password: str, db: DBClient
) -> Optional[User]:
    user = await db[settings.DB_NAME][User.collection_name()].find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user.get("password")):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def create_refresh_token(*, sub: str) -> str:
    return _create_token(
        token_type="refresh_token",
        lifetime=timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_from_refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload and payload["type"] == "refresh_token":
            return create_access_token(sub=payload["sub"]), create_refresh_token(
                sub=payload["sub"]
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def request_user(
    db: DBClient = Depends(get_database),
    auth_info: HTTPAuthorizationCredentials = Security(security),
):
    try:
        payload = jwt.decode(
            auth_info.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(
            detail="Could not validate credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user = user = await db[settings.DB_NAME][User.collection_name()].find_one(
        {"email": email}
    )
    if "_id" in user:
        user["id"] = str(user.pop("_id"))
    if "password" in user:
        user.pop("password")
    if user is None:
        raise HTTPException(
            detail="Could not validate credentials.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return user
