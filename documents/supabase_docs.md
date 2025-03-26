# Supabase Python Client Documentation

## Introduction
This reference documents every object and method available in Supabase's Python library, supabase-py. You can use supabase-py to interact with your Postgres database, listen to database changes, invoke Deno Edge Functions, build login and user management functionality, and manage large files.

## Installation

### Install with PyPi
You can install supabase-py via the terminal (for Python > 3.8):

```bash
pip install supabase
```

## Initializing
Initialize a new Supabase client using the `create_client()` method.

```python
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
```

### Parameters
- `supabase_url` (Required, string): The unique Supabase URL from your project dashboard
- `supabase_key` (Required, string): The unique Supabase Key from your project dashboard
- `options` (Optional, ClientOptions): Options to change the Auth behaviors

## Database Operations

### Fetch Data
```python
response = (
    supabase.table("planets")
    .select("*")
    .execute()
)
```

### Insert Data
```python
response = (
    supabase.table("planets")
    .insert({"id": 1, "name": "Pluto"})
    .execute()
)
```

### Update Data
```python
response = (
    supabase.table("instruments")
    .update({"name": "piano"})
    .eq("id", 1)
    .execute()
)
```

### Delete Data
```python
response = (
    supabase.table("countries")
    .delete()
    .eq("id", 1)
    .execute()
)
```

## Authentication

### Sign Up
```python
response = supabase.auth.sign_up(
    {
        "email": "email@example.com", 
        "password": "password",
    }
)
```

### Sign In
```python
response = supabase.auth.sign_in_with_password(
    {
        "email": "email@example.com", 
        "password": "example-password",
    }
)
```

### Sign Out
```python
response = supabase.auth.sign_out()
```

## Storage

### Create Bucket
```python
response = (
    supabase.storage
    .create_bucket(
        "avatars",
        options={
            "public": False,
            "allowed_mime_types": ["image/png"],
            "file_size_limit": 1024,
        }
    )
)
```

### Upload File
```python
with open("./public/avatar1.png", "rb") as f:
    response = (
        supabase.storage
        .from_("avatars")
        .upload(
            file=f,
            path="public/avatar1.png",
            file_options={"cache-control": "3600", "upsert": "false"}
        )
    )
```

## Realtime

### Subscribe to Channel
```python
channel = supabase.channel("room1")

def on_subscribe(status, err):
    if status == RealtimeSubscribeStates.SUBSCRIBED:
        channel.send_broadcast(
            "cursor-pos", 
            {"x": random.random(), "y": random.random()}
        )

def handle_broadcast(payload):
    print("Cursor position received!", payload)

channel.on_broadcast(event="cursor-pos", callback=handle_broadcast).subscribe(on_subscribe)
```

## Filters

### Basic Filters
```python
# Equal
response = (
    supabase.table("planets")
    .select("*")
    .eq("name", "Earth")
    .execute()
)

# Not Equal
response = (
    supabase.table("planets")
    .select("*")
    .neq("name", "Earth")
    .execute()
)

# Greater Than
response = (
    supabase.table("planets")
    .select("*")
    .gt("id", 2)
    .execute()
)
```

## Modifiers

### Ordering
```python
response = (
    supabase.table("planets")
    .select("*")
    .order("name", desc=True)
    .execute()
)
```

### Limiting
```python
response = (
    supabase.table("planets")
    .select("name")
    .limit(1)
    .execute()
)
```

## Edge Functions

### Invoke Function
```python
response = supabase.functions.invoke(
    "hello-world", 
    invoke_options={
        "body": {"name": "Functions"},
    },
)
```

## Help Resources
- [Contact support](https://supabase.com/support)
- [See Changelog](https://supabase.com/changelog)
- [Check system status](https://status.supabase.com)