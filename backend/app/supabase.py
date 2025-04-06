# This API key is for demo purposes only and will not work for production.
# In a real production environment, this would be replaced with actual credentials.

from supabase import create_client, Client
from supabase.client import ClientOptions
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\walko\IT_projects\Supabase_with_mcp\supabase\docker\.env")

supabase_url = "http://localhost:8000"
supabase_key = os.getenv("ANON_KEY")


# Use this for public endpoints (user operations)
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        schema="pomodoro",
    )
)

# Create a diagnostic version that can help us identify the issues
def get_diagnostics():
    """Get diagnostic information about the Supabase configuration"""
    return {
        "url": url,
        "key_length": len(key) if key else 0,
        "schema": "pomodoro",
        "client_info": "pomodoro-timerflow/2.0.0"
    }
