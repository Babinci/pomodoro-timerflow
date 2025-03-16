
# Implementing Supabase for Your Pomodoro App

Based on your requirements, here's a step-by-step guide to set up Supabase for your project.

## Next Steps for Supabase Implementation

### 1. Create Tables in Supabase

Since you've already got Supabase running locally (`npx supabase start`), you'll need to create tables that match your SQLAlchemy models.

First, create a migration file:

```bash
npx supabase migration new create_initial_schema
```

This will create a new file in the `supabase/migrations` directory. Edit this file to include your table definitions:

```sql:supabase/migrations/[timestamp]_create_initial_schema.sql
-- Create users table
CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    pomodoro_settings JSONB DEFAULT '{
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
    }'::jsonb
);

-- Create tasks table
CREATE TABLE public.tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    user_id INTEGER REFERENCES public.users(id),
    estimated_pomodoros INTEGER NOT NULL,
    completed_pomodoros INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    position INTEGER DEFAULT 999999
);

-- Create pomodoro_sessions table
CREATE TABLE public.pomodoro_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id),
    task_id INTEGER REFERENCES public.tasks(id),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    session_type VARCHAR NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    current_session_number INTEGER NOT NULL
);

-- Create pomodoro_checkpoints table
CREATE TABLE public.pomodoro_checkpoints (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id),
    task_id INTEGER REFERENCES public.tasks(id),
    checkpoint_type VARCHAR NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remaining_time INTEGER NOT NULL,
    session_type VARCHAR NOT NULL,
    is_paused BOOLEAN DEFAULT FALSE,
    round_number INTEGER NOT NULL,
    preset_type VARCHAR NOT NULL,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Apply the Migration

Apply this migration to your local Supabase instance:

```bash
npx supabase db reset
```

This command will apply all migrations in your migration directory to your local database.

### 3. Set Up Python Client

Install the Supabase Python client:

```bash
pip install supabase
```

### 4. Connect Your Backend to Supabase

Create a connection file in your backend:

```python:backend/app/supabase_client.py
from supabase import create_client
import os

# Local development URL and key
url = "http://localhost:54323"  # Local Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"  # Local anon key

# Initialize the Supabase client
supabase = create_client(url, key)
```

For a production environment, you'd store these in environment variables:

```python
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
```

### 5. Update Your Backend Code

Now you'll need to modify your backend to use Supabase instead of SQLAlchemy. Here's a basic example of how to handle user operations:

```python:backend/app/repositories/user_repository.py
from ..supabase_client import supabase

class UserRepository:
    def create_user(self, email, username, hashed_password):
        result = supabase.table('users').insert({
            'email': email,
            'username': username,
            'hashed_password': hashed_password
        }).execute()
        return result.data[0] if result.data else None
    
    def get_user_by_email(self, email):
        result = supabase.table('users').select('*').eq('email', email).execute()
        return result.data[0] if result.data else None
    
    def get_user_by_id(self, user_id):
        result = supabase.table('users').select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    def update_pomodoro_settings(self, user_id, settings):
        result = supabase.table('users').update({
            'pomodoro_settings': settings
        }).eq('id', user_id).execute()
        return result.data[0] if result.data else None
```

### 6. Future Migrations

When you need to add new tables or modify existing ones:

1. Create a new migration:
```bash
npx supabase migration new add_feature_x
```

2. Edit the new migration file with your schema changes:
```sql
ALTER TABLE public.users ADD COLUMN new_field VARCHAR;
```

3. Apply the migration:
```bash
npx supabase db reset
```

### 7. Deployment

When you're ready to deploy:

1. Create a new project on [Supabase.com](https://supabase.com)
2. Link your local project to your Supabase project:
```bash
npx supabase link --project-ref your-project-id
```

3. Push your local migrations to your remote project:
```bash
npx supabase db push
```

## Important Considerations

1. **Authentication**: Supabase provides built-in auth that you might want to use instead of your custom auth system.

2. **Row-Level Security (RLS)**: For security, implement RLS policies:

```sql
-- Example RLS for tasks
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only access their own tasks" 
ON public.tasks 
FOR ALL 
USING (auth.uid() = user_id);
```

3. **Python Client vs Direct SQL**: Supabase-py is relatively new and might not have all features. Consider using SQL migrations for complex operations.

4. **Testing**: Test your migrations locally before applying to production.

Would you like me to elaborate on any specific part of this implementation plan? Or are there any aspects you're particularly concerned about?


# Supabase Migrations vs Django Migrations

You're asking a great question about whether Supabase offers something similar to Django's convenient `makemigrations` and `migrate` workflow. Let me clarify how this works with Supabase.

## Supabase vs Django Migration Approaches

Unlike Django, Supabase doesn't have an ORM that automatically generates migrations from code models. Supabase takes a more SQL-first approach:

1. **Django**: Define models in Python → Run `makemigrations` to generate SQL → Run `migrate` to apply changes
2. **Supabase**: Write SQL migrations directly OR make changes in UI → Generate SQL with `db diff`

## Options for a Django-like Experience with Supabase

### Option 1: Use the Dashboard + Diff Approach

This is the closest to Django's workflow:

1. Make changes to your database schema using the Supabase Dashboard UI
2. Run `npx supabase db diff` to generate the SQL that represents your changes
3. Save this SQL to a migration file
4. Apply with `npx supabase db reset`

```bash
# After making changes in the Supabase Dashboard UI
npx supabase db diff --schema public > supabase/migrations/[timestamp]_my_changes.sql
npx supabase db reset
```

### Option 2: Use a Third-party ORM with Supabase

You could use Prisma or SQLAlchemy with Supabase:

#### Prisma Example:
```bash
# Install Prisma
npm install prisma --save-dev

# Initialize Prisma
npx prisma init

# Define your schema in prisma/schema.prisma
# Then generate migrations
npx prisma migrate dev --name init
```

Then configure Prisma to connect to your Supabase PostgreSQL database.

#### SQLAlchemy with Alembic:
Since you're already using SQLAlchemy models, you could use Alembic to generate migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init migrations

# Generate a migration from your models
alembic revision --autogenerate -m "create tables"

# Apply the migration
alembic upgrade head
```

You'd need to configure Alembic to connect to your Supabase PostgreSQL database.

### Option 3: Hybrid Approach (Recommended)

1. Keep your SQLAlchemy models for your application code
2. Use Alembic to generate migration SQL from your models
3. Copy the generated SQL into Supabase migration files
4. Apply with Supabase CLI

This gives you the best of both worlds - model-driven development with Supabase's deployment workflow.

## Step-by-Step Implementation of the Hybrid Approach

1. **Set up Alembic with your SQLAlchemy models**:
   ```bash
   pip install alembic
   alembic init migrations
   ```

2. **Configure Alembic to use your models**:
   Edit `migrations/env.py` to import your models and set up the MetaData:
   ```python
   # Add this near the top
   import sys
   from os.path import dirname, abspath
   sys.path.insert(0, dirname(dirname(abspath(__file__))))
   
   from backend.app.models import Base
   target_metadata = Base.metadata
   ```

3. **Generate a migration**:
   ```bash
   alembic revision --autogenerate -m "initial_schema"
   ```

4. **Copy the SQL from the generated migration**:
   Open the generated file in `migrations/versions/` and copy the SQL operations.

5. **Create a Supabase migration file**:
   ```bash
   npx supabase migration new initial_schema
   ```

6. **Paste the SQL into the Supabase migration file**:
   Edit the file in `supabase/migrations/` and paste the SQL.

7. **Apply the migration**:
   ```bash
   npx supabase db reset
   ```

## Conclusion

While Supabase doesn't offer the exact same workflow as Django, you can achieve a similar developer experience by:

1. Using the Dashboard + Diff approach for quick iterations
2. Using a third-party ORM like Prisma or SQLAlchemy+Alembic for model-driven development
3. Using a hybrid approach that leverages both your existing models and Supabase's migration system

The hybrid approach is probably the most suitable for your case since you already have SQLAlchemy models defined and want to maintain a clean backend-frontend separation.

Would you like me to provide more details on implementing any of these approaches?


# Supabase Migrations vs Django Migrations

You're asking a great question about whether Supabase offers something similar to Django's convenient `makemigrations` and `migrate` workflow. Let me clarify how this works with Supabase.

## Supabase vs Django Migration Approaches

Unlike Django, Supabase doesn't have an ORM that automatically generates migrations from code models. Supabase takes a more SQL-first approach:

1. **Django**: Define models in Python → Run `makemigrations` to generate SQL → Run `migrate` to apply changes
2. **Supabase**: Write SQL migrations directly OR make changes in UI → Generate SQL with `db diff`

## Options for a Django-like Experience with Supabase

### Option 1: Use the Dashboard + Diff Approach

This is the closest to Django's workflow:

1. Make changes to your database schema using the Supabase Dashboard UI
2. Run `npx supabase db diff` to generate the SQL that represents your changes
3. Save this SQL to a migration file
4. Apply with `npx supabase db reset`

```bash
# After making changes in the Supabase Dashboard UI
npx supabase db diff --schema public > supabase/migrations/[timestamp]_my_changes.sql
npx supabase db reset
```

### Option 2: Use a Third-party ORM with Supabase

You could use Prisma or SQLAlchemy with Supabase:

#### Prisma Example:
```bash
# Install Prisma
npm install prisma --save-dev

# Initialize Prisma
npx prisma init

# Define your schema in prisma/schema.prisma
# Then generate migrations
npx prisma migrate dev --name init
```

Then configure Prisma to connect to your Supabase PostgreSQL database.

#### SQLAlchemy with Alembic:
Since you're already using SQLAlchemy models, you could use Alembic to generate migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init migrations

# Generate a migration from your models
alembic revision --autogenerate -m "create tables"

# Apply the migration
alembic upgrade head
```

You'd need to configure Alembic to connect to your Supabase PostgreSQL database.

### Option 3: Hybrid Approach (Recommended)

1. Keep your SQLAlchemy models for your application code
2. Use Alembic to generate migration SQL from your models
3. Copy the generated SQL into Supabase migration files
4. Apply with Supabase CLI

This gives you the best of both worlds - model-driven development with Supabase's deployment workflow.

## Step-by-Step Implementation of the Hybrid Approach

1. **Set up Alembic with your SQLAlchemy models**:
   ```bash
   pip install alembic
   alembic init migrations
   ```

2. **Configure Alembic to use your models**:
   Edit `migrations/env.py` to import your models and set up the MetaData:
   ```python
   # Add this near the top
   import sys
   from os.path import dirname, abspath
   sys.path.insert(0, dirname(dirname(abspath(__file__))))
   
   from backend.app.models import Base
   target_metadata = Base.metadata
   ```

3. **Generate a migration**:
   ```bash
   alembic revision --autogenerate -m "initial_schema"
   ```

4. **Copy the SQL from the generated migration**:
   Open the generated file in `migrations/versions/` and copy the SQL operations.

5. **Create a Supabase migration file**:
   ```bash
   npx supabase migration new initial_schema
   ```

6. **Paste the SQL into the Supabase migration file**:
   Edit the file in `supabase/migrations/` and paste the SQL.

7. **Apply the migration**:
   ```bash
   npx supabase db reset
   ```

## Conclusion

While Supabase doesn't offer the exact same workflow as Django, you can achieve a similar developer experience by:

1. Using the Dashboard + Diff approach for quick iterations
2. Using a third-party ORM like Prisma or SQLAlchemy+Alembic for model-driven development
3. Using a hybrid approach that leverages both your existing models and Supabase's migration system

The hybrid approach is probably the most suitable for your case since you already have SQLAlchemy models defined and want to maintain a clean backend-frontend separation.

Would you like me to provide more details on implementing any of these approaches?


