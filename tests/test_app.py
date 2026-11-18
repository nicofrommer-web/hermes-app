import os
import sys
from pathlib import Path

# Ensure the repository root is importable when pytest is launched via its console script.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("HERMES_TENANT_ID", "hermes-ci")
os.environ.setdefault("HERMES_SESSION_SECRET", "ci-only-secret-not-for-production")
os.environ.setdefault("HERMES_ADMIN_USER", "ci-admin")
os.environ.setdefault("HERMES_ADMIN_PASSWORD", "ci-test-password")
os.environ.setdefault("HERMES_COOKIE_SECURE", "false")
os.environ.setdefault("DATABASE_URL", "sqlite:///./hermes-ci-test.db")

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_requires_login():
    response = client.get("/api/workspace")
    assert response.status_code == 401


def test_login_and_session():
    response = client.post(
        "/api/login",
        json={"username": "ci-admin", "password": "ci-test-password"},
    )
    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    session = client.get("/api/session")
    assert session.status_code == 200
    assert session.json()["user"] == "ci-admin"


def test_workspace_save_and_read():
    login = client.post(
        "/api/login",
        json={"username": "ci-admin", "password": "ci-test-password"},
    )
    assert login.status_code == 200

    payload = {
        "leads": [],
        "tasks": [],
        "approvals": [],
        "agents": [],
        "workflows": [],
        "logs": [],
    }
    saved = client.put("/api/workspace", json={"data": payload})
    assert saved.status_code == 200
    loaded = client.get("/api/workspace")
    assert loaded.status_code == 200
    assert loaded.json()["data"] == payload


def test_login_rejects_wrong_password():
    response = client.post(
        "/api/login",
        json={"username": "ci-admin", "password": "incorrect"},
    )
    assert response.status_code == 401
