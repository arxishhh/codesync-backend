from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi import APIRouter
from src.websocket.models import Message
from src.websocket.handler import Handler
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.document.service import DocumentService
from fastapi import Depends


handler = Handler()
docService = DocumentService()
socket = APIRouter()

@socket.websocket('/ws/{doc_id}')
async def websockets_endpoint(websocket : WebSocket,doc_id : str,session : AsyncSession = Depends(get_session)):

    document = await docService.get_document(doc_id=doc_id,session=session)
    if not document:
        await websocket.accept()
        await websocket.send_json(
            {
                "type":"error",
                "message" : "Document_Not_Found"
            })
        await websocket.close()
        return 
    
    socketmanager = websocket.app.state.socketmanager
    
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
                session=session,
                document=document
            )
    except WebSocketDisconnect:
        await socketmanager.disconnect(
            websocket=websocket,
            doc_id=doc_id
        )



