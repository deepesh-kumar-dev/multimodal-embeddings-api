from pydantic import BaseModel, Field


class TextEmbeddingRequest(BaseModel):
    texts: list[str] = Field(min_length=1, examples=[["a photo of a cat", "a red sports car"]])
    normalize: bool = Field(default=True, description="L2-normalize vectors (for cosine similarity).")


class TextEmbeddingResponse(BaseModel):
    model: str
    dimensions: int
    embeddings: list[list[float]]


class HealthResponse(BaseModel):
    status: str
    model: str
