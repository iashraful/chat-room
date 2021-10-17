import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

app = FastAPI()
mongo_url = f'mongodb://{os.environ["MONGO_INITDB_ROOT_USERNAME"]}:{os.environ["MONGO_INITDB_ROOT_PASSWORD"]}@{os.environ["MONGO_HOST"]}/{os.environ["DB_NAME"]}?retryWrites=true&w=majority'
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = client.college


@app.get("/")
async def index():
    return {"Health": "OK!"}
