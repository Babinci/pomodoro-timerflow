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
        self.session_completed = False  # New flag to track session completion

    def update_remaining_time(self):
        """Update remaining time if timer is running"""
        if not self.is_paused:
            elapsed = (datetime.now(timezone.utc) - self.last_update).total_seconds()
            new_time = max(0, self.time_remaining - elapsed)
            
            # Check if timer just reached 0
            if new_time == 0 and self.time_remaining > 0:
                self.session_completed = True
            
            self.time_remaining = new_time
            
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
        """Skip to the next session"""
        if user_id not in self.timer_states:
            return
            
        state = self.timer_states[user_id]
        current_session = state.session_type
        current_preset = state.preset_type  # Store current preset type

        # If it was a work session, update the task completion
        if current_session == 'work' and self.db:
            task = self.db.query(models.Task).filter(models.Task.id == state.task_id).first()
            if task:
                task.completed_pomodoros += 1
                self.db.commit()
            
        # Determine the next session type
        if current_session == 'work':
            if state.round_number % state.settings[current_preset]['sessions_before_long_break'] == 0:
                next_session = 'long_break'
            else:
                next_session = 'short_break'
        else:
            next_session = 'work'
            if current_session == 'long_break':
                state.round_number = 1
            else:
                state.round_number += 1
            
        # Set up the next session
        state.session_type = next_session
        if next_session == 'work':
            state.time_remaining = state.settings[current_preset]['work_duration'] * 60
        elif next_session == 'short_break':
            state.time_remaining = state.settings[current_preset]['short_break'] * 60
        else:  # long_break
            state.time_remaining = state.settings[current_preset]['long_break'] * 60
            
        # Update timestamp and pause the timer
        state.last_update = datetime.now(timezone.utc)
        state.is_paused = True

    def reset_rounds(self, user_id: str):
        """Reset the round counter and timer for a user"""
        if user_id not in self.timer_states:
            # If there's no active timer state, create a default one
            if self.db:
                # Get user settings
                from . import models
                user = self.db.query(models.User).filter(models.User.id == user_id).first()
                if user:
                    user_settings = user.pomodoro_settings
                    preset_type = 'short'  # Default preset
                    
                    # Create a new timer state with default values
                    self.timer_states[user_id] = TimerState(
                        task_id=None,
                        session_type='work',
                        time_remaining=user_settings[preset_type]['work_duration'] * 60,
                        user_settings=user_settings,
                        preset_type=preset_type
                    )
                    # Set round number to 1
                    self.timer_states[user_id].round_number = 1
                    # Pause the timer
                    self.timer_states[user_id].is_paused = True
                    return
        else:
            # Reset existing timer state
            state = self.timer_states[user_id]
            # Reset round number
            state.round_number = 1
            # Reset to work session
            state.session_type = 'work'
            # Reset timer duration based on preset
            state.time_remaining = state.settings[state.preset_type]['work_duration'] * 60
            # Update timestamp and pause the timer
            state.last_update = datetime.now(timezone.utc)
            state.is_paused = True

    async def handle_session_completion(self, user_id: str):
        """Handle the completion of a timer session"""
        if user_id not in self.timer_states:
            return
    
        state = self.timer_states[user_id]
        current_session = state.session_type
        current_preset = state.preset_type  # Store current preset
    
        # Update task completion if it was a work session
        if current_session == 'work' and self.db:
            task = self.db.query(models.Task).filter(models.Task.id == state.task_id).first()
            if task:
                task.completed_pomodoros += 1
                self.db.commit()
    
        # Automatically transition to the next session
        self.skip_to_next(user_id)

    async def sync_timer_state(self, user_id: str):
        """Send current timer state to all user's connections"""
        if user_id not in self.timer_states:
            return

        state = self.timer_states[user_id]
        remaining_time = state.get_remaining_time()
        
        # Check if session just completed
        if state.session_completed:
            state.session_completed = False  # Reset the flag
            await self.handle_session_completion(user_id)
            return

        # Get updated task information
        task_info = None
        if self.db and state.task_id:
            task = self.db.query(models.Task).filter(models.Task.id == state.task_id).first()
            if task:
                task_info = {
                    "id": task.id,
                    "title": task.title,
                    "completed_pomodoros": task.completed_pomodoros,
                    "estimated_pomodoros": task.estimated_pomodoros
                }

        message = {
            "type": "timer_sync",
            "data": {
                "task_id": state.task_id,
                "session_type": state.session_type,
                "remaining_time": remaining_time,
                "is_paused": state.is_paused,
                "round_number": state.round_number,
                "active_task": task_info,
                "preset_type": state.preset_type  # Include preset type in sync message
            },
        }
        await self.broadcast_to_user(user_id, message)
    def refresh_user_settings(self, user_id: str, user_settings: dict):
        """Update user settings in timer state"""
        if user_id in self.timer_states:
            self.timer_states[user_id].settings = user_settings
            # Update remaining time based on current session type and preset
            state = self.timer_states[user_id]
            if state.is_paused:  # Only update time if timer is paused
                current_session = state.session_type
                current_preset = state.preset_type
                if current_session == 'work':
                    state.time_remaining = state.settings[current_preset]['work_duration'] * 60
                elif current_session == 'short_break':
                    state.time_remaining = state.settings[current_preset]['short_break'] * 60
                else:  # long_break
                    state.time_remaining = state.settings[current_preset]['long_break'] * 60
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
