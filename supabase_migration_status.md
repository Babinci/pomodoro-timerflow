# Supabase Migration Status

## Completed

1. **Removed SQLAlchemy Dependencies**
   - Removed SQLAlchemy imports from WebSocket implementation
   - Updated main_supabase.py to not depend on database_supabase.py
   - Fixed import dependencies in routers
   - Configured Docker to use the Supabase implementation

2. **Fixed Integration Issues**
   - Added missing Supabase imports
   - Properly set up app.state.supabase for WebSocket access
   - Updated health check endpoint for compatibility

3. **API Routing Fixes**
   - Fixed route handling to properly handle paths both with and without trailing slashes
   - Updated static file serving to avoid conflicts with API routes
   - Fixed 405 Method Not Allowed errors for registration endpoint

## Current Status and Issues

After extensive testing, we've identified several key issues that need to be addressed:

1. **Permission Issues with Supabase**
   - All operations on the `pomodoro.users` table result in permission denied errors
   - RLS policies have been created but don't appear to be effective
   - Error in logs: `permission denied for table users` when attempting database operations

2. **Authentication Strategy**
   - The current implementation attempts to use native Supabase Auth, but our actual table structure doesn't match
   - Our users table has an integer ID column, not a UUID that references auth.users

3. **Schema Structure Discovery**
   - Investigation of the actual schema structure shows:
   ```
   users table: id (integer), email, username, hashed_password, pomodoro_settings (JSONB)
   ```
   - This differs from the expected structure with UUID references to auth.users

4. **API Requests**
   - API endpoints now correctly accept requests (fixed routing issues)
   - However, database operations fail with permission errors
   - Diagnostic endpoints work but also confirm permission issues

## Required Supabase Configuration

The application has been migrated from SQLAlchemy to Supabase, but the following configurations need to be implemented to make it fully functional:

### 1. Adjust to Actual Schema Structure

Based on our investigation, we need to adjust our approach to match the actual schema:

```sql
-- Actual Schema Structure (confirmed via database inspection)
-- Table: pomodoro.users
-- Columns: id (integer), email, username, hashed_password, pomodoro_settings (JSONB)

-- Create RLS Policies that match this structure
CREATE POLICY "Allow anonymous to insert" ON pomodoro.users
FOR INSERT TO anon
WITH CHECK (true);

CREATE POLICY "Allow all operations" ON pomodoro.users
FOR ALL TO authenticated
USING (true);

-- Similar policies for tasks, pomodoro_sessions, and pomodoro_checkpoints
```

### 2. Update Authentication Approach

Since the database doesn't use Supabase Auth for identity management, we need to:

1. Use custom authentication logic instead of Supabase Auth
2. Update the auth_supabase.py file to match this architecture
3. Use proper password hashing and JWT token generation

### 3. Credentials Management

We should update the application with proper environment variables:

```
SUPABASE_URL=your-actual-supabase-url
SUPABASE_KEY=your-actual-supabase-anon-key
JWT_SECRET=your-secure-secret-key
```

## API Endpoint Status

| Endpoint | Method | Status | Issue |
|----------|--------|--------|-------|
| /api/users | POST | ✅ Routing works, ❌ DB access fails | Permission denied for table users |
| /api/token | POST | ⚠️ Not tested fully | Needs testing after schema issues resolved |
| /api/health | GET | ✅ Working | Returns diagnostic information |
| /api/ping | GET | ✅ Working | Basic health check |
| /api/tasks | Various | ⚠️ Not tested fully | Depends on authentication |
| WebSocket | WS | ⚠️ Not tested fully | Depends on authentication |

## Testing Procedure

Once the configuration issues are resolved, test with:

1. **Test User Registration**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"email":"test@example.com", "username":"testuser", "password":"testpassword"}' http://localhost:8003/api/users
   ```

2. **Test User Login**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"test@example.com", "password":"testpassword"}' http://localhost:8003/api/token
   ```

3. **Test Tasks API (with token)**
   ```bash
   curl -X GET -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8003/api/tasks
   ```

## Key Questions to Resolve

1. **Schema Access Issues**:
   - Why are our RLS policies not effective? Do we need additional permissions?
   - What role is the application using when accessing the database (anon, authenticated, or service_role)?
   - Is there a mismatch between the schema specified in ClientOptions and the actual table paths?

2. **Authentication Strategy**:
   - Should we use Supabase Auth at all, or implement custom authentication entirely?
   - How can we securely manage user registration and login with the existing table structure?
   - Is the current integer-based ID system compatible with a JWT-based auth approach?

3. **Permission Model**:
   - What is the correct RLS policy configuration for our specific use case?
   - Do we need more granular permissions for different operations?
   - Should we use a service role key for specific admin operations?

4. **Integration Details**:
   - Do we need to specify the schema in each table query?
   - Are there any Supabase-specific quirks in accessing schemas different from 'public'?
   - Is our Supabase URL and API key correctly formatted and valid?

5. **Test Environment Considerations**:
   - How can we create an isolated test environment to verify the configuration?
   - Should we set up migrations to ensure schema consistency?
   - What logging can we add to diagnose permission issues more precisely?

6. **Backend Authentication Approach**:
   - Since we're not using Supabase Auth user tables, what's the best way to handle authentication tokens?
   - How should we generate, validate, and refresh JWT tokens for our custom users table?
   - What security measures should we implement for password storage and validation?

7. **Production Deployment**:
   - Once the development environment is working, what configuration changes are needed for production?
   - How should environment variables be managed securely in production?
   - What monitoring should be set up to detect authentication or permission issues in production?
