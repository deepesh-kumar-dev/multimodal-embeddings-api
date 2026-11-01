"""Response model for the ``/health`` endpoint."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response of ``GET /health``.

    Attributes:
        status: Always ``"ok"`` when the service is able to respond.
        model: Name of the loaded embedding model.
    """

    status: Literal["ok"]
    model: str
