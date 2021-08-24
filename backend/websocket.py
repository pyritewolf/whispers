from typing import Optional, List

from fastapi import WebSocket, status


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(
        self, websocket: WebSocket, code: Optional[int] = status.WS_1011_INTERNAL_ERROR
    ):
        await websocket.send({"type": "websocket.close", "code": code})
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
