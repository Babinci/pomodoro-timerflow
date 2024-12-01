from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import json

from . import models, schemas, auth
from .database import engine, get_db
from .ws_manager import manager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


# Auth routes
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=auth.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Task routes
@app.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# Pomodoro settings routes
@app.put("/users/settings")
def update_settings(
    settings: schemas.UserSettings,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    current_user.pomodoro_settings = settings.dict()
    db.commit()
    return {"status": "success"}

@app.get("/users/settings", response_model=schemas.UserSettings)
def get_settings(current_user: models.User = Depends(auth.get_current_user)):
    return current_user.pomodoro_settings

# WebSocket connection for real-time timer sync
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data["type"] == "start_session":
                task_id = data["data"]["task_id"]
                session_type = data["data"]["session_type"]
                current_session = data["data"]["current_session_number"]
                
                # Create new session in DB
                db_session = models.PomodoroSession(
                    user_id=user_id,
                    task_id=task_id,
                    session_type=session_type,
                    current_session_number=current_session
                )
                db.add(db_session)
                db.commit()
                
                # Start session in WebSocket manager
                manager.start_session(user_id, {
                    "session_id": db_session.id,
                    "task_id": task_id,
                    "type": session_type,
                    "current_session": current_session
                })
                
                # Broadcast session start to all user's devices
                await manager.broadcast_to_user(user_id, {
                    "type": "session_started",
                    "data": {
                        "session_id": db_session.id,
                        "start_time": db_session.start_time.isoformat(),
                        "type": session_type
                    }
                })
            
            elif data["type"] == "end_session":
                session_id = data["data"]["session_id"]
                
                # Update session in DB
                db_session = db.query(models.PomodoroSession).filter(
                    models.PomodoroSession.id == session_id
                ).first()
                
                if db_session:
                    db_session.end_time = datetime.utcnow()
                    db_session.completed = True
                    
                    # If it was a work session, increment completed_pomodoros
                    if db_session.session_type == "work":
                        task = db.query(models.Task).filter(
                            models.Task.id == db_session.task_id
                        ).first()
                        if task:
                            task.completed_pomodoros += 1
                    
                    db.commit()
                
                # End session in WebSocket manager
                manager.end_session(user_id)
                
                # Broadcast session end
                await manager.broadcast_to_user(user_id, {
                    "type": "session_ended",
                    "data": {
                        "session_id": session_id,
                        "end_time": datetime.utcnow().isoformat()
                    }
                })
            
            elif data["type"] == "pause_session":
                # Broadcast pause to all user's devices
                await manager.broadcast_to_user(user_id, {
                    "type": "session_paused",
                    "data": {
                        "pause_time": datetime.utcnow().isoformat()
                    }
                })
            
            elif data["type"] == "resume_session":
                # Broadcast resume to all user's devices
                await manager.broadcast_to_user(user_id, {
                    "type": "session_resumed",
                    "data": {
                        "resume_time": datetime.utcnow().isoformat()
                    }
                })
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user_id)