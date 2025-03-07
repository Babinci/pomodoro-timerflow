import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  Vibration,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiConfig } from '../config/api';

const LoginScreen = ({ setToken }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter both email and password');
      Vibration.vibrate(200); // Short vibration for error
      return;
    }

    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', email); // API expects 'username' field even for email
      formData.append('password', password);
      
      const response = await fetch(`${apiConfig.baseUrl}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept': 'application/json'
        },
        body: formData.toString()
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }
      
      if (!data.access_token) {
        throw new Error('No access token received');
      }

      // Store token and update state
      await AsyncStorage.setItem('token', data.access_token);
      setToken(data.access_token);
      
      // Success vibration feedback
      Vibration.vibrate(500);
    } catch (error) {
      console.error('Login error:', error);
      Alert.alert('Login Failed', error.message);
      Vibration.vibrate([100, 200, 100]); // Pattern for error
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pomodoro TimerFlow</Text>
      
      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        
        <TouchableOpacity 
          style={styles.button}
          onPress={handleLogin}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Login</Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
  },
  form: {
    width: '100%',
    maxWidth: 200,
  },
  input: {
    width: '100%',
    height: 40,
    backgroundColor: '#222',
    borderRadius: 8,
    marginBottom: 12,
    paddingHorizontal: 12,
    color: '#fff',
  },
  button: {
    width: '100%',
    height: 40,
    backgroundColor: '#7b68ee',
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default LoginScreen;
