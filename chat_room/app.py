import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chat_room.core.config import settings
from chat_room.core import database

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


@app.on_event("startup")
async def startup_db_client():
    await database.connect_to_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.close_database_connection()


# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def index():
    return {"Health": "OK!"}


if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8080, reload=True, access_log=True)
