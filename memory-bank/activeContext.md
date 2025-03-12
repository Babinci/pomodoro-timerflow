# Active Context

# Current work focus

i have problem sometimes if i have web app opened like for 2 hours and i am not active- i lost connection

this is bad

i should not lose connection

this should be like this:

if there is of working session/ break/ long break and i am not comming to computer even for long time- i should be able to use it like normally- so state should be saved

look for potential code issues with that

 think we should store in database states like  a checkpoints

Checkpoint States

WORK_STARTED - When a work session begins
WORK_COMPLETED - When a work session naturally ends
WORK_INTERRUPTED - When a work session is manually skipped
SHORT_BREAK_STARTED - When a short break begins
SHORT_BREAK_COMPLETED - When a short break naturally ends
SHORT_BREAK_INTERRUPTED - When a short break is manually skipped
LONG_BREAK_STARTED - When a long break begins
LONG_BREAK_COMPLETED - When a long break naturally ends
LONG_BREAK_INTERRUPTED - When a long break is manually skipped
SESSION_PAUSED - When any session is paused
SESSION_RESUMED - When a paused session is resumed

Essential Metadata for Each Checkpoint

Timestamp
User ID
Task ID (if applicable)
Remaining time at checkpoint
Round number
Preset type (short/long)

so i am going on that

timer problems (current status- implemented changes of those now testing):


## Status
bugs seems to be fixed, moving to wear os app

## Task: Implement draggable task ordering

**Objective:** Implement draggable task ordering in the web app, involving changes in both the backend and frontend.

**Steps Taken:**

1.  **Planning:** Created an initial implementation plan that included database schema updates, backend API changes, frontend component updates, and WebSocket integration.
2.  **Revised Plan:** Adjusted the plan to exclude database migrations based on user feedback.
3.  **Frontend Implementation:**
    *   Installed the `react-beautiful-dnd` package.
    *   Modified the `TaskList` component to incorporate drag-and-drop functionality using `react-beautiful-dnd`.
    *   Implemented functions to save and update task order in local storage.
4.  **Backend Adjustments:**
    *   Modified the tasks router to handle task ordering without database schema changes.
    *   Added a new endpoint (`/tasks/order`) to update the task order.
    *   Modified the schemas to include a `TaskOrder` schema.
5.  **WebSocket Integration:**
    *   Modified the `useWebSocket` hook to handle task order updates.
    *   Updated the `TaskList` component to use the WebSocket for real-time order updates.

**Current Status:**

The implementation is complete, but the user is reporting that they are unable to reorder tasks by dragging. Further debugging is required.
