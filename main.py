# -*- coding: utf-8 -*-
import asyncio
import json
from random import choices

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from response import SuccessResponse, ErrorResponse
from manager import manager

app = FastAPI()
messages = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            messages[client_id] = data
            # await manager.send_one(client_id, {'action': 'message', 'message': data})
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.send_one(client_id, f"Client #{client_id} left the chat")


@app.get("/do/{action}")
async def do(action):
    client_ids = choices(list(manager.clients.keys()))  # random client
    if not client_ids:
        return ErrorResponse("no online client")
    client_id = client_ids[0]
    response = await manager.send_one(client_id, {
        "action": action
    })
    if not response:
        return ErrorResponse(f"{client_id} offline")
    for _ in range(100):
        await asyncio.sleep(0.1)
        if res := messages.get(client_id):
            messages[client_id] = None
            return SuccessResponse(json.loads(res))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app='main:app',
        log_level="debug",
        port=8000,
        # loop="asyncio",
        # workers=4,
    )
