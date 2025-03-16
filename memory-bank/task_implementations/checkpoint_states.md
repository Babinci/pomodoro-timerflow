# Checkpoint States

## Overview
This document details the checkpoint state system used to track timer sessions and ensure persistence across connections.

## State Types
- **WORK_STARTED** - When a work session begins
- **WORK_COMPLETED** - When a work session naturally ends
- **WORK_INTERRUPTED** - When a work session is manually skipped
- **SHORT_BREAK_STARTED** - When a short break begins
- **SHORT_BREAK_COMPLETED** - When a short break naturally ends
- **SHORT_BREAK_INTERRUPTED** - When a short break is manually skipped
- **LONG_BREAK_STARTED** - When a long break begins
- **LONG_BREAK_COMPLETED** - When a long break naturally ends
- **LONG_BREAK_INTERRUPTED** - When a long break is manually skipped
- **SESSION_PAUSED** - When any session is paused
- **SESSION_RESUMED** - When a paused session is resumed

## Essential Metadata for Each Checkpoint
- Timestamp
- User ID
- Task ID (if applicable)
- Remaining time at checkpoint
- Round number
- Preset type (short/long)

## Implementation
```python
class CheckpointType(Enum):
    WORK_STARTED = "WORK_STARTED"
    WORK_COMPLETED = "WORK_COMPLETED"
    WORK_INTERRUPTED = "WORK_INTERRUPTED"
    SHORT_BREAK_STARTED = "SHORT_BREAK_STARTED"
    SHORT_BREAK_COMPLETED = "SHORT_BREAK_COMPLETED"
    SHORT_BREAK_INTERRUPTED = "SHORT_BREAK_INTERRUPTED"
    LONG_BREAK_STARTED = "LONG_BREAK_STARTED"
    LONG_BREAK_COMPLETED = "LONG_BREAK_COMPLETED"
    LONG_BREAK_INTERRUPTED = "LONG_BREAK_INTERRUPTED"
    SESSION_PAUSED = "SESSION_PAUSED"
    SESSION_RESUMED = "SESSION_RESUMED"
```

## Use Case: Connection Longevity
One of the primary use cases for checkpoint states is to solve the connection longevity issue. When a user has the web app open for an extended period (e.g., 2+ hours) and is inactive, the connection should not be lost.

### Problem
Currently, if the web app is open for a long time without activity, the connection is lost, which disrupts the user experience.

### Solution
By storing checkpoint states in the database, the system can:
1. Periodically save the current timer state
2. Recover the state when a connection is re-established
3. Allow users to resume their session exactly where they left off

This ensures that even if a user is away from their computer during a work session, break, or long break, they can return and continue using the app normally without losing their progress.

## Database Strategy
The checkpoint states will be stored in the database with the following structure:
- Timestamp (when the checkpoint was created)
- User ID (to associate the checkpoint with a specific user)
- Task ID (if applicable, to associate the checkpoint with a specific task)
- Remaining time (the time left in the current session)
- Round number (the current round in the Pomodoro cycle)
- Preset type (short/long, to determine the appropriate durations)
- Session type (work, short break, or long break)
- State type (one of the checkpoint types defined above)

This data will enable the system to accurately reconstruct the timer state when needed, providing a seamless experience across disconnections and device changes.