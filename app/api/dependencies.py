"""Shared dependencies injected into routes with FastAPI's Depends.

Routes declare a parameter typed as EmbeddingServiceDep and FastAPI passes
in the service created at startup. Tests can replace it with
app.dependency_overrides[get_embedding_service] = lambda: FakeService().
"""

from typing import Annotated

from fastapi import Depends, Request

from app.services.embedding import EmbeddingService


def get_embedding_service(request: Request) -> EmbeddingService:
    """Return the EmbeddingService stored on app.state by the lifespan in app/main.py."""
    return request.app.state.embedding_service


EmbeddingServiceDep = Annotated[EmbeddingService, Depends(get_embedding_service)]
