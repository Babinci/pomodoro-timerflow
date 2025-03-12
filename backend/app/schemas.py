from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime

from enum import Enum

class CheckpointType(str, Enum):
    WORK_STARTED = "work_started"
    WORK_COMPLETED = "work_completed"
    WORK_INTERRUPTED = "work_interrupted"
    SHORT_BREAK_STARTED = "short_break_started"
    SHORT_BREAK_COMPLETED = "short_break_completed"
    SHORT_BREAK_INTERRUPTED = "short_break_interrupted"
    LONG_BREAK_STARTED = "long_break_started"
    LONG_BREAK_COMPLETED = "long_break_completed"
    LONG_BREAK_INTERRUPTED = "long_break_interrupted"
    SESSION_PAUSED = "session_paused"
    SESSION_RESUMED = "session_resumed"

class SessionType(str, Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

class PresetType(str, Enum):
    SHORT = "short"
    LONG = "long"


class PomodoroSettingsBase(BaseModel):
    work_duration: float
    short_break: float
    long_break: float
    sessions_before_long_break: int = 4

class UserSettings(BaseModel):
    short: PomodoroSettingsBase
    long: PomodoroSettingsBase

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    pomodoro_settings: UserSettings

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_pomodoros: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int
    completed_pomodoros: int
    created_at: datetime
    completed_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PomodoroSessionBase(BaseModel):
    task_id: int
    session_type: str
    current_session_number: int

class PomodoroSessionCreate(PomodoroSessionBase):
    pass

class PomodoroSession(PomodoroSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    completed: bool

    class Config:
        from_attributes = True

class TaskOrder(BaseModel):
    task_ids: List[int]

class WSMessage(BaseModel):
    type: str
    data: dict