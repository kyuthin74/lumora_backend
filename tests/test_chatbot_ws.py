import pytest
from starlette.websockets import WebSocketDisconnect


def test_connect_without_token(client):
    with pytest.raises(WebSocketDisconnect) as exc:
        with client.websocket_connect("/chatbot/ws"):
            pass
    assert exc.value.code == 1008


def test_connect_with_invalid_token(client):
    with pytest.raises(WebSocketDisconnect) as exc:
        with client.websocket_connect("/chatbot/ws?token=invalid_token"):
            pass
    assert exc.value.code == 1008


def test_connect_with_valid_token_gets_welcome(client, auth_token):
    with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as ws:
        data = ws.receive_json()
        assert data["type"] == "welcome"
        assert "Lumora" in data["content"]


def test_send_and_receive_message(client, auth_token):
    with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as ws:
        ws.receive_json()  # welcome
        ws.send_json({"type": "message", "content": "Hello, how are you?"})
        response = ws.receive_json()
        assert response == {
            "type": "message",
            "role": "assistant",
            "content": "I'm here for you.",
        }


def test_empty_message_returns_error(client, auth_token):
    with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as ws:
        ws.receive_json()
        ws.send_json({"type": "message", "content": "   "})
        assert ws.receive_json()["type"] == "error"


def test_single_connection_per_user(client, auth_token):
    with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as ws1:
        assert ws1.receive_json()["type"] == "welcome"
        with pytest.raises(WebSocketDisconnect) as exc:
            with client.websocket_connect(f"/chatbot/ws?token={auth_token}"):
                pass
        assert exc.value.code == 1008
    # After the first connection closes, the user can reconnect.
    with client.websocket_connect(f"/chatbot/ws?token={auth_token}") as ws3:
        assert ws3.receive_json()["type"] == "welcome"
