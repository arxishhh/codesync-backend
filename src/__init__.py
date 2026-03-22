from fastapi import FastAPI
from src.websocket.routes import socket
from src.document.routes import docroute
from src.document.manager import DocumentManager
from src.websocket.manager import WebSocketManager
from src.db.main import autosave_loop
import asyncio

version = "v1"


codesync = FastAPI(
    title="CodeSync Backend",
    version=version
)

@codesync.on_event("startup")
async def startup():
    codesync.state.docmanager = DocumentManager()
    codesync.state.socketmanager = WebSocketManager()
    asyncio.create_task(autosave_loop(app=codesync))

codesync.include_router(
    router=socket,
    prefix=f"/api/{version}",
    tags=['websocket'],
)
codesync.include_router(
    router=docroute,
    prefix = f"/api/{version}/documents",
    tags=['document']
)