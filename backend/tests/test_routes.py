import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.main import app, clean_text, authenticate_admin, create_access_token, get_database_connection

client = TestClient(app)

def test_clean_text():
    raw = "<b>Hallo</b> wereld! **Test** &amp; meer"
    expected = "Hallo wereld! Test & meer"
    assert clean_text(raw) == expected

def test_login_failure(monkeypatch):
    def mock_auth(email, password, conn):
        return {"authenticated": False}

    monkeypatch.setattr("backend.main.authenticate_admin", mock_auth)
    monkeypatch.setattr("backend.main.get_database_connection", lambda: MagicMock())

    response = client.post("/login", json={"email": "fake@example.com", "password": "wrong"})
    assert response.status_code == 401

def test_login_success(monkeypatch):
    def mock_auth(email, password, conn):
        return {"authenticated": True}

    def mock_token(data):
        return "dummy-token"

    monkeypatch.setattr("backend.main.authenticate_admin", mock_auth)
    monkeypatch.setattr("backend.main.create_access_token", mock_token)
    monkeypatch.setattr("backend.main.get_database_connection", lambda: MagicMock())

    response = client.post("/login", json={"email": "admin@example.com", "password": "admin123"})
    assert response.status_code == 200
    assert response.json()["access_token"] == "dummy-token"
