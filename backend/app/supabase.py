# This API key is for demo purposes only and will not work for production.
# In a real production environment, this would be replaced with actual credentials.

from supabase import create_client, Client
from supabase.client import ClientOptions
import os
from dotenv import load_dotenv

# First try to load from project root .env file
load_dotenv()

# Fallback to specific location if needed
if not os.getenv("ANON_KEY"):
    try:
        load_dotenv(r"C:\Users\walko\IT_projects\Supabase_with_mcp\supabase\docker\.env")
    except:
        pass

# For local development (localhost:8000) with Supabase
supabase_url = os.getenv("SUPABASE_URL", "http://localhost:8000")

# This is a demo key for local development only
supabase_key = os.getenv("ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0")

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url,
    supabase_key,
    options=ClientOptions(
        schema="pomodoro",
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
