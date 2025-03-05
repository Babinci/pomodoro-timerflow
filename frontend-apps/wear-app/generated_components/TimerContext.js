import React, { createContext, useState, useEffect } from 'react';
import useWebSocket from '../hooks/useWebSocket';

export const TimerContext = createContext();

export const TimerProvider = ({ children, token }) => {
  const { ws, isConnected, timerData } = useWebSocket(token);
  
  const [timeLeft, setTimeLeft] = useState('25:00');
  const [isRunning, setIsRunning] = useState(false);
  const [sessionType, setSessionType] = useState('work');
  const [roundNumber, setRoundNumber] = useState(1);
  const [activeTask, setActiveTask] = useState(null);
  const [activePreset, setActivePreset] = useState('short');

  // Format the time for display
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Update the local state from WebSocket data
  useEffect(() => {
    if (timerData) {
      setTimeLeft(formatTime(timerData.remaining_time));
      setIsRunning(!timerData.is_paused);
      setSessionType(timerData.session_type || 'work');
      setRoundNumber(timerData.round_number || 1);
      setActiveTask(timerData.active_task);
      if (timerData.preset_type) {
        setActivePreset(timerData.preset_type);
      }
    }
  }, [timerData]);

  // Timer control functions
  const startTimer = () => {
    if (!ws || !isConnected || !activeTask) return;
    
    ws.send(JSON.stringify({
      type: 'start',
      task_id: activeTask.id,
      session_type: sessionType,
      duration: convertTimeToSeconds(timeLeft),
      preset_type: activePreset
    }));
  };

  const pauseTimer = () => {
    if (!ws || !isConnected) return;
    ws.send(JSON.stringify({ type: 'pause' }));
  };

  const resumeTimer = () => {
    if (!ws || !isConnected) return;
    ws.send(JSON.stringify({ type: 'resume' }));
  };

  const skipToNext = () => {
    if (!ws || !isConnected) return;
    ws.send(JSON.stringify({ type: 'skip_to_next' }));
  };

  const resetRounds = () => {
    if (!ws || !isConnected) return;
    ws.send(JSON.stringify({ type: 'reset_rounds' }));
  };

  const changePreset = (preset) => {
    if (!ws || !isConnected) return;
    ws.send(JSON.stringify({
      type: 'change_preset',
      preset_type: preset
    }));
    setActivePreset(preset);
  };

  // Utility function to convert time string to seconds
  const convertTimeToSeconds = (timeString) => {
    const [minutes, seconds] = timeString.split(':').map(Number);
    return minutes * 60 + seconds;
  };

  return (
    <TimerContext.Provider value={{
      ws,
      isConnected,
      timeLeft,
      isRunning,
      sessionType,
      roundNumber,
      activeTask,
      activePreset,
      startTimer,
      pauseTimer,
      resumeTimer,
      skipToNext,
      resetRounds,
      changePreset
    }}>
      {children}
    </TimerContext.Provider>
  );
};
