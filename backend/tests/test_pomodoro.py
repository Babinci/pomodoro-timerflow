import pytest
from fastapi import status
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import json
import asyncio

class MockWebSocket:
    def __init__(self):
        self.received_messages = []
        self.closed = False

    async def send_json(self, data):
        self.received_messages.append(data)

    async def receive_json(self):
        return {"type": "test_message"}

    async def accept(self):
        pass

def test_websocket_connection(client, test_user, test_user_token):
    """Test WebSocket connection establishment"""
    with client.websocket_connect(f"/ws/{test_user['id']}") as websocket:
        # Send a test message
        websocket.send_json({
            "type": "start_session",
            "data": {
                "task_id": 1,
                "session_type": "work",
                "current_session_number": 1
            }
        })
        
        # Receive the response
        data = websocket.receive_json()
        assert data["type"] == "session_started"
        assert "data" in data
        assert "session_id" in data["data"]

async def test_pomodoro_session_flow(client, test_user_token, db):
    """Test complete Pomodoro session flow"""
    # Create a task first
    task_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Test Task",
            "estimated_pomodoros": 4
        }
    )
    task_id = task_response.json()["id"]

    # Connect to WebSocket
    with client.websocket_connect(f"/ws/{test_user_token}") as websocket:
        # Start work session
        websocket.send_json({
            "type": "start_session",
            "data": {
                "task_id": task_id,
                "session_type": "work",
                "current_session_number": 1
            }
        })
        
        response = websocket.receive_json()
        assert response["type"] == "session_started"
        session_id = response["data"]["session_id"]

        # Simulate work time passing
        await asyncio.sleep(1)

        # End session
        websocket.send_json({
            "type": "end_session",
            "data": {
                "session_id": session_id
            }
        })
        
        response = websocket.receive_json()
        assert response["type"] == "session_ended"

        # Verify task was updated
        task = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        ).json()
        assert task["completed_pomodoros"] == 1

def test_invalid_session_type(client, test_user_token):
    """Test starting session with invalid session type"""
    with client.websocket_connect(f"/ws/{test_user_token}") as websocket:
        websocket.send_json({
            "type": "start_session",
            "data": {
                "task_id": 1,
                "session_type": "invalid_type",
                "current_session_number": 1
            }
        })
        
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "invalid session type" in response["message"].lower()

@pytest.mark.asyncio
async def test_multiple_device_sync(client, test_user_token):
    """Test synchronization between multiple devices"""
    # Simulate two devices connected simultaneously
    with client.websocket_connect(f"/ws/{test_user_token}") as websocket1, \
         client.websocket_connect(f"/ws/{test_user_token}") as websocket2:
        
        # Start session from device 1
        websocket1.send_json({
            "type": "start_session",
            "data": {
                "task_id": 1,
                "session_type": "work",
                "current_session_number": 1
            }
        })
        
        # Both devices should receive the start message
        response1 = websocket1.receive_json()
        response2 = websocket2.receive_json()
        
        assert response1 == response2
        assert response1["type"] == "session_started"