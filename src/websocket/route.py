from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi import APIRouter
from src.manager import WebSocketManager
from src.websocket.schemas import Message


manager = WebSocketManager()

socket = APIRouter()

@socket.websocket('/ws/{room_id}')
async def websockets_endpoint(websocket : WebSocket,room_id : str):

    await manager.connect(
        websocket=websocket,
        room_id=room_id)

    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)

            await manager.broadcast(
                sender=websocket,
                room_id=room_id,
                message=message
            )
    except WebSocketDisconnect:
        await manager.disconnect(
            websocket=websocket,
            room_id=room_id
        )



