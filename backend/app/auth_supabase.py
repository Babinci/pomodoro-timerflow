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
    """Authenticate a user with custom authentication"""
    try:
        # Get the user from the database
        response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
        
        if not response.data or len(response.data) == 0:
            return None
            
        user = response.data[0]
        
        # Verify the password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        if not pwd_context.verify(password, user["hashed_password"]):
            return None
            
        # Create a custom response object
        from types import SimpleNamespace
        
        # Create token for the user
        from datetime import datetime, timedelta
        import jwt
        
        # Use a secure secret key (should be in environment variables)
        SECRET_KEY = "your-secret-key"  # In production, use env variable
        ALGORITHM = "HS256"
        
        # Create JWT token
        token_data = {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=30)}
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        
        # Create a session object
        session = SimpleNamespace()
        session.access_token = access_token
        session.refresh_token = None
        session.expires_at = (datetime.utcnow() + timedelta(minutes=30)).isoformat()
        
        # Create a user object
        user_obj = SimpleNamespace()
        user_obj.id = user["id"]
        user_obj.email = user["email"]
        user_obj.user_metadata = {"username": user["username"]}
        
        # Create a response object
        auth_response = SimpleNamespace()
        auth_response.user = user_obj
        auth_response.session = session
        
        return auth_response
    except Exception as e:
        # Log the error
        print(f"Authentication error: {str(e)}")
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify the token and get the user data
        user_data = await verify_token(token)
        
        # Get the full user data from the database
        response = supabase.table("users").select("*").eq("id", user_data["user_id"]).limit(1).execute()
        
        if not response.data or len(response.data) == 0:
            raise credentials_exception
            
        user = response.data[0]
        
        # Create a user data object
        user_obj = UserData(
            id=user["id"],
            email=user["email"],
            user_metadata={"username": user["username"]}
        )
        
        return user_obj
    except HTTPException:
        raise
    except Exception as e:
        # Log the error
        print(f"Token validation error: {str(e)}")
        raise credentials_exception

async def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token"""
    try:
        # Decode the JWT token
        import jwt
        
        # Use a secure secret key (should be in environment variables)
        SECRET_KEY = "your-secret-key"  # In production, use env variable
        ALGORITHM = "HS256"
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token - missing email"
            )
            
        # Get the user from the database
        response = supabase.table("users").select("id").eq("email", email).limit(1).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
            
        return {
            "user_id": response.data[0]["id"],
            "email": email
        }
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
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
    """Create a new user directly in the database"""
    try:
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
        
        # Hash the password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)
        
        # Insert into users table
        db_response = supabase.table("users").insert({
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "pomodoro_settings": default_settings
        }).execute()
        
        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
            
        return db_response.data[0]
        
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
