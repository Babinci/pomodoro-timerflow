# This API key is for demo purposes only and will not work for production.
# In a real production environment, this would be replaced with actual credentials.
url = "https://mysupabaseapi.cypher-arena.com/"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
import os
from supabase import create_client, Client
from supabase.client import ClientOptions

# Override from environment if available
url = os.getenv("SUPABASE_URL", url)
key = os.getenv("SUPABASE_KEY", key)

# Use this for public endpoints (user operations)
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        schema="pomodoro",
        headers={"x-client-info": "pomodoro-timerflow/2.0.0"}
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
