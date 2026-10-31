from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings, read from environment variables or a .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="EMBED_")

    # CLIP puts text and images in the same vector space, so image
    # embeddings added later will be directly comparable to these.
    model_name: str = "clip-ViT-B-32"
    device: str | None = None  # "cpu", "cuda", or None to auto-detect
    max_batch_size: int = 64


settings = Settings()
