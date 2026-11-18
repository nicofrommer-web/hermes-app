import os
os.environ["HERMES_API_TOKEN"] = "test-secret-token"
os.environ["HERMES_TENANT_ID"] = "test-tenant"
os.environ["DATABASE_URL"] = "sqlite:///./test-hermes-api.db"

import pytest
from fastapi.testclient import TestClient
from app import app, Base, engine, SessionLocal, Lead, WorkTask, Approval, AuditLog

client = TestClient(app)
HEADERS = {"Authorization": "Bearer test-secret-token"}

@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_health_is_public():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_api_requires_bearer_token():
    response = client.get("/api/leads")
    assert response.status_code == 401

def test_create_and_list_lead_is_tenant_scoped():
    created = client.post("/api/leads", headers=HEADERS, json={
        "company": "Testbetrieb GmbH",
        "industry": "Handwerk",
        "city": "Villingen-Schwenningen",
        "opportunity": "Anfragen vorsortieren"
    })
    assert created.status_code == 201
    assert created.json()["company"] == "Testbetrieb GmbH"
    listed = client.get("/api/leads", headers=HEADERS)
    assert listed.status_code == 200
    assert any(item["company"] == "Testbetrieb GmbH" for item in listed.json())

def test_approval_can_only_be_decided_once():
    created = client.post("/api/approvals", headers=HEADERS, json={
        "title": "Demo-Freigabe",
        "payload": "Nur ein Testvorschlag; keine externe Aktion."
    })
    assert created.status_code == 201
    approval_id = created.json()["id"]
    decision = client.post(f"/api/approvals/{approval_id}/decision", headers=HEADERS, json={
        "decision": "approved",
        "actor": "test-user",
        "note": "Testentscheidung"
    })
    assert decision.status_code == 200
    assert decision.json()["status"] == "approved"
    second = client.post(f"/api/approvals/{approval_id}/decision", headers=HEADERS, json={
        "decision": "rejected",
        "actor": "test-user"
    })
    assert second.status_code == 409
