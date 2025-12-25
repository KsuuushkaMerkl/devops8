from fastapi import FastAPI
from app.endpoints import router
from core.db import lifespan

app = FastAPI(title="DevOps pr8", lifespan=lifespan)

app.include_router(router, prefix="/todos", tags=["Todos"])