import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


def mongo_url() -> str:
    return os.getenv("MONGODB_URL", "mongodb://127.0.0.1:27017/todo_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(mongo_url())
    db = client.get_default_database()

    # Проверим, что Mongo жива
    await db.command("ping")

    app.state.mongo_client = client
    app.state.mongo_db = db

    yield

    client.close()
