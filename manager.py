import asyncio
from typing import Dict
from fastapi.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.response_events: Dict[str, asyncio.Event] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.clients[client_id] = websocket
        self.message_queues[client_id] = asyncio.Queue()
        self.response_events[client_id] = asyncio.Event()

    def disconnect(self, client_id: str):
        if client_id in self.clients:
            del self.clients[client_id]
            del self.message_queues[client_id]
            del self.response_events[client_id]

    async def handle_message(self, client_id: str, message: str):
        await self.message_queues[client_id].put(message)

    async def send_one(self, client_id: str, message: dict):
        websocket = self.clients.get(client_id)
        if not websocket:
            return False

        await websocket.send_json(message)
        return True

    async def get_response(self, client_id: str):
        await self.response_events[client_id].wait()
        self.response_events[client_id].clear()
        return await self.message_queues[client_id].get()

    async def send_response(self, client_id: str, response: str):
        if client_id in self.response_events:
            await self.message_queues[client_id].put(response)
            self.response_events[client_id].set()
