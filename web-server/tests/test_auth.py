import pytest
from fastapi import status
from app.models import User

def test_create_user(client):
    """Test user creation endpoint"""
    response = client.post(
        "/users/",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "hashed_password" not in data

def test_create_existing_user(client, test_user):
    """Test creating user with existing email fails"""
    response = client.post(
        "/users/",
        json={
            "email": test_user["email"],
            "username": "different_username",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_get_settings_authenticated(client, test_user_token):
    """Test getting user settings with valid authentication"""
    response = client.get(
        "/users/settings",
        headers=test_user_token
    )
    assert response.status_code == 200
    data = response.json()
    assert "short" in data
    assert "long" in data

def test_get_settings_unauthenticated(client):
    """Test getting user settings without authentication"""
    response = client.get("/users/settings")
    assert response.status_code == 401