from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import SessionLocal
from . import models

def initialize_task_positions():
    """Initialize positions for existing tasks based on creation date"""
    db = SessionLocal()
    try:
        # Get all users
        users = db.query(models.User).all()
        
        for user in users:
            # Get all tasks for user ordered by creation date
            tasks = db.query(models.Task).filter(
                models.Task.user_id == user.id
            ).order_by(models.Task.created_at).all()
            
            # Update positions
            for i, task in enumerate(tasks):
                task.position = i + 1
                
        db.commit()
        print(f"Successfully initialized positions for tasks")
    except Exception as e:
        db.rollback()
        print(f"Error initializing positions: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_task_positions() 