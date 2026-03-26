import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(autouse=True)
def reset_repo():
    """Reset the in-memory store between tests."""
    from app.routes.items import repo
    repo._store.clear()
    repo._counter = 0
    yield


@pytest.fixture
def client():
    return TestClient(app)


# ── Health Check ──────────────────────────────────────────────

def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "UP"}


# ── CREATE ────────────────────────────────────────────────────

def test_create_item(client):
    payload = {"name": "Widget", "description": "A fine widget", "price": 9.99, "quantity": 10}
    resp = client.post("/api/v1/items/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["name"] == "Widget"
    assert data["price"] == 9.99


def test_create_item_validation_error(client):
    resp = client.post("/api/v1/items/", json={"name": "", "price": -1, "quantity": -5})
    assert resp.status_code == 422


# ── READ ──────────────────────────────────────────────────────

def test_get_all_items_empty(client):
    resp = client.get("/api/v1/items/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_all_items(client):
    client.post("/api/v1/items/", json={"name": "A", "price": 1.0, "quantity": 1})
    client.post("/api/v1/items/", json={"name": "B", "price": 2.0, "quantity": 2})
    resp = client.get("/api/v1/items/")
    assert len(resp.json()) == 2


def test_get_item_by_id(client):
    client.post("/api/v1/items/", json={"name": "A", "price": 1.0, "quantity": 1})
    resp = client.get("/api/v1/items/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "A"


def test_get_item_not_found(client):
    resp = client.get("/api/v1/items/999")
    assert resp.status_code == 404


# ── UPDATE ────────────────────────────────────────────────────

def test_update_item(client):
    client.post("/api/v1/items/", json={"name": "A", "price": 1.0, "quantity": 1})
    resp = client.put("/api/v1/items/1", json={"name": "A-updated", "price": 5.0})
    assert resp.status_code == 200
    assert resp.json()["name"] == "A-updated"
    assert resp.json()["price"] == 5.0
    assert resp.json()["quantity"] == 1  # unchanged


def test_update_item_not_found(client):
    resp = client.put("/api/v1/items/999", json={"name": "X"})
    assert resp.status_code == 404


# ── DELETE ────────────────────────────────────────────────────

def test_delete_item(client):
    client.post("/api/v1/items/", json={"name": "A", "price": 1.0, "quantity": 1})
    resp = client.delete("/api/v1/items/1")
    assert resp.status_code == 204
    assert client.get("/api/v1/items/1").status_code == 404


def test_delete_item_not_found(client):
    resp = client.delete("/api/v1/items/999")
    assert resp.status_code == 404
