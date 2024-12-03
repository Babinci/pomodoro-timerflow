import pytest
from fastapi import status

def test_create_user(client):
    """Test user creation endpoint"""
    response = client.post(
        "/users/",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data

def test_create_existing_user(client, test_user):
    """Test attempting to create a user with existing email"""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",  # Same as test_user
            "username": "another",
            "password": "pass123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test login with incorrect password"""
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_settings_authenticated(client, test_user_token):
    """Test accessing settings with valid token"""
    response = client.get(
        "/users/settings",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "short" in data
    assert "long" in data

def test_get_settings_unauthenticated(client):
    """Test accessing settings without token"""
    response = client.get("/users/settings")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED