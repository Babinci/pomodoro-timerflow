## Current Architecture Analysis

### Database & Authentication Components:
1. **Database Configuration** (`database.py`):
   - SQLite database with SQLAlchemy ORM
   - Creates all tables through Base.metadata.create_all
   - Uses SessionLocal for database sessions

2. **Authentication** (`auth.py`):
   - Custom JWT-based authentication with jose
   - Password hashing with passlib
   - Various functions for token creation/validation
   - User lookup and current user dependency

3. **Models** (`models.py`):
   - SQLAlchemy models: User, Task, PomodoroSession, PomodoroCheckpoint
   - Table relationships with foreign keys

4. **Routers**:
   - `auth.py`: Token creation/verification endpoints
   - `users.py`: User CRUD operations
   - `tasks.py`: Task management endpoints
   - `pomodoro_websocket.py`: WebSocket handling (leave for now)

5. **Existing Supabase Setup** (`supabase.py`):
   - Connection established to "pomodoro" schema
   - URL and key already configured

## Required Supabase Functionality

### Authentication Functions:
- `supabase.auth.sign_up()` - Replace user registration
- `supabase.auth.sign_in_with_password()` - Replace login
- `supabase.auth.get_user()` - Get current user
- `supabase.auth.admin.list_users()` - Admin user listing
- `supabase.auth.update_user()` - Update user details
- `supabase.auth.admin.delete_user()` - Delete users

### Database Functions:
- `supabase.table("tablename").select(*)` - Query data
- `supabase.table("tablename").insert({})` - Create records
- `supabase.table("tablename").update({}).eq()` - Update data
- `supabase.table("tablename").delete().eq()` - Delete data
- Query filters: `.eq()`, `.neq()`, `.gt()`, etc.
- Modifiers: `.order()`, `.limit()`, etc.

## Migration Plan

### 1. Database Schema Setup
- [x] Create Supabase tables matching SQLAlchemy models
  - [x] `users` table with matching columns
  - [x] `tasks` table with position field for ordering
  - [x] `pomodoro_sessions` table for tracking sessions
  - [x] `pomodoro_checkpoints` table for state preservation
- [x] Set up foreign key relationships
- [x] Configure Row Level Security (RLS) policies
  - [x] Users can only access their own data
  - [x] Tasks belong to specific users
  - [x] Sessions and checkpoints restricted to owners

### 2. Authentication Migration
- [x] Update `auth.py` to use Supabase Auth
  - [x] Replace JWT functions with Supabase equivalents
  - [x] Update token validation mechanism
  - [x] Create new `get_current_user` dependency
- [x] Modify auth router endpoints
  - [x] Update `/token` endpoint to use Supabase sign-in
  - [x] Update token verification endpoint
  - [x] Adjust error handling

### 3. Data Access Layer Migration
- [x] Refactor user operations:
  - [x] Replace user creation with Supabase auth
  - [x] Update user retrieval with Supabase queries
  - [x] Modify user settings operations
- [x] Refactor task operations:
  - [x] Update task CRUD with Supabase queries
  - [x] Maintain task ordering functionality
  - [x] Preserve WebSocket notification mechanism
- [x] Adjust pomodoro session operations
  - [x] Update session recording with Supabase
  - [x] Maintain checkpoint state preservation
  - [x] Ensure proper user validation

### 4. Integration & Testing
- [x] Update dependency injection mechanism
  - [x] Remove SQLAlchemy session dependency
  - [x] Create Supabase client dependency if needed
- [x] Update error handling
  - [x] Map Supabase errors to FastAPI HTTP exceptions
  - [x] Handle authentication-specific errors
- [x] Create test plan for core flows
  - [x] Authentication flow
  - [x] Task management
  - [x] Session recording
  - [x] Settings management

### 5. Cleanup & Documentation
- [x] Update requirements.txt
  - [x] Add supabase-py
  - [x] Remove unused dependencies
- [x] Create migration documentation
- [x] Create fallback plan
- [x] Create new main.py file using Supabase components

## Implementation Considerations

1. **Database Table Structure**:
   - Supabase is PostgreSQL-based, so column types need adjustment
   - JSON fields for settings (like pomodoro_settings)
   - Handle timestamptz for datetime fields

2. **Authentication Flow**:
   - Supabase JWT format differs from custom JWTs
   - User settings stored in database but auth in Supabase

3. **Row Level Security**:
   - Critical for multi-tenant application
   - Must implement RLS policies for each table

4. **Database Transactions**:
   - Handle task updates consistently
   - Maintain atomicity for related operations

This migration plan focuses on preserving functionality while transitioning from SQLite/SQLAlchemy to Supabase, keeping the existing WebSocket implementation intact for now.