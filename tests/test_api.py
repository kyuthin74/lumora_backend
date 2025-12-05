"""
Example test file for Lumora Backend

To run tests:
    pip install pytest pytest-asyncio httpx
    pytest tests/
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_signup():
    """Test user signup"""
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "TestPass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_signup_duplicate_email():
    """Test signup with duplicate email"""
    # First signup
    client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "full_name": "User One",
            "password": "Pass123"
        }
    )
    
    # Second signup with same email
    response = client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "full_name": "User Two",
            "password": "Pass456"
        }
    )
    assert response.status_code == 400


def test_login():
    """Test user login"""
    # First create a user
    client.post(
        "/auth/signup",
        json={
            "email": "login@example.com",
            "full_name": "Login User",
            "password": "LoginPass123"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "LoginPass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    """Test getting current user info"""
    # Create and login
    client.post(
        "/auth/signup",
        json={
            "email": "current@example.com",
            "full_name": "Current User",
            "password": "Pass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "current@example.com",
            "password": "Pass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"


def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    response = client.get("/auth/me")
    assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
