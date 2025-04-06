import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase.client import ClientOptions

# Load environment variables from the .env file
load_dotenv(r"C:\Users\walko\IT_projects\pomodoro-timerflow\.env")

# Supabase connection settings
supabase_url = "http://localhost:8000"
service_key = os.getenv("SERVICE_ROLE_KEY")
anon_key = os.getenv("ANON_KEY")

print(f"Supabase URL: {supabase_url}")
print(f"Service Key: {service_key[:10]}..." if service_key else "SERVICE_ROLE_KEY not found")
print(f"Anon Key: {anon_key[:10]}..." if anon_key else "ANON_KEY not found")

# Test 1: Basic connectivity test with public schema
print("\n=== Testing connection to public schema ===")
try:
    supabase_public = create_client(supabase_url, service_key)
    # Query a table in public schema (babcia was a test table in your original script)
    response = supabase_public.table("babcia").select("*").limit(1).execute()
    print(f"✓ Successfully connected to public schema: {response.data}")
except Exception as e:
    print(f"✗ Error connecting to public schema: {e}")

# Test 2: Test access to pomodoro schema with service role
print("\n=== Testing connection to pomodoro schema with SERVICE ROLE ===")
try:
    supabase_pomodoro = create_client(
        supabase_url,
        service_key,
        options=ClientOptions(schema="pomodoro")
    )
    
    # Try to list all tables in pomodoro schema
    print("Tables in pomodoro schema:")
    for table in ["profiles", "tasks", "pomodoro_sessions", "pomodoro_checkpoints"]:
        try:
            count_response = supabase_pomodoro.table(table).select("*", count="exact").limit(0).execute()
            row_count = count_response.count if hasattr(count_response, 'count') else 0
            print(f"  ✓ {table}: {row_count} rows")
        except Exception as e:
            print(f"  ✗ {table}: Error - {e}")
except Exception as e:
    print(f"✗ Error connecting to pomodoro schema: {e}")

# Test 3: Test anonymous access (this will likely fail due to RLS policies)
print("\n=== Testing connection with ANON KEY ===")
try:
    supabase_anon = create_client(
        supabase_url,
        anon_key,
        options=ClientOptions(schema="pomodoro")
    )
    
    # Try to access tasks table as anonymous user
    response = supabase_anon.table("tasks").select("*").limit(1).execute()
    print(f"✓ Anonymous access to tasks table works: {response.data}")
except Exception as e:
    print(f"✗ Anonymous access failed (expected if RLS is active): {e}")

# Test 4: Create a test profile (this will help test access)
print("\n=== Attempting to create a test profile ===")
try:
    # First check if a test user already exists in auth.users
    test_email = "test@example.com"
    
    # Generate a UUID for the user (normally this would come from auth.users)
    import uuid
    test_user_id = str(uuid.uuid4())
    
    # Create a profile in pomodoro.profiles
    profile_data = {
        "id": test_user_id,
        "username": "testuser",
        "pomodoro_settings": {
            "short": {
                "work_duration": 25,
                "short_break": 5,
                "long_break": 15,
                "sessions_before_long_break": 4
            },
            "long": {
                "work_duration": 50,
                "short_break": 10,
                "long_break": 30,
                "sessions_before_long_break": 4
            }
        }
    }
    
    response = supabase_pomodoro.table("profiles").insert(profile_data).execute()
    print(f"✓ Successfully created test profile: {response.data}")
    
    # Now try to create a test task
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": test_user_id,
        "estimated_pomodoros": 3,
        "is_active": True
    }
    
    response = supabase_pomodoro.table("tasks").insert(task_data).execute()
    print(f"✓ Successfully created test task: {response.data}")
    
except Exception as e:
    print(f"✗ Error creating test data: {e}")

print("\n=== Test Complete ===")