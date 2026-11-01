"""Application entry point.

Run with::

    uvicorn app.main:app --reload

Startup order:
    1. ``create_app()`` sets up logging and mounts all routes (``app/api/router.py``).
    2. ``lifespan()`` loads the model once and stores it on ``app.state``.
    3. Routes handle requests and get the model via ``app/api/dependencies.py``.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.services.embedding import EmbeddingService

APP_TITLE: Final[str] = "Multimodal Embeddings API"
APP_VERSION: Final[str] = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Run startup work before the app serves requests, and cleanup after it stops.

    Loads the embedding model once here instead of on every request.

    Args:
        app: The FastAPI application being started.

    Yields:
        Control back to FastAPI while the app is running.
    """
    app.state.embedding_service = EmbeddingService(settings.model_name, device=settings.device)
    yield


def create_app() -> FastAPI:
    """Build and configure the FastAPI application.

    Returns:
        The app with logging configured and all routes mounted. The model is not
        loaded until the app starts (see ``lifespan``).
    """
    setup_logging()
    application: FastAPI = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)
    application.include_router(api_router)
    return application


app: Final[FastAPI] = create_app()
"""ASGI app that uvicorn serves."""
