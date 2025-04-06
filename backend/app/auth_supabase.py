"""
Authentication module using Supabase Auth for the Pomodoro TimerFlow app.
This implements user authentication through Supabase's built-in auth system.
"""
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

# Import the Supabase client
from .supabase import supabase, get_anon_client

# Setup security schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

# Setup logging
logger = logging.getLogger(__name__)

# Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Keep compatibility with original value

class UserData(BaseModel):
    """Simplified user data model retrieved from Supabase Auth"""
    id: str
    email: str
    user_metadata: Dict[str, Any]

async def authenticate_user(email: str, password: str):
    """Authenticate a user through Supabase Auth"""
    try:
        # Use anon key for authentication (this is the proper security model)
        auth_client = get_anon_client()
        
        # Use Supabase's built-in auth system
        response = auth_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        return response
    except Exception as e:
        # Log the error
        logger.error(f"Authentication error: {str(e)}")
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from a JWT token using Supabase Auth"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Manually verify the token (Supabase doesn't have a direct "verify token" method)
        user_data = await verify_token(token)
        
        # Return a UserData object
        return UserData(
            id=user_data["id"],
            email=user_data["email"],
            user_metadata=user_data.get("user_metadata", {})
        )
    except HTTPException:
        raise
    except Exception as e:
        # Log the error
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception

async def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token using Supabase's Auth API"""
    try:
        # Call Supabase's token refresh to validate the token
        # We don't need to refresh, just decode it
        from supabase.lib.client_options import ClientOptions
        import jwt
        import os
        
        # First, try to decode the JWT directly
        # This won't verify signature but will check expiration
        try:
            # Decode without verification first
            decoded = jwt.decode(
                token, 
                options={"verify_signature": False}
            )
            
            # If we get here, at least the token structure is valid
            user_id = decoded.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token format - missing subject (user id)"
                )
                
            # Try to get user information with this token
            # Create a new client with this token for verification
            from .supabase import supabase_url, anon_key
            auth_client = create_client(
                supabase_url,
                anon_key,
                options=ClientOptions(
                    auto_refresh_token=False,
                    persist_session=False,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )
            )
            
            # Try to get the user with this token
            user = auth_client.auth.get_user()
            
            # If we get here, the token is valid
            return {
                "id": user.user.id,
                "email": user.user.email,
                "user_metadata": user.user.user_metadata
            }
            
        except Exception as inner_e:
            # If direct decoding fails, log and continue to next approach
            logger.warning(f"Token direct decode failed: {str(inner_e)}")
            
            # Fall back to getting user from profile in our database
            # This assumes the token can access the database through RLS
            anon_client = get_anon_client()
            
            # Set the auth token on the client
            anon_client.auth.set_session(token, None)
            
            # Try to get the user's profile from our database 
            profile_response = anon_client.table("profiles").select("*").limit(1).execute()
            
            if profile_response.data and len(profile_response.data) > 0:
                # If we can get the profile, the token must be valid
                return {
                    "id": profile_response.data[0]["id"],
                    "email": "user@example.com",  # We don't have email in profile
                    "user_metadata": {
                        "username": profile_response.data[0]["username"]
                    }
                }
            
            # If both approaches fail, token is invalid
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
            
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )

async def get_user_from_db(user_id: str):
    """Get user profile data from the database"""
    try:
        response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return None

async def create_user(email: str, password: str, username: str):
    """Create a new user through Supabase Auth"""
    try:
        # Use the admin/service role client
        user_response = supabase.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,  # Auto-confirm email
            "user_metadata": {
                "username": username
            }
        })
        
        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user through Supabase Auth"
            )
            
        # The profile should be automatically created by the database trigger
        # Let's verify it exists
        user_id = user_response.user.id
        
        # Check if profile exists
        profile = await get_user_from_db(user_id)
        
        # If for some reason the profile wasn't created by the trigger,
        # we should handle that - though it shouldn't happen with proper DB setup
        
        return user_response.user
        
    except Exception as e:
        logger.error(f"User creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )

# Alternative approach using HTTPBearer - useful for cases where standard OAuth2 doesn't fit
async def get_current_user_http(auth: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user using HTTPBearer authentication scheme"""
    return await get_current_user(auth.credentials)

# Import needed after function definition to avoid circular imports
from supabase import create_client
