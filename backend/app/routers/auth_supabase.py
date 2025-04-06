# auth_supabase.py (router)
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import logging
from .. import schemas
from ..auth_supabase import authenticate_user, get_current_user, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES, create_user
from ..supabase import get_anon_client

router = APIRouter(tags=["authentication"])
logger = logging.getLogger(__name__)

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # Validate input is not empty
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    auth_response = await authenticate_user(form_data.username, form_data.password)
    if not auth_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return the Supabase session tokens
    session = auth_response.session
    return {
        "access_token": session.access_token,
        "token_type": "bearer",
        "refresh_token": session.refresh_token,
        "expires_at": session.expires_at
    }

@router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    """Refresh an expired access token"""
    try:
        # Create a client with the anon key
        auth_client = get_anon_client()
        
        # Use Supabase's refresh token endpoint
        response = auth_client.auth.refresh_session(refresh_token)
        
        if not response or not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        session = response.session
        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "refresh_token": session.refresh_token,
            "expires_at": session.expires_at
        }
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/verify-token")
async def verify_token_endpoint(current_user = Depends(get_current_user)):
    """Verify if the provided token is valid"""
    return {"valid": True, "user_id": current_user.id}

@router.post("/logout")
async def logout(response: Response):
    """Log the user out by invalidating the session"""
    try:
        auth_client = get_anon_client()
        auth_client.auth.sign_out()
        response.delete_cookie(key="refreshToken")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@router.post("/signup")
async def signup(user_data: schemas.UserCreate):
    """Register a new user"""
    try:
        # Use the auth_supabase implementation which uses admin.create_user with SERVICE_ROLE_KEY
        # This bypasses the email confirmation requirement
        user = await create_user(
            email=user_data.email,
            password=user_data.password,
            username=user_data.username
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register user"
            )
            
        # Return user data without sensitive information
        return {
            "id": user.id,
            "email": user.email,
            "username": user_data.username,
            "confirmed": True  # Will be true since we use email_confirm=True
        }
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to register user: {str(e)}"
        )
