from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import asyncio
from .. import models, schemas, auth
from ..database import get_db
from ..ws_manager import manager

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # Find the highest position number for this user's tasks
    highest_position = db.query(func.max(models.Task.position)).filter(
        models.Task.user_id == current_user.id
    ).scalar() or 0
    
    # Create task with position = highest + 1
    db_task = models.Task(
        **task.dict(), 
        user_id=current_user.id,
        position=highest_position + 1
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # Return tasks ordered by position
    return db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).order_by(models.Task.position).all()


@router.put("/{task_id}")
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


@router.delete("/{task_id}")
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

    # Get the position of the task to be deleted
    deleted_position = db_task.position

    # Delete associated sessions first
    db.query(models.PomodoroSession).filter(
        models.PomodoroSession.task_id == task_id
    ).delete()

    # Delete the task
    db.delete(db_task)
    
    # Update positions of remaining tasks
    db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.position > deleted_position
    ).update(
        {models.Task.position: models.Task.position - 1},
        synchronize_session=False
    )
    
    db.commit()
    return {"status": "success"}


@router.put("/order")
def update_tasks_order(
    task_order: schemas.TaskOrder,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Update the order of tasks for a user"""
    # Verify all tasks belong to the current user
    user_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.id.in_(task_order.task_ids)
    ).all()
    
    # Check if all requested task IDs belong to the user
    if len(user_tasks) != len(task_order.task_ids):
        raise HTTPException(status_code=400, detail="Invalid task IDs")
    
    # Create a mapping of task IDs to their tasks
    task_map = {task.id: task for task in user_tasks}
    
    # Update positions
    for index, task_id in enumerate(task_order.task_ids):
        task = task_map.get(task_id)
        if task:
            task.position = index + 1
    
    db.commit()
    
    # Broadcast the order change to all connected clients for this user
    asyncio.create_task(
        manager.broadcast_to_user(
            str(current_user.id),
            {
                "type": "task_order_updated",
                "data": {"task_ids": task_order.task_ids}
            }
        )
    )
    
    return {"status": "success"}