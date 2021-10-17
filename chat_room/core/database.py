from typing import NewType

from motor.motor_asyncio import AsyncIOMotorClient

from chat_room.core.config import settings as s

DBClient = NewType("DBClient", AsyncIOMotorClient)


class DataBase:
    client: DBClient = None


db = DataBase()


async def get_database() -> DBClient:
    return db.client


async def connect_to_database():
    db.client = AsyncIOMotorClient(
        s.MONGODB_URL,
        maxPoolSize=s.MAX_CONNECTIONS_COUNT,
        minPoolSize=s.MIN_CONNECTIONS_COUNT,
    )


async def close_database_connection():
    db.client.close()
