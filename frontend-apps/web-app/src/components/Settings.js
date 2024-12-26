// src/components/Settings.js
import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { apiConfig } from '../config/api';

export default function Settings({ token, settings, setSettings }) {
  const [shortWork, setShortWork] = useState('25');
  const [shortBreak, setShortBreak] = useState('5');
  const [shortLongBreak, setShortLongBreak] = useState('15');
  const [longWork, setLongWork] = useState('50');
  const [longBreak, setLongBreak] = useState('10');
  const [longLongBreak, setLongLongBreak] = useState('30');

  useEffect(() => {
    const init = async () => {
      await loadSettings();
    };
    init();
  }, [loadSettings]);

  const loadSettings = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/settings`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to load settings');
      const data = await response.json();
      setSettings(data);
      
      // Update form fields
      if (data.short) {
        setShortWork(data.short.work_duration.toString());
        setShortBreak(data.short.short_break.toString());
        setShortLongBreak(data.short.long_break.toString());
      }
      if (data.long) {
        setLongWork(data.long.work_duration.toString());
        setLongBreak(data.long.short_break.toString());
        setLongLongBreak(data.long.long_break.toString());
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const saveSettings = async () => {
    const newSettings = {
      short: {
        work_duration: parseInt(shortWork),
        short_break: parseInt(shortBreak),
        long_break: parseInt(shortLongBreak),
        sessions_before_long_break: 4
      },
      long: {
        work_duration: parseInt(longWork),
        short_break: parseInt(longBreak),
        long_break: parseInt(longLongBreak),
        sessions_before_long_break: 4
      }
    };

    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/settings`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newSettings)
      });

      if (!response.ok) throw new Error('Failed to save settings');
      setSettings(newSettings);
      alert('Settings saved successfully');
    } catch (error) {
      alert('Failed to save settings: ' + error.message);
    }
  };

  return (
    <View className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
      <Text className="text-2xl font-bold mb-4">Settings</Text>
      <View className="grid grid-cols-2 gap-4">
        <View>
          <Text className="font-bold mb-2">Short</Text>
          <TextInput
            value={shortWork}
            onChangeText={setShortWork}
            placeholder="Work (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
          <TextInput
            value={shortBreak}
            onChangeText={setShortBreak}
            placeholder="Break (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
          <TextInput
            value={shortLongBreak}
            onChangeText={setShortLongBreak}
            placeholder="Long Break (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
        </View>
        <View>
          <Text className="font-bold mb-2">Long</Text>
          <TextInput
            value={longWork}
            onChangeText={setLongWork}
            placeholder="Work (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
          <TextInput
            value={longBreak}
            onChangeText={setLongBreak}
            placeholder="Break (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
          <TextInput
            value={longLongBreak}
            onChangeText={setLongLongBreak}
            placeholder="Long Break (min)"
            keyboardType="numeric"
            className="w-full p-2 mb-2 border rounded"
          />
        </View>
      </View>
      <TouchableOpacity
        onPress={saveSettings}
        className="w-full bg-blue-500 p-2 rounded mt-4">
        <Text className="text-white text-center">Save Settings</Text>
      </TouchableOpacity>
    </View>
  );
}