"""Embedding service: the only module that talks to the ML model.

One EmbeddingService is created at startup (see lifespan in app/main.py)
and shared by all requests through app/api/dependencies.py.

To switch model libraries or add a new input type (e.g. images), change
this file; routes only call its public methods.
"""

import logging
import time

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Wraps the embedding model so routes don't depend on the model library directly."""

    def __init__(self, model_name: str, device: str | None = None) -> None:
        self.model_name = model_name

        logger.info("Loading model %r (device=%s)...", model_name, device or "auto")
        start = time.perf_counter()
        self._model = SentenceTransformer(model_name, device=device)
        logger.info("Model loaded in %.1fs on %s", time.perf_counter() - start, self._model.device)

    def embed_texts(self, texts: list[str], normalize: bool = True) -> np.ndarray:
        """Return an array of shape (len(texts), dimensions)."""
        start = time.perf_counter()
        vectors = self._model.encode(texts, normalize_embeddings=normalize)
        logger.debug(
            "Embedded %d text(s) in %.0fms", len(texts), (time.perf_counter() - start) * 1000
        )
        return vectors
