"""Core layer: app-wide setup used by every other layer.

- config.py   Settings loaded from EMBED_* environment variables or .env
- logging.py  Logging format and level

Must not import from api/, schemas/ or services/.
"""
