import React, { useContext, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Vibration,
} from 'react-native';
import { TimerContext } from '../context/TimerContext';

const TimerScreen = () => {
  const { 
    timeLeft, 
    isRunning, 
    isConnected, 
    sessionType, 
    roundNumber, 
    activeTask,
    pauseTimer,
    resumeTimer,
    skipToNext
  } = useContext(TimerContext);
  
  // Handle vibration when work session ends
  useEffect(() => {
    if (timeLeft === '00:00' && sessionType === 'work') {
      Vibration.vibrate([0, 500, 200, 500, 200, 500]);
    }
  }, [timeLeft, sessionType]);

  // Toggle play/pause
  const toggleTimer = () => {
    if (!isConnected) {
      // Handle offline state
      return;
    }

    if (isRunning) {
      pauseTimer();
    } else {
      if (timeLeft === '00:00') {
        // If timer is at 0, send skip to next
        skipToNext();
      } else {
        resumeTimer();
      }
    }
  };

  // Get color based on session type
  const getSessionColor = () => {
    switch (sessionType) {
      case 'work':
        return '#ef4444'; // Red for work
      case 'short_break':
        return '#22c55e'; // Green for short break
      case 'long_break':
        return '#3b82f6'; // Blue for long break
      default:
        return '#7b68ee'; // Default purple
    }
  };

  return (
    <View style={styles.container}>
      {/* Task Name - Prominently Displayed */}
      <Text style={styles.taskName} numberOfLines={1} ellipsizeMode="tail">
        {activeTask ? activeTask.title : 'No Task Selected'}
      </Text>
      
      {/* Round Number - Less Prominently Displayed */}
      <Text style={styles.roundNumber}>
        Round {roundNumber}/4
      </Text>
      
      {/* Timer Display */}
      <View style={[styles.timerCircle, { borderColor: getSessionColor() }]}>
        <Text style={styles.timerText}>{timeLeft}</Text>
        <Text style={styles.sessionType}>
          {sessionType === 'work' ? 'WORK' : 
           sessionType === 'short_break' ? 'BREAK' : 'LONG BREAK'}
        </Text>
      </View>
      
      {/* Main Start/Stop Button */}
      <TouchableOpacity 
        style={[styles.button, { backgroundColor: isRunning ? '#ef4444' : '#22c55e' }]} 
        onPress={toggleTimer}
      >
        <Text style={styles.buttonText}>
          {isRunning ? 'STOP' : timeLeft === '00:00' ? 'NEXT' : 'START'}
        </Text>
      </TouchableOpacity>
      
      {/* Connection Status Indicator */}
      <View style={[
        styles.connectionIndicator, 
        { backgroundColor: isConnected ? '#22c55e' : '#ef4444' }
      ]} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  taskName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
    textAlign: 'center',
    width: '100%',
  },
  roundNumber: {
    fontSize: 12,
    color: '#aaa',
    marginBottom: 20,
  },
  timerCircle: {
    width: 140,
    height: 140,
    borderRadius: 70,
    borderWidth: 4,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  timerText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  sessionType: {
    fontSize: 12,
    color: '#aaa',
    marginTop: 4,
  },
  button: {
    width: 80,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  connectionIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    position: 'absolute',
    top: 8,
    right: 8,
  },
});

export default TimerScreen;
