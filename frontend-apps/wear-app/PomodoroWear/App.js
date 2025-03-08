import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Import screens
import LoginScreen from './src/screens/LoginScreen';
import TimerScreen from './src/screens/TimerScreen';
import ControlsScreen from './src/screens/ControlsScreen';
import TaskDescriptionScreen from './src/screens/TaskDescriptionScreen';

// Import context provider
import { TimerProvider } from './src/context/TimerContext';

// Import API configuration
import { apiConfig } from './src/config/api';

const Tab = createMaterialTopTabNavigator();

const App = () => {
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const storedToken = await AsyncStorage.getItem('token');
        if (storedToken) {
          // Verify token validity
          const response = await fetch(`${apiConfig.baseUrl}/verify-token`, {
            headers: {
              'Authorization': `Bearer ${storedToken}`
            }
          });
          
          if (response.ok) {
            setToken(storedToken);
          } else {
            // Invalid token, clear it
            await AsyncStorage.removeItem('token');
          }
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkLoginStatus();
  }, []);

  if (isLoading) {
    // You could show a splash screen or loading indicator here
    return null;
  }

  // If not logged in, show the login screen
  if (!token) {
    return <LoginScreen setToken={setToken} />;
  }

  // If logged in, show the main app with tabs
  return (
    <TimerProvider token={token}>
      <NavigationContainer>
        <Tab.Navigator
          initialRouteName="Timer"
          tabBarPosition="bottom"
          screenOptions={{
            tabBarStyle: { backgroundColor: '#7b68ee' },
            tabBarActiveTintColor: '#ffffff',
            tabBarInactiveTintColor: '#c7c5df',
            tabBarShowLabel: true,
            tabBarLabelStyle: { fontSize: 10 },
            swipeEnabled: true,
            tabBarIndicator: () => null, // Hide the indicator for a cleaner look
          }}
        >
          <Tab.Screen 
            name="Timer" 
            component={TimerScreen}
            options={{ tabBarLabel: 'Timer' }}
          />
          
          <Tab.Screen 
            name="Controls" 
            component={ControlsScreen}
            options={{ tabBarLabel: 'Controls' }}
          />
          
          <Tab.Screen 
            name="TaskInfo" 
            component={TaskDescriptionScreen}
            options={{ tabBarLabel: 'Task' }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </TimerProvider>
  );
};

export default App;