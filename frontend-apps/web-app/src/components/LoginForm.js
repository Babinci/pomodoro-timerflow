import React, { useState } from 'react';
import { apiConfig } from '../config/api';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { styles, colors } from '../styles/styles';

export default function LoginForm({ setToken }) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [success, setSuccess] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      formData.append('grant_type', 'password');
      
      const response = await fetch(`${apiConfig.baseUrl}/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept': 'application/json'
        },
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }
      
      if (!data.access_token) {
        throw new Error('No access token received');
      }

      localStorage.setItem('token', data.access_token);
      setToken(data.access_token);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    // Basic validation
    if (!email || !username || !password) {
      setError('All fields are required');
      return;
    }
    
    try {
      const response = await fetch(`${apiConfig.baseUrl}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email,
          username,
          password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      setSuccess('Registration successful! You can now log in.');
      setIsRegistering(false);
      // Clear only username as email might be needed for login
      setUsername('');
      setPassword('');
    } catch (err) {
      setError(err.message);
    }
  };

  const toggleForm = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setSuccess('');
  };

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>{isRegistering ? 'Register' : 'Login'}</Text>
        
        {error ? (
          <View style={[styles.card, { backgroundColor: '#FEE2E2' }]}>
            <Text style={{ color: '#DC2626' }}>{error}</Text>
          </View>
        ) : null}
        
        {success ? (
          <View style={[styles.card, { backgroundColor: '#DCFCE7' }]}>
            <Text style={{ color: '#166534' }}>{success}</Text>
          </View>
        ) : null}
        
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          placeholder="Email"
          keyboardType="email-address"
          autoCapitalize="none"
        />
        
        {isRegistering && (
          <TextInput
            style={styles.input}
            value={username}
            onChangeText={setUsername}
            placeholder="Username"
            autoCapitalize="none"
          />
        )}
        
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          placeholder="Password"
          secureTextEntry
        />
        
        <TouchableOpacity 
          style={styles.button} 
          onPress={isRegistering ? handleRegister : handleLogin}
        >
          <Text style={styles.buttonText}>
            {isRegistering ? 'Register' : 'Login'}
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={{ marginTop: 16, alignItems: 'center' }}
          onPress={toggleForm}
        >
          <Text style={{ color: colors.primary }}>
            {isRegistering 
              ? 'Already have an account? Login' 
              : 'Need an account? Register'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}