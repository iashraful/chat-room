from datetime import timedelta, datetime
from typing import Optional

from passlib.context import CryptContext
from pydantic import EmailStr

from jose import jwt, JWTError

from chat_room.app.user.models import User
from chat_room.core.config import settings
from chat_room.core.database import DBClient

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
