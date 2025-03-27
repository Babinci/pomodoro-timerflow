# pomodoro_session_supabase.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from .. import schemas
from ..auth_supabase import get_current_user
from ..supabase import supabase

router = APIRouter(prefix="/pomodoro", tags=["pomodoro"])

@router.post("/sessions", response_model=schemas.PomodoroSession)
async def create_pomodoro_session(
    session: schemas.PomodoroSessionCreate,
    current_user = Depends(get_current_user)
):
    """Create a new pomodoro session record"""
    try:
        # Verify the task belongs to the user
        task_check = supabase.table("tasks") \
            .select("id") \
            .eq("id", session.task_id) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not task_check.data or len(task_check.data) == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Create the session
        session_data = {
            "user_id": current_user.id,
            "task_id": session.task_id,
            "session_type": session.session_type,
            "current_session_number": session.current_session_number,
            "start_time": datetime.utcnow().isoformat(),
            "completed": False
        }
        
        response = supabase.table("pomodoro_sessions").insert(session_data).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create session")
            
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

@router.put("/sessions/{session_id}/complete")
async def complete_pomodoro_session(
    session_id: int,
    current_user = Depends(get_current_user)
):
    """Mark a pomodoro session as completed"""
    try:
        # Verify the session belongs to the user
        session_check = supabase.table("pomodoro_sessions") \
            .select("id, task_id, session_type") \
            .eq("id", session_id) \
            .eq("user_id", current_user.id) \
            .execute()
            
        if not session_check.data or len(session_check.data) == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = session_check.data[0]
        task_id = session_data["task_id"]
        session_type = session_data["session_type"]
        
        # Update the session to mark as completed
        update_data = {
            "completed": True,
            "end_time": datetime.utcnow().isoformat()
        }
        
        response = supabase.table("pomodoro_sessions") \
            .update(update_data) \
            .eq("id", session_id) \
            .execute()
            
        # If it was a work session, increment the task's completed_pomodoros count
        if session_type == "work":
            task_update = supabase.table("tasks") \
                .select("completed_pomodoros") \
                .eq("id", task_id) \
                .execute()
                
            if task_update.data and len(task_update.data) > 0:
                current_count = task_update.data[0]["completed_pomodoros"] or 0
                
                supabase.table("tasks") \
                    .update({"completed_pomodoros": current_count + 1}) \
                    .eq("id", task_id) \
                    .execute()
        
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete session: {str(e)}")

@router.get("/sessions", response_model=List[schemas.PomodoroSession])
async def get_user_sessions(
    current_user = Depends(get_current_user)
):
    """Get all pomodoro sessions for the current user"""
    try:
        response = supabase.table("pomodoro_sessions") \
            .select("*") \
            .eq("user_id", current_user.id) \
            .order("start_time", desc=True) \
            .execute()
            
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve sessions: {str(e)}")

@router.post("/checkpoints")
async def create_pomodoro_checkpoint(
    checkpoint_data: dict,
    current_user = Depends(get_current_user)
):
    """Create a checkpoint for the current timer state"""
    try:
        # Validate required fields
        required_fields = ["checkpoint_type", "remaining_time", "session_type", "round_number", "preset_type"]
        for field in required_fields:
            if field not in checkpoint_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Prepare checkpoint data
        checkpoint = {
            "user_id": current_user.id,
            "task_id": checkpoint_data.get("task_id"),  # Optional
            "checkpoint_type": checkpoint_data["checkpoint_type"],
            "timestamp": datetime.utcnow().isoformat(),
            "remaining_time": checkpoint_data["remaining_time"],
            "session_type": checkpoint_data["session_type"],
            "is_paused": checkpoint_data.get("is_paused", False),
            "round_number": checkpoint_data["round_number"],
            "preset_type": checkpoint_data["preset_type"],
            "last_active": datetime.utcnow().isoformat()
        }
        
        # Insert the checkpoint
        response = supabase.table("pomodoro_checkpoints").insert(checkpoint).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create checkpoint")
            
        return {"status": "success", "checkpoint_id": response.data[0]["id"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create checkpoint: {str(e)}")

@router.get("/checkpoints/latest")
async def get_latest_checkpoint(
    current_user = Depends(get_current_user)
):
    """Get the latest checkpoint for the current user"""
    try:
        response = supabase.table("pomodoro_checkpoints") \
            .select("*") \
            .eq("user_id", current_user.id) \
            .order("timestamp", desc=True) \
            .limit(1) \
            .execute()
            
        if not response.data or len(response.data) == 0:
            return {"status": "no_checkpoint_found"}
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve latest checkpoint: {str(e)}")
