// src/config/api.js
export const apiConfig = {
    // Update this with your backend server IP when testing with a physical device
    baseUrl: __DEV__ 
      ? 'http://10.0.2.2:8003/api'  // Android emulator points to localhost
      : 'https://pomodoro.cypher-arena.com/api', // Production URL
  };
