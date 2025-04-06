# supabase.py
"""
Configuration for Supabase client
"""
from supabase import create_client, Client
from supabase.client import ClientOptions
import os
from dotenv import load_dotenv
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# For Docker networking, we need to use host.docker.internal instead of localhost
# This allows the container to connect to services on the host machine
supabase_url = os.getenv("SUPABASE_URL", "http://host.docker.internal:8000")

# Use the service role key for admin operations
supabase_key = os.getenv("SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU")

try:
    # Initialize Supabase client
    logger.info(f"Initializing Supabase client with URL: {supabase_url}")
    supabase: Client = create_client(
        supabase_url,
        supabase_key,
        options=ClientOptions(
            schema="pomodoro",
        )
    )
    logger.info("Supabase client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Supabase client: {str(e)}")
    # Create a placeholder client that will raise appropriate errors when used
    from types import SimpleNamespace
    supabase = SimpleNamespace()
    supabase.table = lambda _: SimpleNamespace(
        select=lambda *args: SimpleNamespace(
            execute=lambda: {"data": [], "error": f"Failed to connect to Supabase: {str(e)}"}
        )
    )

# Create a diagnostic version that can help us identify the issues
def get_diagnostics():
    """Get diagnostic information about the Supabase configuration"""
    return {
        "url": supabase_url,
        "key_length": len(supabase_key) if supabase_key else 0,
        "schema": "pomodoro",
        "client_info": "pomodoro-timerflow/2.0.0"
    }
