# users_supabase.py
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas
from ..auth_supabase import get_current_user, create_user, get_user_from_db
from ..supabase import supabase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
@router.post("", response_model=schemas.User)  # Add this route to handle requests without trailing slash
async def register_user(user: schemas.UserCreate):
    """Create a new user account"""
    try:
        # Check if email exists in our database
        email_check = supabase.table("users").select("email").eq("email", user.email).execute()
        if email_check.data and len(email_check.data) > 0:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Check if username exists
        username_check = supabase.table("users").select("username").eq("username", user.username).execute()
        if username_check.data and len(username_check.data) > 0:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create the user in Supabase Auth and our database
        new_user = await create_user(
            email=user.email,
            password=user.password,
            username=user.username
        )
        
        # Retrieve the user from our database to get the standard format
        user_data = await get_user_from_db(new_user.id)
        if not user_data:
            raise HTTPException(status_code=500, detail="User created but could not be retrieved")
        
        return user_data
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    try:
        # Get full user data from our database
        user_data = await get_user_from_db(current_user.id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found in database")
        return user_data
    except Exception as e:
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
        
        # Delete from our users table
        supabase.table("users").delete().eq("id", current_user.id).execute()
        
        # Delete from Supabase Auth 
        # Note: This would typically require admin credentials
        # supabase.auth.admin.delete_user(current_user.id)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Account deletion failed: {str(e)}")

# Pomodoro settings routes
@router.put("/settings")
async def update_settings(
    settings: schemas.UserSettings,
    current_user = Depends(get_current_user)
):
    try:
        response = supabase.table("users").update({
            "pomodoro_settings": settings.dict()
        }).eq("id", current_user.id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settings update failed: {str(e)}")

@router.get("/settings", response_model=schemas.UserSettings)
async def get_settings(current_user = Depends(get_current_user)):
    try:
        response = supabase.table("users").select("pomodoro_settings").eq("id", current_user.id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
            
        return response.data[0]["pomodoro_settings"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve settings: {str(e)}")
