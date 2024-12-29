// useWebSocket.js
import { useState, useEffect, useCallback, useRef } from 'react';
import { apiConfig } from '../config/api';

export default function useWebSocket(token) {
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const reconnectAttempt = useRef(0);
  const MAX_RECONNECT_ATTEMPTS = 5;
  const RECONNECT_INTERVAL = 2000; // 2 seconds
  const wsRef = useRef(null);

  const connectWebSocket = useCallback(() => {
    if (!token) return;

    try {
      const tokenData = JSON.parse(atob(token.split('.')[1]));
      const userId = tokenData.sub;
      
      // Close existing connection if any
      if (wsRef.current) {
        wsRef.current.close();
      }

      const wsUrl = `${apiConfig.baseUrl.replace('http', 'ws')}/ws/${userId}?token=${token}`;
      const websocket = new WebSocket(wsUrl);
      
      websocket.onopen = () => {
        console.log('WebSocket Connected');
        setIsConnected(true);
        reconnectAttempt.current = 0;
        wsRef.current = websocket;
        setWs(websocket);
      };
      
      websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('WebSocket message received:', data);
          // Handle different message types here if needed
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      websocket.onerror = (error) => {
        console.error('WebSocket Error:', error);
        setIsConnected(false);
      };
      
      websocket.onclose = (event) => {
        console.log('WebSocket Disconnected', event.code, event.reason);
        setIsConnected(false);
        wsRef.current = null;
        setWs(null);
        
        // Attempt to reconnect if we haven't exceeded max attempts
        if (reconnectAttempt.current < MAX_RECONNECT_ATTEMPTS) {
          console.log(`Attempting to reconnect (${reconnectAttempt.current + 1}/${MAX_RECONNECT_ATTEMPTS})`);
          setTimeout(() => {
            reconnectAttempt.current += 1;
            connectWebSocket();
          }, RECONNECT_INTERVAL);
        }
      };

      return websocket;
    } catch (error) {
      console.error('Error setting up WebSocket:', error);
      return null;
    }
  }, [token]);

  // Connect when component mounts or token changes
  useEffect(() => {
    const websocket = connectWebSocket();
    
    return () => {
      if (websocket) {
        websocket.close();
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectWebSocket]);

  // Expose connection status and websocket instance
  return {
    ws,
    isConnected,
    reconnect: connectWebSocket
  };
}