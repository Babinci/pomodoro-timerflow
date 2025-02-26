import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { apiConfig } from '../config/api';
import { styles as defaultStyles } from '../styles/styles';

const UserProfile = ({ token, setToken }) => {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
        setUsername(data.username);
        setEmail(data.email);
      } else {
        setMessage('Failed to load profile.');
      }
    } catch (error) {
      setMessage('Error loading profile.');
    }
  };

  const updateUserProfile = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/me`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
      });
      if (response.ok) {
        setMessage('Profile updated successfully.');
        fetchUserProfile(); // Refresh the user profile
      } else {
        setMessage('Failed to update profile.');
      }
    } catch (error) {
      setMessage('Error updating profile.');
    }
  };

  const deleteUserProfile = async () => {
    try {
      const response = await fetch(`${apiConfig.baseUrl}/users/me`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.status === 204) {
        setMessage('Profile deleted successfully.');
        setToken(null); // Logout user
        localStorage.removeItem('token');
      } else {
        setMessage('Failed to delete profile.');
      }
    } catch (error) {
      setMessage('Error deleting profile.');
    }
  };

  return (
    <View style={defaultStyles.container}>
      <Text style={defaultStyles.heading}>User Profile</Text>
      {message ? <Text>{message}</Text> : null}
      {user ? (
        <View>
          <Text>Username:</Text>
          <TextInput
            style={defaultStyles.input}
            value={username}
            onChangeText={setUsername}
          />
          <Text>Email:</Text>
          <TextInput
            style={defaultStyles.input}
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
          />
          <Text>New Password:</Text>
          <TextInput
            style={defaultStyles.input}
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
          <TouchableOpacity style={defaultStyles.button} onPress={updateUserProfile}>
            <Text style={defaultStyles.buttonText}>Update Profile</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.deleteButton} onPress={deleteUserProfile}>
            <Text style={defaultStyles.buttonText}>Delete Profile</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <Text>Loading profile...</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  deleteButton: {
    backgroundColor: 'red',
    padding: 10,
    borderRadius: 5,
    marginTop: 10,
  },
});

export default UserProfile;