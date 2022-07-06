# -*- coding: utf-8 -*-
from typing import Dict
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.clients[client_id] = websocket

    def disconnect(self, client_id: str):
        self.clients.pop(client_id)

    @staticmethod
    async def _send(connection, message: str, mode: str = "json"):
        if mode == "json":
            await connection.send_json(message)
        elif mode == "text":
            await connection.send_text(message)
        else:
            await connection.send(message)

    async def send_all(self, message: str, mode: str = "json"):
        if not self.clients:
            return False
        for client_id, connection in self.clients.items():
            await self._send(connection, message, mode)
        return True

    async def send_one(self, client_id, message, mode: str = "json"):
        if client_id not in self.clients.keys():
            return False
        await self._send(self.clients[client_id], message, mode)
        return True

    sendAll = send_all
    sendOne = send_one


manager = WSManager()
