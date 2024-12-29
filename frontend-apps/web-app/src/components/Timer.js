// src/components/Timer.js
import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles, colors } from '../styles/styles';

export default function Timer({ currentTask, currentPreset, setCurrentPreset, settings, ws: { ws, isConnected } }) {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionType, setSessionType] = useState('work');
  const [currentSessionNumber, setCurrentSessionNumber] = useState(1);

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Timer received message:', data);

      // Handle timer_sync message from backend
      if (data.type === 'timer_sync') {
        const { task_id, session_type, remaining_time, is_paused } = data.data;
        
        setTimeLeft(remaining_time);
        setSessionType(session_type);
        setIsRunning(!is_paused);
        
        // Update current task if needed
        if (task_id !== currentTask?.id) {
          // You might want to fetch task details here or handle this differently
          console.log('Task ID mismatch:', task_id, currentTask?.id);
        }
      }

      // Handle timer_stopped message
      if (data.type === 'timer_stopped') {
        setIsRunning(false);
        updateTimerDurations(); // Reset to default duration
      }
    };
  }, [ws, currentTask]);

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

  const startTimer = () => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      alert('Not connected to server. Please try again.');
      return;
    }

    if (!currentTask) {
      alert('Please select a task first');
      return;
    }

    // Modified to match backend message structure
    ws.send(JSON.stringify({
      type: 'start',
      task_id: currentTask.id,
      session_type: sessionType,
      duration: timeLeft
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

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Regular interval to request sync from server
  useEffect(() => {
    if (!ws || !isConnected) return;

    const interval = setInterval(() => {
      ws.send(JSON.stringify({ type: 'sync_request' }));
    }, 1000);

    return () => clearInterval(interval);
  }, [ws, isConnected]);

  // Rest of the component remains the same...
  return (
    <View style={styles.card}>
      {/* Connection status indicator */}
      <View style={{ alignItems: 'center', marginBottom: 8 }}>
        <Text style={{ color: isConnected ? colors.success : colors.danger }}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </Text>
      </View>

      {/* Timer controls */}
      <View style={styles.timerContainer}>
        <Text style={styles.timerDisplay}>{formatTime(timeLeft)}</Text>
        <Text style={[styles.text, { marginTop: 8 }]}>
          {sessionType === 'work' && currentTask
            ? `Work Session - ${currentTask.title}`
            : sessionType === 'short_break'
            ? 'Short Break'
            : 'Long Break'}
        </Text>

        <View style={{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginTop: 24 }}>
          {!isRunning ? (
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.success }]}
              onPress={startTimer}
            >
              <Text style={styles.buttonText}>Start</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.warning }]}
              onPress={pauseTimer}
            >
              <Text style={styles.buttonText}>Pause</Text>
            </TouchableOpacity>
          )}
          <TouchableOpacity
            style={[styles.button, { backgroundColor: colors.danger }]}
            onPress={stopTimer}
          >
            <Text style={styles.buttonText}>Stop</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}