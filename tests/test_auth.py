SIGNUP = {"email": "new@example.com", "full_name": "New User", "password": "StrongPass123"}


def test_signup(client):
    response = client.post("/auth/signup", json=SIGNUP)
    assert response.status_code == 201
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert isinstance(data["user_id"], int)


def test_signup_duplicate_email(client):
    assert client.post("/auth/signup", json=SIGNUP).status_code == 201
    response = client.post("/auth/signup", json={**SIGNUP, "full_name": "Other"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login(client):
    client.post("/auth/signup", json=SIGNUP)
    response = client.post(
        "/auth/login", data={"username": SIGNUP["email"], "password": SIGNUP["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/signup", json=SIGNUP)
    response = client.post(
        "/auth/login", data={"username": SIGNUP["email"], "password": "WrongPass123"}
    )
    assert response.status_code == 401


def test_get_current_user(client):
    token = client.post("/auth/signup", json=SIGNUP).json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == SIGNUP["email"]


def test_unauthorized_access(client):
    assert client.get("/auth/me").status_code == 401


def test_invalid_token_rejected(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not-a-token"})
    assert response.status_code == 401
