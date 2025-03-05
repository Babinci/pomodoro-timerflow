import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { styles } from '../styles/styles';
import { apiConfig } from '../config/api';

export default function Settings({ token, settings, setSettings, setToken, ws }) {
  const [shortWork, setShortWork] = useState('25');
  const [shortBreak, setShortBreak] = useState('5');
  const [shortLongBreak, setShortLongBreak] = useState('15');
  const [longWork, setLongWork] = useState('50');
  const [longBreak, setLongBreak] = useState('10');
  const [longLongBreak, setLongLongBreak] = useState('30');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

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
      
      // Update local settings state
      setSettings(newSettings);
      
      // Force sync with server to update timer state
      if (ws && ws.ws && ws.ws.readyState === WebSocket.OPEN) {
        ws.ws.send(JSON.stringify({
          type: 'settings_updated',
          settings: newSettings
        }));
      }
      
      alert('Settings saved successfully');
    } catch (error) {
      alert('Failed to save settings: ' + error.message);
    }
  };

  const deleteAccount = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/me`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        // Clear token from localStorage and state
        localStorage.removeItem('token');
        setToken(null);
        alert('Your account has been deleted successfully');
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete account');
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  const handleDeleteRequest = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDelete = () => {
    deleteAccount();
    setShowDeleteConfirm(false);
  };

  const cancelDelete = () => {
    setShowDeleteConfirm(false);
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

      {/* Account Management Section */}
      <View style={{ marginTop: 32, borderTopWidth: 1, borderTopColor: '#E5E7EB', paddingTop: 16 }}>
        <Text style={[styles.title, { fontSize: 18 }]}>Account Management</Text>
        
        <TouchableOpacity
          style={[styles.button, { backgroundColor: '#EF4444', marginTop: 16 }]}
          onPress={handleDeleteRequest}
        >
          <Text style={styles.buttonText}>Delete My Account</Text>
        </TouchableOpacity>
      </View>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <View style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          justifyContent: 'center',
          alignItems: 'center',
          padding: 16,
        }}>
          <View style={{
            backgroundColor: 'white',
            padding: 20,
            borderRadius: 8,
            width: '100%',
            maxWidth: 400,
          }}>
            <Text style={[styles.text, { fontWeight: 'bold', marginBottom: 12 }]}>
              Confirm Account Deletion
            </Text>
            <Text style={[styles.text, { marginBottom: 16 }]}>
              Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently lost.
            </Text>
            <View style={{ flexDirection: 'row', justifyContent: 'flex-end', gap: 12 }}>
              <TouchableOpacity
                style={[styles.button, { backgroundColor: '#6B7280' }]}
                onPress={cancelDelete}
              >
                <Text style={styles.buttonText}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, { backgroundColor: '#EF4444' }]}
                onPress={confirmDelete}
              >
                <Text style={styles.buttonText}>Delete Account</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      )}
    </View>
  );
}