# Active Context

## Strategic Focus

-   **Primary Goal:** Database migration to Supabase
    -   ✅ Basic Docker container with Supabase integration 
    -   ✅ Configure Supabase tables and Row Level Security
    -   ✅ Migrate authentication endpoints to Supabase
    -   ⏩ Migrate remaining API endpoints from SQLite to Supabase
    -   ⏩ Implement WebSocket functionality with Supabase
-   **Secondary Goals:**
    -   Implement draggable task ordering
    -   Resolve web app connection longevity issues
    -   Continue Wear OS app development

## Current Work Focus

-   **HIGH PRIORITY: Complete Supabase implementation**
    -   ✅ Update Supabase API keys and server configuration
    -   ✅ Set up Row Level Security policies for all tables
    -   ⏩ Migrate remaining API endpoints using Supabase
    -   ⏩ Test and debug the Supabase integration
-   **HIGH PRIORITY: WebSocket integration**
    -   Adapt WebSocket implementation to work with Supabase
    -   Ensure timer state synchronization works across devices
    -   Implement persistent connection management
-   Implement draggable task ordering (frontend/backend)
-   Resolve web app connection longevity issues
-   Wear OS app development (current phase: build setup)

## Recent Changes

-   **Supabase Authentication Integration**
    -   ✅ Fixed Supabase client connection configuration
    -   ✅ Implemented proper environment variable handling
    -   ✅ Created new auth system using Supabase Auth
    -   ✅ Added support for both service role and anon access
    -   ✅ Created verification tools to test database access
-   **Supabase Security Model**
    -   ✅ Set up Row Level Security policies for all tables
    -   ✅ Configured table relationships and permissions
    -   ✅ Implemented proper user isolation for data
    -   ✅ Tested and verified security boundaries
-   **Docker Environment**
    -   ✅ Updated Docker configuration for Supabase
    -   ✅ Created .env example for documentation
    -   ✅ Improved error handling and logging
-   Supabase environment working in development without Docker

## Next Steps

1.  **Complete API endpoint migration**
    -   ⏩ Migrate tasks API to use Supabase
    -   ⏩ Migrate pomodoro sessions API to use Supabase
    -   ⏩ Test all API endpoints thoroughly
    -   ⏩ Update API documentation
2.  **Implement WebSocket with Supabase**
    -   Create Supabase compatible WebSocket manager
    -   Implement real-time synchronization
    -   Test multi-device synchronization
3.  **Frontend integration**
    -   Update frontend to work with new authentication flow
    -   Ensure all components use the new API correctly
    -   Optimize request handling and error management
4.  **Clean up repository**
    -   Remove unused files and old implementations
    -   Document new architecture and setup
    -   Create comprehensive tests for the new system

## Active Decisions & Considerations

-   **Supabase Auth Model**
    -   ✅ Using Supabase's built-in authentication system
    -   ✅ Leveraging database triggers for profile creation
    -   ✅ Using JWT tokens for authentication with Row Level Security
    -   ⏩ Considering adding support for social logins in the future
-   **WebSocket Strategy**
    -   Evaluating whether to use Supabase Realtime or custom WebSockets
    -   Need to ensure timer state can be synchronized across devices
    -   Consider fallback mechanisms for connection issues
-   **Data Migration**
    -   Need to develop a strategy for migrating existing user data to Supabase
    -   May need to provide a one-time migration utility
    -   Consider backward compatibility during transition
-   **Checkpoint States:** Decided on 10 state types with essential metadata
-   **Drag-and-Drop Approach:** Using `react-beautiful-dnd` over alternatives
-   **Wear OS Priority:** Focus on core timer before expanding features

## Connection Longevity Solution

The web app currently loses connection after extended periods of inactivity (2+ hours). This will be addressed with Supabase by:

1.  Implementing checkpoint states stored in Supabase database (design complete)
2.  Leveraging Supabase Realtime for enhanced connection management (in design phase)
3.  Implementing robust reconnection strategies with exponential backoff (pending)

## Current Task Status

-   **Supabase Docker Integration:** ✅ Complete and verified working
-   **Supabase Auth:** ✅ Implemented and tested
-   **Row Level Security:** ✅ Configured and tested
-   **API endpoints:** ⏩ In progress - User endpoints complete, others pending
-   **WebSocket implementation:** 🔜 Planned - Design in progress
-   **Drag-and-drop implementation:** Complete but needs debugging
-   **Connection longevity:** Design phase complete, implementation pending
-   **Wear OS app:** Setup in progress, developing in Android Studio on Windows with git syncs to Linux
