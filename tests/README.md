# Tests Directory

Automated backend tests (pytest + FastAPI `TestClient`). They use an in-memory SQLite
database and mock Gemini, SMTP and the push scheduler, so no real services are touched.

## Running Tests

Run everything from the `lumora_backend` folder, inside the virtual environment:

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest                      # all tests
pytest tests/test_auth.py -v
pytest --cov=app tests/     # with coverage
```

## Test Structure

| File | Covers |
| --- | --- |
| `conftest.py` | Fixtures: test DB, `client`, `test_user`, `auth_token`, fake Gemini chat |
| `test_health.py` | `/` and `/health` |
| `test_auth.py` | Signup, duplicate email, login, `/auth/me`, unauthorized access |
| `test_chatbot_ws.py` | `/chatbot/ws`: no/invalid/valid token, message exchange, empty message, one connection per user |
