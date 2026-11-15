"""Shared dependencies injected into routes with FastAPI's ``Depends``.

Routes declare a parameter typed as ``EmbeddingServiceDep`` and FastAPI passes in
the service created at startup.

Example:
    Replace the real service with a fake one in tests::

        app.dependency_overrides[get_embedding_service] = lambda: FakeService()
"""

from typing import Annotated

from fastapi import Depends, Request

from app.services.embedding import EmbeddingService


def get_embedding_service(request: Request) -> EmbeddingService:
    """Return the service stored on ``app.state`` by the lifespan in ``app/main.py``.

    Args:
        request: The incoming request, injected by FastAPI.

    Returns:
        The shared ``EmbeddingService`` instance.
    """
    service: EmbeddingService = request.app.state.embedding_service
    return service


EmbeddingServiceDep = Annotated[EmbeddingService, Depends(get_embedding_service)]
"""Type to use on route parameters that need the embedding service."""
