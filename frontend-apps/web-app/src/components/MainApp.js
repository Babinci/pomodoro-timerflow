// src/components/MainApp.js
import React, { useState } from 'react';
import { View } from 'react-native';
import Timer from './Timer';
import TaskList from './TaskList';
import Settings from './Settings';
import useWebSocket from '../hooks/useWebSocket';

export default function MainApp({ token, setToken }) {
  const [currentTask, setCurrentTask] = useState(null);
  const [currentPreset, setCurrentPreset] = useState('short');
  const [settings, setSettings] = useState(null);
  const ws = useWebSocket(token);

  return (
    <View style={{ flex: 1 }}>
      <Timer 
        currentTask={currentTask}
        currentPreset={currentPreset}
        setCurrentPreset={setCurrentPreset}
        settings={settings}
        ws={ws}
      />
      <TaskList 
        token={token}
        currentTask={currentTask}
        setCurrentTask={setCurrentTask}
      />
      <Settings 
        token={token}
        settings={settings}
        setSettings={setSettings}
      />
    </View>
  );
}