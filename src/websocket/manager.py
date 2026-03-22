from fastapi import WebSocket, WebSocketDisconnect
from typing import Set,Dict
from src.websocket.models import Message
import asyncio
import logging

class WebSocketManager:
    def __init__(self):
        self.connected_clients : Dict[str,Set[WebSocket]] = {}
    
    async def connect(self,websocket:WebSocket,doc_id:str):
        
        logging.info(f"Connected doc: {doc_id} using {websocket.client}")
        await websocket.accept()
        if doc_id not in self.connected_clients:
            self.connected_clients[doc_id] = set()
        
        self.connected_clients[doc_id].add(websocket)
        

    async def disconnect(self,websocket:WebSocket,doc_id:str):

        docmanager = websocket.app.state.docmanager
        logging.info(f"Disconnecting User: {websocket.client} from doc : {doc_id}")

        if doc_id in self.connected_clients:

            clients = self.connected_clients[doc_id]
            clients.discard(websocket)
            
            if not clients:
                self.connected_clients.pop(doc_id)
                docmanager.delete(doc_id=doc_id)
            

    
    async def send_message(self,websocket : WebSocket,message : Message,doc_id : str)  -> None:
        try :
            await websocket.send_json(message.model_dump())

        except WebSocketDisconnect:
            await self.disconnect(
                websocket=websocket,
                doc_id=doc_id)
            
    async def broadcast(self,sender:WebSocket,message : Message,doc_id : str):
        logging.info(f"Broadcasting Message in doc : {doc_id}")

        target_clients = self.connected_clients.get(doc_id)
        tasks = []

        if target_clients:
            for client in list(target_clients):
                if client == sender:
                    continue
                tasks.append(self.send_message(
                    websocket=client,
                    message=message,
                    doc_id=doc_id
                ))
        
        await asyncio.gather(*tasks,return_exceptions=True)
    
    