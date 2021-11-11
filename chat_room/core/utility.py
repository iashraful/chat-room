from typing import Any, List

from motor.motor_asyncio import AsyncIOMotorCursor


async def async_cursor_parser(cursor: AsyncIOMotorCursor, limit=None) -> List[dict]:
    data = await cursor.to_list(length=limit)
    for d in data:
        if "_id" in d:
            d["id"] = str(d.pop("_id", ""))
    return data
