"""POST /embed/*: embedding endpoints.

Input validation:  app/schemas/embeddings.py
Model logic:       app/services/embedding.py
"""

from fastapi import APIRouter

from app.api.dependencies import EmbeddingServiceDep
from app.schemas import TextEmbeddingRequest, TextEmbeddingResponse

router = APIRouter(prefix="/embed", tags=["embeddings"])


# Plain `def` so FastAPI runs the CPU/GPU-bound encode in a thread pool
# instead of blocking the event loop.
@router.post("/text", response_model=TextEmbeddingResponse)
def embed_text(body: TextEmbeddingRequest, service: EmbeddingServiceDep) -> TextEmbeddingResponse:
    vectors = service.embed_texts(body.texts, normalize=body.normalize)
    return TextEmbeddingResponse(
        model=service.model_name,
        dimensions=vectors.shape[1],
        embeddings=vectors.tolist(),
    )
