// src/components/Timer.js
import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

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
  }, [isRunning, handleSessionComplete]);

  const formatTime = () => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <View className="card p-8 mb-8">
      <View className="flex flex-row justify-center space-x-4 mb-4">
        <TouchableOpacity
          onPress={() => setCurrentPreset('short')}
          className={`btn ${currentPreset === 'short' ? 'btn-primary' : 'btn-secondary'}`}>
          <Text className="text-white">Short Preset (25/5)</Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => setCurrentPreset('long')}
          className={`btn ${currentPreset === 'long' ? 'btn-primary' : 'btn-secondary'}`}>
          <Text className="text-white">Long Preset (50/10)</Text>
        </TouchableOpacity>
      </View>
      
      <View className={`text-center ${isRunning ? 'timer-active' : ''}`}>
        <Text className="timer-display mb-4">{formatTime()}</Text>
        <Text className="text-xl text-clickup-text-light mb-4">
          {sessionType === 'work' && currentTask 
            ? `Work Session - ${currentTask.title}`
            : sessionType === 'short_break'
            ? 'Short Break'
            : 'Long Break'}
        </Text>
        
        <View className="flex flex-row justify-center space-x-4 mb-4">
          {!isRunning ? (
            <TouchableOpacity
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
              className="btn btn-success">
              <Text className="text-white">Start</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              onPress={() => {
                setIsRunning(false);
                if (ws?.readyState === WebSocket.OPEN) {
                  ws.send(JSON.stringify({ type: 'pause_session' }));
                }
              }}
              className="btn btn-warning">
              <Text className="text-white">Pause</Text>
            </TouchableOpacity>
          )}
          <TouchableOpacity
            onPress={() => {
              setIsRunning(false);
              setSessionType('work');
              updateTimerDurations();
            }}
            className="btn btn-danger">
            <Text className="text-white">Reset</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}