from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
import logging
from .. import auth_supabase
from ..ws_manager_supabase import manager

router = APIRouter(tags=["pomodoro_websocket"])

logger = logging.getLogger(__name__)

@router.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None),
):
    logger.info(f"WebSocket connection attempt with token: {token}")
    if not token:
        await websocket.close()
        return

    try:
        # Verify token and get user
        user_data = await auth_supabase.verify_token(token)
        if not user_data:
            await websocket.close()
            return
          
        user_id = str(user_data["user_id"])
        logger.info(f"User authenticated: {user_id}")
        
        await manager.connect(websocket, user_id)
          
        while True:
            try:
                data = await websocket.receive_json()
                  
                if data["type"] == "start":
                    # Get user settings from Supabase
                    try:
                        user_response = await websocket.app.supabase.table("users").select("pomodoro_settings").eq("id", user_id).execute()
                        user_settings = user_response.data[0]["pomodoro_settings"] if user_response.data else None
                        
                        if not user_settings:
                            # Default settings if not found
                            user_settings = {
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
                            }
                    except Exception as e:
                        logger.error(f"Error getting user settings: {str(e)}")
                        # Default settings
                        user_settings = {
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
                        }
                    
                    # Start new timer session
                    manager.start_timer(
                        user_id=user_id,
                        task_id=data["task_id"],
                        session_type=data["session_type"],
                        duration=data["duration"],
                        preset_type=data.get("preset_type", "short"),
                        user_settings=user_settings
                    )
                    await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "stop":
                    manager.stop_timer(user_id)
                    await manager.broadcast_to_user(user_id, {"type": "timer_stopped"})
                  
                elif data["type"] == "pause":
                    if user_id in manager.timer_states:
                        manager.timer_states[user_id].pause()
                        await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "resume":
                    if user_id in manager.timer_states:
                        manager.timer_states[user_id].resume()
                        await manager.sync_timer_state(user_id)
                  
                elif data["type"] == "sync_request":
                    await manager.sync_timer_state(user_id)
                    
                elif data["type"] == "skip_to_next":
                    if user_id in manager.timer_states:
                        manager.skip_to_next(user_id)
                        await manager.sync_timer_state(user_id)

                elif data["type"] == "reset_rounds":
                    # Reset rounds for the user
                    manager.reset_rounds(user_id)
                    await manager.sync_timer_state(user_id)
                    await manager.broadcast_to_user(user_id, {"type": "rounds_reset"})
                
                elif data["type"] == "settings_updated":
                    # Refresh the user settings in memory
                    try:
                        user_response = await websocket.app.supabase.table("users").select("pomodoro_settings").eq("id", user_id).execute()
                        if user_response.data and len(user_response.data) > 0:
                            user_settings = user_response.data[0]["pomodoro_settings"]
                            if user_id in manager.timer_states:
                                manager.timer_states[user_id].settings = user_settings
                        
                        # Notify all clients about settings update
                        await manager.broadcast_to_user(user_id, {
                            "type": "settings_updated",
                            "data": {
                                "settings": user_settings
                            }
                        })
                    except Exception as e:
                        logger.error(f"Error refreshing settings: {str(e)}")
                    
                    # Force timer state sync
                    await manager.sync_timer_state(user_id)
                
                # Add a new handler for preset type changes
                elif data["type"] == "change_preset":
                    if user_id in manager.timer_states:
                        manager.timer_states[user_id].preset_type = data["preset_type"]
                        # Update timer duration based on new preset type and current session
                        state = manager.timer_states[user_id]
                        current_session = state.session_type
                        if current_session == 'work':
                            state.time_remaining = state.settings[data["preset_type"]]['work_duration'] * 60
                        elif current_session == 'short_break':
                            state.time_remaining = state.settings[data["preset_type"]]['short_break'] * 60
                        else:  # long_break
                            state.time_remaining = state.settings[data["preset_type"]]['long_break'] * 60
                        await manager.sync_timer_state(user_id)

            except WebSocketDisconnect:
                await manager.disconnect(websocket, user_id)
                return

    except Exception as e:
        logger.exception(f"WebSocket Error: {str(e)}")
        if not websocket.client_state.DISCONNECTED:
            await websocket.close()
