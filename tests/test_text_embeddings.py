"""Tests for ``POST /embed/text`` (``app/api/routes/embeddings.py``)."""

import math
from typing import Any, Final

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from app.core.config import settings

ENDPOINT: Final[str] = "/embed/text"


def _dot(a: list[float], b: list[float]) -> float:
    """Return the dot product of two vectors (cosine similarity if both are normalized)."""
    return sum(x * y for x, y in zip(a, b, strict=True))


def test_returns_one_normalized_vector_per_text(client: TestClient) -> None:
    """Each input text gets one unit-length vector of the reported size."""
    response: Response = client.post(
        ENDPOINT, json={"texts": ["a photo of a cat", "a red sports car"]}
    )

    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert len(data["embeddings"]) == 2
    assert all(len(vector) == data["dimensions"] for vector in data["embeddings"])
    norm: float = math.sqrt(_dot(data["embeddings"][0], data["embeddings"][0]))
    assert norm == pytest.approx(1.0, abs=1e-4)


def test_similar_texts_score_higher(client: TestClient) -> None:
    """Texts with related meaning are closer than unrelated texts."""
    texts: list[str] = ["a photo of a cat", "a picture of a kitten", "a stock market report"]

    vectors: list[list[float]] = client.post(ENDPOINT, json={"texts": texts}).json()["embeddings"]

    assert _dot(vectors[0], vectors[1]) > _dot(vectors[0], vectors[2])


def test_empty_list_rejected(client: TestClient) -> None:
    """An empty ``texts`` list fails validation."""
    assert client.post(ENDPOINT, json={"texts": []}).status_code == 422


def test_too_many_texts_rejected(client: TestClient) -> None:
    """More than ``max_batch_size`` texts fails validation."""
    texts: list[str] = ["x"] * (settings.max_batch_size + 1)

    assert client.post(ENDPOINT, json={"texts": texts}).status_code == 422
