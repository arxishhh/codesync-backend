from fastapi import WebSocket
from src.websocket.models import Message
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.schemas import Document
import base64
import logging


class Handler:
    def __init__(self):
        self.handlerDict = {
            'update':self.apply_update,
            'join':self.join,
            'leave':self.leave,
            'cursor':self.cursor
        }

    async def handler(self,message : Message,websocket : WebSocket,token_data : dict,document : Document,session : AsyncSession):
        messageType = message.message_type
        
        handlerFunc = self.handlerDict.get(messageType)

        if not handlerFunc:
            logging.error(f"Unknown Message Type :{messageType}")
            return

        await handlerFunc(
            websocket=websocket,
            token_data = token_data,
            session=session,
            document=document,
            payload=message.payload
        )

    async def join(self,websocket : WebSocket,token_data : dict,session : AsyncSession,document : Document,payload = None):

        doc_id = token_data['doc_id']
        logging.info(f"Fetching Document {doc_id} For {websocket.client}")

        socketmanager = websocket.app.state.socketmanger
        user_details = socketmanager.client_meta.get(websocket)
        
        doc = await self.sync(doc_id=doc_id,
                              session=session,
                              websocket=websocket,
                              document=document)
        if not doc :
            return None
        
        doc_encoded = base64.b64encode(doc).decode()

        users = []
        connectedSockets = socketmanager.connected_clients.get(doc_id)

        if connectedSockets:
            for socket in connectedSockets:
                if socket == websocket:
                    continue
                user_data = socketmanager.client_meta.get(socket)
                if user_data:
                    users.append(user_data)


        sync_message = {
            'message_type' : 'sync',
            'payload':
            {
                'state':doc_encoded,
                'permission':token_data['permission'],
                'users':users
            }
        }

        join_message = {
            'message_type':"user_joined",
            'payload':user_details
        }

        await socketmanager.send_message(
            doc_id=doc_id,
            websocket=websocket,
            message=Message(**sync_message)
        )

        await socketmanager.broadcast(
            sender=websocket,
            message = Message(**join_message),
            doc_id = doc_id
        )


    async def sync(self,doc_id:str,websocket : WebSocket,session : AsyncSession,document : Document):
        
        docmanager = websocket.app.state.docmanager
        return await docmanager.get_state(doc_id=doc_id,session=session,
        document=document)

    async def leave(self,websocket : WebSocket,token_data : dict,session : AsyncSession,payload = None):
        socketmanager = websocket.app.state.socketmanger
        user_details = socketmanager.client_meta.get(websocket)
        doc_id = token_data['doc_id']

        message = {
            "message_type":"user_left",
            "payload":user_details
        }

        await socketmanager.broadcast(
            sender=websocket,
            doc_id=doc_id,
            message=Message(**message)
        )
        await socketmanager.disconnect(
            websocket=websocket,
            doc_id=doc_id
        )

    async def apply_update(self,websocket : WebSocket,token_data : dict,session : AsyncSession,payload,document : Document):

        socketmanager = websocket.app.state.socketmanger
        docmanager = websocket.app.state.docmanager
        doc_id = token_data['doc_id']
        permission = token_data['permission']

        if permission != "edit":
            return

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
            session=session,
            document=document
        )

        message = {'type':"update",
                   'payload':{
                       'content':payload['update']
                   }}
        
        await socketmanager.broadcast(
            sender=websocket,
            message = Message(**message),
            doc_id = doc_id)
        
    async def cursor(self,websocket:WebSocket,token_data : dict,session : AsyncSession,payload):

        socketmanager = websocket.app.state.socketmanager
        user_details = socketmanager.client_meta.get(websocket)

        if not user_details: 
            return

        cursor_message = {
            "message_type":"cursor",
            "payload":{
                **user_details,
                **payload
            }
        }

        await socketmanager.broadcast(
            sender=websocket,
            message=Message(**cursor_message),
            doc_id=token_data['doc_id']
        )
    
    async def error(self,websocket : WebSocket,message : dict):
        await websocket.accept()
        await websocket.send_json(message)
        await websocket.close()

        


