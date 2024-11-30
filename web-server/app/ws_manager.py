from fastapi import WebSocket
from typing import Dict, List, Optional
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        # user_id -> list of WebSocket connections (support multiple devices)
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # user_id -> current session info
        self.active_sessions: Dict[int, dict] = {}
        
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]

    async def broadcast_to_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    await self.disconnect(connection, user_id)

    def start_session(self, user_id: int, session_data: dict):
        """Start a new Pomodoro session for a user"""
        self.active_sessions[user_id] = {
            "start_time": datetime.utcnow(),
            "end_time": None,
            **session_data
        }

    def end_session(self, user_id: int):
        """End the current Pomodoro session for a user"""
        if user_id in self.active_sessions:
            self.active_sessions[user_id]["end_time"] = datetime.utcnow()

    def get_user_session(self, user_id: int) -> Optional[dict]:
        """Get the current session info for a user"""
        return self.active_sessions.get(user_id)

manager = ConnectionManager()