# API Migration Plan: Task Order Updates

## Objective
Remove WebSocket-based task ordering functionality and consolidate all drag-and-drop updates through the existing `update_tasks_order` API endpoint.

---

## Phase 1: Backend Cleanup (Est. 2hrs)
1. **Remove WebSocket Handlers**
   - File: `backend/app/routers/pomodoro_websocket.py`
   - Actions:
     - Delete any `@websocket.on(...)` decorators handling:
       - `task_reorder` events
       - `drag_start`/`drag_end` events
     - Remove related helper methods (e.g., `broadcast_task_order()`)

2. **Strengthen API Endpoint**
   - File: `backend/app/routers/tasks.py` - update_tasks_order
   - Actions:
     - Add validation for task order payloads
     - Implement proper error handling
     - Add database transaction rollback on failure
     - Update response model to include order verification

---

## Phase 2: Frontend Migration (Est. 4hrs)
1. **Identify WebSocket Usage**
   - Likely locations:
     - Drag context providers
     - Task list components
     - Custom hooks (`useWebSocketDrag`)

2. **Replace with API Calls**
   - Create service module:
   ```javascript:src/services/taskService.js
   export const updateTaskOrder = async (newOrder) => {
     try {
       const response = await api.put('/tasks/update_tasks_order', {
         order: newOrder
       });
       return response.data;
     } catch (error) {
       throw new Error('Failed to update task order');
     }
   };
   ```

3. **Update Drag Handlers**
   - Before:
   ```javascript
   const handleDragEnd = (result) => {
     websocket.emit('task_reorder', newOrder);
   };
   ```
   - After:
   ```javascript
   const handleDragEnd = async (result) => {
     try {
       await updateTaskOrder(newOrder);
     } catch (error) {
       showErrorToast('Failed to save new order');
     }
   };
   ```

---

## Phase 3: Testing & Validation (Est. 3hrs)
1. **Test Scenarios**
   - Basic drag reordering
   - Network failure during drag
   - Concurrent updates from multiple tabs
   - Large lists (>100 items)

2. **Monitoring**
   - Add Sentry/Rollbar tracking to update endpoint
   - Log success/failure rates in analytics

---

## Phase 4: Cleanup (Est. 1hr)
1. **Remove Deprecated Packages**
   - Check `requirements.txt` for unused WebSocket dependencies
   - Remove frontend WebSocket libraries if unused elsewhere

2. **Update Documentation**
   - Remove WebSocket examples from API docs
   - Add new sequence diagram for order updates

---

!!!! Important!!!

all other parts with websockets on frontend and backend that are not part of drag and drop- they must stay untouched!!!


