from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime

class PomodoroSettingsBase(BaseModel):
    work_duration: int
    short_break: int
    long_break: int
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

class WSMessage(BaseModel):
    type: str
    data: dict