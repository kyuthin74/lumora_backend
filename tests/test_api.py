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


# WebSocket Tests
def test_websocket_connection_without_token(client):
    """Test WebSocket connection fails without auth token"""
    with pytest.raises(Exception):  # Connection should fail
        with client.websocket_connect("/chatbot/ws") as websocket:
            pass


def test_websocket_connection_with_invalid_token(client):
    """Test WebSocket connection fails with invalid token"""
    with pytest.raises(Exception):  # Connection should fail
        with client.websocket_connect("/chatbot/ws?token=invalid_token") as websocket:
            pass


def test_websocket_connection_with_valid_token(client, test_user, auth_token, db_session):
    """Test WebSocket connection succeeds with valid token"""
    # Override get_db for this test
    from app.database import get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as websocket:
            # Should receive welcome message
            data = websocket.receive_json()
            assert data["type"] == "welcome"
            assert "assistant" in data["content"].lower() or "lumora" in data["content"].lower()
    finally:
        app.dependency_overrides.clear()


def test_websocket_send_message(client, test_user, auth_token, db_session):
    """Test sending message through WebSocket"""
    from app.database import get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as websocket:
            # Receive welcome message
            welcome = websocket.receive_json()
            assert welcome["type"] == "welcome"
            
            # Send a message
            websocket.send_json({
                "type": "message",
                "content": "Hello, how are you?"
            })
            
            # Receive response (could be from Gemini or error if API key not set)
            response = websocket.receive_json()
            assert response["type"] in ["message", "error"]
            if response["type"] == "message":
                assert "content" in response
    finally:
        app.dependency_overrides.clear()


def test_websocket_empty_message(client, test_user, auth_token, db_session):
    """Test sending empty message through WebSocket"""
    from app.database import get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as websocket:
            # Receive welcome message
            websocket.receive_json()
            
            # Send empty message
            websocket.send_json({
                "type": "message",
                "content": ""
            })
            
            # Should receive error
            response = websocket.receive_json()
            assert response["type"] == "error"
    finally:
        app.dependency_overrides.clear()

def test_concurrent_websocket_connections(client, test_user, auth_token, db_session):
    """Test that only one WebSocket connection per user is allowed"""
    from app.database import get_db
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        # First connection should succeed
        with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as websocket1:
            websocket1.receive_json()  # welcome message
            
            # Second connection should fail (same user)
            with pytest.raises(Exception):
                with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as websocket2:
                    pass
    finally:
        app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
