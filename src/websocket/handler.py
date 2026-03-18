from src.document.manager import DocumentManager
from src.websocket.manager import WebSocketManager
from fastapi import WebSocket
from src.websocket.models import Message
from sqlmodel.ext.asyncio.session import AsyncSession
import base64
import logging

docmanager = DocumentManager()


class Handler:
    def __init__(self,socketmanager : WebSocketManager):
        self.socketmanager = socketmanager
        self.handlerDict = {
            'update':self.apply_update,
            'join':self.join,
            'leave':self.leave,
        }

    async def handler(self,message : Message,websocket : WebSocket,doc_id : str,session : AsyncSession):
        messageType = message.message_type
        
        handlerFunc = self.handlerDict.get(messageType)

        if not handlerFunc:
            logging.error(f"Unknown Message Type :{messageType}")
            return

        await handlerFunc(
            websocket=websocket,
            doc_id=doc_id,
            session=session,
            payload=message.payload
        )

    async def join(self,websocket : WebSocket,doc_id : str,session : AsyncSession,payload = None):
        logging.info(f"Fetching Document {doc_id} For {websocket.client}")
    
        doc = await self.sync(doc_id=doc_id,session=session)
        if not doc :
            return None
        
        doc_encoded = base64.b64encode(doc).decode()

        message = {
            'type' : 'sync',
            'payload':
            {
                'state':doc_encoded
            }
        }

        await self.socketmanager.send_message(
            doc_id=doc_id,
            websocket=websocket,
            message=Message(**message)
        )


    async def sync(self,doc_id:str,session : AsyncSession):
        return await docmanager.get_state(doc_id=doc_id,session=session)

    async def leave(self,websocket : WebSocket, doc_id : str,session : AsyncSession,payload = None):
        await self.socketmanager.disconnect(
            websocket=websocket,
            doc_id=doc_id
        )

    async def apply_update(self,websocket : WebSocket,doc_id : str,session : AsyncSession,payload):

        if not payload or 'update' not in payload:
            logging.error("Update Not Present In Payload")
            return

        try : 
            updates_bytes = base64.b64decode(payload['update'])
        except Exception as e: 
            logging.error(f"Invalid update payload : {str(e)}")
            return 

        await docmanager.update(
            doc_id=doc_id,
            updates=updates_bytes,
            session=session
        )

        message = {'type':"update",
                   'payload':{
                       'content':payload['update']
                   }}
        
        await self.socketmanager.broadcast(
            sender=websocket,
            message = Message(**message),
            doc_id = doc_id)

        


