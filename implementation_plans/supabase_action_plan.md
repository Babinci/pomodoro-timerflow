# Supabase Integration: Action Plan

This document outlines the precise steps needed to make the Supabase integration fully functional in the Pomodoro TimerFlow application.

## 1. Supabase Configuration and Permissions

- [ ] **Setup Database Structure**
  - [ ] Login to Supabase dashboard for your project
  - [ ] Verify that all required tables exist:
    - [ ] `users` table
    - [ ] `tasks` table
    - [ ] `pomodoro_sessions` table
    - [ ] `pomodoro_checkpoints` table
  - [ ] Create any missing tables using SQL in the SQL Editor

- [ ] **Configure Row Level Security**
  - [ ] Enable RLS on all tables:
    ```sql
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;
    ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
    ALTER TABLE pomodoro_sessions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE pomodoro_checkpoints ENABLE ROW LEVEL SECURITY;
    ```
  - [ ] Create policy for users table:
    ```sql
    CREATE POLICY "Users can view and edit their own data" ON users
    FOR ALL TO authenticated
    USING (auth.uid() = id);
    ```
  - [ ] Create policies for tasks table:
    ```sql
    CREATE POLICY "Users can view their own tasks" ON tasks
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

    CREATE POLICY "Users can insert their own tasks" ON tasks
    FOR INSERT TO authenticated
    WITH CHECK (auth.uid() = user_id);

    CREATE POLICY "Users can update their own tasks" ON tasks
    FOR UPDATE TO authenticated
    USING (auth.uid() = user_id);

    CREATE POLICY "Users can delete their own tasks" ON tasks
    FOR DELETE TO authenticated
    USING (auth.uid() = user_id);
    ```
  - [ ] Create similar policies for pomodoro_sessions and pomodoro_checkpoints tables

- [ ] **Setup Authentication**
  - [ ] Configure Email Auth provider in Supabase Dashboard
  - [ ] Set up Site URL and Redirect URLs

- [ ] **Configure Environment Variables**
  - [ ] Update the `.env` file with proper Supabase credentials:
    ```
    SUPABASE_URL=https://your-project-url.supabase.co
    SUPABASE_KEY=your-public-anon-key
    SUPABASE_SERVICE_KEY=your-service-role-key (if needed)
    ```
  - [ ] Make sure these values are correctly passed to the Docker container

## 2. Backend Implementation

- [ ] **Implement User Authentication Routes**
  - [ ] Check `auth_supabase.py` for missing functionality
  - [ ] Ensure sign-up, login, logout, and token refresh are working
  - [ ] Test authentication routes with Postman or curl

- [ ] **Implement Task Management Routes**
  - [ ] Verify tasks_supabase.py implements all required endpoints:
    - [ ] `GET /api/tasks` - List all tasks
    - [ ] `POST /api/tasks` - Create a new task
    - [ ] `PUT /api/tasks/{id}` - Update a task
    - [ ] `DELETE /api/tasks/{id}` - Delete a task
    - [ ] `PUT /api/tasks/order` - Update task order
  - [ ] Test task API endpoints

- [ ] **Implement Pomodoro Session Routes**
  - [ ] Verify pomodoro_session_supabase.py implements:
    - [ ] `POST /api/pomodoro/sessions` - Create session
    - [ ] `PUT /api/pomodoro/sessions/{id}/complete` - Complete session
    - [ ] `GET /api/pomodoro/sessions` - List sessions
    - [ ] `POST /api/pomodoro/checkpoints` - Create checkpoint
    - [ ] `GET /api/pomodoro/checkpoints/latest` - Get latest checkpoint

- [ ] **Create WebSocket Implementation**
  - [ ] Review and fix WebSocket functionality in `ws_manager_supabase.py`
  - [ ] Update `pomodoro_websocket.py` router to work with Supabase
  - [ ] Test WebSocket connection and events

## 3. Docker and Deployment Configuration

- [ ] **Fix Docker Environment Variables**
  - [ ] Ensure Docker has access to environment variables
  - [ ] Modify restart_docker.cmd to include environment variables:
    ```bash
    docker run -d -p 8003:8003 \
      -v $(pwd)/logs:/app/logs \
      -e SUPABASE_URL=your-url \
      -e SUPABASE_KEY=your-key \
      -v $(pwd)/backend/credentials/.env:/app/.env \
      --name pomodoro-app-container pomodoro-app
    ```

- [ ] **Update Dockerfile**
  - [ ] Create a directory for logs:
    ```dockerfile
    RUN mkdir -p /app/logs
    ```
  - [ ] Set proper permissions:
    ```dockerfile
    RUN chmod -R 777 /app/logs
    ```

## 4. Debugging and Testing

- [ ] **Setup Logging**
  - [ ] Configure detailed logging for authentication process
  - [ ] Add logging to all Supabase API calls
  - [ ] Log WebSocket events and state changes

- [ ] **Test Authentication Flow**
  - [ ] Test user registration
  - [ ] Test login and session management
  - [ ] Test token refresh
  - [ ] Verify that auth states persist correctly

- [ ] **Test Task Management**
  - [ ] Test creating tasks
  - [ ] Test updating tasks
  - [ ] Test deleting tasks
  - [ ] Test changing task order

- [ ] **Test Pomodoro Timer**
  - [ ] Test starting timer
  - [ ] Test pausing and resuming
  - [ ] Test completing pomodoro sessions
  - [ ] Test session transitions (work → break → work)
  - [ ] Test preset changes

## 5. Fallback and Migration Strategy

- [ ] **Create Database Migration Scripts**
  - [ ] Script to export data from SQLite
  - [ ] Script to import data to Supabase
  - [ ] Test migration with sample data

- [ ] **Implement Dual Backend Support**
  - [ ] Create environment flag to switch between SQLite and Supabase
  - [ ] Test both backends to ensure they work correctly

## 6. Code Cleanup and Documentation

- [ ] **Clean Up Codebase**
  - [ ] Remove unused compatibility layers once everything works
  - [ ] Refactor code for clarity and maintainability
  - [ ] Remove duplicate code

- [ ] **Document Supabase Implementation**
  - [ ] Update README.md with Supabase information
  - [ ] Document environment variables and configuration options
  - [ ] Create deployment guide for Supabase version

## 7. Performance and Monitoring

- [ ] **Implement Performance Monitoring**
  - [ ] Add request timing logs
  - [ ] Monitor database query performance
  - [ ] Set up error tracking and reporting

- [ ] **Optimize Database Queries**
  - [ ] Review and optimize Supabase queries
  - [ ] Add indexes where needed:
    ```sql
    CREATE INDEX idx_tasks_user_id ON tasks(user_id);
    CREATE INDEX idx_pomodoro_sessions_user_id ON pomodoro_sessions(user_id);
    ```

## Testing Checklist

- [ ] **Functionality Testing**
  - [ ] User registration works
  - [ ] Login and authentication work
  - [ ] Task creation and management work
  - [ ] Pomodoro timer functions work
  - [ ] WebSocket synchronization works

- [ ] **Performance Testing**
  - [ ] Application loads quickly
  - [ ] Timer updates are responsive
  - [ ] Multiple clients can connect simultaneously
  - [ ] Database operations complete in acceptable time

- [ ] **Security Testing**
  - [ ] Users can only access their own data
  - [ ] JWT tokens are validated correctly
  - [ ] Invalid tokens are rejected
  - [ ] Password reset functionality works securely

## Technical Requirements Review

- [ ] **Verify Supabase Requirements**
  - [ ] Supabase client version is compatible with API
  - [ ] All required tables and fields exist
  - [ ] RLS policies are properly configured

- [ ] **Verify Database Schema**
  - [ ] Schema matches expected fields and types
  - [ ] Foreign key relationships are correctly defined
  - [ ] Indexes are created for query optimization

This action plan provides a comprehensive roadmap for completing the Supabase integration. Each section contains specific, actionable steps with code examples where appropriate. Following this plan will ensure a methodical approach to resolving the remaining issues and making the application fully functional with Supabase.