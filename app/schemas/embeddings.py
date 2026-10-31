"""Request and response models for the /embed endpoints.

Validation rules live here, not in the routes: an empty list or more than
EMBED_MAX_BATCH_SIZE texts is rejected with a 422 before the route runs.
"""

from pydantic import BaseModel, Field

from app.core.config import settings


class TextEmbeddingRequest(BaseModel):
    """Body of POST /embed/text."""

    texts: list[str] = Field(
        min_length=1,
        max_length=settings.max_batch_size,
        examples=[["a photo of a cat", "a red sports car"]],
    )
    normalize: bool = Field(
        default=True, description="L2-normalize vectors (for cosine similarity)."
    )


class TextEmbeddingResponse(BaseModel):
    """Response of POST /embed/text. One vector per input text, in the same order."""

    model: str
    dimensions: int
    embeddings: list[list[float]]
