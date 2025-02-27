// useWebSocket.js
import { useState, useEffect, useCallback, useRef } from 'react';
import { apiConfig } from '../config/api';

export default function useWebSocket(token) {
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const reconnectAttempt = useRef(0);
  const MAX_RECONNECT_ATTEMPTS = 5;
  const RECONNECT_INTERVAL = 2000;
  const wsRef = useRef(null);

  const connectWebSocket = useCallback(() => {
    if (!token) return;

    try {
      // Close existing connection if any
      if (wsRef.current) {
        wsRef.current.close();
      }

      // Modified to match backend endpoint structure
      const wsUrl = `${apiConfig.baseUrl.replace('http', 'ws')}/ws/?token=${token}`;
      const websocket = new WebSocket(wsUrl);
      
      websocket.onopen = () => {
        console.log('WebSocket Connected');
        setIsConnected(true);
        reconnectAttempt.current = 0;
        wsRef.current = websocket;
        setWs(websocket);

        // Request initial timer state sync including preset type
        websocket.send(JSON.stringify({
          type: 'sync_request'
        }));
      };
      
      websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('WebSocket message received:', data);
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

  return {
    ws,
    isConnected,
    reconnect: connectWebSocket
  };
}
