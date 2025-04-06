import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase.client import ClientOptions

# Load first .env file and store its values
load_dotenv(r"C:\Users\walko\IT_projects\Supabase_with_mcp\supabase\docker\.env")
docker_anon_key = os.getenv("ANON_KEY")
docker_service_role_key = os.getenv("SERVICE_ROLE_KEY")

# Load the second .env file temporarily without affecting current environment
from dotenv import dotenv_values
local_env = dotenv_values(".env")
local_anon_key = local_env.get("ANON_KEY")
local_service_role_key = local_env.get("SERVICE_ROLE_KEY")

# Compare keys
print(f"ANON_KEYs match: {docker_anon_key == local_anon_key}")
print(f"SERVICE_ROLE_KEYs match: {docker_service_role_key == local_service_role_key}")

# Display values for verification
print(f"Docker ANON_KEY: {docker_anon_key}")
print(f"Local ANON_KEY: {local_anon_key}")
print(f"Docker SERVICE_ROLE_KEY: {docker_service_role_key}")
print(f"Local SERVICE_ROLE_KEY: {local_service_role_key}")

# Continue with existing code
env2path = ".env"

supabase_url = "http://localhost:8000"
# supabase_key = os.getenv("ANON_KEY")
supabase_key = os.getenv("SERVICE_ROLE_KEY")


# Create two clients: one for default schema and one for pomodoro schema
supabase_default: Client = create_client(supabase_url, supabase_key)
supabase_pomodoro: Client = create_client(
    supabase_url,
    supabase_key,
    options=ClientOptions(schema="pomodoro")
)

# Test connection with public schema
print("Public schema test:")
try:
    response = supabase_default.table("babcia").select("*").limit(1).execute()
    print(f"Successfully queried 'babcia' table: {response.data}")
except Exception as e:
    print(f"Failed to query public schema: {e}")

# New code for testing user creation and profile access
print("\n--- COMPREHENSIVE AUTH AND PROFILE ACCESS TEST ---")

# Generate a unique email for testing
import random
import string
import uuid
from datetime import datetime, timezone

# Generate random email to avoid conflicts
random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
test_email = f"test_{random_suffix}@example.com"
test_password = "TestPassword123!"
test_username = f"testuser_{random_suffix}"

print(f"\nCreating test user with email: {test_email}")

# 1. Create user with Supabase Auth
try:
    # Create user using the service role key which bypasses email confirmation
    auth_response = supabase_default.auth.admin.create_user({
        "email": test_email,
        "password": test_password,
        "email_confirm": True,  # Automatically confirm the email
        "user_metadata": {
            "username": test_username
        }
    })
    
    if auth_response:
        user_id = auth_response.user.id
        print(f"Successfully created user with ID: {user_id}")
    else:
        print("Failed to get user ID from response")
        user_id = None
except Exception as e:
    print(f"Failed to create user: {e}")
    user_id = None

# 2. Check if profile was automatically created (by the trigger)
if user_id:
    print("\nChecking for existing profile (should be created by trigger)")
    try:
        # Check for existing profile
        profile_response = supabase_pomodoro.table("profiles").select("*").eq("id", user_id).execute()
        
        if profile_response.data and len(profile_response.data) > 0:
            print(f"Found existing profile (created by trigger): {profile_response.data[0]}")
        else:
            print("No profile found, which is unexpected since there's a trigger")
            
            # If for some reason no profile exists, create one
            print("Creating profile manually as fallback")
            
            # Default pomodoro settings
            default_settings = {
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
            
            # Insert profile record
            profile_data = {
                "id": user_id,
                "username": test_username,
                "pomodoro_settings": default_settings,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            profile_response = supabase_pomodoro.table("profiles").insert(profile_data).execute()
            
            if profile_response.data and len(profile_response.data) > 0:
                print(f"Successfully created profile manually: {profile_response.data[0]}")
            else:
                print("No data returned when creating profile")
    except Exception as e:
        print(f"Error checking/creating profile: {e}")

# 3. Create a task for the user
if user_id:
    print("\nCreating a task for the user")
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task created by the connection test script",
            "user_id": user_id,
            "estimated_pomodoros": 3,
            "completed_pomodoros": 0,
            "is_active": True,
            "position": 1,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        task_response = supabase_pomodoro.table("tasks").insert(task_data).execute()
        
        if task_response.data and len(task_response.data) > 0:
            task_id = task_response.data[0]['id']
            print(f"Successfully created task with ID: {task_id}")
        else:
            print("No data returned when creating task")
            task_id = None
    except Exception as e:
        print(f"Failed to create task: {e}")
        task_id = None

# 4. Log in with the created user
print("\nLogging in with the created user")
try:
    auth_client = create_client(supabase_url, os.getenv("ANON_KEY"))
    login_response = auth_client.auth.sign_in_with_password({
        "email": test_email,
        "password": test_password
    })
    
    if login_response.user:
        print(f"Successfully logged in as: {login_response.user.email}")
        logged_in_user_id = login_response.user.id
        user_token = login_response.session.access_token if login_response.session else None
        
        # Create a client with the user's JWT
        if user_token:
            user_client = create_client(
                supabase_url, 
                os.getenv("ANON_KEY"),
                options=ClientOptions(
                    schema="pomodoro",
                    headers={"Authorization": f"Bearer {user_token}"}
                )
            )
            
            # 5. Fetch the user's profile using their token
            print("\nFetching profile using user's token")
            try:
                profile_response = user_client.table("profiles").select("*").eq("id", logged_in_user_id).execute()
                
                if profile_response.data and len(profile_response.data) > 0:
                    print(f"Successfully fetched user profile: {profile_response.data[0]}")
                else:
                    print("No profile found for the user")
            except Exception as e:
                print(f"Failed to fetch profile with user token: {e}")
                
            # 6. Fetch the user's tasks
            if task_id:
                print("\nFetching user's tasks")
                try:
                    tasks_response = user_client.table("tasks").select("*").eq("user_id", logged_in_user_id).execute()
                    
                    if tasks_response.data and len(tasks_response.data) > 0:
                        print(f"Successfully fetched user tasks: {tasks_response.data}")
                    else:
                        print("No tasks found for the user")
                except Exception as e:
                    print(f"Failed to fetch tasks: {e}")
        else:
            print("No access token available after login")
    else:
        print("Failed to get user from login response")
except Exception as e:
    print(f"Failed to log in: {e}")

print("\n--- TEST COMPLETED ---")
