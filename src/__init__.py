from fastapi import FastAPI
from src.websocket.route import socket

version = "v1"

codesync = FastAPI(
    title="CodeSync Backend",
    version=version
)

codesync.include_router(
    router=socket,
    tags=['websocket'],
)