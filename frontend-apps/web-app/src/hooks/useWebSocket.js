import { useState, useEffect } from 'react';
import { apiConfig } from '../config/api';

export default function useWebSocket(token) {
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!token) return;

    const tokenData = JSON.parse(atob(token.split('.')[1]));
    const userId = tokenData.sub;
    const wsUrl = `ws://${apiConfig.baseUrl.replace('http://', '')}/ws/${userId}`;

    const websocket = new WebSocket(wsUrl);
    setWs(websocket);

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, [token]);

  return ws;
}