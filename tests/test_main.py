from fastapi.testclient import TestClient

from src.main import app


def test_root_serves_chip_page():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "CHIP" in response.text
    assert "data-face" in response.text
    assert "speechSynthesis" in response.text
    assert "enable voice" in response.text
    assert "pointerdown" in response.text
    assert "interactionForPoint" in response.text
    assert "kawaii" in response.text


def test_websocket_text_turn_returns_pet_update_and_response_text():
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        greeting = websocket.receive_json()
        assert greeting["type"] == "pet_update"

        websocket.send_json({"type": "user_text", "text": "good gremlin, have a snack"})
        update = websocket.receive_json()
        response = websocket.receive_json()

    assert update["type"] == "pet_update"
    assert update["state"]["mood"] in {"happy", "playful"}
    assert update["state"]["hunger"] < greeting["state"]["hunger"] or update["state"]["affection"] > greeting["state"]["affection"]
    assert response["type"] == "response_text"
    assert response["text"]
    assert response["vocal_noise"] == "bzz-uwu"
    assert response["spoken_text"].startswith("bzz-uwu")
    assert len(response["text"].split()) <= 30
