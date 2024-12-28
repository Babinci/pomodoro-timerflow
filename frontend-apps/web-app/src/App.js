// src/App.js
import React, { useState, useEffect, useCallback } from 'react';
import { View } from 'react-native';
import LoginForm from './components/LoginForm';
import MainApp from './components/MainApp';
import { apiConfig } from './config/api';
import { styles } from './styles/styles';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const verifyToken = useCallback(async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/verify-token`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        localStorage.removeItem('token');
        setToken(null);
      }
    } catch (error) {
      localStorage.removeItem('token');
      setToken(null);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      verifyToken();
    }
  }, [token, verifyToken]);

  return (
    <View style={styles.container}>
      {token ? (
        <MainApp token={token} setToken={setToken} />
      ) : (
        <LoginForm setToken={setToken} />
      )}
    </View>
  );
}