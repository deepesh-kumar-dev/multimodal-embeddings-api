"""Tests for GET /health (app/api/routes/health.py)."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
