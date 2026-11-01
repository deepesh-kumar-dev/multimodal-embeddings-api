"""Embedding service: the only module that talks to the ML model.

One ``EmbeddingService`` is created at startup (see ``lifespan`` in ``app/main.py``)
and shared by all requests through ``app/api/dependencies.py``.

To switch model libraries or add a new input type (e.g. images), change this
file; routes only call its public methods.
"""

import logging
import time

import numpy as np
import numpy.typing as npt
from sentence_transformers import SentenceTransformer

logger: logging.Logger = logging.getLogger(__name__)

EmbeddingMatrix = npt.NDArray[np.float32]
"""2-D array of shape ``(n_inputs, dimensions)``, one embedding per row."""


class EmbeddingService:
    """Loads an embedding model once and computes embeddings with it.

    Wrapping the model keeps routes independent of the model library, so the
    library can be swapped without touching the API layer.

    Attributes:
        model_name: Name of the loaded model, as passed to the constructor.
    """

    def __init__(self, model_name: str, device: str | None = None) -> None:
        """Load the model. This is slow (seconds) and should happen only at startup.

        Args:
            model_name: Sentence-transformers model name or local path. Downloaded
                from the Hugging Face Hub on first use and cached afterwards.
            device: Torch device such as ``"cpu"`` or ``"cuda"``. ``None`` picks the
                best available device automatically.

        Raises:
            OSError: If the model cannot be found or downloaded.
            ValueError: If the model needs a package that is not installed.
        """
        self.model_name: str = model_name

        logger.info("Loading model %r (device=%s)...", model_name, device or "auto")
        start: float = time.perf_counter()
        self._model: SentenceTransformer = SentenceTransformer(model_name, device=device)
        logger.info("Model loaded in %.1fs on %s", time.perf_counter() - start, self._model.device)

    def embed_texts(self, texts: list[str], normalize: bool = True) -> EmbeddingMatrix:
        """Embed a batch of texts.

        Args:
            texts: Texts to embed. CLIP models truncate each text to 77 tokens.
            normalize: If ``True``, scale each vector to unit length so that the dot
                product of two vectors equals their cosine similarity.

        Returns:
            Array of shape ``(len(texts), dimensions)``, rows in the same order as
            ``texts``.
        """
        start: float = time.perf_counter()
        vectors: EmbeddingMatrix = np.asarray(
            self._model.encode(texts, normalize_embeddings=normalize, convert_to_numpy=True),
            dtype=np.float32,
        )
        elapsed_ms: float = (time.perf_counter() - start) * 1000
        logger.debug("Embedded %d text(s) in %.0fms", len(texts), elapsed_ms)
        return vectors
