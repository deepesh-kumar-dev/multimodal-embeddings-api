"""``GET /health``: reports that the service is up and which model is loaded."""

from typing import Final

from fastapi import APIRouter

from app.api.dependencies import EmbeddingServiceDep
from app.schemas import HealthResponse

router: Final[APIRouter] = APIRouter(tags=["health"])
"""Router for health check endpoints, registered in ``app/api/router.py``."""


@router.get("/health", response_model=HealthResponse)
def health(service: EmbeddingServiceDep) -> HealthResponse:
    """Report service status.

    Args:
        service: Shared embedding service, injected by FastAPI.

    Returns:
        Status ``"ok"`` and the name of the loaded model.
    """
    return HealthResponse(status="ok", model=service.model_name)
