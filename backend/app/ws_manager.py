# app/ws_manager.py
from fastapi import WebSocket
from typing import Dict, Set, Optional
from datetime import datetime, timezone
import json


class TimerState:
    def __init__(self, task_id: int, session_type: str, time_remaining: int):
        self.task_id = task_id
        self.session_type = session_type  # 'work', 'short_break', 'long_break'
        self.time_remaining = time_remaining  # in seconds
        self.is_paused = True  # Start paused
        self.last_update = datetime.now(timezone.utc)

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

    def start_timer(self, user_id: str, task_id: int, session_type: str, duration: int):
        self.timer_states[user_id] = TimerState(
            task_id=task_id, session_type=session_type, time_remaining=duration
        )
        self.timer_states[user_id].resume()  # Start running immediately

    def stop_timer(self, user_id: str):
        if user_id in self.timer_states:
            del self.timer_states[user_id]
    def skip_to_next(self, user_id: str):
        """Skip to the next session (work/break)
        to refine
        """
        if user_id not in self.timer_states:
            return

        state = self.timer_states[user_id]
        current_session = state.session_type
        
        # Determine the next session type
        if current_session == 'work':
            # If we just finished work, determine break type
            if state.round_number % 4 == 0:  # Every 4th session
                next_session = 'long_break'
            else:
                next_session = 'short_break'
        else:
            # After any break, go back to work and increment round
            next_session = 'work'
            if current_session == 'long_break':
                state.round_number = 1
            else:
                state.round_number += 1

        # Update session type and reset timer
        state.session_type = next_session
        if next_session == 'work':
            state.time_remaining = state.settings[state.preset_type]['work_duration'] * 60
        elif next_session == 'short_break':
            state.time_remaining = state.settings[state.preset_type]['short_break'] * 60
        else:  # long_break
            state.time_remaining = state.settings[state.preset_type]['long_break'] * 60
        
        # Update last_update time and resume the timer
        state.last_update = datetime.now(timezone.utc)
        state.is_paused = False

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
