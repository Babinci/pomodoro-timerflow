# tasks_supabase.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import asyncio
from datetime import datetime
from .. import schemas
from ..auth_supabase import get_current_user
from ..supabase import supabase
from ..ws_manager import manager

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    current_user = Depends(get_current_user),
):
    try:
        # Find the highest position number for this user's tasks
        position_query = supabase.table("tasks") \
            .select("position") \
            .eq("user_id", current_user.id) \
            .order("position", desc=True) \
            .limit(1) \
            .execute()
            
        highest_position = 0
        if position_query.data and len(position_query.data) > 0:
            highest_position = position_query.data[0]["position"]
        
        # Create task with position = highest + 1
        task_data = {
            "title": task.title,
            "description": task.description,
            "user_id": current_user.id,
            "estimated_pomodoros": task.estimated_pomodoros,
            "completed_pomodoros": 0,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "position": highest_position + 1
        }
        
        response = supabase.table("tasks").insert(task_data).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create task")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@router.get("/", response_model=List[schemas.Task])
async def get_tasks(
    current_user = Depends(get_current_user),
):
    try:
        # Return tasks ordered by position
        response = supabase.table("tasks") \
            .select("*") \
            .eq("user_id", current_user.id) \
            .order("position") \
            .execute()
            
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")

@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task: schemas.TaskCreate,
    current_user = Depends(get_current_user),
):
    try:
        # First, verify task belongs to user
        task_check = supabase.table("tasks") \
            .select("id") \
            .eq("id", task_id) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not task_check.data or len(task_check.data) == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update the task
        task_data = {
            "title": task.title,
            "description": task.description,
            "estimated_pomodoros": task.estimated_pomodoros
        }
        
        response = supabase.table("tasks") \
            .update(task_data) \
            .eq("id", task_id) \
            .execute()
            
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to update task")
            
        return response.data[0]
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
):
    try:
        # First, verify task belongs to user and get its position
        task_query = supabase.table("tasks") \
            .select("id, position") \
            .eq("id", task_id) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not task_query.data or len(task_query.data) == 0:
            raise HTTPException(status_code=404, detail="Task not found")
            
        deleted_position = task_query.data[0]["position"]
        
        # Delete associated pomodoro sessions
        supabase.table("pomodoro_sessions") \
            .delete() \
            .eq("task_id", task_id) \
            .execute()
            
        # Delete associated checkpoints
        supabase.table("pomodoro_checkpoints") \
            .delete() \
            .eq("task_id", task_id) \
            .execute()
            
        # Delete the task
        supabase.table("tasks") \
            .delete() \
            .eq("id", task_id) \
            .execute()
            
        # Update positions of remaining tasks
        tasks_to_update = supabase.table("tasks") \
            .select("id, position") \
            .eq("user_id", current_user.id) \
            .gt("position", deleted_position) \
            .execute()
            
        # Update each task's position individually
        # (This could be optimized with a batch update in PostgreSQL)
        for task in tasks_to_update.data:
            supabase.table("tasks") \
                .update({"position": task["position"] - 1}) \
                .eq("id", task["id"]) \
                .execute()
            
        return {"status": "success"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

@router.put("/order")
async def update_tasks_order(
    task_order: schemas.TaskOrder,
    current_user = Depends(get_current_user),
):
    """Update the order of tasks for a user"""
    # Validate input
    if not task_order.task_ids:
        raise HTTPException(status_code=400, detail="Task IDs list cannot be empty")
    
    try:
        # Get all user tasks
        user_tasks_query = supabase.table("tasks") \
            .select("id") \
            .eq("user_id", current_user.id) \
            .in_("id", task_order.task_ids) \
            .execute()
            
        user_tasks = user_tasks_query.data
        
        # Check if all requested task IDs belong to the user
        if len(user_tasks) != len(task_order.task_ids):
            raise HTTPException(status_code=400, detail="Invalid task IDs")
        
        # Check for duplicate task IDs
        if len(task_order.task_ids) != len(set(task_order.task_ids)):
            raise HTTPException(status_code=400, detail="Duplicate task IDs found")
        
        # Update each task's position individually
        for index, task_id in enumerate(task_order.task_ids):
            supabase.table("tasks") \
                .update({"position": index + 1}) \
                .eq("id", task_id) \
                .execute()
        
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
        
        # Return updated task order for verification
        return {
            "status": "success",
            "data": {
                "task_ids": task_order.task_ids,
                "updated_count": len(user_tasks)
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task order: {str(e)}")
