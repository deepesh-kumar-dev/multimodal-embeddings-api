from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.schemas import HealthResponse, TextEmbeddingRequest, TextEmbeddingResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model once at startup instead of on every request.
    app.state.model = SentenceTransformer(settings.model_name, device=settings.device)
    yield


app = FastAPI(title="Multimodal Embeddings API", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model=settings.model_name)


# Plain `def` so FastAPI runs the CPU/GPU-bound encode in a thread pool
# instead of blocking the event loop.
@app.post("/embed/text", response_model=TextEmbeddingResponse)
def embed_text(body: TextEmbeddingRequest, request: Request) -> TextEmbeddingResponse:
    if len(body.texts) > settings.max_batch_size:
        raise HTTPException(
            status_code=422,
            detail=f"Too many texts: {len(body.texts)} (max {settings.max_batch_size}).",
        )

    model: SentenceTransformer = request.app.state.model
    vectors = model.encode(body.texts, normalize_embeddings=body.normalize)
    return TextEmbeddingResponse(
        model=settings.model_name,
        dimensions=vectors.shape[1],
        embeddings=vectors.tolist(),
    )
