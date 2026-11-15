"""``POST /embed/*``: embedding endpoints.

- Input validation: ``app/schemas/embeddings.py``
- Model logic: ``app/services/embedding.py``
"""

from typing import Final

from fastapi import APIRouter

from app.api.dependencies import EmbeddingServiceDep
from app.schemas import TextEmbeddingRequest, TextEmbeddingResponse
from app.services.embedding import EmbeddingMatrix

router: Final[APIRouter] = APIRouter(prefix="/embed", tags=["embeddings"])
"""Router for all ``/embed`` endpoints, registered in ``app/api/router.py``."""


# Plain `def` so FastAPI runs the CPU/GPU-bound encode in a thread pool
# instead of blocking the event loop.
@router.post("/text", response_model=TextEmbeddingResponse)
def embed_text(body: TextEmbeddingRequest, service: EmbeddingServiceDep) -> TextEmbeddingResponse:
    """Embed a batch of texts.

    Args:
        body: Validated request body with the texts and the normalize flag.
        service: Shared embedding service, injected by FastAPI.

    Returns:
        One embedding per input text, in the same order, plus the model name and
        vector size.
    """
    vectors: EmbeddingMatrix = service.embed_texts(body.texts, normalize=body.normalize)
    return TextEmbeddingResponse(
        model=service.model_name,
        dimensions=vectors.shape[1],
        embeddings=vectors.tolist(),
    )
