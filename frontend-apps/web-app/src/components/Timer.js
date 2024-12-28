// src/components/Timer.js
import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles, colors } from '../styles/styles';

export default function Timer({ currentTask, currentPreset, setCurrentPreset, settings, ws }) {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionType, setSessionType] = useState('work');
  const [currentSessionNumber, setCurrentSessionNumber] = useState(1);

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
    if (!settings) return;
    updateTimerDurations();
  }, [settings, updateTimerDurations]);

  useEffect(() => {
    let interval;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft(time => {
          if (time <= 1) {
            handleSessionComplete();
            return 0;
          }
          return time - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const handleSessionComplete = useCallback(() => {
    setIsRunning(false);
    
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'end_session',
        data: {
          session_id: currentSessionNumber,
          task_id: currentTask?.id
        }
      }));
    }

    const current = settings?.[currentPreset];
    if (!current) return;
    
    if (sessionType === 'work') {
      if (currentSessionNumber % current.sessions_before_long_break === 0) {
        setSessionType('long_break');
      } else {
        setSessionType('short_break');
      }
    } else {
      setSessionType('work');
      setCurrentSessionNumber(prev => 
        sessionType === 'long_break' ? 1 : prev + 1
      );
    }
  }, [ws, currentSessionNumber, currentTask, sessionType, settings, currentPreset]);

  const formatTime = () => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <View style={styles.card}>
      <View style={{ flexDirection: 'row', justifyContent: 'center', gap: 16, marginBottom: 24 }}>
        <TouchableOpacity
          style={[
            styles.button,
            {
              backgroundColor: currentPreset === 'short' ? colors.primary : colors.background,
              padding: 8,
              paddingHorizontal: 16,
            }
          ]}
          onPress={() => setCurrentPreset('short')}
        >
          <Text style={[styles.buttonText, 
            { color: currentPreset === 'short' ? 'white' : colors.text }]}>
            Short Preset (25/5)
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.button,
            {
              backgroundColor: currentPreset === 'long' ? colors.primary : colors.background,
              padding: 8,
              paddingHorizontal: 16,
            }
          ]}
          onPress={() => setCurrentPreset('long')}
        >
          <Text style={[styles.buttonText, 
            { color: currentPreset === 'long' ? 'white' : colors.text }]}>
            Long Preset (50/10)
          </Text>
        </TouchableOpacity>
      </View>

      <View style={styles.timerContainer}>
        <Text style={styles.timerDisplay}>{formatTime()}</Text>
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
              onPress={() => {
                setIsRunning(true);
                if (ws?.readyState === WebSocket.OPEN) {
                  ws.send(JSON.stringify({
                    type: 'start_session',
                    data: {
                      task_id: currentTask?.id,
                      session_type: sessionType,
                      current_session_number: currentSessionNumber
                    }
                  }));
                }
              }}
            >
              <Text style={styles.buttonText}>Start</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.button, { backgroundColor: colors.warning }]}
              onPress={() => {
                setIsRunning(false);
                if (ws?.readyState === WebSocket.OPEN) {
                  ws.send(JSON.stringify({ type: 'pause_session' }));
                }
              }}
            >
              <Text style={styles.buttonText}>Pause</Text>
            </TouchableOpacity>
          )}
          <TouchableOpacity
            style={[styles.button, { backgroundColor: colors.danger }]}
            onPress={() => {
              setIsRunning(false);
              setSessionType('work');
              updateTimerDurations();
            }}
          >
            <Text style={styles.buttonText}>Reset</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}