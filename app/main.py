"""Application entry point.

Run with:  uvicorn app.main:app --reload

Startup order:
  1. create_app() sets up logging and mounts all routes (app/api/router.py)
  2. lifespan() loads the model once and stores it on app.state
  3. Requests are handled by routes, which get the model via app/api/dependencies.py
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.services.embedding import EmbeddingService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model once at startup instead of on every request.
    app.state.embedding_service = EmbeddingService(settings.model_name, device=settings.device)
    yield


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="Multimodal Embeddings API", version="0.1.0", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
