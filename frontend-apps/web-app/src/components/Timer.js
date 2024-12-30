import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles, colors } from '../styles/styles';

export default function Timer({ currentTask, currentPreset, setCurrentPreset, settings, ws: { ws, isConnected } }) {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionType, setSessionType] = useState('work');
  const [roundNumber, setRoundNumber] = useState(1);
  const [presetType, setPresetType] = useState('short'); // 'short' or 'long'

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (!ws) return;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Timer received message:', data);

      if (data.type === 'timer_sync') {
        const { task_id, session_type, remaining_time, is_paused, round_number } = data.data;
        
        setTimeLeft(remaining_time);
        setSessionType(session_type);
        setIsRunning(!is_paused);
        if (round_number) setRoundNumber(round_number);
        
        if (task_id !== currentTask?.id) {
          console.log('Task ID mismatch:', task_id, currentTask?.id);
        }
      }

      if (data.type === 'timer_stopped') {
        setIsRunning(false);
        updateTimerDurations();
      }
    };
  }, [ws, currentTask]);

  const updateTimerDurations = useCallback(() => {
    if (!settings) return;
    const current = settings[presetType];
        
    if (sessionType === 'work') {
      setTimeLeft(current.work_duration * 60);
    } else if (sessionType === 'short_break') {
      setTimeLeft(current.short_break * 60);
    } else if (sessionType === 'long_break') {
      setTimeLeft(current.long_break * 60);
    }
  }, [settings, presetType, sessionType]);

  useEffect(() => {
    updateTimerDurations();
  }, [presetType, updateTimerDurations]);

  const startTimer = () => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      alert('Not connected to server. Please try again.');
      return;
    }

    if (!currentTask) {
      alert('Please select a task first');
      return;
    }

    ws.send(JSON.stringify({
      type: 'start',
      task_id: currentTask.id,
      session_type: sessionType,
      duration: timeLeft,
      preset_type: presetType
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

  const skipToNextSession = () => {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'skip_to_next' }));
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
      ws.send(JSON.stringify({ 
        type: 'sync_request',
        preset_type: presetType 
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, [ws, isConnected, presetType]);

  return (
    <View style={styles.card}>
      <View style={styles.timerContainer}>
        {/* Add skip button container */}
        <View style={{ 
          position: 'absolute', 
          right: -48, 
          top: '50%', 
          transform: [{ translateY: -20 }] 
        }}>
          <TouchableOpacity
            style={[
              styles.button,
              { 
                width: 40, 
                height: 40, 
                borderRadius: 20,
                justifyContent: 'center',
                alignItems: 'center',
                backgroundColor: colors.primary 
              }
            ]}
            onPress={skipToNextSession}
          >
            <Text style={[styles.buttonText, { fontSize: 20 }]}>→</Text>
          </TouchableOpacity>
        </View>

        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Text style={styles.text}>Round {roundNumber}/4</Text>
          <View style={{ flexDirection: 'row', gap: 8 }}>
            <TouchableOpacity
              style={[
                styles.button,
                presetType === 'short' && { backgroundColor: colors.primary }
              ]}
              onPress={() => setPresetType('short')}
            >
              <Text style={styles.buttonText}>Short</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.button,
                presetType === 'long' && { backgroundColor: colors.primary }
              ]}
              onPress={() => setPresetType('long')}
            >
              <Text style={styles.buttonText}>Long</Text>
            </TouchableOpacity>
          </View>
        </View>

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
        </View>
      </View>
    </View>
  );
}