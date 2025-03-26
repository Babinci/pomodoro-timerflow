# Active Context

## Strategic Focus
- **Primary Goal:** Database migration to Supabase
  - Install Supabase locally
  - Create MCP server for Supabase interaction
  - Migrate from SQLite to Supabase (tables, auth, websockets)
- **Secondary Goals:**
  - Implement draggable task ordering
  - Resolve web app connection longevity issues
  - Continue Wear OS app development

## Current Work Focus
- Resolve database migrations problems (HIGH PRIORITY)
  - Supabase integration with tables as chosen solution
  - Later extend to websockets and auth change
- Implement draggable task ordering (frontend/backend)
- Resolve web app connection longevity issues
- Wear OS app development (current phase: build setup)

## Recent Changes
- Added `react-beautiful-dnd` for task reordering
- Created backend `/tasks/order` endpoint
- WebSocket integration for real-time task updates

## Next Steps
1. Complete Supabase integration
   - Install Supabase locally
   - Create MCP server for interaction
   - Migrate database schema
2. Debug drag-and-drop functionality in TaskList component (see task_implementations/drag_and_drop_implementation.md)
3. Implement session checkpoint states (see checkpoint_states.md)
4. Implement connection keep-alive mechanism
5. Transition to Wear OS app development

## Active Decisions & Considerations
- **Database Strategy:** Migrate to Supabase for better scalability and features
  - Store timer states with:
    - Timestamp
    - User ID
    - Remaining time
    - Round number
    - Preset type
- **Venv Credentials Handling:**
  - Currently using environment variables for credentials
  - Need to implement secure credential storage solution
  - Todo: Research and implement proper credential management
- **Checkpoint States:** Decided on 10 state types with essential metadata (details in checkpoint_states.md)
- **Drag-and-Drop Approach:** Using `react-beautiful-dnd` over alternatives
- **Wear OS Priority:** Focus on core timer before expanding features

## Connection Longevity Solution
The web app currently loses connection after extended periods of inactivity (2+ hours). This will be addressed by:
1. Implementing checkpoint states to save timer progress
2. Creating a connection keep-alive mechanism
3. Ensuring state persistence across sessions

This will allow users to return to their session after periods of inactivity without losing progress, even during work sessions, breaks, or long breaks.

## Current Task Status
- **Drag-and-drop implementation:** Complete but needs debugging (see task_implementations/drag_and_drop_implementation.md)
- **Connection longevity:** Planning phase, will implement checkpoint states
- **Wear OS app:** Setup in progress, developing in Android Studio on Windows with git syncs to Linux
