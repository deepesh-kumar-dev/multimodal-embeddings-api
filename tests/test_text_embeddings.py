import math

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    # Entering the context runs the lifespan, which loads the model.
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_embed_text_returns_one_normalized_vector_per_text(client):
    r = client.post("/embed/text", json={"texts": ["a photo of a cat", "a red sports car"]})
    assert r.status_code == 200
    data = r.json()
    assert len(data["embeddings"]) == 2
    assert all(len(v) == data["dimensions"] for v in data["embeddings"])
    norm = math.sqrt(sum(x * x for x in data["embeddings"][0]))
    assert norm == pytest.approx(1.0, abs=1e-4)


def test_similar_texts_score_higher(client):
    texts = ["a photo of a cat", "a picture of a kitten", "a stock market report"]
    vecs = client.post("/embed/text", json={"texts": texts}).json()["embeddings"]
    dot = lambda a, b: sum(x * y for x, y in zip(a, b))  # noqa: E731
    assert dot(vecs[0], vecs[1]) > dot(vecs[0], vecs[2])


def test_empty_list_rejected(client):
    assert client.post("/embed/text", json={"texts": []}).status_code == 422
