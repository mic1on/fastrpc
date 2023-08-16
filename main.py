import asyncio
from random import choices

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from response import SuccessResponse, ErrorResponse
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


@app.get("/do/{action}")
async def do(action):
    if not manager.clients:
        return ErrorResponse("No clients connected")

    client_id = choices(list(manager.clients.keys()))[0]
    if not client_id:
        return ErrorResponse("No clients connected")
    response = await manager.send_one(client_id, {"action": action})
    if not response:
        return ErrorResponse(f"{client_id} offline")

    try:
        result = await asyncio.wait_for(manager.get_response(client_id), timeout=10)  # Set timeout
    except asyncio.TimeoutError:
        return ErrorResponse("Timeout waiting for client response")

    return SuccessResponse(result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        log_level="info",
        port=8000,
        # loop="asyncio",
        workers=1,
    )