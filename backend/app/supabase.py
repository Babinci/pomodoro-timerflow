url = "https://mysupabaseapi.cypher-arena.com/"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
import os
from supabase import create_client, Client
from supabase.client import ClientOptions

url: str =  url
key: str =  key
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        schema="pomodoro"
    )
)

