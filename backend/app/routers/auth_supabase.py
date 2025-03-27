# auth_supabase.py (router)
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .. import schemas
from ..auth_supabase import authenticate_user, get_current_user, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..supabase import supabase

router = APIRouter(tags=["authentication"])

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
        # For now, we don't have refresh tokens implemented
        # In a production environment, you would validate the refresh token
        # and issue a new access token
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Token refresh not implemented in this version",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
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
        supabase.auth.sign_out()
        response.delete_cookie(key="refreshToken")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )
