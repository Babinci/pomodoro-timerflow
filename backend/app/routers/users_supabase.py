# users_supabase.py
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from .. import schemas
from ..auth_supabase import get_current_user, create_user, get_user_from_db
from ..supabase import supabase, get_anon_client

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.User)
@router.post("", response_model=schemas.User)  # Add this route to handle requests without trailing slash
async def register_user(user: schemas.UserCreate):
    """Create a new user account"""
    try:
        # Check if email exists using admin client
        auth_response = supabase.auth.admin.list_users({
            "filter": {
                "email": user.email
            }
        })
        
        if auth_response and auth_response.users and len(auth_response.users) > 0:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create the user in Supabase Auth
        user_response = await create_user(
            email=user.email,
            password=user.password,
            username=user.username
        )
        
        # The profile should be created automatically by the database trigger
        # Retrieve the user's profile to return
        profile = await get_user_from_db(user_response.id)
        if not profile:
            raise HTTPException(status_code=500, detail="User created but profile not found")
        
        # Return profile data in the format expected by the frontend
        return {
            "id": profile["id"],
            "email": user.email,
            "username": profile["username"],
            "pomodoro_settings": profile["pomodoro_settings"]
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    try:
        # Get full user data from our database
        profile = await get_user_from_db(current_user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Combine auth user data with profile data
        return {
            "id": current_user.id,
            "email": current_user.email,
            "username": profile["username"],
            "pomodoro_settings": profile["pomodoro_settings"]
        }
    except Exception as e:
        logger.error(f"Error retrieving user info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user information: {str(e)}")

@router.delete("/me", status_code=204)
async def delete_current_user(current_user = Depends(get_current_user)):
    """Delete the current user's account"""
    try:
        # Delete associated pomodoro sessions
        supabase.table("pomodoro_sessions").delete().eq("user_id", current_user.id).execute()
        
        # Delete pomodoro checkpoints
        supabase.table("pomodoro_checkpoints").delete().eq("user_id", current_user.id).execute()
        
        # Delete tasks
        supabase.table("tasks").delete().eq("user_id", current_user.id).execute()
        
        # Delete profile
        supabase.table("profiles").delete().eq("id", current_user.id).execute()
        
        # Delete the user from Supabase Auth 
        supabase.auth.admin.delete_user(current_user.id)
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Account deletion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Account deletion failed: {str(e)}")

# Pomodoro settings routes
@router.put("/settings")
async def update_settings(
    settings: schemas.UserSettings,
    current_user = Depends(get_current_user)
):
    try:
        response = supabase.table("profiles").update({
            "pomodoro_settings": settings.dict()
        }).eq("id", current_user.id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
            
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Settings update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Settings update failed: {str(e)}")

@router.get("/settings", response_model=schemas.UserSettings)
async def get_settings(current_user = Depends(get_current_user)):
    try:
        response = supabase.table("profiles").select("pomodoro_settings").eq("id", current_user.id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
            
        return response.data[0]["pomodoro_settings"]
    except Exception as e:
        logger.error(f"Settings retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve settings: {str(e)}")
