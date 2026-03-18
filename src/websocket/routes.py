from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi import APIRouter
from src.websocket.manager import WebSocketManager
from src.websocket.models import Message
from src.websocket.handler import Handler
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi import Depends


socketmanager = WebSocketManager()
handler = Handler(socketmanager=socketmanager)
socket = APIRouter()

@socket.websocket('/ws/{doc_id}')
async def websockets_endpoint(websocket : WebSocket,doc_id : str,session : AsyncSession = Depends(get_session)):

    await socketmanager.connect(
        websocket=websocket,
        doc_id=doc_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)

            await handler.handler(
                message=message,
                websocket=websocket,
                doc_id=doc_id,
                session=session
            )
    except WebSocketDisconnect:
        await socketmanager.disconnect(
            websocket=websocket,
            doc_id=doc_id
        )



