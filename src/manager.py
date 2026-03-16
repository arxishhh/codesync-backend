from fastapi import WebSocket, WebSocketDisconnect
from typing import Set,Dict
from src.websocket.schemas import Message
import asyncio

class WebSocketManager:
    def __init__(self):
        self.connected_clients : Dict[str,Set[WebSocket]] = {}

    
    async def connect(self,websocket:WebSocket,room_id:str):
        
        print(f"Connected Room: {room_id} using {websocket.client.host}:{websocket.client.port}")
        await websocket.accept()
        if room_id not in self.connected_clients:
            self.connected_clients[room_id] = set()
        
        self.connected_clients[room_id].add(websocket)
        

    async def disconnect(self,websocket:WebSocket,room_id:str):
        print(f"Disconnecting User: {room_id}")

        if room_id in self.connected_clients:

            clients = self.connected_clients[room_id]
            clients.discard(websocket)
            
            if not clients:
                self.connected_clients.pop(room_id)

    
    async def send_message(self,websocket : WebSocket,message : Message,room_id : str)  -> None:
        try :
            await websocket.send_json(message.model_dump())

        except WebSocketDisconnect:
            await self.disconnect(
                websocket=websocket,
                room_id=room_id)
            
    async def broadcast(self,sender:WebSocket,message : Message,room_id : str):
        target_clients = self.connected_clients.get(room_id)

        tasks = []

        if target_clients:
            for client in list(target_clients):
                if client == sender:
                    continue
                tasks.append(self.send_message(
                    websocket=client,
                    message=message,
                    room_id=room_id
                ))

        
        asyncio.gather(*tasks)