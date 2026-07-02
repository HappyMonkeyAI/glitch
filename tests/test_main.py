from fastapi.testclient import TestClient

from src.main import app


def test_root_serves_glitch_page():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "GLITCH" in response.text
    assert "data-face" in response.text
    assert "speechSynthesis" in response.text
    assert "enable voice" in response.text
    assert "pointerdown" in response.text
    assert "interactionForPoint" in response.text
    assert "kawaii" in response.text
    assert "micToggle" in response.text
    assert "webkitSpeechRecognition" in response.text
    assert "continuous = true" in response.text
    assert "font-awesome" in response.text
    assert "fa-microphone" in response.text
    assert "fa-volume-high" in response.text
    assert "ensureAudioContext" in response.text
    assert "playDroidCue" in response.text
    assert "createOscillator" in response.text
    assert "createBiquadFilter" in response.text
    assert "sound_cue" in response.text
    assert "glitchIdleChirpsEnabled" in response.text
    assert "scheduleNextAttentionProbe" in response.text
    assert "lastHumanActivityAt" in response.text
    assert "document.visibilityState" in response.text
    assert "IDLE CHIRPS" in response.text
    assert "handleLocalVoiceCommand" in response.text
    assert "play music" in response.text
    assert "stop music" in response.text
    assert "setMusicPlaying" in response.text
    assert "startDemoDance" in response.text
    assert "stopDemoDance" in response.text
    assert "body.dancing" in response.text
    assert "demo-color-cycle" in response.text
    assert "getPetCommandNames" in response.text
    assert "stripPetNameWakeWord" in response.text
    assert "dongle play music" in response.text
    assert "wantsStopCommand" in response.text
    assert "stop dumbs" in response.text


def test_websocket_text_turn_returns_pet_update_and_response_text():
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        greeting = websocket.receive_json()
        assert greeting["type"] == "pet_update"

        websocket.send_json({"type": "user_text", "text": "good gremlin, have a snack"})
        update = websocket.receive_json()
        cue = websocket.receive_json()
        response = websocket.receive_json()

    assert update["type"] == "pet_update"
    assert update["state"]["mood"] in {"happy", "playful"}
    assert update["state"]["hunger"] < greeting["state"]["hunger"] or update["state"]["affection"] > greeting["state"]["affection"]
    assert cue["type"] == "sound_cue"
    assert cue["cue"]["category"] == "turn_ack"
    assert response["type"] == "response_text"
    assert response["text"]
    assert response["vocal_noise"] == cue["cue"]["vocal_text"]
    assert response["spoken_text"] == cue["cue"]["vocal_text"]
    assert len(response["text"].split()) <= 30


def test_websocket_avoids_repeating_same_vocal_noise_on_chatter():
    client = TestClient(app)
    messages = ["respect", "same to you", "the videos"]
    noises = []

    with client.websocket_connect("/ws") as websocket:
        greeting = websocket.receive_json()
        assert greeting["type"] == "pet_update"

        for text in messages:
            websocket.send_json({"type": "user_text", "text": text})
            websocket.receive_json()
            websocket.receive_json()
            response = websocket.receive_json()
            websocket.receive_json()
            noises.append(response["vocal_noise"])

    assert len(set(noises)) >= 2
    assert all(a != b for a, b in zip(noises, noises[1:]))


def test_websocket_idle_probe_returns_sound_cue_without_full_response():
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        greeting = websocket.receive_json()
        assert greeting["type"] == "pet_update"

        websocket.send_json({"type": "idle_probe", "idle_seconds": 60})
        cue = websocket.receive_json()

    assert cue["type"] == "sound_cue"
    assert cue["cue"]["category"] == "idle_probe"
    assert cue["cue"]["sequence"]
