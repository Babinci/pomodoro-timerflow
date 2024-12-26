// src/components/TaskList.js
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
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

  const createTask = async () => {
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
    <View className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md mb-8">
      <Text className="text-2xl font-bold mb-4">Tasks</Text>
      <View className="mb-4">
        <TextInput
          value={title}
          onChangeText={setTitle}
          placeholder="Task Title"
          className="w-full p-2 mb-2 border rounded"
        />
        <TextInput
          value={estimatedPomodoros}
          onChangeText={setEstimatedPomodoros}
          placeholder="Estimated Pomodoros"
          keyboardType="numeric"
          className="w-full p-2 mb-2 border rounded"
        />
        <TouchableOpacity
          onPress={createTask}
          className="w-full bg-blue-500 p-2 rounded">
          <Text className="text-white text-center">Add Task</Text>
        </TouchableOpacity>
      </View>
      <ScrollView className="space-y-2">
        {tasks.map((task) => (
          <View key={task.id} className="p-4 bg-gray-50 rounded mb-2">
            <View className="flex flex-row justify-between items-center">
              <View className="flex-1">
                <Text className={`font-bold ${task.is_active ? '' : 'line-through'}`}>
                  {task.title}
                </Text>
                <Text className="text-sm text-gray-600">
                  {task.completed_pomodoros}/{task.estimated_pomodoros} Pomodoros
                </Text>
              </View>
              <TouchableOpacity
                onPress={() => setCurrentTask(task)}
                className="bg-blue-500 px-4 py-1 rounded">
                <Text className="text-white">Select</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}