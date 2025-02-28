import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles, colors } from '../styles/styles';

export default function Timer({ currentTask, currentPreset, setCurrentPreset, settings, ws: { ws, isConnected }, setTimerCountdown }) {
  const [timeLeft, setTimeLeft] = useState(settings?.[currentPreset]?.work_duration * 60 || 25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionType, setSessionType] = useState('work');
  const [roundNumber, setRoundNumber] = useState(1);
  const [activeTask, setActiveTask] = useState(null);
  const [showStartBreak, setShowStartBreak] = useState(false);

  // Notify server about preset type changes
  useEffect(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'change_preset',
        preset_type: currentPreset
      }));
    }
  }, [currentPreset, ws]);

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'timer_sync') {
        const { preset_type, ...otherData } = data.data;
        
        if (preset_type && preset_type !== currentPreset) {
          setCurrentPreset(preset_type);
        }
        
        setTimeLeft(otherData.remaining_time);
        setTimerCountdown(formatTime(otherData.remaining_time));
        setSessionType(otherData.session_type);
        setIsRunning(!otherData.is_paused);
        if (otherData.round_number) setRoundNumber(otherData.round_number);
        
        if (otherData.active_task) {
          setActiveTask(otherData.active_task);
          if (otherData.remaining_time === 0 && otherData.session_type.includes('break')) {
            setShowStartBreak(true);
          }
        }
      }
    };
  }, [ws]);

  useEffect(() => {
    const formattedTime = formatTime(timeLeft);
    setTimerCountdown(formattedTime);
    console.log('Timer timeLeft:', timeLeft, 'formattedTime:', formattedTime);
  }, [timeLeft, setTimerCountdown]);

  const updateTimerDurations = useCallback(() => {
    if (!settings) return;
    const current = settings[currentPreset];
          
    if (sessionType === 'work') {
      setTimeLeft(current.work_duration * 60);
    } else if (sessionType === 'short_break') {
      setTimeLeft(current.short_break * 60);
    } else if (sessionType === 'long_break') {
      setTimeLeft(current.long_break * 60);
    }
  }, [settings, currentPreset, sessionType]);

  useEffect(() => {
    updateTimerDurations();
  }, [currentPreset, updateTimerDurations]);

  // Regular interval to request sync from server
  useEffect(() => {
    if (!ws || !isConnected) return;

    const interval = setInterval(() => {
      ws.send(JSON.stringify({
        type: 'sync_request',
        preset_type: currentPreset
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, [ws, isConnected, currentPreset]);

  const startTimer = () => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      alert('Not connected to server. Please try again.');
      return;
    }

    if (!currentTask && sessionType === 'work' && !activeTask) {
      alert('Please select a task first');
      return;
    }

    setShowStartBreak(false);
    ws.send(JSON.stringify({
      type: 'start',
      task_id: currentTask?.id || activeTask?.id,
      session_type: sessionType,
      duration: timeLeft,
      preset_type: currentPreset  // Always send current preset type
    }));
  };

  const pauseTimer = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'pause' }));
    }
  };

  const resumeTimer = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'resume' }));
    }
  };

  const stopTimer = () => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'stop' }));
      }
    };
  
    const resetAllRounds = () => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'reset_rounds' }));
      }
    };

  const skipToNextSession = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'skip_to_next' }));
    }
  };

  const handleSkip = () => {
    if (!isRunning) return;
      
    if (ws?.readyState === WebSocket.OPEN) {
      skipToNextSession();
      // Timer will be automatically paused by the server
    }
  };

  // Handle rounds reset response from server
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Display logic for session info and progress
  const getSessionDisplay = () => {
    const task = activeTask || currentTask;
    if (sessionType === 'work' && task) {
      return `Work Session - ${task.title} (${task.completed_pomodoros}/${task.estimated_pomodoros})`;
    } else if (sessionType === 'short_break') {
      return 'Short Break';
    } else {
      return 'Long Break';
    }
  };

  return (
    <View style={styles.card}>
      <View style={styles.timerContainer}>
        {/* Header */}
        <View style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 16
        }}>
          <Text style={styles.text}>Round {roundNumber}/4</Text>
          <View style={{ flexDirection: 'row', gap: 8 }}>
            <TouchableOpacity
              style={[
                styles.button,
                currentPreset === 'short' && { backgroundColor: colors.primary }
              ]}
              onPress={() => {
                setCurrentPreset('short');
                if (ws?.readyState === WebSocket.OPEN) {
                  ws.send(JSON.stringify({
                    type: 'change_preset',
                    preset_type: 'short'
                  }));
                }
              }}
            >
              <Text style={styles.buttonText}>Short</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.button,
                currentPreset === 'long' && { backgroundColor: colors.primary }
              ]}
              onPress={() => {
                setCurrentPreset('long');
                if (ws?.readyState === WebSocket.OPEN) {
                  ws.send(JSON.stringify({
                    type: 'change_preset',
                    preset_type: 'long'
                  }));
                }
              }}
            >
              <Text style={styles.buttonText}>Long</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Timer display and controls */}
        <View style={{
          width: '100%',
          maxWidth: 400,
          alignSelf: 'center'
        }}>
          <View style={{
            width: '100%',
            marginBottom: 24,
            position: 'relative'
          }}>
            <Text style={[
              styles.timerDisplay,
              {
                fontSize: 48,
                fontWeight: 'bold',
                color: colors.text,
                textAlign: 'center'
              }
            ]}>
              {formatTime(timeLeft)}
            </Text>

            <TouchableOpacity
              style={{
                position: 'absolute',
                right: 0,
                top: '50%',
                transform: [{ translateY: -20 }],
                backgroundColor: colors.primary,
                width: 40,
                height: 40,
                borderRadius: 20,
                justifyContent: 'center',
                alignItems: 'center',
                opacity: isRunning ? 1 : 0.5
              }}
              onPress={handleSkip}
            >
              <Text style={{ color: 'white', fontSize: 20 }}>→</Text>
            </TouchableOpacity>

            <Text style={[
              styles.text,
              {
                textAlign: 'center',
                fontSize: 16,
                color: colors.text,
                marginTop: 8
              }
            ]}>
              {getSessionDisplay()}
            </Text>
          </View>

          {/* Control buttons */}
          <View style={{
            flexDirection: 'row',
            justifyContent: 'center',
            gap: 16
          }}>
            {!isRunning ? (
              <TouchableOpacity
                style={[styles.button, { backgroundColor: colors.success }]}
                onPress={startTimer}
              >
                <Text style={styles.buttonText}>
                  {showStartBreak ? 'Start Break' : 'Start'}
                </Text>
              </TouchableOpacity>
            ) : (
              <>
                <TouchableOpacity
                  style={[styles.button, { backgroundColor: colors.warning }]}
                  onPress={pauseTimer}
                >
                  <Text style={styles.buttonText}>Pause</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.button, { backgroundColor: colors.success }]}
                  onPress={resumeTimer}
                >
                  <Text style={styles.buttonText}>Resume</Text>
                </TouchableOpacity>
              </>
            )}
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.danger }]}
              onPress={stopTimer}
            >
              <Text style={styles.buttonText}>Stop</Text>
            </TouchableOpacity>
            
            {/* Add this new Reset All Rounds button */}
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.warning }]}
              onPress={resetAllRounds}
            >
              <Text style={styles.buttonText}>Reset All Rounds</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </View>
  );
}