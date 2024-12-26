# app/ws_manager.py
from fastapi import WebSocket
from typing import Dict, List, Optional
from datetime import datetime
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.active_sessions: Dict[int, Dict] = {}
        
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    async def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    def start_session(self, user_id: int, session_data: dict):
        self.active_sessions[user_id] = {
            **session_data,
            "start_time": datetime.utcnow(),
            "is_running": True,
            "remaining_time": session_data.get("duration", 1500),  # default 25 minutes
            "paused_at": None
        }
    
    def pause_session(self, user_id: int):
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            session["is_running"] = False
            session["paused_at"] = datetime.utcnow()
    
    def resume_session(self, user_id: int):
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            if session["paused_at"]:
                # Adjust start_time to account for pause duration
                pause_duration = (datetime.utcnow() - session["paused_at"]).total_seconds()
                session["start_time"] = session["start_time"] + timedelta(seconds=pause_duration)
            session["is_running"] = True
            session["paused_at"] = None
    
    def end_session(self, user_id: int):
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]
    
    def get_session_state(self, user_id: int) -> dict:
        if user_id not in self.active_sessions:
            return {"active_session": False}
            
        session = self.active_sessions[user_id]
        if session["is_running"]:
            elapsed = (datetime.utcnow() - session["start_time"]).total_seconds()
            remaining = max(0, session["remaining_time"] - elapsed)
        else:
            remaining = session["remaining_time"]
            
        return {
            "active_session": True,
            "session_id": session["session_id"],
            "task_id": session["task_id"],
            "session_type": session["type"],
            "current_session": session["current_session"],
            "remaining_time": int(remaining),
            "is_running": session["is_running"]
        }
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

manager = ConnectionManager()