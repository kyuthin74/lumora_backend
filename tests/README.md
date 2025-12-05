# Tests Directory

This directory contains test files for the Lumora backend.

## Running Tests

### Install test dependencies
```bash
pip install pytest pytest-asyncio httpx
```

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pip install pytest-cov
pytest --cov=app tests/
```

### Run specific test file
```bash
pytest tests/test_api.py -v
```

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_api.py` - API endpoint tests
- `test_auth.py` - Authentication tests (to be added)
- `test_crud.py` - Database operation tests (to be added)
- `test_ml.py` - ML prediction tests (to be added)

## Writing Tests

Example test:
```python
def test_example(client):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

## Test Coverage

Aim for:
- 80%+ code coverage
- All critical paths tested
- Edge cases covered
