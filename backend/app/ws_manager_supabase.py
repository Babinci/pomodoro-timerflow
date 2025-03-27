# app/ws_manager_supabase.py
from fastapi import WebSocket
from typing import Dict, Set, Optional
from datetime import datetime, timezone
import json
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Import Supabase client
from .supabase import supabase

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
        current_time = datetime.now(timezone.utc)
        
        if not self.is_paused:
            elapsed = (current_time - self.last_update).total_seconds()
            new_time = max(0, self.time_remaining - elapsed)
            
            # Check if timer just reached 0
            if new_time == 0 and self.time_remaining > 0:
                self.session_completed = True
            
            self.time_remaining = new_time
            self.last_update = current_time  # Only update timestamp when timer is running

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

    def start_timer(self, user_id: str, task_id: int, session_type: str, duration: int, preset_type: str = 'short', user_settings: dict = None):
        """Start a new timer session with user's settings"""
        if not user_settings:
            raise ValueError("User settings are required")
        
        # Preserve round_number if exists, otherwise default to 1
        current_round = 1
        if user_id in self.timer_states:
            current_round = self.timer_states[user_id].round_number
                
        self.timer_states[user_id] = TimerState(
            task_id=task_id,
            session_type=session_type,
            time_remaining=duration,
            user_settings=user_settings,
            preset_type=preset_type
        )
        
        # Set the preserved round number
        self.timer_states[user_id].round_number = current_round
        self.timer_states[user_id].resume()  # Start running immediately
        
        # Load and store the active task details
        try:
            task_response = supabase.table("tasks").select("id, title").eq("id", task_id).execute()
            if task_response.data and len(task_response.data) > 0:
                self.timer_states[user_id].active_task = {
                    "id": task_response.data[0]["id"],
                    "title": task_response.data[0]["title"],
                }
        except Exception as e:
            logger.error(f"Error fetching task: {str(e)}")

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
        if current_session == 'work':
            try:
                task_id = state.task_id
                # Get current completed pomodoros
                task_response = supabase.table("tasks").select("completed_pomodoros").eq("id", task_id).execute()
                if task_response.data and len(task_response.data) > 0:
                    current_count = task_response.data[0]["completed_pomodoros"] or 0
                    # Update completed pomodoros
                    supabase.table("tasks").update({"completed_pomodoros": current_count + 1}).eq("id", task_id).execute()
            except Exception as e:
                logger.error(f"Error updating task completion: {str(e)}")
            
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
            try:
                # Get user settings
                user_response = supabase.table("users").select("pomodoro_settings").eq("id", user_id).execute()
                if user_response.data and len(user_response.data) > 0:
                    user_settings = user_response.data[0]["pomodoro_settings"]
                    preset_type = 'short'  # Default preset
                    
                    # Create a new timer state with default values
                    # Always initialize with 'work' session type
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
            except Exception as e:
                logger.error(f"Error creating default timer state: {str(e)}")
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

        # Update task completion if it was a work session
        if current_session == 'work':
            try:
                task_id = state.task_id
                # Get current completed pomodoros
                task_response = supabase.table("tasks").select("completed_pomodoros").eq("id", task_id).execute()
                if task_response.data and len(task_response.data) > 0:
                    current_count = task_response.data[0]["completed_pomodoros"] or 0
                    # Update completed pomodoros
                    supabase.table("tasks").update({"completed_pomodoros": current_count + 1}).eq("id", task_id).execute()
            except Exception as e:
                logger.error(f"Error updating task completion: {str(e)}")

        # Update state to reflect completion
        state.time_remaining = 0
        
        # Automatically transition to the next session
        self.skip_to_next(user_id)

    async def sync_timer_state(self, user_id: str):
        """Send current timer state to all user's connections"""
        if user_id not in self.timer_states:
            return

        state = self.timer_states[user_id]
        
        # Don't modify the actual state, just calculate the current time
        current_time = datetime.now(timezone.utc)
        remaining_time = state.time_remaining
        
        # Only calculate elapsed time if timer is running
        if not state.is_paused:
            elapsed = (current_time - state.last_update).total_seconds()
            remaining_time = max(0, state.time_remaining - elapsed)
            
            # Check if timer just completed
            if remaining_time == 0 and state.time_remaining > 0:
                # Handle completion without modifying the state
                await self.handle_session_completion(user_id)
                return

        # Get updated task information
        task_info = None
        if state.task_id:
            try:
                task_response = supabase.table("tasks").select("id, title, completed_pomodoros, estimated_pomodoros").eq("id", state.task_id).execute()
                if task_response.data and len(task_response.data) > 0:
                    task_info = task_response.data[0]
            except Exception as e:
                logger.error(f"Error fetching task info: {str(e)}")

        message = {
            "type": "timer_sync",
            "data": {
                "task_id": state.task_id,
                "session_type": state.session_type,
                "remaining_time": round(remaining_time),
                "is_paused": state.is_paused,
                "round_number": state.round_number,
                "active_task": task_info,
                "preset_type": state.preset_type
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