diff --git a/backend/app/main.py b/backend/app/main.py
index ff2a575..2cc4f36 100644
--- a/backend/app/main.py
+++ b/backend/app/main.py
@@ -291,6 +291,51 @@ async def websocket_endpoint(
                     await manager.sync_timer_state(user_id)
                     await manager.broadcast_to_user(user_id, {"type": "rounds_reset"})
 
+                elif data["type"] == "set_timezone":
+                    timezone_offset = data.get("timezone_offset", 0)
+                    if user_id in manager.timer_states:
+                        manager.timer_states[user_id].set_timezone_offset(timezone_offset)
+                    else:
+                        # If no timer state exists, create a default one with the timezone
+                        # Load user settings first
+                        user = db.query(models.User).filter(models.User.id == user_id).first()
+                        if user:
+                            # Create default timer state
+                            manager.timer_states[user_id] = TimerState(
+                                task_id=None,
+                                session_type='work',
+                                time_remaining=user.pomodoro_settings['short']['work_duration'] * 60,
+                                user_settings=user.pomodoro_settings,
+                                preset_type='short'
+                            )
+                            manager.timer_states[user_id].set_timezone_offset(timezone_offset)
+                            # Sync immediately
+                            await manager.sync_timer_state(user_id)
+
+                elif data["type"] == "sync_request":
+                    if user_id not in manager.timer_states:
+                        # Create a default timer state if none exists
+                        user = db.query(models.User).filter(models.User.id == user_id).first()
+                        if user:
+                            # Create default timer state with user settings
+                            default_preset = 'short'
+                            work_duration = user.pomodoro_settings[default_preset]['work_duration']
+                            
+                            manager.timer_states[user_id] = TimerState(
+                                task_id=None,
+                                session_type='work',
+                                time_remaining=work_duration * 60,
+                                user_settings=user.pomodoro_settings,
+                                preset_type=default_preset
+                            )
+                            
+                            # Log the creation of default state
+                            logger.info(f"Created default timer state for user {user_id}")
+                    
+                    # Always send a sync response, even if we just created the state
+                    await manager.sync_timer_state(user_id)
+                    logger.info(f"Sent timer sync to user {user_id}")
+
                 # Add a new handler for preset type changes
                 elif data["type"] == "change_preset":
                     if user_id in manager.timer_states:
diff --git a/backend/app/ws_manager.py b/backend/app/ws_manager.py
index e0e36da..2d0e351 100644
--- a/backend/app/ws_manager.py
+++ b/backend/app/ws_manager.py
@@ -18,6 +18,13 @@ class TimerState:
         self.settings = user_settings  # Use user's actual settings
         self.active_task = None  # Store the active task details
         self.session_completed = False  # New flag to track session completion
+        # Add these new fields for daily reset
+        self.last_daily_reset = datetime.now(timezone.utc)
+        self.timezone_offset = 0  # Will be set by client in minutes
+
+    def set_timezone_offset(self, offset_minutes: int):
+        """Set the client's timezone offset in minutes"""
+        self.timezone_offset = offset_minutes
 
     def update_remaining_time(self):
         """Update remaining time if timer is running"""
@@ -33,6 +40,44 @@ class TimerState:
             
         self.last_update = datetime.now(timezone.utc)
 
+    def update_remaining_time(self):
+        """Update remaining time if timer is running and check for daily reset"""
+        current_time = datetime.now(timezone.utc)
+        
+        # Check for daily reset at 5 AM in user's local time
+        # Convert UTC to user's local time by subtracting the timezone offset
+        # (offset is in minutes, positive for behind UTC, negative for ahead)
+        user_local_time = current_time - timedelta(minutes=self.timezone_offset)
+        reset_hour = 5  # 5 AM local time
+        
+        # If it's past 5 AM and we haven't reset today
+        last_reset_local = self.last_daily_reset - timedelta(minutes=self.timezone_offset)
+        current_date = user_local_time.date()
+        last_reset_date = last_reset_local.date()
+        
+        if (current_date > last_reset_date and user_local_time.hour >= reset_hour):
+            # Reset for new day
+            self.round_number = 1
+            self.session_type = 'work'
+            self.is_paused = True
+            self.time_remaining = self.settings[self.preset_type]['work_duration'] * 60
+            self.last_daily_reset = current_time
+            self.session_completed = False
+            return
+        
+        # Continue with regular time update logic
+        if not self.is_paused:
+            elapsed = (current_time - self.last_update).total_seconds()
+            new_time = max(0, self.time_remaining - elapsed)
+            
+            # Check if timer just reached 0
+            if new_time == 0 and self.time_remaining > 0:
+                self.session_completed = True
+            
+            self.time_remaining = new_time
+            
+        self.last_update = datetime.now(timezone.utc)
+
     def get_remaining_time(self) -> int:
         """Get current remaining time"""
         self.update_remaining_time()
diff --git a/frontend-apps/web-app/src/components/Timer.js b/frontend-apps/web-app/src/components/Timer.js
index eaf882d..95c049a 100644
--- a/frontend-apps/web-app/src/components/Timer.js
+++ b/frontend-apps/web-app/src/components/Timer.js
@@ -6,6 +6,7 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
   const [timeLeft, setTimeLeft] = useState(25 * 60);
   const [isRunning, setIsRunning] = useState(false);
   const [sessionType, setSessionType] = useState('work');
+  const [initialized, setInitialized] = useState(false);
   const [roundNumber, setRoundNumber] = useState(1);
   const [presetType, setPresetType] = useState(currentPreset || 'short');
   const [activeTask, setActiveTask] = useState(null);
@@ -60,8 +61,42 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
             setShowStartBreak(true);
           }
         }
+        
+        // Mark as initialized after receiving first sync
+        if (!initialized) {
+          setInitialized(true);
+        }
+      }
+      console.log('WebSocket raw message:', event.data);
+      
+      try {
+        const data = JSON.parse(event.data);
+        console.log('Timer received message:', data);
+
+        if (data.type === 'timer_sync') {
+          // Existing sync code...
+          
+          // Make sure to log initialization
+          console.log('Setting initialized to true');
+          setInitialized(true);
+        }
+      } catch (error) {
+        console.error('Error parsing WebSocket message:', error);
       }
 
+      // Add a timeout to prevent being stuck in the loading state
+      useEffect(() => {
+        if (!initialized) {
+          // Set a 5-second timeout to force initialization if sync doesn't happen
+          const timeoutId = setTimeout(() => {
+            console.log('Forcing initialization after timeout');
+            setInitialized(true);
+          }, 5000);
+          
+          return () => clearTimeout(timeoutId);
+        }
+      }, [initialized]);
+
       if (data.type === 'timer_stopped') {
         setIsRunning(false);
         setShowStartBreak(false);
@@ -75,14 +110,6 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
         setIsRunning(false);
         setShowStartBreak(false);
       }
-      if (data.type === 'rounds_reset') {
-        // Reset local round state
-        setRoundNumber(1);
-        setSessionType('work');
-        updateTimerDurations();
-        setIsRunning(false);
-        setShowStartBreak(false);
-      }
     };
   }, [ws]);
 
@@ -124,7 +151,7 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
   }, [ws, isConnected, presetType]);
 
   const startTimer = () => {
-    if (!ws || ws.readyState !== WebSocket.OPEN) {
+    if (!initialized || !ws || ws.readyState !== WebSocket.OPEN) {
       alert('Not connected to server. Please try again.');
       return;
     }
@@ -145,30 +172,55 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
   };
 
   const pauseTimer = () => {
+    if (!initialized || !ws || ws?.readyState !== WebSocket.OPEN) {
+      alert('Not connected to server. Please try again.');
+      return;
+    }
     if (ws?.readyState === WebSocket.OPEN) {
       ws.send(JSON.stringify({ type: 'pause' }));
     }
   };
 
   const resumeTimer = () => {
+    if (!initialized || !ws || ws?.readyState !== WebSocket.OPEN) {
+      alert('Not connected to server. Please try again.');
+      return;
+    }
     if (ws?.readyState === WebSocket.OPEN) {
       ws.send(JSON.stringify({ type: 'resume' }));
     }
   };
 
   const stopTimer = () => {
-      if (ws?.readyState === WebSocket.OPEN) {
-        ws.send(JSON.stringify({ type: 'stop' }));
-      }
-    };
+    if (!initialized || !ws || ws?.readyState !== WebSocket.OPEN) {
+      alert('Not connected to server. Please try again.');
+      return;
+    }
+    if (ws?.readyState === WebSocket.OPEN) {
+      ws.send(JSON.stringify({ type: 'stop' }));
+    }
+  };
+
+  const resetAllRounds = () => {
+    if (!initialized || !ws || ws?.readyState !== WebSocket.OPEN) {
+      alert('Not connected to server. Please try again.');
+      return;
+    }
+    if (ws?.readyState === WebSocket.OPEN) {
+      ws.send(JSON.stringify({ type: 'reset_rounds' }));
+    }
+  };
   
-    const resetAllRounds = () => {
-      if (ws?.readyState === WebSocket.OPEN) {
-        ws.send(JSON.stringify({ type: 'reset_rounds' }));
+    useEffect(() => {
+      if (ws && ws.readyState === WebSocket.OPEN) {
+        ws.send(JSON.stringify({
+          type: 'set_timezone',
+          timezone_offset: new Date().getTimezoneOffset()
+        }));
       }
-    };
-
-  const skipToNextSession = () => {
+    }, [ws, isConnected]);
+  
+    const skipToNextSession = () => {
     if (ws?.readyState === WebSocket.OPEN) {
       ws.send(JSON.stringify({ type: 'skip_to_next' }));
     }
@@ -202,6 +254,25 @@ export default function Timer({ currentTask, currentPreset, setCurrentPreset, se
     }
   };
 
+  if (!initialized) {
+    return (
+      <View style={styles.card}>
+        <View style={styles.timerContainer}>
+          <Text style={styles.text}>Syncing timer state...</Text>
+          <Text style={[styles.smallText, {marginTop: 8}]}>
+            Connection status: {isConnected ? 'Connected' : 'Disconnected'}
+          </Text>
+          <TouchableOpacity
+            style={[styles.button, {marginTop: 16}]}
+            onPress={() => setInitialized(true)}
+          >
+            <Text style={styles.buttonText}>Continue Anyway</Text>
+          </TouchableOpacity>
+        </View>
+      </View>
+    );
+  }
+
   return (
     <View style={styles.card}>
       <View style={styles.timerContainer}>
diff --git a/frontend-apps/web-app/src/hooks/useWebSocket.js b/frontend-apps/web-app/src/hooks/useWebSocket.js
index 5bde29b..fb0d031 100644
--- a/frontend-apps/web-app/src/hooks/useWebSocket.js
+++ b/frontend-apps/web-app/src/hooks/useWebSocket.js
@@ -34,6 +34,21 @@ export default function useWebSocket(token) {
         websocket.send(JSON.stringify({
           type: 'sync_request'
         }));
+
+        // Immediately request timer state sync on connection or reconnection
+        websocket.send(JSON.stringify({
+          type: 'sync_request'
+        }));
+
+        // Add console log to confirm sync request is being sent
+        console.log('Sending initial sync request');
+        try {
+          websocket.send(JSON.stringify({
+            type: 'sync_request'
+          }));
+        } catch (error) {
+          console.error('Error sending sync request:', error);
+        }
       };
       
       websocket.onmessage = (event) => {
