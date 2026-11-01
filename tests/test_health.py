"""Tests for ``GET /health`` (``app/api/routes/health.py``)."""

from fastapi.testclient import TestClient
from httpx2 import Response

from app.core.config import settings


def test_health_reports_ok_and_model(client: TestClient) -> None:
    """The health check returns 200 with status ``"ok"`` and the configured model."""
    response: Response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model": settings.model_name}
