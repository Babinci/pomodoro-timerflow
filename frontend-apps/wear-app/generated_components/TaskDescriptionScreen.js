import React, { useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { TimerContext } from '../context/TimerContext';

const TaskDescriptionScreen = () => {
  const { timeLeft, activeTask } = useContext(TimerContext);

  return (
    <View style={styles.container}>
      {/* Mini Timer Display at the top */}
      <View style={styles.miniTimer}>
        <Text style={styles.miniTimerText}>{timeLeft}</Text>
      </View>
      
      <ScrollView style={styles.contentContainer}>
        {activeTask ? (
          <>
            <Text style={styles.taskTitle}>{activeTask.title}</Text>
            
            <View style={styles.progressContainer}>
              <Text style={styles.progressText}>
                Progress: {activeTask.completed_pomodoros}/{activeTask.estimated_pomodoros} Pomodoros
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { 
                      width: `${Math.min(100, (activeTask.completed_pomodoros / activeTask.estimated_pomodoros) * 100)}%`,
                    }
                  ]} 
                />
              </View>
            </View>
            
            <Text style={styles.sectionTitle}>Description</Text>
            <View style={styles.descriptionContainer}>
              <Text style={styles.descriptionText}>
                {activeTask.description || 'No description available for this task.'}
              </Text>
            </View>
          </>
        ) : (
          <View style={styles.noTaskContainer}>
            <Text style={styles.noTaskText}>No task selected</Text>
            <Text style={styles.noTaskSubtext}>
              Select a task from the main app to see details here.
            </Text>
          </View>
        )}
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
    borderColor: '#7b68ee',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  miniTimerText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
  },
  contentContainer: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  progressContainer: {
    marginBottom: 16,
  },
  progressText: {
    color: '#aaa',
    marginBottom: 4,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#333',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#7b68ee',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  descriptionContainer: {
    backgroundColor: '#222',
    borderRadius: 8,
    padding: 12,
    minHeight: 100,
  },
  descriptionText: {
    color: '#fff',
    lineHeight: 20,
  },
  noTaskContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  noTaskText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  noTaskSubtext: {
    color: '#aaa',
    textAlign: 'center',
  },
});

export default TaskDescriptionScreen;
