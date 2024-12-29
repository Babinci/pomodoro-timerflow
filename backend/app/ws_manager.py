# app/ws_manager.py
from fastapi import WebSocket
from typing import Dict, Set
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections per user
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Store timer state per user
        self.timer_states: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        
        # Send current timer state to newly connected client
        if user_id in self.timer_states:
            await websocket.send_json({
                "type": "timer_sync",
                "data": self.timer_states[user_id]
            })

    async def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    def start_session(self, user_id: str, session_data: dict):
        self.timer_states[user_id] = {
            **session_data,
            "last_update": datetime.utcnow().isoformat()
        }

    def pause_session(self, user_id: str):
        if user_id in self.timer_states:
            self.timer_states[user_id]["is_running"] = False
            self.timer_states[user_id]["paused_at"] = datetime.utcnow().isoformat()

    def resume_session(self, user_id: str):
        if user_id in self.timer_states:
            self.timer_states[user_id]["is_running"] = True
            self.timer_states[user_id]["resumed_at"] = datetime.utcnow().isoformat()

    def end_session(self, user_id: str):
        if user_id in self.timer_states:
            del self.timer_states[user_id]

    def get_session_state(self, user_id: str) -> dict:
        return self.timer_states.get(user_id, None)

    async def broadcast_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for dead in dead_connections:
                await self.disconnect(dead, user_id)

# Global instance
manager = ConnectionManager()
