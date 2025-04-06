"""
Supabase client configuration for the Pomodoro TimerFlow application.
This module establishes the connection to Supabase services.
"""
from supabase import create_client, Client
from supabase.client import ClientOptions
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Try to load from .env file if it exists (for local development)
try:
    load_dotenv()
except Exception as e:
    logger.warning(f"Unable to load .env file: {str(e)}")

# Get environment variables
# First try direct environment variables (for Docker/production)
supabase_url = os.getenv("SUPABASE_URL", "http://localhost:8000")
# Use service role key for backend operations
supabase_key = os.getenv("SERVICE_ROLE_KEY")
# Anon key for client-facing operations
anon_key = os.getenv("ANON_KEY")

if not supabase_key:
    logger.warning("SERVICE_ROLE_KEY not found in environment variables")

# Create service role client for administrative operations
try:
    supabase: Client = create_client(
        supabase_url,
        supabase_key,
        options=ClientOptions(
            schema="pomodoro",
        )
    )
    logger.info(f"Supabase client initialized with URL: {supabase_url}")
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    # Create a placeholder client to avoid errors at import time
    # The actual connection will fail later when used
    supabase = None

# Convenience function to get a client with anon privileges
def get_anon_client():
    """Get a Supabase client with anonymous role privileges"""
    return create_client(
        supabase_url,
        anon_key,
        options=ClientOptions(
            schema="pomodoro",
        )
    )

# Create a diagnostic function that can help identify issues
def get_diagnostics():
    """Get diagnostic information about the Supabase configuration"""
    return {
        "url": supabase_url,
        "service_key_length": len(supabase_key) if supabase_key else 0,
        "anon_key_length": len(anon_key) if anon_key else 0,
        "schema": "pomodoro",
        "client_info": "pomodoro-timerflow/2.0.0"
    }
