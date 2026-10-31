"""Response model for the /health endpoint."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response of GET /health."""

    status: str
    model: str
