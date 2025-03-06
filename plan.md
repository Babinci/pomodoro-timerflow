# Implementation Plan: Pomodoro Session Checkpointing System

this plan is being executed- for now only models are created, need to do proper data migration- have solution for database migrations with current setup

## Step 2: Update the TimerState Class
File: `/backend/app/ws_manager.py`

Add checkpoint handling to the TimerState class:

```python
# Add to imports at the top
from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timezone, timedelta

# Update TimerState class to include checkpoint handling
class TimerState:
    def __init__(self, task_id, session_type, time_remaining, user_settings, preset_type="short"):
        # Existing initialization code remains the same
        self.task_id = task_id
        self.session_type = session_type
        self.time_remaining = time_remaining
        self.is_paused = True
        self.last_update = datetime.now(timezone.utc)
        self.round_number = 1
        self.preset_type = preset_type
        self.settings = user_settings
        self.active_task = None
        self.session_completed = False
        
        # Add last_active timestamp
        self.last_active = datetime.now(timezone.utc)
    
    # Add method to update last_active
    def update_last_active(self):
        self.last_active = datetime.now(timezone.utc)
    
    # Modify existing update_remaining_time method to update last_active
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
        
        # Always update last_active
        self.last_active = current_time
```

## Step 3: Update ConnectionManager
File: `/backend/app/ws_manager.py`

Add checkpoint creation and restoration methods:

```python
# Add to ConnectionManager class
class ConnectionManager:
    # Existing code remains
    
    def create_checkpoint(self, user_id: str, checkpoint_type: str):
        """Create a checkpoint of the current timer state"""
        if user_id not in self.timer_states or not self.db:
            return
            
        state = self.timer_states[user_id]
        
        # Update remaining time before creating checkpoint
        state.update_remaining_time()
        
        # Create checkpoint
        checkpoint = models.PomodoroCheckpoint(
            user_id=int(user_id),
            task_id=state.task_id,
            checkpoint_type=checkpoint_type,
            remaining_time=int(state.time_remaining),
            session_type=state.session_type,
            is_paused=state.is_paused,
            round_number=state.round_number,
            preset_type=state.preset_type,
            last_active=datetime.now(timezone.utc)
        )
        
        self.db.add(checkpoint)
        self.db.commit()
    
    def update_active_timestamp(self, user_id: str):
        """Update the last_active timestamp for a user's latest checkpoint"""
        if not self.db or user_id not in self.timer_states:
            return
            
        # Get latest checkpoint
        checkpoint = self.db.query(models.PomodoroCheckpoint).filter(
            models.PomodoroCheckpoint.user_id == int(user_id)
        ).order_by(models.PomodoroCheckpoint.timestamp.desc()).first()
        
        if checkpoint:
            checkpoint.last_active = datetime.now(timezone.utc)
            self.db.commit()
    
    async def restore_from_checkpoint(self, user_id: str):
        """Restore timer state from the most recent checkpoint"""
        if not self.db:
            return False
            
        # Get latest checkpoint
        checkpoint = self.db.query(models.PomodoroCheckpoint).filter(
            models.PomodoroCheckpoint.user_id == int(user_id)
        ).order_by(models.PomodoroCheckpoint.timestamp.desc()).first()
        
        if not checkpoint:
            return False
            
        # Check if checkpoint is too old (e.g., more than 24 hours)
        if (datetime.now(timezone.utc) - checkpoint.last_active).total_seconds() > 86400:  # 24 hours
            return False
            
        # Get user settings
        user = self.db.query(models.User).filter(models.User.id == int(user_id)).first()
        if not user:
            return False
            
        # Create new timer state from checkpoint
        self.timer_states[user_id] = TimerState(
            task_id=checkpoint.task_id,
            session_type=checkpoint.session_type,
            time_remaining=checkpoint.remaining_time,
            user_settings=user.pomodoro_settings,
            preset_type=checkpoint.preset_type
        )
        
        # Set other properties
        self.timer_states[user_id].round_number = checkpoint.round_number
        self.timer_states[user_id].is_paused = checkpoint.is_paused
        
        # If not paused, adjust for elapsed time
        if not checkpoint.is_paused:
            elapsed = (datetime.now(timezone.utc) - checkpoint.last_active).total_seconds()
            if elapsed < checkpoint.remaining_time:
                self.timer_states[user_id].time_remaining -= elapsed
            else:
                self.timer_states[user_id].time_remaining = 0
                self.timer_states[user_id].is_paused = True
        
        # Load task info if available
        if checkpoint.task_id and self.db:
            task = self.db.query(models.Task).filter(models.Task.id == checkpoint.task_id).first()
            if task:
                self.timer_states[user_id].active_task = {
                    "id": task.id,
                    "title": task.title,
                }
        
        return True
```

## Step 4: Modify Existing Methods to Create Checkpoints
File: `/backend/app/ws_manager.py`

Update these key methods to create checkpoints:

```python
# In start_timer method
def start_timer(self, user_id: str, task_id: int, session_type: str, duration: int, preset_type: str = 'short', user_settings: dict = None):
    # Existing code...
    
    # At the end add:
    # Create checkpoint
    self.create_checkpoint(user_id, f"{session_type.upper()}_STARTED")

# In skip_to_next method
def skip_to_next(self, user_id: str):
    if user_id not in self.timer_states:
        return
        
    state = self.timer_states[user_id]
    current_session = state.session_type
    
    # Create checkpoint for current session ending
    self.create_checkpoint(user_id, f"{current_session.upper()}_INTERRUPTED")
    
    # Rest of existing code...
    
    # At the end add:
    # Create checkpoint for new session
    self.create_checkpoint(user_id, f"{state.session_type.upper()}_STARTED")

# In async handle_session_completion method
async def handle_session_completion(self, user_id: str):
    if user_id not in self.timer_states:
        return

    state = self.timer_states[user_id]
    current_session = state.session_type
    
    # Create checkpoint for session completion
    self.create_checkpoint(user_id, f"{current_session.upper()}_COMPLETED")
    
    # Rest of existing code...
```

## Step 5: Update WebSocket Connection Logic
File: `/backend/app/routers/pomodoro_websocket.py`

Modify the connection handler to restore from checkpoint:

```python
@router.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None),
    db: Session = Depends(get_db)
):
    # Existing validation code...
    
    # After this line:
    await manager.connect(websocket, user_id)
    
    # Add this:
    # Try to restore from checkpoint if no active session
    if user_id not in manager.timer_states:
        restored = await manager.restore_from_checkpoint(user_id)
        if restored:
            await manager.sync_timer_state(user_id)
            
    # Rest of the existing code...
```

## Step 6: Add Periodic Active State Updates
File: `/backend/app/routers/pomodoro_websocket.py`

Add logic to periodically update the last_active timestamp:

```python
# Inside the websocket endpoint, within the while True loop:
while True:
    try:
        # Add this at the beginning of the loop to handle periodic updates
        if user_id in manager.timer_states:
            manager.timer_states[user_id].update_last_active()
            # Update DB checkpoint every 30 seconds
            if datetime.now().second % 30 == 0:  # Every 30 seconds
                manager.update_active_timestamp(user_id)
                
        # Rest of existing code handling messages...
```

## Step 7: Add Checkpoint Cleanup Function
File: `/backend/app/cleanup.py` (new file)

Create a utility to clean up old checkpoints:

```python
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def cleanup_old_checkpoints(db: Session):
    """Remove checkpoints older than 48 hours"""
    cutoff_time = datetime.utcnow() - timedelta(hours=48)
    
    db.query(models.PomodoroCheckpoint).filter(
        models.PomodoroCheckpoint.timestamp < cutoff_time
    ).delete()
    
    db.commit()
```

## Step 8: Update Database Initialization
File: `/backend/app/database.py`

Make sure the new table is created:

```python
# Update Base.metadata.create_all call if needed
Base.metadata.create_all(bind=engine)
```

## Step 9: Test the Implementation

1. Test reconnection after browser refresh
2. Test resuming session after closing the browser and reopening
3. Test long periods of inactivity
4. Test checkpoint creation and restoration logic
5. Verify that timer states are maintained correctly

This detailed implementation plan provides a comprehensive approach to handle connection losses by persisting timer state in the database through checkpoints. Each checkpoint captures the full state needed to restore a session, and the system is designed to gracefully handle various scenarios including normal session progression, interruptions, and reconnections.