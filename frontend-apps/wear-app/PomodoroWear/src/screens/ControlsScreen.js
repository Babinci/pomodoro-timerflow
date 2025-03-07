import React, { useContext } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { TimerContext } from '../context/TimerContext';

const ControlsScreen = () => {
  const {
    timeLeft,
    isRunning,
    sessionType,
    roundNumber,
    activePreset,
    startTimer,
    pauseTimer,
    resumeTimer,
    skipToNext,
    resetRounds,
    changePreset
  } = useContext(TimerContext);

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
      {/* Mini Timer Display at the top */}
      <View style={[styles.miniTimer, { borderColor: getSessionColor() }]}>
        <Text style={styles.miniTimerText}>{timeLeft}</Text>
      </View>
      
      <ScrollView style={styles.controlsContainer}>
        {/* Preset Selection */}
        <View style={styles.controlSection}>
          <Text style={styles.sectionTitle}>Preset</Text>
          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={[
                styles.presetButton,
                activePreset === 'short' && styles.activeButton
              ]}
              onPress={() => changePreset('short')}
            >
              <Text style={styles.buttonText}>Short</Text>
              <Text style={styles.buttonSubtext}>25/5</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[
                styles.presetButton,
                activePreset === 'long' && styles.activeButton
              ]}
              onPress={() => changePreset('long')}
            >
              <Text style={styles.buttonText}>Long</Text>
              <Text style={styles.buttonSubtext}>50/10</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        {/* Timer Controls */}
        <View style={styles.controlSection}>
          <Text style={styles.sectionTitle}>Controls</Text>
          <View style={styles.buttonGrid}>
            {isRunning ? (
              <TouchableOpacity
                style={[styles.controlButton, { backgroundColor: '#ef4444' }]}
                onPress={pauseTimer}
              >
                <Text style={styles.buttonText}>Pause</Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                style={[styles.controlButton, { backgroundColor: '#22c55e' }]}
                onPress={resumeTimer}
              >
                <Text style={styles.buttonText}>
                  {timeLeft === '00:00' ? 'Next' : 'Start'}
                </Text>
              </TouchableOpacity>
            )}
            
            <TouchableOpacity
              style={[styles.controlButton, { backgroundColor: '#3b82f6' }]}
              onPress={skipToNext}
            >
              <Text style={styles.buttonText}>Skip</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.controlButton, { backgroundColor: '#f59e0b' }]}
              onPress={resetRounds}
            >
              <Text style={styles.buttonText}>Reset</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        {/* Session Info */}
        <View style={styles.controlSection}>
          <Text style={styles.sectionTitle}>Session Info</Text>
          <View style={styles.infoContainer}>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Round:</Text>
              <Text style={styles.infoValue}>{roundNumber}/4</Text>
            </View>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Mode:</Text>
              <Text style={styles.infoValue}>
                {sessionType === 'work' ? 'Work' : 
                 sessionType === 'short_break' ? 'Short Break' : 'Long Break'}
              </Text>
            </View>
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Preset:</Text>
              <Text style={styles.infoValue}>
                {activePreset === 'short' ? 'Short (25/5)' : 'Long (50/10)'}
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 16,
  },
  miniTimer: {
    alignSelf: 'center',
    width: 80,
    height: 40,
    borderRadius: 20,
    borderWidth: 2,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  miniTimerText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
  },
  controlsContainer: {
    flex: 1,
  },
  controlSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  presetButton: {
    flex: 1,
    height: 50,
    backgroundColor: '#333',
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 4,
  },
  activeButton: {
    backgroundColor: '#7b68ee',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  buttonSubtext: {
    color: '#aaa',
    fontSize: 12,
  },
  buttonGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  controlButton: {
    width: '30%',
    height: 40,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  infoContainer: {
    backgroundColor: '#222',
    borderRadius: 8,
    padding: 12,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  infoLabel: {
    color: '#aaa',
  },
  infoValue: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default ControlsScreen;
