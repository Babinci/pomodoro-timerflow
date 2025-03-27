-- Supabase Schema Setup Script for Pomodoro TimerFlow

-- The schema appears to already exist in Supabase with the following structure:
-- Users Table: id (integer), email, username, hashed_password, pomodoro_settings (JSONB)
-- Tasks Table: Standard structure
-- Pomodoro Sessions Table: Standard structure 
-- Pomodoro Checkpoints Table: Standard structure

-- This script focuses on setting up proper permissions

-- Create Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  user_id UUID REFERENCES users(id) NOT NULL,
  estimated_pomodoros INTEGER,
  completed_pomodoros INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  is_active BOOLEAN DEFAULT TRUE,
  position INTEGER DEFAULT 999999
);

-- Create Pomodoro Sessions Table
CREATE TABLE IF NOT EXISTS pomodoro_sessions (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) NOT NULL,
  task_id INTEGER REFERENCES tasks(id),
  start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  end_time TIMESTAMP WITH TIME ZONE,
  session_type TEXT,
  completed BOOLEAN DEFAULT FALSE,
  current_session_number INTEGER
);

-- Create Pomodoro Checkpoints Table
CREATE TABLE IF NOT EXISTS pomodoro_checkpoints (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id) NOT NULL,
  task_id INTEGER REFERENCES tasks(id),
  checkpoint_type TEXT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  remaining_time INTEGER,
  session_type TEXT,
  is_paused BOOLEAN DEFAULT FALSE,
  round_number INTEGER,
  preset_type TEXT,
  last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE pomodoro_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE pomodoro_checkpoints ENABLE ROW LEVEL SECURITY;

-- Create Policies for Users Table
-- For anonymous users to register
CREATE POLICY "Allow anonymous to insert" ON pomodoro.users
FOR INSERT TO anon
WITH CHECK (true);

-- For app/API usage
CREATE POLICY "Allow all operations" ON pomodoro.users
FOR ALL TO authenticated
USING (true);

-- Create Policies for Tasks Table
CREATE POLICY "Allow all operations on tasks" ON pomodoro.tasks
FOR ALL TO authenticated
USING (true);

CREATE POLICY "Allow anonymous to view tasks" ON pomodoro.tasks
FOR SELECT TO anon
USING (true);

-- Create Policies for Pomodoro Sessions Table
CREATE POLICY "Allow all operations on sessions" ON pomodoro.pomodoro_sessions
FOR ALL TO authenticated
USING (true);

CREATE POLICY "Allow anonymous to view sessions" ON pomodoro.pomodoro_sessions
FOR SELECT TO anon
USING (true);

-- Create Policies for Pomodoro Checkpoints Table
CREATE POLICY "Allow all operations on checkpoints" ON pomodoro.pomodoro_checkpoints
FOR ALL TO authenticated
USING (true);

CREATE POLICY "Allow anonymous to view checkpoints" ON pomodoro.pomodoro_checkpoints
FOR SELECT TO anon
USING (true);

-- Create Indexes for Better Performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_pomodoro_sessions_user_id ON pomodoro_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_pomodoro_sessions_task_id ON pomodoro_sessions(task_id);
CREATE INDEX IF NOT EXISTS idx_pomodoro_checkpoints_user_id ON pomodoro_checkpoints(user_id);
CREATE INDEX IF NOT EXISTS idx_pomodoro_checkpoints_task_id ON pomodoro_checkpoints(task_id);
