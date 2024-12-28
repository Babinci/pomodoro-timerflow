// src/components/TaskList.js
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { styles, colors } from '../styles/styles';
import { apiConfig } from '../config/api';

export default function TaskList({ token, currentTask, setCurrentTask }) {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [estimatedPomodoros, setEstimatedPomodoros] = useState('');

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    if (!title || !estimatedPomodoros) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`${apiConfig.baseUrl}/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title,
          estimated_pomodoros: parseInt(estimatedPomodoros),
          description: ''
        })
      });
      
      if (!response.ok) throw new Error('Failed to create task');

      const task = await response.json();
      setTasks([...tasks, task]);
      setTitle('');
      setEstimatedPomodoros('');
    } catch (error) {
      alert('Failed to create task: ' + error.message);
    }
  };

  return (
    <View style={styles.card}>
      <Text style={styles.title}>Tasks</Text>
      <View style={{ marginBottom: 24 }}>
        <TextInput
          style={styles.input}
          value={title}
          onChangeText={setTitle}
          placeholder="Task Title"
        />
        <TextInput
          style={styles.input}
          value={estimatedPomodoros}
          onChangeText={setEstimatedPomodoros}
          placeholder="Estimated Pomodoros"
          keyboardType="numeric"
        />
        <TouchableOpacity style={styles.button} onPress={createTask}>
          <Text style={styles.buttonText}>Add Task</Text>
        </TouchableOpacity>
      </View>
      
      <ScrollView style={{ maxHeight: 400 }}>
        {tasks.map((task) => (
          <View
            key={task.id}
            style={[
              styles.taskItem,
              currentTask?.id === task.id && styles.taskItemActive
            ]}
          >
            <View style={{ flex: 1 }}>
              <Text style={[
                styles.text,
                task.is_active ? {} : { textDecorationLine: 'line-through' }
              ]}>
                {task.title}
              </Text>
              <Text style={styles.smallText}>
                {task.completed_pomodoros}/{task.estimated_pomodoros} Pomodoros
              </Text>
            </View>
            <TouchableOpacity
              style={[styles.button, { paddingHorizontal: 16, paddingVertical: 8 }]}
              onPress={() => setCurrentTask(task)}
            >
              <Text style={styles.buttonText}>Select</Text>
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}