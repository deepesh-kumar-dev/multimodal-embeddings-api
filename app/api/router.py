"""Combines all route modules into a single router, mounted in ``app/main.py``.

When you add a new file under ``app/api/routes/``, register its router here.
"""

from typing import Final

from fastapi import APIRouter

from app.api.routes import embeddings, health

api_router: Final[APIRouter] = APIRouter()
"""Top-level router holding every route in the app."""

api_router.include_router(health.router)
api_router.include_router(embeddings.router)
