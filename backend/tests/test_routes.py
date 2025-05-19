import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_generate_response(monkeypatch):
    async def mock_chat_completion(msg):
        return "Mocked response"
    
    def mock_topic_modelling(msg):
        return ""

    monkeypatch.setattr("chatbot.pixie.chat_completion", lambda msg: "Mocked response")
    monkeypatch.setattr("chatbot.input_sanitizer.topic_modelling", lambda msg: "")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/pixie", params={"message": "Hello"})
    assert response.status_code == 200
    assert "data" in response.json()


def test_clean_text():
    from main import clean_text
    raw = "<b>Hallo</b> wereld! **Test** &amp; meer"
    expected = "Hallo wereld! Test & meer"
    assert clean_text(raw) == expected


def test_tts(monkeypatch):
    from main import clean_text
    from fastapi.testclient import TestClient
    import builtins

    client = TestClient(app)

    def dummy_save(path):
        with open(path, "wb") as f:
            f.write(b"fake audio data")

    monkeypatch.setattr("gtts.gTTS.save", dummy_save)

    response = client.get("/tts", params={"text": "Hallo wereld"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"


@pytest.mark.asyncio
async def test_transcribe(monkeypatch):
    from faster_whisper import WhisperModel

    class DummyModel:
        def transcribe(self, *args, **kwargs):
            return ([MagicMock(text="Hallo wereld.")], None)

    monkeypatch.setattr("main.whisperModel", DummyModel())

    dummy_audio = b"\x00" * 1000
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/transcribe",
            files={"audio": ("audio.wav", dummy_audio, "audio/wav")}
        )
    assert response.status_code == 200
    assert response.json()["text"] == "Hallo wereld."


def test_login_failure(monkeypatch):
    def mock_authenticate_admin(email, password, conn):
        return {"authenticated": False}

    monkeypatch.setattr("main.authenticate_admin", mock_authenticate_admin)
    monkeypatch.setattr("main.get_database_connection", lambda: MagicMock())

    response = client.post("/login", json={"email": "fake@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_login_success(monkeypatch):
    def mock_authenticate_admin(email, password, conn):
        return {"authenticated": True}

    def mock_create_token(data):
        return "dummy-token"

    monkeypatch.setattr("main.authenticate_admin", mock_authenticate_admin)
    monkeypatch.setattr("main.create_access_token", mock_create_token)
    monkeypatch.setattr("main.get_database_connection", lambda: MagicMock())

    response = client.post("/login", json={"email": "admin@example.com", "password": "admin123"})
    assert response.status_code == 200
    assert response.json()["access_token"] == "dummy-token"
