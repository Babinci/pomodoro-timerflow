import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { styles } from '../styles/styles';
import { apiConfig } from '../config/api';

export default function Settings({ token, settings, setSettings }) {
  const [shortWork, setShortWork] = useState('25');
  const [shortBreak, setShortBreak] = useState('5');
  const [shortLongBreak, setShortLongBreak] = useState('15');
  const [longWork, setLongWork] = useState('50');
  const [longBreak, setLongBreak] = useState('10');
  const [longLongBreak, setLongLongBreak] = useState('30');

  const loadSettings = useCallback(async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/settings`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to load settings');
      const data = await response.json();
      setSettings(data);
      
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
  }, [token, setSettings]);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  const saveSettings = async (e) => {
    e.preventDefault();
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
    <View style={styles.card}>
      <Text style={styles.title}>Settings</Text>
      <View style={styles.settingsGrid}>
        <View style={styles.settingsSection}>
          <Text style={[styles.text, { fontWeight: 'bold', marginBottom: 16 }]}>
            Short Preset
          </Text>
          <View style={{ gap: 12 }}>
            <View>
              <Text style={styles.smallText}>Work Duration (minutes)</Text>
              <TextInput
                style={styles.input}
                value={shortWork}
                onChangeText={setShortWork}
                keyboardType="numeric"
              />
            </View>
            <View>
              <Text style={styles.smallText}>Short Break (minutes)</Text>
              <TextInput
                style={styles.input}
                value={shortBreak}
                onChangeText={setShortBreak}
                keyboardType="numeric"
              />
            </View>
            <View>
              <Text style={styles.smallText}>Long Break (minutes)</Text>
              <TextInput
                style={styles.input}
                value={shortLongBreak}
                onChangeText={setShortLongBreak}
                keyboardType="numeric"
              />
            </View>
          </View>
        </View>

        <View style={styles.settingsSection}>
          <Text style={[styles.text, { fontWeight: 'bold', marginBottom: 16 }]}>
            Long Preset
          </Text>
          <View style={{ gap: 12 }}>
            <View>
              <Text style={styles.smallText}>Work Duration (minutes)</Text>
              <TextInput
                style={styles.input}
                value={longWork}
                onChangeText={setLongWork}
                keyboardType="numeric"
              />
            </View>
            <View>
              <Text style={styles.smallText}>Short Break (minutes)</Text>
              <TextInput
                style={styles.input}
                value={longBreak}
                onChangeText={setLongBreak}
                keyboardType="numeric"
              />
            </View>
            <View>
              <Text style={styles.smallText}>Long Break (minutes)</Text>
              <TextInput
                style={styles.input}
                value={longLongBreak}
                onChangeText={setLongLongBreak}
                keyboardType="numeric"
              />
            </View>
          </View>
        </View>
      </View>

      <TouchableOpacity
        style={[styles.button, { marginTop: 24 }]}
        onPress={saveSettings}
      >
        <Text style={styles.buttonText}>Save Settings</Text>
      </TouchableOpacity>
    </View>
  );
}