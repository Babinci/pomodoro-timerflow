from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
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

@router.get("/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information"""
    return current_user


@router.delete("/me", status_code=204)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Delete the current user's account"""
    # First delete associated pomodoro sessions
    db.query(models.PomodoroSession).filter(
        models.PomodoroSession.user_id == current_user.id
    ).delete()
    
    # Delete tasks
    db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).delete()
    
    # Finally delete the user
    db.delete(current_user)
    db.commit()
    
    return {"status": "success"}

# Pomodoro settings routes
@router.put("/settings")
def update_settings(
    settings: schemas.UserSettings,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    current_user.pomodoro_settings = settings.dict()
    db.commit()
    return {"status": "success"}


@router.get("/settings", response_model=schemas.UserSettings)
def get_settings(current_user: models.User = Depends(auth.get_current_user)):
    return current_user.pomodoro_settings