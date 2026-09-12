"""
test_auth.py — Tests for JWT auth endpoints using FastAPI TestClient.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():
    resp = client.post("/auth/token", data={"username": "kushal", "password": "password123"})
    return resp.json()["access_token"]


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_login_success():
    resp = client.post("/auth/token", data={"username": "kushal", "password": "password123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


def test_login_wrong_password():
    resp = client.post("/auth/token", data={"username": "kushal", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_user():
    resp = client.post("/auth/token", data={"username": "ghost", "password": "pass"})
    assert resp.status_code == 401


def test_protected_with_valid_token():
    token = get_token()
    resp = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["role"] == "admin"


def test_protected_without_token():
    resp = client.get("/protected")
    assert resp.status_code == 401


def test_me_endpoint():
    token = get_token()
    resp = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "kushal"


def test_invalid_token():
    resp = client.get("/me", headers={"Authorization": "Bearer invalidtoken"})
    assert resp.status_code == 401
