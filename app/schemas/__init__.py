"""Schemas layer: Pydantic models for request and response bodies.

FastAPI uses these to validate input (returning 422 on bad requests) and to
generate the ``/docs`` page. One module per feature:

- ``embeddings.py``: text (and later image) embedding requests/responses
- ``health.py``: health check response

Re-exported here so other layers can write ``from app.schemas import HealthResponse``.
"""

from app.schemas.embeddings import TextEmbeddingRequest, TextEmbeddingResponse
from app.schemas.health import HealthResponse

__all__: list[str] = ["HealthResponse", "TextEmbeddingRequest", "TextEmbeddingResponse"]
