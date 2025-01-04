# main.py
from fastapi import (
    Query,
    FastAPI,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
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
from typing import Optional
from jose import JWTError

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


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Validate input is not empty
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

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


@app.get("/verify-token")
async def verify_token(current_user: models.User = Depends(auth.get_current_user)):
    """Verify if the provided token is valid"""
    return {"valid": True, "user_id": current_user.id}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username exists
    db_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=auth.get_password_hash(user.password),
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
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == current_user.id)
        .first()
    )
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete associated sessions first
    db.query(models.PomodoroSession).filter(
        models.PomodoroSession.task_id == task_id
    ).delete()

    # Then delete the task
    db.delete(db_task)
    db.commit()
    return {"status": "success"}


# Pomodoro settings routes
@app.put("/users/settings")
def update_settings(
    settings: schemas.UserSettings,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    current_user.pomodoro_settings = settings.dict()
    db.commit()
    return {"status": "success"}


@app.get("/users/settings", response_model=schemas.UserSettings)
def get_settings(current_user: models.User = Depends(auth.get_current_user)):
    return current_user.pomodoro_settings


@app.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None),
    db: Session = Depends(get_db)
):
    if not token:
        await websocket.close()
        return

    try:
        # Verify token and get user
        payload = auth.verify_token(token)
        email = payload.get("sub")
        if not email:
            await websocket.close()
            return
              
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            await websocket.close()
            return
          
        user_id = str(user.id)
        
        # Set the database session for the manager
        manager.db = db
        
        await manager.connect(websocket, user_id)
          
        while True:
            try:
                data = await websocket.receive_json()
                  
                if data["type"] == "start":
                    # Start new timer session
                    manager.start_timer(
                        user_id=user_id,
                        task_id=data["task_id"],
                        session_type=data["session_type"],
                        duration=data["duration"],
                        preset_type=data.get("preset_type", "short"),
                        user_settings=user.pomodoro_settings  # Pass user's settings
                    )
                    await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "stop":
                    manager.stop_timer(user_id)
                    await manager.broadcast_to_user(user_id, {"type": "timer_stopped"})
                  
                elif data["type"] == "pause":
                    if user_id in manager.timer_states:
                        manager.timer_states[user_id].pause()
                        await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "resume":
                    if user_id in manager.timer_states:
                        manager.timer_states[user_id].resume()
                        await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "sync_request":
                    await manager.sync_timer_state(user_id)
                    
                elif data["type"] == "skip_to_next":
                    if user_id in manager.timer_states:
                        manager.skip_to_next(user_id)
                        await manager.sync_timer_state(user_id)

            except WebSocketDisconnect:
                await manager.disconnect(websocket, user_id)
                return
                  
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()
    finally:
        manager.db = None  # Clear the database session