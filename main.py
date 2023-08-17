import asyncio
from random import choices
from typing import Any

from fastapi import FastAPI, Depends, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from manager import WebSocketManager

app = FastAPI()
manager = WebSocketManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_response(client_id, data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.send_one(client_id, f"Client #{client_id} left the chat")


async def client():
    if not manager.clients:
        raise HTTPException(status_code=400, detail="No clients connected")

    client_id = choices(list(manager.clients.keys()))[0]
    if not client_id:
        raise HTTPException(status_code=400, detail="No clients connected")
    return client_id


class InvokeParams(BaseModel):
    action: str
    param: Any = None


async def send_request(client_id: str, params: dict):
    response = await manager.send_one(client_id, params)
    if not response:
        raise HTTPException(status_code=400, detail=f"{client_id} offline")

    try:
        result = await asyncio.wait_for(manager.get_response(client_id), timeout=10)  # Set timeout
    except asyncio.TimeoutError:
        raise HTTPException(status_code=400, detail="Timeout waiting for client response")

    return result


@app.post("/invoke")
async def handle_invoke(
        params: InvokeParams,
        client_id: str = Depends(client)
):
    return await send_request(client_id, {"action": params.action, "param": params.param})


@app.get("/invoke")
async def handle_invoke_get(
        action: str,
        param: Any = None,
        client_id: str = Depends(client)
):
    return await send_request(client_id, {"action": action, "param": param})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        log_level="info",
        port=8000,
        # loop="asyncio",
        workers=1,
    )
