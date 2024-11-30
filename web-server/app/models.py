from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    pomodoro_settings = Column(JSON, default={
        "short": {
            "work_duration": 25,
            "short_break": 5,
            "long_break": 15,
            "sessions_before_long_break": 4
        },
        "long": {
            "work_duration": 50,
            "short_break": 10,
            "long_break": 30,
            "sessions_before_long_break": 4
        }
    })
    
    tasks = relationship("Task", back_populates="user")
    sessions = relationship("PomodoroSession", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    estimated_pomodoros = Column(Integer)
    completed_pomodoros = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="tasks")
    sessions = relationship("PomodoroSession", back_populates="task")

class PomodoroSession(Base):
    __tablename__ = "pomodoro_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    session_type = Column(String)  # 'work', 'short_break', 'long_break'
    completed = Column(Boolean, default=False)
    current_session_number = Column(Integer)  # Track which session in the cycle (1-4)
    
    user = relationship("User", back_populates="sessions")
    task = relationship("Task", back_populates="sessions")