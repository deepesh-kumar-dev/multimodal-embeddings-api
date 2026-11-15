"""Application settings.

Every setting can be overridden with an environment variable prefixed with
``EMBED_`` (e.g. ``EMBED_MODEL_NAME``) or in a ``.env`` file in the project root.
See ``.env.example`` for the full list.

Example:
    Import the shared instance instead of creating a new one::

        from app.core.config import settings
"""

from typing import Final, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["debug", "info", "warning", "error", "critical"]
"""Log levels accepted by ``EMBED_LOG_LEVEL``."""


class Settings(BaseSettings):
    """App settings, read from environment variables or a ``.env`` file.

    Attributes:
        model_name: Sentence-transformers model to load. CLIP models embed text and
            images into the same vector space, so the two can be compared directly.
        device: Torch device to run the model on (``"cpu"``, ``"cuda"``, ...).
            ``None`` lets the library pick the best available device.
        max_batch_size: Maximum number of items accepted in one embedding request.
        log_level: Minimum level of log messages to print.
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="EMBED_")

    model_name: str = Field(default="clip-ViT-B-32", min_length=1)
    device: str | None = None
    max_batch_size: int = Field(default=64, gt=0)
    log_level: LogLevel = "info"


settings: Final[Settings] = Settings()
"""Shared settings instance, created once at import time."""
