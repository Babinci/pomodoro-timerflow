# Active Context

## Strategic Focus

-   **Primary Goal:** Database migration to Supabase
    -   ✅ Basic Docker container with Supabase integration 
    -   Configure Supabase tables and Row Level Security
    -   Migrate all API endpoints from SQLite to Supabase
    -   Implement WebSocket functionality with Supabase
-   **Secondary Goals:**
    -   Implement draggable task ordering
    -   Resolve web app connection longevity issues
    -   Continue Wear OS app development

## Current Work Focus

-   **HIGH PRIORITY: Configure Supabase security and tables**
    -   Update Supabase API keys and server configuration
    -   Set up Row Level Security policies for all tables
    -   Implement remaining API endpoints using Supabase
-   **HIGH PRIORITY: Credentials management**
    -   Review and secure API keys and tokens
    -   Clean up repository of sensitive data
    -   Implement proper environment variable management
-   Implement draggable task ordering (frontend/backend)
-   Resolve web app connection longevity issues
-   Wear OS app development (current phase: build setup)

## Recent Changes

-   **Supabase Docker Integration**
    -   Created dedicated Supabase requirements file
    -   Modified Dockerfile to use Supabase instead of SQLite
    -   Implemented clean FastAPI entry point to bypass SQLAlchemy dependencies
    -   Successfully built and ran Docker container with Supabase connection
    -   Created detailed implementation plan and action checklist
-   Added `react-beautiful-dnd` for task reordering
-   Created backend `/tasks/order` endpoint
-   WebSocket integration for real-time task updates
-   Organized Supabase documentation into manageable files

## Next Steps

1.  **Immediately: Update Supabase tokens and server configuration**
    -   Update API keys in the server environment
    -   Configure proper server URL and credentials
    -   Test connection with real Supabase instance
2.  **Configure Supabase tables and security**
    -   Set up Row Level Security policies
    -   Configure table relationships and indexes
    -   Set up authentication flow
3.  **Implement Supabase API endpoints**
    -   Complete user authentication with Supabase Auth
    -   Implement task management endpoints
    -   Implement Pomodoro session endpoints
4.  **Implement WebSocket with Supabase**
    -   Create Supabase compatible WebSocket manager
    -   Implement real-time synchronization
5.  **Clean up repository**
    -   Remove unused files and old implementations
    -   Secure sensitive tokens and credentials
    -   Document new architecture and setup

## Active Decisions & Considerations

-   **Docker Implementation Strategy:** 
    -   Decided on a clean implementation (`main_clean.py`) that avoids SQLAlchemy dependencies
    -   Using in-memory SQLite for remaining SQLAlchemy dependencies as needed
    -   Long-term plan to completely remove SQLAlchemy dependencies
-   **Supabase Security Model:**
    -   Will implement Row Level Security at the database level
    -   Each user will only access their own data
    -   Using JWT authentication with Supabase Auth
-   **Credentials Management:**
    -   Need to immediately update API keys and server URLs
    -   Will implement proper .env file management with Docker secrets
    -   Need to clean repository of any committed credentials
-   **WebSocket Strategy:**
    -   Will create new WebSocket implementation using Supabase
    -   May use Supabase Realtime for enhanced functionality
-   **Checkpoint States:** Decided on 10 state types with essential metadata (details in checkpoint_states.md)
-   **Drag-and-Drop Approach:** Using `react-beautiful-dnd` over alternatives
-   **Wear OS Priority:** Focus on core timer before expanding features

## Connection Longevity Solution

The web app currently loses connection after extended periods of inactivity (2+ hours). This will be addressed with Supabase by:

1.  Implementing checkpoint states stored in Supabase database
2.  Leveraging Supabase Realtime for enhanced connection management
3.  Implementing robust reconnection strategies with exponential backoff

This approach will be more reliable than the current WebSocket implementation and will allow for better state persistence across devices.

## Current Task Status

-   **Supabase Docker Integration:** Basic implementation complete, needs security configuration
-   **API endpoints:** New implementation needed with Supabase
-   **WebSocket implementation:** Needs complete redesign with Supabase
-   **Drag-and-drop implementation:** Complete but needs debugging (see task_implementations/drag_and_drop_implementation.md)
-   **Connection longevity:** Will be addressed with Supabase implementation
-   **Wear OS app:** Setup in progress, developing in Android Studio on Windows with git syncs to Linux
