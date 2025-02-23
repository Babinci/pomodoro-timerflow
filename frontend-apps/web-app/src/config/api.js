// src/config/api.js
export const apiConfig = {
  baseUrl: process.env.NODE_ENV === 'development' 
      ? 'http://localhost:8003/api'  // Local development with Docker
      : '/api',                      // Production (relative path)
};