import React, { useState } from 'react';
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
    <div className="min-h-screen bg-[#f7f6fb] p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
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
      </div>
    </div>
  );
}