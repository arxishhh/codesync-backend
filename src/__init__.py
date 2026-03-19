from fastapi import FastAPI
from src.websocket.routes import socket
from src.document.routes import docroute

version = "v1"

codesync = FastAPI(
    title="CodeSync Backend",
    version=version
)

codesync.include_router(
    router=socket,
    prefix=f"/api/{version}",
    tags=['websocket'],
)
codesync.include_router(
    router=docroute,
    prefix = f"/api/{version}/doc",
    tags=['document']
)