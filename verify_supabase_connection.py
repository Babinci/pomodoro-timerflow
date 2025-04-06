"""
Verify Supabase Connection Script

This script tests the Supabase connection configuration by importing the
modified supabase.py file and attempting to connect to the database.
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.append(backend_dir)

# Try to load .env file
try:
    load_dotenv()
    print("Loaded environment variables from .env file")
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# Import the supabase.py file
try:
    from app.supabase import supabase, get_anon_client, get_diagnostics
    
    # Print diagnostic information
    diagnostics = get_diagnostics()
    print("\nSUPABASE CONNECTION DIAGNOSTICS:")
    print(f"URL: {diagnostics['url']}")
    print(f"Service Key Length: {diagnostics['service_key_length']}")
    print(f"Anon Key Length: {diagnostics['anon_key_length']}")
    print(f"Schema: {diagnostics['schema']}")
    
    # Check if environment variables are set
    print("\nENVIRONMENT VARIABLES:")
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SERVICE_ROLE_KEY")
    anon_key = os.getenv("ANON_KEY")
    
    print(f"SUPABASE_URL: {'SET' if supabase_url else 'NOT SET'}")
    print(f"SERVICE_ROLE_KEY: {'SET' if service_role_key else 'NOT SET'}")
    print(f"ANON_KEY: {'SET' if anon_key else 'NOT SET'}")
    
    # Test the service role connection
    print("\nTESTING SERVICE ROLE CONNECTION:")
    if supabase:
        try:
            # Try to query the database
            response = supabase.table("profiles").select("count", count="exact").limit(1).execute()
            print(f"Connection successful! Found {response.count if hasattr(response, 'count') else 0} profiles.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
    else:
        print("Supabase client not initialized.")
    
    # Test the anon connection
    print("\nTESTING ANON CLIENT CONNECTION:")
    try:
        anon_client = get_anon_client()
        response = anon_client.table("profiles").select("count", count="exact").limit(1).execute()
        print(f"Anon connection successful! Found {response.count if hasattr(response, 'count') else 0} profiles.")
    except Exception as e:
        print(f"Error connecting with anon client: {e}")
    
except ImportError as e:
    print(f"Error importing Supabase modules: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

print("\nVerification completed.")
