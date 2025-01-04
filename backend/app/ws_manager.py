# app/ws_manager.py
from fastapi import WebSocket
from typing import Dict, Set, Optional
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from . import models

class TimerState:
    def __init__(self, task_id: int, session_type: str, time_remaining: int, user_settings: dict, preset_type: str = 'short'):
        self.task_id = task_id
        self.session_type = session_type
        self.time_remaining = time_remaining
        self.is_paused = True
        self.last_update = datetime.now(timezone.utc)
        self.round_number = 1  # Track which round we're on
        self.preset_type = preset_type  # Current preset type (short/long)
        self.settings = user_settings  # Use user's actual settings
        self.active_task = None  # Store the active task details

    def update_remaining_time(self):
        """Update remaining time if timer is running"""
        if not self.is_paused:
            elapsed = (datetime.now(timezone.utc) - self.last_update).total_seconds()
            self.time_remaining = max(0, self.time_remaining - elapsed)
        self.last_update = datetime.now(timezone.utc)

    def get_remaining_time(self) -> int:
        """Get current remaining time"""
        self.update_remaining_time()
        return max(0, round(self.time_remaining))

    def pause(self):
        """Pause the timer"""
        self.update_remaining_time()  # Update time before pausing
        self.is_paused = True

    def resume(self):
        """Resume the timer"""
        self.last_update = datetime.now(timezone.utc)  # Reset the update time
        self.is_paused = False
    


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.timer_states: Dict[str, TimerState] = {}
        self.db: Optional[Session] = None

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

        # Send current timer state if exists
        if user_id in self.timer_states:
            await self.sync_timer_state(user_id)

    async def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    def start_timer(self, user_id: str, task_id: int, session_type: str, duration: int, preset_type: str = 'short', user_settings: dict = None):
        """Start a new timer session with user's settings"""
        if not user_settings:
            raise ValueError("User settings are required")
              
        self.timer_states[user_id] = TimerState(
            task_id=task_id,
            session_type=session_type,
            time_remaining=duration,
            user_settings=user_settings,
            preset_type=preset_type
        )
        self.timer_states[user_id].resume()  # Start running immediately
        
        # Load and store the active task details
        if self.db:
            task = self.db.query(models.Task).filter(models.Task.id == task_id).first()
            if task:
                self.timer_states[user_id].active_task = {
                    "id": task.id,
                    "title": task.title,
                }

    def stop_timer(self, user_id: str):
        if user_id in self.timer_states:
            del self.timer_states[user_id]

    def skip_to_next(self, user_id: str):
        """Skip to the next session by completing current session and starting next one"""
        if user_id not in self.timer_states:
            return
              
        state = self.timer_states[user_id]
        current_session = state.session_type
          
        # Complete the current session by setting remaining time to 0
        state.time_remaining = 0
        state.update_remaining_time()
          
        # Determine the next session type based on current session and round number
        if current_session == 'work':
            # After work session, determine break type
            if state.round_number % 4 == 0:  # Every 4th session
                next_session = 'long_break'
            else:
                next_session = 'short_break'
        else:
            # After any break, go back to work
            next_session = 'work'
            if current_session == 'long_break':
                state.round_number = 1
            else:
                state.round_number += 1
          
        # Set up the next session with proper duration
        state.session_type = next_session
        if next_session == 'work':
            state.time_remaining = state.settings[state.preset_type]['work_duration'] * 60
        elif next_session == 'short_break':
            state.time_remaining = state.settings[state.preset_type]['short_break'] * 60
        else:  # long_break
            state.time_remaining = state.settings[state.preset_type]['long_break'] * 60
          
        # Update timestamp and pause the timer
        state.last_update = datetime.now(timezone.utc)
        state.is_paused = True  # Pause after skipping to next session

    async def sync_timer_state(self, user_id: str):
        """Send current timer state to all user's connections"""
        if user_id not in self.timer_states:
            return

        state = self.timer_states[user_id]
        message = {
            "type": "timer_sync",
            "data": {
                "task_id": state.task_id,
                "session_type": state.session_type,
                "remaining_time": state.get_remaining_time(),
                "is_paused": state.is_paused,
                "round_number": state.round_number,  # Include round number
                "active_task": state.active_task,    # Include active task details
            },
        }
        await self.broadcast_to_user(user_id, message)

    async def broadcast_to_user(self, user_id: str, message: dict):
        """Send message to all user's connections"""
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

manager = ConnectionManager()
