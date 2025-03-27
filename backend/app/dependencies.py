# dependencies.py
"""
Dependency injection for the FastAPI application.
Provides dependencies for Supabase client and error handling.
"""
from fastapi import Depends, HTTPException, status
from supabase import Client

from .supabase import supabase

def get_supabase_client():
    """Get the Supabase client instance.
    
    This dependency allows for easier testing and mocking
    of the Supabase client in unit tests.
    """
    return supabase

class SupabaseErrorHandler:
    """Error handler for Supabase operations.
    
    This class provides methods to handle common Supabase errors
    and convert them to appropriate FastAPI HTTPExceptions.
    """
    
    @staticmethod
    def handle_auth_error(error):
        """Handle authentication errors from Supabase."""
        error_message = str(error)
        
        if "Invalid login credentials" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        elif "Email not confirmed" in error_message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not confirmed"
            )
        elif "JWT expired" in error_message or "Token expired" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication error: {error_message}",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    @staticmethod
    def handle_database_error(error):
        """Handle database errors from Supabase."""
        error_message = str(error)
        
        if "duplicate key" in error_message:
            if "users_email_key" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already in use"
                )
            elif "users_username_key" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Duplicate key violation"
                )
        elif "violates foreign key constraint" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foreign key constraint violation"
            )
        elif "permission denied" in error_message:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied for this operation"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {error_message}"
            )
