import pytest
from fastapi import status

def test_create_task(client, test_user_token):
    """Test creating a new task"""
    response = client.post(
        "/tasks/",
        headers=test_user_token,  # Use the fixture directly
        json={
            "title": "Test Task",
            "description": "Test Description",
            "estimated_pomodoros": 4
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["estimated_pomodoros"] == 4
    assert data["completed_pomodoros"] == 0
    assert data["is_active"] is True

def test_get_tasks(client, test_user_token):
    """Test retrieving user's tasks"""
    # First create a task
    client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Test Task",
            "estimated_pomodoros": 4
        }
    )

    # Then get all tasks
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Test Task"

def test_update_task(client, test_user_token):
    """Test updating a task"""
    # First create a task
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Original Title",
            "estimated_pomodoros": 4
        }
    )
    task_id = create_response.json()["id"]

    # Then update it
    update_response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Updated Title",
            "estimated_pomodoros": 5
        }
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["estimated_pomodoros"] == 5

def test_update_nonexistent_task(client, test_user_token):
    """Test updating a task that doesn't exist"""
    response = client.put(
        "/tasks/999",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "Updated Title",
            "estimated_pomodoros": 5
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_tasks_unauthorized(client):
    """Test accessing tasks without authentication"""
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED