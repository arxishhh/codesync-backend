from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi import APIRouter
from src.websocket.models import Message,UserDetails
from src.websocket.handler import Handler
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.document.service import DocumentService,InviteService
from fastapi import Depends


handler = Handler()
docService = DocumentService()
socket = APIRouter()
inviteService = InviteService()

@socket.websocket('/ws/{token}')
async def websockets_endpoint(websocket : WebSocket,token : str,user_details : UserDetails,session : AsyncSession = Depends(get_session)):

    token_data = await inviteService.deserialize(token=token)

    if not token_data :
        await handler.error(
            websocket=websocket,
            message={
                "message_type":"error",
                "payload":{
                    "details":"Invalid Invite"
                }
            }
        )
        return 
    
    doc_id = token_data.get("doc_id")

    document = await docService.get_document(doc_id=doc_id,session=session)
    if not document:
        await handler.error(
            websocket=websocket,
            message={
                "message_type":"error",
                "payload":{
                "details":"Document Not Found"
                }
            }) 
        
        return
    
    socketmanager = websocket.app.state.socketmanager
    
    await socketmanager.connect(
        websocket=websocket,
        doc_id=doc_id,
        user_details=user_details.model_dump())
    
    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)

            await handler.handler(
                message=message,
                websocket=websocket,
                token_data=token_data,
                session=session,
                document=document
            )
    except WebSocketDisconnect:
        await socketmanager.disconnect(
            websocket=websocket,
            doc_id=doc_id
        )



