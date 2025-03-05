import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { styles, colors } from '../styles/styles';
import { apiConfig } from '../config/api';

export default function TaskList({ token, currentTask, setCurrentTask }) {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [estimatedPomodoros, setEstimatedPomodoros] = useState('1');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editDescription, setEditDescription] = useState('');

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/tasks/`, {
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
    if (!title) {
      alert('Please fill in the task title');
      return;
    }

    try {
      const response = await fetch(`${apiConfig.baseUrl}/tasks/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title,
          estimated_pomodoros: parseInt(estimatedPomodoros || '1'),
          description: ''
        })
      });
        
      if (!response.ok) throw new Error('Failed to create task');

      const task = await response.json();
      setTasks([...tasks, task]);
      setTitle('');
      setEstimatedPomodoros('1');
    } catch (error) {
      alert('Failed to create task: ' + error.message);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to delete task');
      setTasks(tasks.filter(task => task.id !== taskId));
      if (currentTask?.id === taskId) {
        setCurrentTask(null);
      }
      // Clear editing state if we're deleting the task being edited
      if (editingTaskId === taskId) {
        setEditingTaskId(null);
        setEditDescription('');
      }
    } catch (error) {
      alert('Failed to delete task: ' + error.message);
    }
  };

  const updateTask = async (taskId, updatedFields) => {
    try {
      const taskToUpdate = tasks.find(t => t.id === taskId);
      if (!taskToUpdate) return;

      const updatedTask = { ...taskToUpdate, ...updatedFields };
      
      const response = await fetch(`${apiConfig.baseUrl}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: updatedTask.title,
          description: updatedTask.description,
          estimated_pomodoros: updatedTask.estimated_pomodoros
        })
      });

      if (!response.ok) throw new Error('Failed to update task');
      const updatedTaskData = await response.json();
      setTasks(tasks.map(t => t.id === taskId ? updatedTaskData : t));
      
      // Update current task if this is the selected one
      if (currentTask?.id === taskId) {
        setCurrentTask(updatedTaskData);
      }
    } catch (error) {
      console.error('Failed to update task:', error);
      alert('Failed to update task: ' + error.message);
    }
  };

  const startEditingDescription = (task) => {
    setEditingTaskId(task.id);
    setEditDescription(task.description || '');
  };

  const saveDescription = (taskId) => {
    updateTask(taskId, { description: editDescription });
    setEditingTaskId(null);
  };

  const cancelEditingDescription = () => {
    setEditingTaskId(null);
    setEditDescription('');
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
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8, marginVertical: 8 }}>
          <Text style={styles.text}>Estimated Pomodoros: </Text>
          <TouchableOpacity
            style={[styles.button, { paddingHorizontal: 12 }]}
            onPress={() => setEstimatedPomodoros(Math.max(1, parseInt(estimatedPomodoros || '1') - 1).toString())}
          >
            <Text style={styles.buttonText}>-</Text>
          </TouchableOpacity>
          <Text style={styles.text}>{estimatedPomodoros || '1'}</Text>
          <TouchableOpacity
            style={[styles.button, { paddingHorizontal: 12 }]}
            onPress={() => setEstimatedPomodoros((parseInt(estimatedPomodoros || '1') + 1).toString())}
          >
            <Text style={styles.buttonText}>+</Text>
          </TouchableOpacity>
        </View>
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
              <TextInput
                style={[styles.input, { marginBottom: 4 }]}
                value={task.title}
                onChangeText={(text) => updateTask(task.id, { title: text })}
              />
              
              {/* Description Field with Edit/Save Pattern */}
              {editingTaskId === task.id ? (
                <View style={{ marginVertical: 8 }}>
                  <TextInput
                    style={[
                      styles.input, 
                      { 
                        minHeight: 80, 
                        textAlignVertical: 'top',
                        paddingTop: 8
                      }
                    ]}
                    placeholder="Description (optional)"
                    value={editDescription}
                    onChangeText={setEditDescription}
                    multiline={true}
                    numberOfLines={4}
                  />
                  <View style={{ flexDirection: 'row', gap: 8, marginTop: 4 }}>
                    <TouchableOpacity
                      style={[styles.button, { backgroundColor: colors.success }]}
                      onPress={() => saveDescription(task.id)}
                    >
                      <Text style={styles.buttonText}>Save</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.button, { backgroundColor: colors.textLight }]}
                      onPress={cancelEditingDescription}
                    >
                      <Text style={styles.buttonText}>Cancel</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ) : (
                <View style={{ marginVertical: 8 }}>
                  <TouchableOpacity
                    style={[
                      styles.input,
                      { 
                        minHeight: 60, 
                        paddingTop: 8,
                        paddingBottom: 8
                      }
                    ]}
                    onPress={() => startEditingDescription(task)}
                  >
                    {task.description ? (
                      <Text style={{ color: colors.text }}>{task.description}</Text>
                    ) : (
                      <Text style={{ color: colors.textLight }}>
                        Description (optional) - Click to edit
                      </Text>
                    )}
                  </TouchableOpacity>
                </View>
              )}
              
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <Text style={styles.smallText}>
                  {task.completed_pomodoros}/
                </Text>
                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                  <TouchableOpacity
                    style={[styles.button, { paddingHorizontal: 8, paddingVertical: 4 }]}
                    onPress={() => updateTask(task.id, { 
                      estimated_pomodoros: Math.max(1, task.estimated_pomodoros - 1)
                    })}
                  >
                    <Text style={[styles.buttonText, { fontSize: 12 }]}>-</Text>
                  </TouchableOpacity>
                  <Text style={[styles.smallText, { marginHorizontal: 8 }]}>
                    {task.estimated_pomodoros}
                  </Text>
                  <TouchableOpacity
                    style={[styles.button, { paddingHorizontal: 8, paddingVertical: 4 }]}
                    onPress={() => updateTask(task.id, { 
                      estimated_pomodoros: task.estimated_pomodoros + 1
                    })}
                  >
                    <Text style={[styles.buttonText, { fontSize: 12 }]}>+</Text>
                  </TouchableOpacity>
                </View>
                <Text style={styles.smallText}> Pomodoros</Text>
              </View>
            </View>
            <View style={{ flexDirection: 'row', gap: 8 }}>
              <TouchableOpacity
                style={[styles.button, { paddingHorizontal: 16, paddingVertical: 8 }]}
                onPress={() => setCurrentTask(task)}
              >
                <Text style={styles.buttonText}>Select</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, { 
                  paddingHorizontal: 16, 
                  paddingVertical: 8,
                  backgroundColor: colors.danger 
                }]}
                onPress={() => deleteTask(task.id)}
              >
                <Text style={styles.buttonText}>Delete</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}