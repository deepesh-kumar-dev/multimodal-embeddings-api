"""GET /health: reports that the service is up and which model is loaded."""

from fastapi import APIRouter

from app.api.dependencies import EmbeddingServiceDep
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(service: EmbeddingServiceDep) -> HealthResponse:
    return HealthResponse(status="ok", model=service.model_name)
