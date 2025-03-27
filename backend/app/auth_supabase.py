# auth_supabase.py
"""
Authentication module using Supabase Auth for the Pomodoro TimerFlow app.
This replaces the custom JWT implementation with Supabase's built-in auth system.
"""
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Import the Supabase client
from .supabase import supabase

# Setup security schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

# Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Keep compatibility with original value

class UserData(BaseModel):
    """Simplified user data model retrieved from Supabase Auth"""
    id: str
    email: str
    user_metadata: Dict[str, Any]

async def authenticate_user(email: str, password: str):
    """Authenticate a user with Supabase Auth"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            return response
        return None
    except Exception as e:
        # Log the error
        print(f"Authentication error: {str(e)}")
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from a JWT token using Supabase Auth"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Set the session with the provided token
        response = supabase.auth.set_session(token, None)
        user = response.user
        
        if not user:
            raise credentials_exception
            
        # Get the full user data
        user_response = supabase.auth.get_user(token)
        
        # Create a user data object
        user_data = UserData(
            id=user.id,
            email=user.email,
            user_metadata=user.user_metadata
        )
        
        return user_data
    except Exception as e:
        # Log the error
        print(f"Token validation error: {str(e)}")
        raise credentials_exception

async def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token using Supabase Auth"""
    try:
        # Use get_user to verify the token
        response = supabase.auth.get_user(token)
        if response.user:
            return {
                "user_id": response.user.id,
                "email": response.user.email
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )

async def get_user_from_db(user_id: str):
    """Get user data from the database"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

async def create_user(email: str, password: str, username: str):
    """Create a new user with Supabase Auth and add to database"""
    try:
        # First, create the auth user
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        # Then add the user to our database table
        user_id = auth_response.user.id
        
        # Define default pomodoro settings
        default_settings = {
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
        }
        
        # Insert into our users table
        db_response = supabase.table("users").insert({
            "id": user_id,
            "email": email,
            "username": username,
            "pomodoro_settings": default_settings
        }).execute()
        
        return auth_response.user
        
    except Exception as e:
        print(f"User creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )

# Alternative approach using HTTPBearer - useful for cases where standard OAuth2 doesn't fit
async def get_current_user_http(auth: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user using HTTPBearer authentication scheme"""
    return await get_current_user(auth.credentials)
